"""Etapa 3 da sondagem: análise offline (sem API) dos registros coletados.
Lê amostra_vinculada.jsonl.gz (+ contagens.json, outros_jec.jsonl.gz se existirem) e grava resultados_analise.md
(tabelas usadas no RELATORIO_SONDAGEM.md) e derivado_amostra.csv (variáveis derivadas dos movimentos, por processo)."""
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

import tpu

AQUI = Path(__file__).resolve().parent
PKL = AQUI.parent / 'dat' / 'processado' / 'ed2_tidy.pkl'
COD_4JEC = '13285'
COD_CEJUSC = '82567'  # CEJUSC dos Juizados de Natal: pode lançar audiência/homologação no processo
CORTE = pd.Timestamp('2026-10-07')   # data da planilha de controle (atualização 07/10/2026)
OUT = []


def md(df, titulo=None, idx=True):
    if titulo:
        OUT.append(f'\n### {titulo}\n')
    OUT.append(tabela(df, idx) + '\n')


def tabela(df, idx=True):
    """DataFrame/Series -> tabela Markdown (sem depender do pacote tabulate)."""
    if isinstance(df, pd.Series):
        df = df.to_frame()
    df = df.copy()
    if idx:
        df = df.reset_index()
    df.columns = [' / '.join(map(str, c)) if isinstance(c, tuple) else str(c) for c in df.columns]

    def fmt(x):
        if isinstance(x, (list, dict, tuple)):
            return str(x)
        if pd.isna(x):
            return ''
        if isinstance(x, float):
            return f'{x:.3f}'.rstrip('0').rstrip('.')
        return str(x)
    linhas = ['| ' + ' | '.join(df.columns) + ' |', '|' + '---|' * len(df.columns)]
    linhas += ['| ' + ' | '.join(fmt(x).replace('|', '/') for x in row) + ' |' for row in df.itertuples(index=False)]
    return '\n'.join(linhas)


def txt(s):
    OUT.append(s + '\n')


def ler(arq):
    with gzip.open(arq, 'rt', encoding='utf-8') as f:
        return [json.loads(linha) for linha in f]


def dt_local(s):
    """dataHora (UTC, 'Z') -> data/hora de Natal (UTC-3), sem fuso."""
    return pd.Timestamp(s).tz_convert('America/Fortaleza').tz_localize(None)


def dt_ajuiz(s):
    s = str(s)
    if s.isdigit():
        return pd.to_datetime(s[:14], format='%Y%m%d%H%M%S', errors='coerce')
    return pd.to_datetime(s, errors='coerce')


def compl(m):
    return {c.get('descricao'): c.get('nome') for c in (m.get('complementosTabelados') or [])}


def oj_mov(m):
    return str((m.get('orgaoJulgador') or {}).get('codigo') or '')


def classe_julg(codigo):
    """'merito' / 'homologacao' / 'sem_merito' / None conforme a hierarquia oficial da TPU (193 Julgamento)."""
    ch = tpu.cadeia(codigo)
    if 193 not in ch:
        return None
    if 385 in ch:
        nome = (tpu.movimento(codigo)['nome'] or '').lower()
        return 'homologacao' if 'homologa' in nome else 'merito'
    if 218 in ch:
        return 'sem_merito'
    return 'outro_julgamento'


def derivar(reg, cod_unidade=None):
    """Variáveis do estudo a partir dos movimentos de um registro. cod_unidade: órgão de referência (4º JEC)."""
    movs = sorted(reg.get('movimentos') or [], key=lambda m: m['dataHora'])
    r = {'n_mov': len(movs)}
    julg, aud, redis = [], [], []
    for m in movs:
        c = m['codigo']
        k = classe_julg(c)
        if k:
            julg.append((dt_local(m['dataHora']), k, c, m['nome'], oj_mov(m)))
        cp = compl(m)
        if c == 970 or 970 in tpu.cadeia(c):
            # 970 traz o tipo em complemento; os filhos (12740 'de Conciliação', 12750 'de Instrução e Julgamento'...) no nome
            tipo = cp.get('tipo_de_audiencia') or (tpu.movimento(c)['nome'] or '').lower().removeprefix('de ').strip()
            aud.append((dt_local(m['dataHora']), tipo, cp.get('situacao_da_audiencia'), c, cp, oj_mov(m)))
        if c == 36:
            redis.append((dt_local(m['dataHora']), c, oj_mov(m), cp))
    ref = cod_unidade
    if ref is None:  # órgão do primeiro movimento
        ref = next((oj_mov(m) for m in movs if oj_mov(m)), '')
    jr = [j for j in julg if j[4] in ('', ref, COD_CEJUSC)]
    r['julg_primeiro_dt'] = jr[0][0] if jr else pd.NaT
    r['julg_primeiro_tipo'] = jr[0][1] if jr else None
    r['julg_primeiro_cod'] = jr[0][2] if jr else None
    r['julg_primeiro_nome'] = jr[0][3] if jr else None
    r['tem_466'] = any(j[2] == 466 for j in julg)
    r['homolog_dt'] = next((j[0] for j in julg if j[1] == 'homologacao'), pd.NaT)
    ojs = [(dt_local(m['dataHora']), oj_mov(m)) for m in movs]
    entrou = next((d for d, o in ojs if o == ref), None)
    # saída da unidade = 1ª redistribuição (36) posterior à entrada, lançada já no órgão de destino
    saida = next((x[0] for x in redis if entrou is not None and x[0] > entrou and x[2] not in ('', ref, COD_CEJUSC)), None)
    r['entrada_unid_dt'] = entrou if entrou is not None else pd.NaT
    r['saida_unid_dt'] = saida if saida is not None else pd.NaT
    r['n_redistrib'] = len(redis)
    r['redistrib_motivos'] = ';'.join(sorted({str(x[3].get('motivo_da_redistribuicao')) for x in redis}))
    concil = [a for a in aud if (a[1] or '').lower().startswith('concilia')]
    real = [a for a in concil if a[2] == 'realizada']
    r['ac_designada'] = any((a[2] or '') in ('designada', 'redesignada') for a in concil)
    r['ac_realizada_dj'] = bool(real)
    r['ac_realizada_dt'] = real[0][0] if real else pd.NaT
    r['ac_naorealizada_dj'] = any(a[2] == 'não-realizada' for a in concil)
    r['ac_cancelada_dj'] = any(a[2] == 'cancelada' for a in concil)
    r['aud_qualquer_realizada'] = any(a[2] == 'realizada' for a in aud)
    r['aud_tipos'] = ';'.join(sorted({f'{a[1]}|{a[2]}' for a in aud}))
    r['ac_orgaos'] = ';'.join(sorted({a[5] for a in concil}))
    r['ac_realizada_dirigida'] = ';'.join(sorted({str(a[4].get('dirigida_por')) for a in real}))
    r['aud_compl_extra'] = ';'.join(sorted({k for a in aud for k in a[4] if k not in ('tipo_de_audiencia', 'situacao_da_audiencia')}))
    r['transito_dt'] = next((dt_local(m['dataHora']) for m in movs if m['codigo'] == 848), pd.NaT)
    r['arquiv_def_dt'] = next((dt_local(m['dataHora']) for m in movs if m['codigo'] in (246, 22)), pd.NaT)
    r['ult_mov_dt'] = dt_local(movs[-1]['dataHora']) if movs else pd.NaT
    return r


def desfecho(r, corte):
    """Primeiro entre julgamento na unidade e saída da unidade, até a data de corte."""
    jd, sd = r['julg_primeiro_dt'], r['saida_unid_dt']
    jd = jd if pd.notna(jd) and jd.normalize() <= corte else pd.NaT
    sd = sd if pd.notna(sd) and sd.normalize() <= corte else pd.NaT
    if pd.isna(jd) and pd.isna(sd):
        return 'Ativo', pd.NaT
    if pd.notna(sd) and (pd.isna(jd) or sd < jd):
        return 'Redistribuição', sd
    rot = {'merito': 'Mérito', 'homologacao': 'Homologação', 'sem_merito': 'Sem mérito'}
    return rot.get(r['julg_primeiro_tipo'], r['julg_primeiro_tipo']), jd


def passou(reg, cod):
    return any(oj_mov(m) == cod for m in reg.get('movimentos') or [])


def main():
    d = pd.read_pickle(PKL).copy()
    d['numero'] = d['processo'].astype(str).str.replace(r'\D', '', regex=True)
    regs = list({x['_id']: x for x in ler(AQUI / 'amostra_vinculada.jsonl.gz')}.values())  # sem duplicatas de retomada
    por_num = defaultdict(list)
    for x in regs:
        por_num[x['numeroProcesso']].append(x)
    txt(f'Registros devolvidos pela API: {len(regs)}; números distintos: {len(por_num)}; amostra: {d.numero.nunique()}')

    # ---------- 1. Vinculação
    d['n_registros'] = d.numero.map(lambda n: len(por_num.get(n, [])))
    d['vinculado'] = d.n_registros > 0
    md(d.groupby('grupo', observed=True).vinculado.agg(['size', 'sum', 'mean']).round(3), 'Taxa de vinculação por grupo')
    md(d.groupby('origem_externa').vinculado.agg(['size', 'sum', 'mean']).round(3), 'Taxa de vinculação por origem_externa')
    nv = d[~d.vinculado]
    md(nv[['processo', 'grupo', 'tipo_desfecho', 'dt_distribuicao', 'cnj_corrigido', 'origem_externa']].head(40), f'Não vinculados ({len(nv)})', idx=False)
    md(d.n_registros.value_counts().sort_index().to_frame(), 'Registros por número')
    md(pd.Series(Counter(x.get('grau') for x in regs)).to_frame('registros'), 'Graus dos registros')
    oj = Counter((x['orgaoJulgador'].get('codigo'), x['orgaoJulgador'].get('nome'), x['orgaoJulgador'].get('codigoMunicipioIBGE'), x.get('grau')) for x in regs)
    md(pd.DataFrame([(*k, v) for k, v in oj.most_common()], columns=['codigo', 'nome', 'municipio', 'grau', 'n']), 'Órgão julgador do registro (órgão atual)', idx=False)
    md(pd.DataFrame(Counter((x['classe']['codigo'], x['classe']['nome']) for x in regs).most_common(), columns=['classe', 'n']), 'Classe', idx=False)
    md(pd.DataFrame(Counter((x.get('sistema', {}).get('nome'), x.get('formato', {}).get('nome'), x.get('nivelSigilo')) for x in regs).most_common(), columns=['sistema/formato/sigilo', 'n']), 'Sistema, formato, sigilo', idx=False)
    atual = pd.to_datetime(pd.Series([x.get('dataHoraUltimaAtualizacao') for x in regs]), utc=True, format='ISO8601')
    md(atual.dt.tz_localize(None).dt.to_period('M').value_counts().sort_index().to_frame('registros'), 'dataHoraUltimaAtualizacao (mês)')
    ultmov = pd.to_datetime(pd.Series([max((m['dataHora'] for m in x.get('movimentos') or []), default=None) for x in regs]).dropna(), utc=True, format='ISO8601')
    txt(f'Último movimento: máximo {ultmov.max()}; mediana {ultmov.median()}; P90 {ultmov.quantile(.9)}')
    txt(f'dataHoraUltimaAtualizacao: máximo {atual.max()}; mediana {atual.median()}')
    md(ultmov.dt.tz_localize(None).dt.to_period('M').value_counts().sort_index().to_frame('registros'), 'Mês do último movimento')

    def principal(lst):
        pri = [x for x in lst if x.get('grau') in ('G1', 'JE')] or lst
        com4 = [x for x in pri if passou(x, COD_4JEC)]
        return max(com4 or pri, key=lambda x: len(x.get('movimentos') or []))
    lig = d[d.vinculado].copy()
    princ = {n: principal(por_num[n]) for n in lig.numero}
    lig['dj_orgao_cod'] = lig.numero.map(lambda n: princ[n]['orgaoJulgador'].get('codigo'))
    lig['dj_orgao_atual'] = lig.numero.map(lambda n: princ[n]['orgaoJulgador'].get('nome'))
    lig['dj_classe'] = lig.numero.map(lambda n: princ[n]['classe']['codigo'])
    lig['dj_grau'] = lig.numero.map(lambda n: princ[n].get('grau'))
    lig['dj_ajuiz'] = lig.numero.map(lambda n: dt_ajuiz(princ[n].get('dataAjuizamento')))
    lig['passou_4jec'] = lig.numero.map(lambda n: passou(princ[n], COD_4JEC))
    txt(f'Vinculados com movimento no 4º JEC (cód. {COD_4JEC}): {lig.passou_4jec.sum()} de {len(lig)}')
    md(pd.crosstab(lig.passou_4jec, lig.origem_externa), 'Passou pelo 4º JEC × origem_externa')
    lig['dif_ajuiz'] = (lig.dj_ajuiz.dt.normalize() - lig.dt_distribuicao).dt.days
    md(lig.dif_ajuiz.clip(-30, 30).value_counts().sort_index().to_frame('n'), 'dataAjuizamento − dt_distribuicao (dias; truncado ±30)')
    der = pd.DataFrame([derivar(princ[n], COD_4JEC) for n in lig.numero], index=lig.index)
    lig = lig.join(der)
    lig['dif_entrada4'] = (lig.entrada_unid_dt.dt.normalize() - lig.dt_distribuicao).dt.days
    md(lig.dif_entrada4.clip(-30, 30).value_counts().sort_index().to_frame('n'), '1º movimento no 4º JEC − dt_distribuicao (dias; truncado ±30)')
    md(pd.crosstab(lig.origem_externa, lig.dif_ajuiz.fillna(-999).ne(0), margins=True), 'origem_externa × (ajuizamento ≠ distribuição)')

    # ---------- 2. Movimentos
    cont, proc, comp = Counter(), defaultdict(set), Counter()
    for n in lig.numero:
        for m in princ[n].get('movimentos') or []:
            cont[(m['codigo'], m['nome'])] += 1
            proc[(m['codigo'], m['nome'])].add(n)
            cp = compl(m)
            if cp:
                comp[(m['codigo'], m['nome'], '; '.join(f'{a}={b}' for a, b in sorted(cp.items(), key=str)))] += 1
    tm = pd.DataFrame([(c, nm, v, len(proc[(c, nm)]), ' > '.join(map(str, tpu.cadeia(c))), tpu.movimento(c)['nome'])
                       for (c, nm), v in cont.most_common()],
                      columns=['codigo', 'nome', 'ocorrencias', 'processos', 'hierarquia_TPU', 'nome_TPU_oficial'])
    tm['nome_confere'] = tm.nome.str.lower() == tm.nome_TPU_oficial.fillna('').str.lower()
    tm.to_csv(AQUI / 'freq_movimentos_amostra.csv', index=False, encoding='utf-8')
    md(tm, 'Frequência de movimentos (registro principal dos vinculados)', idx=False)
    tc = pd.DataFrame([(*k, v) for k, v in comp.most_common()], columns=['codigo', 'nome', 'complementos', 'n'])
    tc.to_csv(AQUI / 'freq_complementos_amostra.csv', index=False, encoding='utf-8')
    md(tc.head(80), 'Movimentos × complementos tabelados (80 mais frequentes)', idx=False)

    # ---------- 3. Validação
    v = lig[lig.passou_4jec].copy()
    v[['dj_desfecho', 'dj_dt_desfecho']] = v.apply(lambda r: pd.Series(desfecho(r, CORTE)), axis=1)
    v[['dj_desfecho_hoje', 'dj_dt_desfecho_hoje']] = v.apply(lambda r: pd.Series(desfecho(r, pd.Timestamp('2100-01-01'))), axis=1)
    md(pd.crosstab(v.tipo_desfecho.astype(str), v.dj_desfecho, margins=True), 'Desfecho: planilha (linhas) × DataJud até 07/10/2026 (colunas)')
    txt(f'Concordância do tipo de desfecho: {(v.tipo_desfecho.astype(str) == v.dj_desfecho).mean():.1%} (n={len(v)})')
    amb = v[v.dt_sentenca.notna() & v.dj_dt_desfecho.notna()]
    dd = (amb.dj_dt_desfecho.dt.normalize() - amb.dt_sentenca).dt.days
    md(dd.clip(-15, 15).value_counts().sort_index().to_frame('n'), 'Data do desfecho: DataJud − planilha (dias; truncado ±15)')
    txt(f'Datas idênticas: {(dd == 0).mean():.1%}; |dif| ≤ 1 dia: {(dd.abs() <= 1).mean():.1%}; ≤ 7 dias: {(dd.abs() <= 7).mean():.1%} (n={len(dd)})')
    md(pd.crosstab(amb.tipo_desfecho.astype(str), dd.abs().le(1), margins=True), 'Data com |dif| ≤ 1 dia, por tipo de desfecho da planilha')
    mesmo = amb[amb.tipo_desfecho.astype(str) == amb.dj_desfecho]
    dd2 = (mesmo.dj_dt_desfecho.dt.normalize() - mesmo.dt_sentenca).dt.days
    txt(f'Entre os de mesmo tipo: datas idênticas {(dd2 == 0).mean():.1%}; |dif| ≤ 1: {(dd2.abs() <= 1).mean():.1%} (n={len(dd2)})')
    fs = v[v.sentenca_fim_semana.fillna(False).astype(bool)]
    if len(fs):
        t = fs[['processo', 'dt_sentenca', 'tipo_desfecho', 'dj_desfecho', 'dj_dt_desfecho']].copy()
        t['dia_planilha'] = t.dt_sentenca.dt.day_name()
        t['dia_datajud'] = t.dj_dt_desfecho.dt.day_name()
        md(t, 'Sentenças em fim de semana na planilha × DataJud', idx=False)
    md(pd.crosstab(v.ac_realizada.astype('object').fillna('NA'), v.ac_realizada_dj, margins=True), 'AC realizada: planilha (linhas) × DataJud (970 conciliação/realizada)')
    md(pd.crosstab([v.grupo, v.ac_realizada.astype('object').fillna('NA')], v.ac_realizada_dj), 'AC realizada por grupo')
    md(pd.crosstab(v.hibrida.astype('object').fillna('NA'), v.ac_realizada_dj), 'Híbrida (planilha) × AC realizada (DataJud)')
    md(pd.Series(Counter(t for s in v.aud_tipos for t in s.split(';') if t)).sort_values(ascending=False).to_frame('processos'), 'Audiências (tipo|situação) — nº de processos')
    txt('Complementos de audiência além de tipo/situação: ' + str(Counter(t for s in v.aud_compl_extra for t in s.split(';') if t)))
    md(pd.crosstab([v.acordo_ac.astype('object').fillna('NA'), v.acordo_fora.astype('object').fillna('NA')], v.tem_466, margins=True), 'acordo_ac × acordo_fora (linhas) × Homologação de Transação 466 (colunas)')
    v['dj_encerrado'] = v.dj_desfecho != 'Ativo'
    md(pd.crosstab(v.encerrado, v.dj_encerrado, margins=True), 'Encerrado em 07/10/2026: planilha × DataJud')
    at = v[v.tipo_desfecho.astype(str) == 'Ativo']
    md(at.dj_desfecho_hoje.value_counts().to_frame('n'), f'Ativos (censurados) na planilha: situação no DataJud na data da coleta (n={len(at)})')
    if len(at):
        md(at.dj_dt_desfecho_hoje.dt.to_period('M').value_counts().sort_index().to_frame('n'), 'Mês do desfecho dos censurados (DataJud)')
    cols = ['processo', 'grupo', 'tipo_desfecho', 'dt_distribuicao', 'dt_sentenca', 'encerrado', 'ac_realizada', 'hibrida', 'acordo_ac',
            'acordo_fora', 'origem_externa', 'dj_grau', 'dj_orgao_cod', 'dj_orgao_atual', 'dj_classe', 'dj_ajuiz', 'entrada_unid_dt',
            'dj_desfecho', 'dj_dt_desfecho', 'dj_desfecho_hoje', 'dj_dt_desfecho_hoje', 'julg_primeiro_cod', 'julg_primeiro_nome',
            'saida_unid_dt', 'n_redistrib', 'redistrib_motivos', 'ac_designada', 'ac_realizada_dj', 'ac_realizada_dt',
            'ac_naorealizada_dj', 'ac_cancelada_dj', 'ac_orgaos', 'ac_realizada_dirigida', 'tem_466', 'homolog_dt', 'transito_dt', 'arquiv_def_dt', 'ult_mov_dt', 'n_mov', 'aud_tipos']
    v[cols].to_csv(AQUI / 'derivado_amostra.csv', index=False, encoding='utf-8')
    div = v[v.tipo_desfecho.astype(str) != v.dj_desfecho]
    md(pd.crosstab(div.tipo_desfecho.astype(str), div.julg_primeiro_nome.fillna('—')), 'Divergências: tipo na planilha × 1º julgamento no DataJud')
    md(div[['processo', 'tipo_desfecho', 'dt_sentenca', 'dj_desfecho', 'dj_dt_desfecho', 'julg_primeiro_nome', 'saida_unid_dt']].head(30), f'Divergências de desfecho (30 de {len(div)})', idx=False)

    ass = Counter((a.get('codigo'), a.get('nome')) for n in lig.numero for a in princ[n].get('assuntos') or [])
    md(pd.DataFrame([(*k, x) for k, x in ass.most_common(25)], columns=['codigo', 'nome', 'n']), 'Assuntos (25 mais frequentes)', idx=False)
    chaves = Counter(k for x in regs for k in x)
    txt('Campos presentes nos registros: ' + ', '.join(f'{k} ({c})' for k, c in chaves.most_common()))

    # ---------- 4. População e outros JECs
    cj = AQUI / 'contagens.json'
    if cj.exists():
        c = json.loads(cj.read_text(encoding='utf-8'))
        for p, r in c.items():
            if not isinstance(r, dict) or 'orgaos' not in r:
                continue
            t = pd.DataFrame(r['orgaos'])
            t['classes'] = t.classes.map(lambda z: ', '.join(f'{a}:{b}' for a, b in list(z.items())[:5]))
            jz = t[t.nome.str.contains('JUIZADO', case=False, na=False)].sort_values('nome')
            md(jz, f'Juizados de Natal (órgão atual), ajuizados em {p} — total G1 em Natal: {r["total"]}', idx=False)
    oj_arq = AQUI / 'outros_jec.jsonl.gz'
    if oj_arq.exists():
        outros = ler(oj_arq)
    if oj_arq.exists() and outros:
        cnt, pr = Counter(), defaultdict(set)
        for x in outros:
            for m in x.get('movimentos') or []:
                cnt[(m['codigo'], m['nome'])] += 1
                pr[(m['codigo'], m['nome'])].add(x['numeroProcesso'])
        t2 = pd.DataFrame([(c_, nm, len(pr[(c_, nm)]) / len(outros)) for (c_, nm), _ in cnt.most_common()], columns=['codigo', 'nome', 'prop_outros'])
        base = tm.assign(prop_4jec=tm.processos / len(lig))[['codigo', 'prop_4jec']]
        comp_t = t2.merge(base, on='codigo', how='outer').fillna(0).sort_values('prop_outros', ascending=False)
        md(comp_t.head(45).round(3), f'Proporção de processos com cada movimento: outros JECs (n={len(outros)}) × amostra 4º JEC', idx=False)
        der_o = pd.DataFrame([{**derivar(x, str(x['orgaoJulgador']['codigo'])), 'orgao': x['orgaoJulgador']['nome']} for x in outros])
        md(der_o.julg_primeiro_tipo.value_counts(dropna=False).to_frame('n'), 'Outros JECs: tipo do 1º julgamento')
        md(pd.crosstab(der_o.orgao, der_o.ac_realizada_dj), 'Outros JECs: AC de conciliação realizada, por órgão')
        md(pd.Series(Counter(t for s in der_o.aud_tipos for t in s.split(';') if t)).sort_values(ascending=False).to_frame('processos'), 'Outros JECs: audiências (tipo|situação)')

    (AQUI / 'resultados_analise.md').write_text('\n'.join(OUT), encoding='utf-8')
    print('ok', len(OUT))


if __name__ == '__main__':
    main()
