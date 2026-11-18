# =====================================================================================
# PARTE VIII — DataJud: validação externa, seguimento estendido, regras TPU e os JECs de Natal
# Arquivo executado (exec) por build_rafaelcc_ed2.py; textos de interpretação em interp_datajud.py (INTERP_DATAJUD, 'dj_').
# =====================================================================================

md(r'''
# PARTE VIII — DATAJUD: VALIDAÇÃO EXTERNA, SEGUIMENTO ESTENDIDO E OS JUIZADOS CÍVEIS DE NATAL

A planilha do experimento é a fonte primária deste notebook, mas é **alimentada à mão** pela própria unidade e termina em 07/10/2026. Esta parte confronta a planilha com uma fonte **independente e pública**, a API Pública do **DataJud** (CNJ), que reproduz os metadados e os **movimentos processuais** de cada processo do TJRN, codificados pelas Tabelas Processuais Unificadas (TPU, Resolução CNJ nº 46/2007). Responde a quatro perguntas, na ordem em que dependem umas das outras:

| Seção | Pergunta | Papel no estudo |
|---|---|---|
| 8.1–8.2 | De onde vêm os dados e como os movimentos viram variáveis? | coleta reprodutível e regras explícitas |
| 8.3 (VIII-A) | A planilha confere com o DataJud, processo a processo? | **validação da medida** (datas, desfechos, audiência, redistribuição; sentenças em fim de semana) |
| 8.4 (VIII-B) | O que acontece com os 206 censurados depois de 07/10/2026? | **sensibilidade**: seguimento estendido; não substitui a análise principal (Parte IV) |
| 8.5 (VIII-C) | As variáveis do estudo podem ser reconstruídas **só** pelos movimentos? | condição para usar o DataJud na população |
| 8.6 (VIII-D) | O experimento mudou a unidade? O 4º JEC é típico entre os 14 JECs cíveis de Natal? | comparação **observacional** (questões 2.5 e 2.10; os "106,8 dias") |

O que fica fora de escopo, por decisão de desenho: outra comarca, outro estado, controle sintético e estudo de evento completo (questão 2.10, seção 6.9). Toda comparação entre unidades desta parte é **observacional**: mede o efeito do experimento **sobre a unidade**, nunca o efeito do rito, que só o sorteio interno identifica.
''')

# =====================================================================================
md(r'''
## 8.1 Fonte, coleta e reprodutibilidade

**A API.** O endpoint `api_publica_tjrn` aceita consultas Elasticsearch; cada documento é um processo em um grau (JE = juizado; TR = turma recursal; G1/G2 = justiça comum), com `numeroProcesso`, `dataAjuizamento`, `classe`, `orgaoJulgador`, `assuntos`, `dataHoraUltimaAtualizacao` e a lista de `movimentos` (código TPU, data e hora, órgão que lançou e complementos tabelados, como o tipo e a situação de uma audiência). A chave é a pública, divulgada pelo CNJ. A API **não** traz partes, advogados, valor da causa nem o teor das decisões (seção 6.4).

**A coleta foi feita fora do notebook**, por scripts em `datajud_sondagem/`, porque a API estava sobrecarregada (respostas HTTP 429, `es_rejected_execution_exception`, falhas de *shard* e quedas de conexão): cada consulta é repetida com espera crescente e **só é aceita se nenhum shard falhar**; a coleta é retomável e grava um cache local comprimido (`.jsonl.gz`). O notebook lê **apenas o cache**: não acessa a rede e é reprodutível.

| Script | O que faz | Saída |
|---|---|---|
| `api.py` | cliente com tentativas (aceita só respostas sem falha de shard) | — |
| `coleta_amostra.py` | busca os 938 números da planilha, em lotes de 25 (`terms` em `numeroProcesso`) | `amostra_vinculada.jsonl.gz`, `amostra_estado.json` |
| `coleta_natal.py` | população dos 14 JECs cíveis de Natal, por juizado e janela de ajuizamento (01/01 a 03/08 de 2025 e de 2026; resto de 2025; o 4º JEC também em 2024), páginas de 500 com `search_after` | `natal/*.jsonl.gz`, `natal/estado.json` |
| `tpu.py`, `preparar_tpu.py` | nome, item-pai e glossário de cada código de movimento na TPU oficial (SGT/CNJ) | `tpu_movimentos.json` |

A célula abaixo lê os caches e mostra o que foi coletado.
''')

code(r'''
import gzip
import json
import os
from collections import Counter, defaultdict
from sklearn.metrics import cohen_kappa_score
from lifelines.utils import restricted_mean_survival_time

if 'dados' not in globals():
    dados = pd.read_pickle(PROC / 'ed2_tidy.pkl')

DJ_PASTA = RAIZ / 'datajud_sondagem'
DJ_NATAL = Path(os.environ.get('DJ_NATAL_TESTE', DJ_PASTA / 'natal'))   # variável só para testes do código
FONTE_DJ = ('Fonte: elaboração própria a partir da API Pública do DataJud (CNJ), endpoint do TJRN (coleta em nov./2026), '
            'e da planilha de controle do 4º JEC de Natal/RN (atualização de 07/10/2026).')
FONTE_DJ_POP = ('Fonte: elaboração própria a partir da API Pública do DataJud (CNJ), endpoint do TJRN, '
                'Juizados Especiais Cíveis de Natal (coleta em nov./2026).')
COD_4JEC, COD_CEJUSC = '13285', '82567'   # 4º JEC; CEJUSC dos Juizados de Natal (pode lançar audiência/homologação)
DJ_LOTE = 25
JECS_NATAL = {'13282': '1º', '13283': '2º', '5153': '3º', '13285': '4º', '13286': '5º', '83097': '6º', '13288': '7º',
              '13289': '8º', '13290': '9º', '13291': '10º', '13292': '11º', '13293': '12º', '13284': '13º', '77266': '14º'}
COR_4JEC, COR_OUTROS = TINTA, CINZA


def dj_ler(arq):
    with gzip.open(arq, 'rt', encoding='utf-8') as f:
        return [json.loads(linha) for linha in f]


def dj_data_arquivo(arq):
    return pd.Timestamp.fromtimestamp(arq.stat().st_mtime).normalize()   # hora local


# ---- amostra (os números da planilha)
dj_regs = list({x['_id']: x for x in dj_ler(DJ_PASTA / 'amostra_vinculada.jsonl.gz')}.values())  # sem repetições de retomada
dj_lotes_feitos = set(json.loads((DJ_PASTA / 'amostra_estado.json').read_text())['lotes_feitos'])
dj_numeros = sorted({re.sub(r'\D', '', p) for p in dados['processo'].astype(str)})   # a mesma ordem do coletor
dj_lotes = [dj_numeros[i:i + DJ_LOTE] for i in range(0, len(dj_numeros), DJ_LOTE)]
dj_consultados = {n for k in dj_lotes_feitos for n in dj_lotes[k]}
DJ_AMOSTRA_COMPLETA = len(dj_lotes_feitos) == len(dj_lotes)
DJ_DATA_COLETA = dj_data_arquivo(DJ_PASTA / 'amostra_vinculada.jsonl.gz')

# ---- população dos JECs de Natal
dj_pop_arqs = sorted(DJ_NATAL.glob('*.jsonl.gz')) if DJ_NATAL.exists() else []
dj_pop_estado = json.loads((DJ_NATAL / 'estado.json').read_text(encoding='utf-8')) if (DJ_NATAL / 'estado.json').exists() else {}
dj_pop_regs = {}
# só fatias concluídas: uma fatia interrompida é um subconjunto não aleatório (a paginação segue o @timestamp)
dj_pop_parciais = [a.name for a in dj_pop_arqs if not dj_pop_estado.get(a.name.removesuffix('.jsonl.gz'), {}).get('fim')]
for _arq in dj_pop_arqs:
    if _arq.name in dj_pop_parciais:
        continue
    for _x in dj_ler(_arq):
        dj_pop_regs[_x['_id']] = _x
DJ_FATIAS_TOTAL = 14 * 3 + 1
dj_fatias_feitas = sum(1 for k, v in dj_pop_estado.items() if v.get('fim') and not k[-6:].isdigit())
_fatias_nucleo = [f'{c}_janela{a}' for c in JECS_NATAL for a in (2025, 2026)]
DJ_POP_FALTAM = [k for k in _fatias_nucleo if not dj_pop_estado.get(k, {}).get('fim')]
_feita = lambda k: bool(dj_pop_estado.get(k, {}).get('fim'))
DJ_POP_OK = len(dj_pop_regs) > 0 and not DJ_POP_FALTAM          # os 14 juizados, janelas de 2025 e 2026
DJ_POP4_OK = _feita(f'{COD_4JEC}_janela2025') and _feita(f'{COD_4JEC}_janela2026')   # 4º JEC antes × durante
DJ_4JEC_2024_2025 = DJ_POP4_OK and _feita(f'{COD_4JEC}_resto2025') and _feita(f'{COD_4JEC}_ano2024')
DJ_RESTO2025 = DJ_POP_OK and all(_feita(f'{c}_resto2025') for c in JECS_NATAL)
if DJ_POP_FALTAM:
    print(f'População incompleta: faltam {len(DJ_POP_FALTAM)} de {len(_fatias_nucleo)} fatias (juizado × janela de 2025 e 2026); '
          'as comparações com os outros juizados (8.6.1, 8.6.3, 8.6.4 e 8.6.6) ficam pendentes até a coleta terminar '
          '(coleta_natal.py retoma de onde parou).')
print('4º JEC antes × durante disponível:', DJ_POP4_OK, '| 4º JEC 2024–2025 completo:', DJ_4JEC_2024_2025,
      '| resto de 2025 dos 14:', DJ_RESTO2025)

# ---- TPU (cache local; sem rede)
DJ_TPU = json.loads((DJ_PASTA / 'tpu_movimentos.json').read_text(encoding='utf-8'))

_atual = pd.to_datetime(pd.Series([x.get('dataHoraUltimaAtualizacao') for x in dj_regs]).str[:19])
quadro_coleta = pd.DataFrame([
    ['Amostra (números da planilha)', f'{len(dj_lotes_feitos)} de {len(dj_lotes)} lotes de {DJ_LOTE}',
     len(dj_consultados), len({x["numeroProcesso"] for x in dj_regs}), len(dj_regs),
     _atual.max().strftime('%d/%m/%Y') if len(_atual) else '–'],
    ['População: 14 JECs cíveis de Natal', f'{dj_fatias_feitas} de {DJ_FATIAS_TOTAL} fatias (juizado × janela)',
     np.nan, len({x["numeroProcesso"] for x in dj_pop_regs.values()}), len(dj_pop_regs),
     pd.to_datetime(pd.Series([x.get('dataHoraUltimaAtualizacao') for x in dj_pop_regs.values()]).str[:19]).max().strftime('%d/%m/%Y')
     if dj_pop_regs else '–'],
], columns=['Coleta', 'Progresso', 'Números consultados', 'Números encontrados', 'Registros (processo × grau)',
            'Última atualização no índice'])
tabela(quadro_coleta, 'dj_coleta', 'O que foi coletado no DataJud (cache local lido pelo notebook)', secao='8.1',
       fonte=FONTE_DJ, formatos={'Números consultados': 'int'},
       nota='Um mesmo número pode ter mais de um registro (um por grau: juizado, turma recursal, justiça comum). '
            f'Códigos de movimento no cache da TPU: {len(DJ_TPU)}. '
            + (f'Fatias interrompidas, ainda não usadas: {", ".join(a.removesuffix(".jsonl.gz") for a in dj_pop_parciais)}.' if dj_pop_parciais else ''))
print('Amostra completa:', DJ_AMOSTRA_COMPLETA, '| população disponível:', DJ_POP_OK)
''')

# =====================================================================================
md(r'''
## 8.2 Dos movimentos às variáveis: as regras TPU

Cada variável do estudo é reconstruída por uma **regra explícita** sobre os códigos de movimento. A classificação usa a **hierarquia oficial da TPU** (o item-pai de cada código, consultado no SGT/CNJ e guardado em `tpu_movimentos.json`), e não os nomes digitados: um movimento é **julgamento** se descende de *193 Julgamento*; **com resolução do mérito** se descende de *385*; **sem resolução do mérito** se descende de *218*. As exceções foram tiradas dos dados (seção 8.3):

| Variável | Regra no DataJud | Códigos (exemplos) |
|---|---|---|
| Unidade e entrada | órgão do 1º movimento; entrada = 1º movimento lançado na unidade | 26 Distribuição; 36 Redistribuição |
| Sentença (data e tipo) | **1º julgamento** lançado na unidade (ou no CEJUSC) depois da entrada e antes da saída | — |
| · Homologação | homologação de transação ou de acordo | 466; **14099** (o 4º JEC usa o código de "acordo em cumprimento de sentença" também na fase de conhecimento) |
| · Mérito | demais descendentes de 385 | 219 Procedência, 220 Improcedência, 221 Procedência em parte, 11406–11409 |
| · Sem mérito | descendentes de 218 | 11376 Ausência do autor à audiência, 11377 Inadmissibilidade do procedimento, 454 Indeferimento da inicial, 463 Desistência, 11378 Incompetência territorial |
| · não contam como sentença | embargos de declaração e atos da execução | 198, 200, 871, 15408 (ED); 196 Extinção da execução |
| Saída da unidade (redistribuição) | 1ª decisão de declínio na unidade **ou** redistribuição lançada já no órgão de destino | 941 Incompetência; 12255 Redistribuição por prevenção; 36 |
| AC realizada | audiência de **conciliação** com situação "realizada" | 12740 *de Conciliação*; 970 com complemento tipo = conciliação |
| Acordo homologado depois da sentença | homologação posterior ao 1º julgamento (regra R2, abaixo) | 466, 14099 |

**Duas regras para o desfecho.** A **R1** toma o **primeiro** julgamento (a definição usada na Parte IV: tempo até a sentença). A **R2** acrescenta uma convenção que a seção 8.3 mostrou ser a da planilha: quando um **acordo é homologado depois da sentença** (por exemplo, na fase de cumprimento ou durante o recurso), a planilha registra a **homologação** como desfecho, com a data dela.

**Datas.** O campo `dataHora` vem com o sufixo "Z" (UTC), mas a hora do movimento de distribuição coincide, ao segundo, com a de `dataAjuizamento`, que é hora local; a distribuição das horas dos julgamentos (pico das 9h às 11h e das 14h às 16h) também é a de um expediente local. A hora é tratada, portanto, como **hora local**, sem conversão (nenhum julgamento cai entre 0h e 3h, de modo que a escolha não altera nenhuma data).
''')

code(r'''
def dj_cadeia(c):
    """Código e seus itens-pai na TPU (ex.: 219 → 385 → 193 → 1)."""
    out, c = [], int(c)
    while c and c not in out and len(out) < 12:
        out.append(c)
        c = (DJ_TPU.get(str(c)) or {}).get('pai')
    return out


def dj_nome(c):
    return (DJ_TPU.get(str(int(c))) or {}).get('nome') or ''


DJ_HOMOLOG = {466, 14099}
DJ_DECLINIO = {941, 12255}


def dj_tipo_julgamento(c):
    """'Homologação' | 'Mérito' | 'Sem mérito' | None, pela hierarquia oficial da TPU."""
    c = int(c)
    nome = dj_nome(c).lower()
    if 'embargos de declara' in nome:                         # decisão sobre ED não é a sentença
        return None
    if c in DJ_HOMOLOG:
        return 'Homologação'
    if 'execução' in nome or 'cumprimento' in nome:          # atos da fase de execução
        return None
    ch = dj_cadeia(c)
    if 193 not in ch:
        return None
    if 385 in ch:
        return 'Homologação' if 'homologa' in nome else 'Mérito'
    if 218 in ch:
        return 'Sem mérito'
    return None


def dj_dt(s):
    return pd.Timestamp(str(s)[:19])          # hora local (ver texto)


def dj_oj(m):
    return str((m.get('orgaoJulgador') or {}).get('codigo') or '')


def dj_compl(m):
    return {c.get('descricao'): c.get('nome') for c in (m.get('complementosTabelados') or [])}


def dj_derivar(reg, unidade=None, desde=None):
    """Variáveis do estudo a partir dos movimentos de um registro, em relação a `unidade` (padrão: órgão do 1º movimento).
    `desde`: só considera a entrada na unidade a partir dessa data (processos que já tinham passado pela unidade)."""
    movs = sorted(reg.get('movimentos') or [], key=lambda m: m['dataHora'])
    unidade = unidade or next((dj_oj(m) for m in movs if dj_oj(m)), '')
    na_unidade = lambda m: dj_oj(m) in (unidade, COD_CEJUSC, '')
    entrada = next((dj_dt(m['dataHora']) for m in movs if dj_oj(m) == unidade
                    and (desde is None or dj_dt(m['dataHora']) >= desde)), pd.NaT)
    r = {'unidade': unidade, 'entrada': entrada, 'n_mov': len(movs),
         'classe': (reg.get('classe') or {}).get('codigo'),
         'ajuizamento': pd.to_datetime(str(reg.get('dataAjuizamento'))[:8], format='%Y%m%d', errors='coerce'),
         'evolucao_classe': any(int(m['codigo']) == 14739 for m in movs),
         'ult_mov': dj_dt(movs[-1]['dataHora']) if movs else pd.NaT,
         'atualizacao': dj_dt(reg.get('dataHoraUltimaAtualizacao')) if reg.get('dataHoraUltimaAtualizacao') else pd.NaT}
    if pd.isna(entrada):
        return r
    julg, saidas, concil = [], [], []
    for m in movs:
        c, t = int(m['codigo']), dj_dt(m['dataHora'])
        if t < entrada:
            continue
        k = dj_tipo_julgamento(c)
        if k and na_unidade(m):
            julg.append((t, k, c))
        if t > entrada and ((c in DJ_DECLINIO and dj_oj(m) == unidade) or (c == 36 and not na_unidade(m))):
            saidas.append(t)
        cp = dj_compl(m)
        if c == 12740 or (c == 970 and (cp.get('tipo_de_audiencia') or '').lower().startswith('concilia')):
            concil.append((t, cp.get('situacao_da_audiencia')))
    saida = min(saidas) if saidas else pd.NaT
    validos = [j for j in julg if pd.isna(saida) or j[0] < saida]
    s1 = validos[0] if validos else (pd.NaT, None, None)
    hom_pos = [j for j in validos[1:] if j[1] == 'Homologação' and j[0] > s1[0]]
    realizadas = [t for t, s in concil if s == 'realizada']
    r.update({'sent_dt': s1[0], 'sent_tipo': s1[1], 'sent_cod': s1[2],
              'homolog_pos_dt': hom_pos[0][0] if hom_pos else pd.NaT,
              'homolog_dt': next((j[0] for j in validos if j[1] == 'Homologação'), pd.NaT),
              'saida_dt': saida,
              'ac_designada': any(s in ('designada', 'redesignada') for _, s in concil),
              'ac_realizada_dt': realizadas[0] if realizadas else pd.NaT,
              'n_julgamentos': len(julg)})
    return r


def dj_desfecho_em(r, corte, regra='R1'):
    """(tipo, data) do desfecho até `corte`: sentença (R1 = 1º julgamento; R2 = acordo homologado depois prevalece),
    redistribuição (saída da unidade) ou 'Ativo'."""
    corte = pd.Timestamp(corte)
    tipo, data = r.get('sent_tipo'), r.get('sent_dt')
    if regra == 'R2' and pd.notna(r.get('homolog_pos_dt')) and r['homolog_pos_dt'].normalize() <= corte:
        tipo, data = 'Homologação', r['homolog_pos_dt']
    if pd.notna(data) and data.normalize() <= corte:
        return tipo, data.normalize()
    if pd.notna(r.get('saida_dt')) and r['saida_dt'].normalize() <= corte:
        return 'Redistribuição', r['saida_dt'].normalize()
    return 'Ativo', pd.NaT


# conferência: classificação dos códigos de julgamento presentes na amostra
_cods = Counter(int(m['codigo']) for x in dj_regs if x.get('grau') == 'JE' for m in x.get('movimentos') or [])
quadro_regras = pd.DataFrame([{'Código': c, 'Movimento (TPU)': dj_nome(c), 'Hierarquia TPU': ' › '.join(map(str, dj_cadeia(c))),
                               'Classificação': dj_tipo_julgamento(c) or 'não conta como sentença', 'Ocorrências': n}
                              for c, n in _cods.items() if 193 in dj_cadeia(c) or c in DJ_HOMOLOG]).sort_values(
    ['Classificação', 'Ocorrências'], ascending=[True, False]).reset_index(drop=True)
tabela(quadro_regras, 'dj_regras', 'Movimentos de julgamento encontrados na amostra e a classificação atribuída pela regra',
       secao='8.2', fonte=FONTE_DJ, formatos={'Código': 'texto'},
       nota='Hierarquia: código › item-pai › ... › 1 (Magistrado). 193 = Julgamento; 385 = com resolução do mérito; '
            '218 = sem resolução do mérito. Registros de juizado (grau JE).')
''')

# =====================================================================================
md(r'''
## 8.3 VIII-A — Vínculo e validação da planilha

### 8.3.1 Vínculo pelo número CNJ

O número CNJ é um identificador único com dígito verificador (seção 1.9), e o vínculo planilha × DataJud é **exato**: não há casamento aproximado por nome ou data. Um mesmo número pode, porém, aparecer em **mais de um registro**, porque o DataJud guarda um documento por grau: o processo no juizado (JE), o recurso inominado na **Turma Recursal** (TR) e, para os processos que vieram de outro órgão, o registro na justiça comum (G1). O cumprimento de sentença **não** gera registro novo: a classe do mesmo registro evolui de 436 para 156 (movimento 14739). Para não contar o mesmo processo duas vezes, cada número tem **um registro principal**: o de juizado com algum movimento lançado no 4º JEC (cód. 13285); os demais são classificados, não somados.

**Teste.** H₀: a taxa de vínculo não depende do grupo sorteado. Como quase todos os números são encontrados, as frequências esperadas de "não vinculado" são minúsculas e o qui-quadrado assintótico não vale; usa-se o **teste de permutação** da estatística qui-quadrado (10.000 permutações do rótulo de grupo).
''')

code(r'''
dj_por_num = defaultdict(list)
for x in dj_regs:
    dj_por_num[x['numeroProcesso']].append(x)


def dj_passou_4jec(x):
    return any(dj_oj(m) == COD_4JEC for m in x.get('movimentos') or [])


def dj_tipo_registro(x):
    if x.get('grau') == 'TR':
        return 'Turma Recursal (recurso inominado)'
    if x.get('grau') == 'JE' and dj_passou_4jec(x):
        return 'Juizado, com passagem pelo 4º JEC'
    return 'Outro órgão (sem passagem pelo 4º JEC)'


dj = dados.copy()
dj['numero'] = dj['processo'].astype(str).str.replace(r'\D', '', regex=True)
dj['consultado'] = dj['numero'].isin(dj_consultados)
dj['n_registros'] = dj['numero'].map(lambda n: len(dj_por_num.get(n, [])))
dj['encontrado'] = dj['n_registros'] > 0
_principal = {}
for n, lst in dj_por_num.items():
    cand = [x for x in lst if dj_tipo_registro(x).startswith('Juizado')]
    if cand:
        _principal[n] = max(cand, key=lambda x: len(x.get('movimentos') or []))
dj['vinculado'] = dj['numero'].isin(_principal)
dj['n_principais'] = dj['numero'].map(lambda n: sum(dj_tipo_registro(x).startswith('Juizado') for x in dj_por_num.get(n, [])))
dj['tem_recurso'] = dj['numero'].map(lambda n: any(x.get('grau') == 'TR' for x in dj_por_num.get(n, [])))
dj_c = dj[dj['consultado']].copy()

# variáveis derivadas do registro principal
_der = pd.DataFrame([dj_derivar(_principal[n], COD_4JEC, desde=d0 - pd.Timedelta(days=30))
                     for n, d0 in zip(dj_c.loc[dj_c.vinculado, 'numero'], dj_c.loc[dj_c.vinculado, 'dt_distribuicao'])],
                    index=dj_c.index[dj_c.vinculado])
dj_c = dj_c.join(_der.add_prefix('dj_'))

# tabela de vínculo por grupo
vinc = (dj_c.groupby('grupo', observed=True)
        .agg(Consultados=('numero', 'size'), Encontrados=('encontrado', 'sum'), Vinculados=('vinculado', 'sum'))
        .reindex(ORDEM_GRUPO))
vinc.loc['Total'] = vinc.sum()
vinc['Vínculo (%)'] = vinc['Vinculados'] / vinc['Consultados']
tabela(vinc.rename_axis('Grupo'), 'dj_vinculo', 'Quase todos os processos da planilha são encontrados no DataJud, com a mesma taxa nos três grupos',
       secao='8.3.1', fonte=FONTE_DJ, formatos={'Vínculo (%)': 'pct'},
       nota='Encontrado = algum registro com o número; vinculado = registro de juizado com movimento no 4º JEC (registro principal).'
            + ('' if DJ_AMOSTRA_COMPLETA else f' Coleta parcial: {len(dj_lotes_feitos)} de {len(dj_lotes)} lotes.'))


def dj_perm_chi2(x, g, B=10000, rng=None):
    """Teste de permutação da estatística qui-quadrado de independência (x binária × g categórica)."""
    rng = rng or np.random.default_rng(SEMENTE)
    x, g = np.asarray(x).astype(int), np.asarray(g)
    cats = np.unique(g)
    def chi(gg):
        tab = np.array([[np.sum((gg == c) & (x == v)) for v in (0, 1)] for c in cats], float)
        esp = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.nansum(np.where(esp > 0, (tab - esp) ** 2 / esp, 0))
    obs = chi(g)
    perm = np.array([chi(rng.permutation(g)) for _ in range(B)])
    return obs, (1 + np.sum(perm >= obs - 1e-12)) / (B + 1)


chi_v, p_v = dj_perm_chi2(dj_c['vinculado'], dj_c['grupo'].astype(str))
fig, ax = plt.subplots(figsize=(8, 4.8))
vv = vinc.loc[ORDEM_GRUPO]
barras_verticais(ax, ORDEM_GRUPO, 100 * vv['Vínculo (%)'], cores=CORES_GRUPO, ns=vv['Consultados'],
                 fmt=lambda v: pct_br(v / 100), ylabel='Processos vinculados (%)', ymax=112)
ax.set_title('Vínculo exato pelo número CNJ, por grupo sorteado')
anotar_teste(ax, texto_teste('Permutação (χ², 10.000)', f'χ² = {fmt_br(chi_v, 2)}', p_v,
                             f'não vinculados: {fmt_int((~dj_c.vinculado).sum())}'), loc='lower right')
figura(fig, 'dj_vinculo', 'O vínculo com o DataJud é praticamente completo e não depende do grupo', secao='8.3.1', fonte=FONTE_DJ,
       nota='H₀: taxa de vínculo igual nos três grupos.')

# composição dos registros
comp = Counter(dj_tipo_registro(x) for n in dj_c['numero'] for x in dj_por_num.get(n, []))
comp_tab = pd.DataFrame({'Registros': pd.Series(comp)}).rename_axis('Tipo de registro')
comp_tab['Números'] = [sum(any(dj_tipo_registro(x) == t for x in dj_por_num.get(n, [])) for n in dj_c['numero'])
                       for t in comp_tab.index]
tabela(comp_tab.sort_values('Registros', ascending=False), 'dj_registros',
       'Um número, vários registros: o recurso na Turma Recursal e a origem em outro órgão são o mesmo processo em outra instância',
       secao='8.3.1', fonte=FONTE_DJ,
       nota=f'Números com mais de um registro principal (duplicidade no índice): {fmt_int((dj_c.n_principais > 1).sum())}. '
            f'Números com recurso inominado (registro TR): {fmt_int(dj_c.tem_recurso.sum())}.')
nv = dj_c[~dj_c['vinculado']]
tabela(nv[['processo', 'grupo', 'tipo_desfecho', 'dt_distribuicao', 'origem_externa', 'n_registros']].assign(
    registros=nv['numero'].map(lambda n: '; '.join(sorted({f"{x.get('grau')} {x['orgaoJulgador'].get('codigo')}" for x in dj_por_num.get(n, [])})) or '—'))
    .rename(columns={'processo': 'Processo', 'grupo': 'Grupo', 'tipo_desfecho': 'Desfecho (planilha)', 'dt_distribuicao': 'Distribuição',
                     'origem_externa': 'Origem externa', 'n_registros': 'Registros', 'registros': 'Registros encontrados (grau e órgão)'})
    .reset_index(drop=True),
    'dj_nao_vinculados', 'Processos da planilha sem registro de juizado com passagem pelo 4º JEC', secao='8.3.1', fonte=FONTE_DJ,
    formatos={'Registros': 'int'})
''')

interp('dj_vinculo')

# -------------------------------------------------------------------------------------
md(r'''
### 8.3.2 Concordância processo a processo

Para cada processo vinculado comparam-se cinco informações da planilha com a reconstrução pelas regras de 8.2, **na mesma data de corte (07/10/2026)**:

1. **data de distribuição**: `dt_distribuicao` × 1º movimento no 4º JEC (e × `dataAjuizamento`);
2. **data da sentença**: `dt_sentenca` × data do julgamento (R1 e R2), entre os que têm sentença nas duas fontes;
3. **tipo de desfecho** em 07/10/2026 (Homologação, Mérito, Sem mérito, Redistribuição, Ativo);
4. **AC realizada** (`ac_realizada`) × audiência de conciliação "realizada" até 07/10/2026;
5. **redistribuição** (saída da unidade) até 07/10/2026.

**Medidas.** Para as datas, a diferença em dias (DataJud − planilha) e o percentual de coincidência exata. Para as categorias, a **concordância observada** e o **kappa de Cohen**, κ = (p_o − p_e)/(1 − p_e), que desconta a concordância esperada por acaso; IC 95% por *bootstrap* (2.000 reamostras de processos). Leitura usual de κ: > 0,80 quase perfeita; 0,61–0,80 substancial (LANDIS; KOCH, 1977).
''')

code(r'''
CORTE_PLANILHA = DATA_CORTE
v = dj_c[dj_c['vinculado']].copy()
for regra in ('R1', 'R2'):
    _res = [dj_desfecho_em({k[3:]: r[k] for k in r.index if k.startswith('dj_')}, CORTE_PLANILHA, regra) for _, r in v.iterrows()]
    v[f'dj_desf_{regra}'] = [a for a, _ in _res]
    v[f'dj_data_{regra}'] = pd.to_datetime([b for _, b in _res])
v['tipo_pl'] = v['tipo_desfecho'].astype(str)
v['dif_dist'] = (v['dj_entrada'].dt.normalize() - v['dt_distribuicao']).dt.days
v['dif_ajuiz'] = (v['dj_ajuizamento'] - v['dt_distribuicao']).dt.days
_sent_pl = v['tipo_pl'].isin(['Homologação', 'Mérito', 'Sem mérito'])
for regra in ('R1', 'R2'):
    v[f'dif_sent_{regra}'] = np.where(_sent_pl & v[f'dj_desf_{regra}'].isin(['Homologação', 'Mérito', 'Sem mérito']),
                                      (v[f'dj_data_{regra}'] - v['dt_sentenca']).dt.days, np.nan)
v['ac_dj'] = v['dj_ac_realizada_dt'].notna() & (v['dj_ac_realizada_dt'].dt.normalize() <= CORTE_PLANILHA)
v['red_pl'] = v['tipo_pl'] == 'Redistribuição'
v['red_dj'] = v['dj_desf_R1'] == 'Redistribuição'

FAIXAS_DIF = ['< −7', '−7 a −2', '−1', '0', '+1', '+2 a +7', '> +7']


def dj_faixa(d):
    d = pd.Series(d).dropna()
    cat = pd.cut(d, [-1e9, -8, -2, -1, 0, 1, 7, 1e9], right=True, labels=FAIXAS_DIF)
    return cat.value_counts().reindex(FAIXAS_DIF, fill_value=0)


rng_k = np.random.default_rng(SEMENTE + 81)


def dj_kappa(a, b, B=2000):
    a, b = np.asarray(a, dtype=str), np.asarray(b, dtype=str)
    k = cohen_kappa_score(a, b)
    idx = [rng_k.integers(0, len(a), len(a)) for _ in range(B)]
    bs = np.array([cohen_kappa_score(a[i], b[i]) if len(set(a[i]) | set(b[i])) > 1 else np.nan for i in idx])
    return k, np.nanpercentile(bs, 2.5), np.nanpercentile(bs, 97.5), np.mean(a == b)


# ---- datas: distribuição e sentença
fig, axs = plt.subplots(1, 2, figsize=(13, 5))
for ax, (col, tit, n_) in zip(axs, [('dif_dist', 'Distribuição: 1º movimento no 4º JEC − planilha', None),
                                     ('dif_sent_R1', 'Sentença: 1º julgamento (R1) − planilha', None)]):
    fx = dj_faixa(v[col])
    cores = [TINTA if f == '0' else CINZA for f in FAIXAS_DIF]
    barras_verticais(ax, FAIXAS_DIF, fx.values, cores=cores, ylabel='Processos', xlabel='Diferença (dias)')
    ax.set_title(tit)
    d = v[col].dropna()
    anotar_teste(ax, texto_teste(f'n = {fmt_int(len(d))}', f'iguais: {pct_br((d == 0).mean())}',
                                 extra=f'|dif.| ≤ 1 dia: {pct_br((d.abs() <= 1).mean())}'), loc='upper left')
figura(fig, 'dj_datas', 'As datas da planilha coincidem com as do DataJud; as divergências da sentença são de definição, não de digitação',
       secao='8.3.2', fonte=FONTE_DJ, nota='Diferença em dias corridos (DataJud − planilha). Sentença: processos com sentença '
       'nas duas fontes até 07/10/2026. As divergências grandes são examinadas a seguir.')

datas_tab = pd.DataFrame([
    {'Comparação': 'Distribuição × 1º movimento no 4º JEC', 'n': v['dif_dist'].notna().sum(), 'Iguais': (v['dif_dist'] == 0).mean(),
     '|dif.| ≤ 1 dia': (v['dif_dist'].abs() <= 1).mean(), 'Mediana da dif. (dias)': v['dif_dist'].median()},
    {'Comparação': 'Distribuição × dataAjuizamento', 'n': v['dif_ajuiz'].notna().sum(), 'Iguais': (v['dif_ajuiz'] == 0).mean(),
     '|dif.| ≤ 1 dia': (v['dif_ajuiz'].abs() <= 1).mean(), 'Mediana da dif. (dias)': v['dif_ajuiz'].median()},
] + [{'Comparação': f'Sentença × julgamento ({regra})', 'n': v[f'dif_sent_{regra}'].notna().sum(),
      'Iguais': (v[f'dif_sent_{regra}'].dropna() == 0).mean(), '|dif.| ≤ 1 dia': (v[f'dif_sent_{regra}'].dropna().abs() <= 1).mean(),
      'Mediana da dif. (dias)': v[f'dif_sent_{regra}'].median()} for regra in ('R1', 'R2')])
tabela(datas_tab, 'dj_datas', 'Concordância das datas: planilha × DataJud', secao='8.3.2', fonte=FONTE_DJ,
       formatos={'Iguais': 'pct', '|dif.| ≤ 1 dia': 'pct', 'Mediana da dif. (dias)': 0, 'n': 'int'},
       nota='R1 = 1º julgamento; R2 = acordo homologado depois da sentença prevalece (8.2).')
''')

interp('dj_datas')

code(r'''
# ---- tipo de desfecho: matriz de confusão (R1 e R2)
ORD5 = ORDEM_DESFECHO
fig, axs = plt.subplots(1, 2, figsize=(13, 5.6))
kap_desf = {}
for ax, regra in zip(axs, ('R1', 'R2')):
    m = pd.crosstab(v['tipo_pl'], v[f'dj_desf_{regra}']).reindex(index=ORD5, columns=ORD5, fill_value=0)
    ax.imshow(m.values, cmap=SEQ, vmin=0, vmax=max(1, m.values.max()))
    for i in range(5):
        for j in range(5):
            val = m.values[i, j]
            ax.text(j, i, fmt_int(val), ha='center', va='center', fontsize=9,
                    color='white' if val > 0.55 * m.values.max() else TINTA)
    ax.set_xticks(range(5), [quebra(ROTULO_DESFECHO[c], 12) for c in ORD5], fontsize=8)
    ax.set_yticks(range(5), [quebra(ROTULO_DESFECHO[c], 14) for c in ORD5], fontsize=8)
    ax.set_xlabel(f'DataJud, regra {regra}')
    ax.set_ylabel('Planilha')
    ax.grid(False)
    k, lo, hi, po = dj_kappa(v['tipo_pl'], v[f'dj_desf_{regra}'])
    kap_desf[regra] = (k, lo, hi, po)
    ax.set_title(f'Regra {regra}: ' + ('1º julgamento' if regra == 'R1' else 'acordo posterior prevalece')
                 + f'\nKappa de Cohen: κ = {fmt_br(k, 3)} [{fmt_br(lo, 3)}; {fmt_br(hi, 3)}]; concordância = {pct_br(po)}', fontsize=10)
figura(fig, 'dj_desfecho_confusao', 'O tipo de desfecho da planilha é reproduzido quase sem erro quando o acordo posterior à sentença prevalece',
       secao='8.3.2', fonte=FONTE_DJ, nota='Situação em 07/10/2026. Diagonal = concordância. IC 95% do κ por bootstrap (2.000).')

div = v[v['tipo_pl'] != v['dj_desf_R2']]
tabela(div[['processo', 'grupo', 'tipo_pl', 'dt_sentenca', 'dj_desf_R1', 'dj_data_R1', 'dj_desf_R2', 'dj_data_R2', 'dj_sent_cod']]
       .rename(columns={'tipo_pl': 'Planilha', 'dt_sentenca': 'Data (planilha)', 'dj_desf_R1': 'DataJud R1', 'dj_data_R1': 'Data R1',
                        'dj_desf_R2': 'DataJud R2', 'dj_data_R2': 'Data R2', 'dj_sent_cod': 'Código do 1º julgamento'})
       .assign(**{'Código do 1º julgamento': lambda d: d['Código do 1º julgamento'].map(lambda c: '–' if pd.isna(c) else f'{int(c)} {dj_nome(c)}')})
       .sort_values('Planilha').reset_index(drop=True),
       'dj_divergencias', 'Processos em que a planilha e o DataJud (R2) discordam quanto ao desfecho em 07/10/2026', secao='8.3.2',
       fonte=FONTE_DJ, formatos={'Código do 1º julgamento': 'texto'})
''')

interp('dj_desfecho')

code(r'''
# ---- AC realizada, redistribuição e acordo: concordância e kappa
v_ac = v[v['ac_realizada'].notna()].copy()
v['acordo_dj'] = v['dj_homolog_dt'].notna() & (v['dj_homolog_dt'].dt.normalize() <= CORTE_PLANILHA)
comparacoes = {
    'AC realizada': (v_ac['ac_realizada'].astype(bool), v_ac['ac_dj']),
    'Redistribuição': (v['red_pl'], v['red_dj']),
    'Acordo homologado': (v['tipo_pl'] == 'Homologação', v['acordo_dj']),
    'Encerrado em 07/10': (v['tipo_pl'] != 'Ativo', v['dj_desf_R2'] != 'Ativo'),
}
fig, axs = plt.subplots(2, 2, figsize=(11, 8.5))
linhas_k = []
for ax, (nome, (a, b)) in zip(axs.flat, comparacoes.items()):
    a, b = pd.Series(a).astype(bool).values, pd.Series(b).astype(bool).values
    m = pd.crosstab(pd.Categorical(a, [False, True]), pd.Categorical(b, [False, True]), dropna=False).values
    ax.imshow(m, cmap=SEQ, vmin=0, vmax=max(1, m.max()))
    for i in range(2):
        for j in range(2):
            ax.text(j, i, fmt_int(m[i, j]), ha='center', va='center', fontsize=11,
                    color='white' if m[i, j] > 0.55 * m.max() else TINTA)
    ax.set_xticks([0, 1], ['Não', 'Sim'])
    ax.set_yticks([0, 1], ['Não', 'Sim'])
    ax.set_xlabel('DataJud')
    ax.set_ylabel('Planilha')
    ax.grid(False)
    k, lo, hi, po = dj_kappa(a, b)
    ax.set_title(f'{nome}\nKappa: κ = {fmt_br(k, 3)} [{fmt_br(lo, 2)}; {fmt_br(hi, 2)}]; concordância {pct_br(po)}', fontsize=10)
    linhas_k.append({'Variável': nome, 'n': len(a), 'Concordância': po, 'κ': k, 'IC 95% inf.': lo, 'IC 95% sup.': hi,
                     'Só na planilha': int(m[1, 0]), 'Só no DataJud': int(m[0, 1])})
figura(fig, 'dj_binarias', 'Audiência, redistribuição e acordo: a planilha e os movimentos contam a mesma história', secao='8.3.2',
       fonte=FONTE_DJ, nota='Até 07/10/2026. AC realizada: só os processos com ac_realizada informado (o Controle é sempre "Não"). '
       'Acordo homologado: desfecho "Homologação" na planilha × qualquer homologação (466/14099) no DataJud.')
for regra in ('R1', 'R2'):
    k, lo, hi, po = kap_desf[regra]
    linhas_k.insert(0, {'Variável': f'Tipo de desfecho ({regra})', 'n': len(v), 'Concordância': po, 'κ': k, 'IC 95% inf.': lo,
                        'IC 95% sup.': hi, 'Só na planilha': np.nan, 'Só no DataJud': np.nan})
kap_tab = pd.DataFrame(linhas_k)
tabela(kap_tab, 'dj_concordancia', 'Resumo da concordância planilha × DataJud (kappa de Cohen, IC 95% bootstrap)', secao='8.3.2',
       fonte=FONTE_DJ, formatos={'Concordância': 'pct', 'κ': 3, 'IC 95% inf.': 3, 'IC 95% sup.': 3, 'n': 'int',
                                 'Só na planilha': 'int', 'Só no DataJud': 'int'})

fig, ax = plt.subplots(figsize=(10, 5))
xk = np.arange(len(kap_tab))
ax.bar(xk, kap_tab['κ'], color='#5B7389', width=0.6)
ax.errorbar(xk, kap_tab['κ'], yerr=[kap_tab['κ'] - kap_tab['IC 95% inf.'], kap_tab['IC 95% sup.'] - kap_tab['κ']], fmt='none',
            ecolor=TINTA, capsize=4)
for xi, (k, po, hi_) in enumerate(zip(kap_tab['κ'], kap_tab['Concordância'], kap_tab['IC 95% sup.'])):
    ax.annotate(f'κ = {fmt_br(k, 2)}\n{pct_br(po)}', (xi, hi_ + 0.02), ha='center', va='bottom', fontsize=8.5)
ax.axhline(0.8, color=DESTAQUE, ls='--', lw=1, label='κ = 0,80 (quase perfeita)')
ax.axhline(0.6, color=DESTAQUE, ls=':', lw=1, label='κ = 0,60 (substancial)')
legenda_abaixo(ax, ncol=2, dy=-0.2)
ax.set_xticks(xk, [quebra(t, 14) for t in kap_tab['Variável']])
ax.set_ylim(0, 1.22)
ax.set_ylabel('Kappa de Cohen (IC 95%)')
ax.set_title('Kappa por variável; rótulo = κ e concordância observada')
ax.grid(axis='x', visible=False)
figura(fig, 'dj_kappa', ('Todas as variáveis concordam em nível quase perfeito (κ > 0,80)' if (kap_tab['κ'] > 0.8).all()
                        else 'Todas as variáveis concordam além do acaso; a maioria em nível quase perfeito'), secao='8.3.2',
       fonte=FONTE_DJ, nota='Linhas de referência de Landis e Koch (1977).')
''')

interp('dj_concordancia')

# -------------------------------------------------------------------------------------
md(r'''
### 8.3.3 As sentenças em fim de semana

A auditoria (A16; seção 2.5.4) encontrou **135 sentenças datadas em sábado ou domingo** na planilha (18,4% das sentenças), o que levantou a suspeita de digitação errada. O DataJud permite separar duas hipóteses: (a) a data da planilha está errada (o ato é de um dia útil); (b) o ato foi mesmo **registrado** no fim de semana. O movimento de julgamento no PJe é gerado quando o magistrado **assina eletronicamente** a sentença, e é essa data e hora que o DataJud reproduz; a publicação no Diário (movimentos 1061/92) é posterior e cai em dia útil. Se as datas de fim de semana da planilha coincidem com as do movimento, a planilha registrou a data da **assinatura**, e o fim de semana é real.
''')

code(r'''
DIAS_PT = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
fs = v[_sent_pl & v['dif_sent_R2'].notna()].copy()
fs['dia_pl'] = fs['dt_sentenca'].dt.dayofweek
fs['dia_dj'] = fs['dj_data_R2'].dt.dayofweek
_dt_julg = np.where(fs['dif_sent_R1'] == fs['dif_sent_R2'], fs['dj_sent_dt'], fs['dj_homolog_pos_dt'])
fs['hora_dj'] = pd.to_datetime(_dt_julg).hour
fs['fds_pl'] = fs['dia_pl'] >= 5
fds = fs[fs['fds_pl']]
fig, axs = plt.subplots(1, 2, figsize=(13, 5))
tab_d = pd.DataFrame({'Planilha': fs['dia_pl'].value_counts().reindex(range(7), fill_value=0).values,
                      'DataJud': fs['dia_dj'].value_counts().reindex(range(7), fill_value=0).values}, index=DIAS_PT)
barras_agrupadas(axs[0], tab_d, cores={'Planilha': CINZA, 'DataJud': TINTA}, ylabel='Sentenças', rotular=True)
axs[0].set_title('Dia da semana da sentença: planilha × DataJud')
anotar_teste(axs[0], texto_teste(f'Fim de semana: {fmt_int(fds.shape[0])} (planilha)',
                                 f'mesmo dia no DataJud: {pct_br((fds["dif_sent_R2"] == 0).mean())}'), loc='upper center')
legenda_abaixo(axs[0], ncol=2)
hrs = fds['hora_dj'].value_counts().reindex(range(6, 22), fill_value=0)
hru = fs.loc[~fs['fds_pl'], 'hora_dj'].value_counts().reindex(range(6, 22), fill_value=0)
tab_h = pd.DataFrame({'Fim de semana': hrs.values / max(1, hrs.sum()), 'Dia útil': hru.values / max(1, hru.sum())},
                     index=[f'{h}h' for h in range(6, 22)])
barras_agrupadas(axs[1], 100 * tab_h, cores={'Fim de semana': DESTAQUE, 'Dia útil': CINZA}, ylabel='Sentenças (%)')
axs[1].set_title('Hora do registro do julgamento no PJe')
legenda_abaixo(axs[1], ncol=2)
figura(fig, 'dj_fim_semana', 'As sentenças "de fim de semana" foram de fato assinadas no sábado ou no domingo',
       secao='8.3.3', fonte=FONTE_DJ, nota='Sentenças com data nas duas fontes (regra R2). Hora local do movimento de julgamento '
       '(assinatura eletrônica no PJe); a publicação no DJe é posterior.')
''')

interp('dj_fim_semana')

# =====================================================================================
md(r'''
## 8.4 VIII-B — Seguimento estendido dos censurados

Em 07/10/2026, 206 processos estavam sem sentença (censurados) e 24 haviam saído da unidade. O DataJud foi consultado em novembro de 2026: os processos que receberam sentença depois de 07/10 passam a ter o **evento observado**, e os demais ficam censurados numa data posterior. Isso **reduz a censura** sem mudar o desenho, e permite verificar se as conclusões da Parte IV dependiam do seguimento curto (mínimo de 65 dias).

### 8.4.1 Até quando o DataJud é confiável?

O índice do DataJud é alimentado pelos tribunais **com defasagem**: um movimento lançado hoje no PJe pode levar dias para aparecer na API. Usar como corte a data da coleta trataria como "sem sentença" processos cuja sentença ainda não chegou ao índice, e enviesaria a extensão para baixo. Também não se usa a última atualização de cada registro como corte individual: os registros atualizados recentemente são justamente os que tiveram movimento (por exemplo, uma sentença), e a censura passaria a depender do desfecho (censura informativa). Adota-se, portanto, um **corte único**: o último dia em que o volume diário de movimentos ainda está no nível habitual, definido pela regra abaixo e conferido no gráfico.

**Regra.** Para cada dia útil depois de 07/10/2026, compara-se o número de movimentos dos processos da amostra com a mediana dos dias úteis das quatro semanas anteriores a 07/10; o corte é o último dia útil antes do primeiro dia em que o volume cai abaixo de **50%** desse nível e não se recupera.
''')

code(r'''
def dj_volume_diario(regs_iter, desde, ate):
    cont = Counter()
    for x in regs_iter:
        for m in x.get('movimentos') or []:
            d = str(m['dataHora'])[:10]
            if desde <= d <= ate:
                cont[d] += 1
    s = pd.Series(cont, dtype=float)
    s.index = pd.to_datetime(s.index)
    return s.reindex(pd.date_range(desde, ate), fill_value=0)


def dj_corte_confiavel(vol, ref_ini, ref_fim, limiar=0.5):
    uteis = vol[vol.index.dayofweek < 5]
    nivel = uteis[(uteis.index >= ref_ini) & (uteis.index <= ref_fim)].median()
    depois = uteis[uteis.index > ref_fim]
    baixo = depois < limiar * nivel
    # primeiro dia útil a partir do qual o volume fica abaixo do limiar até o fim da série
    queda = None
    for d in depois.index:
        if baixo.loc[d:].all():
            queda = d
            break
    corte = (depois.index[depois.index < queda].max() if queda is not None and (depois.index < queda).any()
             else depois.index.max())
    return corte, nivel, queda


_ate = DJ_DATA_COLETA.strftime('%Y-%m-%d')
vol_am = dj_volume_diario([_principal[n] for n in v['numero']], '2026-08-15', _ate)
DJ_CORTE, nivel_am, queda_am = dj_corte_confiavel(vol_am, DATA_CORTE - pd.Timedelta(days=28), DATA_CORTE)

fig, ax = plt.subplots(figsize=(12, 4.8))
cores_v = [CINZA if d.dayofweek >= 5 else ('#5B7389' if d <= DJ_CORTE else DESTAQUE) for d in vol_am.index]
ax.bar(vol_am.index, vol_am.values, color=cores_v, width=0.8)
ax.axhline(nivel_am, color=TINTA, ls=':', lw=1)
ax.axhline(0.5 * nivel_am, color=DESTAQUE, ls='--', lw=1)
ax.axvline(DATA_CORTE, color=TINTA, lw=1)
ax.axvline(DJ_CORTE, color=DESTAQUE, lw=1.5)
ax.text(DATA_CORTE, ax.get_ylim()[1] * 0.95, ' corte da planilha\n 07/10/2026', fontsize=8, va='top')
ax.text(DJ_CORTE, ax.get_ylim()[1] * 0.75, f' corte DataJud\n {DJ_CORTE:%d/%m/%Y}', fontsize=8, va='top', color=DESTAQUE)
ax.set_ylabel('Movimentos por dia (processos da amostra)')
ax.set_title('Volume diário de movimentos no índice; pontilhado = nível de referência; tracejado = 50%')
eixo_meses(ax, formato='dia')
figura(fig, 'dj_corte', f'O índice do DataJud é confiável até {DJ_CORTE:%d/%m/%Y}; depois, a queda de volume é defasagem de carga',
       secao='8.4.1', fonte=FONTE_DJ, nota=f'Dias úteis em azul (até o corte) e laranja (depois); fins de semana em cinza. Nível de '
       f'referência = mediana dos dias úteis de 09/09 a 07/10/2026 ({fmt_br(nivel_am, 0)} movimentos). Coleta concluída em {DJ_DATA_COLETA:%d/%m/%Y}.')
print('Corte confiável do DataJud (amostra):', DJ_CORTE.date(), '| 1º dia da queda:', queda_am)
''')

interp('dj_corte')

md(r'''
### 8.4.2 Os censurados que receberam sentença depois de 07/10/2026

**Regra da extensão.** Os 708 processos com sentença e os 24 redistribuídos mantêm o tempo e o evento da planilha (a análise principal). Para os 206 censurados: se o DataJud registra o 1º julgamento (R1) até o corte confiável, o evento passa a 1 com o tempo até essa data; se registra a saída da unidade, o processo fica censurado na data da saída; caso contrário, fica censurado no corte do DataJud (ou em 07/10/2026, se o processo não foi vinculado ou não foi consultado). Nenhuma data da planilha é alterada.
''')

code(r'''
ext = dj[['processo', 'numero', 'grupo', 'dt_distribuicao', 'tempo', 'evento', 'evento_cr', 'tipo_desfecho', 'mes_distribuicao',
          'origem_externa']].copy()
ext = ext.join(v[['dj_sent_dt', 'dj_sent_tipo', 'dj_saida_dt']], how='left')
ext['T_ext'] = ext['tempo'].astype(float)
ext['E_ext'] = ext['evento'].astype(int)
ext['tipo_ext'] = ext['tipo_desfecho'].astype(str)
cens = ext['evento_cr'].astype(int) == 0
_vinc = ext.index.isin(v.index)
_sd = ext['dj_sent_dt'].dt.normalize()
_xd = ext['dj_saida_dt'].dt.normalize()
com_sent = cens & _sd.notna() & (_sd <= DJ_CORTE) & (_xd.isna() | (_sd < _xd))
com_saida = cens & ~com_sent & _xd.notna() & (_xd <= DJ_CORTE)
sem_nada = cens & ~com_sent & ~com_saida & _vinc
ext.loc[com_sent, 'T_ext'] = (_sd[com_sent] - ext.loc[com_sent, 'dt_distribuicao']).dt.days
ext.loc[com_sent, 'E_ext'] = 1
ext.loc[com_sent, 'tipo_ext'] = ext.loc[com_sent, 'dj_sent_tipo']
ext.loc[com_saida, 'T_ext'] = (_xd[com_saida] - ext.loc[com_saida, 'dt_distribuicao']).dt.days
ext.loc[com_saida, 'tipo_ext'] = 'Redistribuição'
ext.loc[sem_nada, 'T_ext'] = (DJ_CORTE - ext.loc[sem_nada, 'dt_distribuicao']).dt.days
ext['sit_ext'] = np.select([~cens, com_sent & (_sd <= DATA_CORTE), com_sent, com_saida, sem_nada],
                           ['sem alteração', 'sentença antes de 07/10 (omitida na planilha)', 'sentença depois de 07/10',
                            'saída da unidade', 'ainda sem sentença'], 'não vinculado / não consultado')

cens_tab = (ext[cens].groupby(['grupo', 'sit_ext'], observed=True).size().unstack(fill_value=0).reindex(ORDEM_GRUPO))
cens_tab['Censurados em 07/10'] = cens_tab.sum(axis=1)
cens_tab.loc['Total'] = cens_tab.sum()
tabela(cens_tab.rename_axis('Grupo'), 'dj_censurados', 'O que aconteceu, no DataJud, com os processos censurados em 07/10/2026',
       secao='8.4.2', fonte=FONTE_DJ, nota=f'Corte do DataJud: {DJ_CORTE:%d/%m/%Y}.')

tipos_ext = ext[cens].assign(cat=np.where(com_sent[cens], ext.loc[cens, 'tipo_ext'],
                                          np.where(com_saida[cens], 'Redistribuição', 'Ativo')))
tab_pc = pd.crosstab(tipos_ext['grupo'], tipos_ext['cat']).reindex(index=ORDEM_GRUPO, columns=ORDEM_DESFECHO, fill_value=0)
fig, ax = plt.subplots(figsize=(9, 5.2))
barras_empilhadas(ax, tab_pc.div(tab_pc.sum(axis=1), axis=0), cores=CORES_DESFECHO, ns=tab_pc.sum(axis=1).values,
                  rotulos_serie=ROTULO_DESFECHO)
eixo_pct(ax)
ax.set_ylabel('Censurados em 07/10/2026 (%)')
ax.set_title(f'Situação no DataJud em {DJ_CORTE:%d/%m/%Y} dos censurados na planilha')
_tc = pd.crosstab(tipos_ext['grupo'], tipos_ext['cat'] != 'Ativo').reindex(ORDEM_GRUPO)
chi_c, p_c, gl_c, _ = stats.chi2_contingency(_tc.values)
anotar_teste(ax, texto_teste('Qui-quadrado (encerrado × grupo)', f'χ² = {fmt_br(chi_c, 2)} ({gl_c} gl)', p_c), loc='upper left')
ax.set_ylim(0, 1.18)
legenda_abaixo(ax, ncol=3)
_enc = 1 - tab_pc['Ativo'] / tab_pc.sum(axis=1)
figura(fig, 'dj_censurados', f"Depois de 07/10/2026, o Controle encerrou {pct_br(_enc['Controle'], 0)} dos seus censurados; "
       f"a AC presencial, {pct_br(_enc['Presencial'], 0)}; a remota, {pct_br(_enc['Remota'], 0)}",
       secao='8.4.2', fonte=FONTE_DJ, nota='H₀: a proporção de censurados encerrados depois de 07/10 não depende do grupo.')
''')

interp('dj_censurados')

md(r'''
### 8.4.3 Kaplan-Meier, log-rank, Cox e RMST com o seguimento estendido

Refazem-se, com o seguimento estendido, as quatro análises centrais da Parte IV, com a **mesma especificação**: Kaplan-Meier por grupo; log-rank de 3 grupos (H₀: S_Controle = S_Presencial = S_Remota); Cox (b) com grupo + mês de distribuição (julho e agosto juntos) + origem externa (Efron); e diferenças de RMST até 180 dias com IC por *bootstrap* estratificado por grupo (2.000 reamostras). As mesmas funções são aplicadas à base original, para que a comparação seja entre estimativas calculadas do mesmo modo (elas reproduzem os números da Parte IV).
''')

code(r'''
DJ_MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul-ago']
DJ_COLS_MES = ['mes_fev', 'mes_mar', 'mes_abr', 'mes_mai', 'mes_jun', 'mes_julago']
DJ_X = ['Presencial', 'Remota'] + DJ_COLS_MES + ['origem_ext']


def dj_base_sob(df, T, E):
    s = pd.DataFrame({'T': df[T].astype(float).values, 'E': df[E].astype(int).values, 'grupo': df['grupo'].astype(str).values})
    s['Presencial'] = (s['grupo'] == 'Presencial').astype(int)
    s['Remota'] = (s['grupo'] == 'Remota').astype(int)
    mes = df['mes_distribuicao'].astype(str).replace({'jul': 'jul-ago', 'ago': 'jul-ago'}).values
    for c, m in zip(DJ_COLS_MES, DJ_MESES[1:]):
        s[c] = (mes == m).astype(int)
    s['origem_ext'] = df['origem_externa'].astype(int).values
    return s


def dj_km_grade(T, E, H):
    """S(t) de Kaplan-Meier nos dias inteiros t = 0..H (S[t] = P(T > t))."""
    T = np.asarray(T, dtype=int); E = np.asarray(E, dtype=int)
    n_sai = np.bincount(np.minimum(T, H + 1), minlength=H + 2)[:H + 1]
    risco = len(T) - np.concatenate([[0], np.cumsum(n_sai)[:-1]])
    d = np.bincount(np.minimum(T[E == 1], H + 1), minlength=H + 2)[:H + 1]
    with np.errstate(divide='ignore', invalid='ignore'):
        haz = np.where(risco > 0, d / risco, 0.0)
    return np.cumprod(1 - haz)


def dj_rmst(T, E, tau):
    return dj_km_grade(T, E, tau)[:tau].sum()


def dj_analise_sob(s, rotulo, B=2000, tau=180, semente=SEMENTE + 82):
    """Medianas, log-rank, Cox (b) e ΔRMST(tau) com bootstrap — a especificação da Parte IV."""
    out = {'rotulo': rotulo}
    for g in ORDEM_GRUPO:
        sg = s[s.grupo == g]
        out[f'mediana_{g}'] = KaplanMeierFitter().fit(sg['T'], sg['E']).median_survival_time_
        out[f'eventos_{g}'] = int(sg['E'].sum())
    lr = multivariate_logrank_test(s['T'], s['grupo'], s['E'])
    out['lr_chi2'], out['lr_p'] = lr.test_statistic, lr.p_value
    xs = [c for c in DJ_X if s[c].nunique() > 1]          # covariável constante no subconjunto sai do modelo
    out['X'] = xs
    cox = CoxPHFitter().fit(s[['T', 'E'] + xs], 'T', 'E')
    out['cox'] = cox
    for g in ('Presencial', 'Remota'):
        out[f'HR_{g}'] = np.exp(cox.params_[g])
        lo, hi = np.exp(cox.confidence_intervals_.loc[g].values)
        out[f'HR_{g}_ic'] = (lo, hi)
        out[f'HR_{g}_p'] = cox.summary.loc[g, 'p']
    rng = np.random.default_rng(semente)
    idx = {g: np.where(s.grupo.values == g)[0] for g in ORDEM_GRUPO}
    T_, E_ = s['T'].values.astype(int), s['E'].values.astype(int)
    est = {g: dj_rmst(T_[idx[g]], E_[idx[g]], tau) for g in ORDEM_GRUPO}
    bs = {g: np.array([dj_rmst(T_[ii], E_[ii], tau) for ii in (rng.choice(idx[g], len(idx[g])) for _ in range(B))])
          for g in ORDEM_GRUPO}
    for g in ORDEM_GRUPO:
        out[f'RMST_{g}'] = est[g]
    for g in ('Presencial', 'Remota'):
        dist = bs[g] - bs['Controle']
        dd = est[g] - est['Controle']
        out[f'dRMST_{g}'] = dd
        out[f'dRMST_{g}_ic'] = (np.percentile(dist, 2.5), np.percentile(dist, 97.5))
        out[f'dRMST_{g}_p'] = 2 * stats.norm.sf(abs(dd / dist.std(ddof=1)))
    out['n_eventos'] = int(s['E'].sum())
    out['n_censurados'] = int((s['E'] == 0).sum())
    return out


sob_base = dj_base_sob(ext, 'tempo', 'evento')
sob_ext = dj_base_sob(ext, 'T_ext', 'E_ext')
res_base = dj_analise_sob(sob_base, 'Parte IV (planilha, corte 07/10/2026)')
res_ext = dj_analise_sob(sob_ext, f'Estendido (DataJud, corte {DJ_CORTE:%d/%m/%Y})')

fig, ax = plt.subplots(figsize=(11, 6.6))
plot_km(ax, sob_ext, tempo='T', evento='E', grupo='grupo', passo=30)
ax.set_title(f'Kaplan-Meier com o seguimento estendido até {DJ_CORTE:%d/%m/%Y}')
anotar_teste(ax, texto_teste('Log-rank (3 grupos)', f'χ² = {fmt_br(res_ext["lr_chi2"], 2)} (2 gl)', res_ext['lr_p'],
                             f'Parte IV: χ² = {fmt_br(res_base["lr_chi2"], 2)}; p = {fmt_p(res_base["lr_p"])}'), loc='center right')
figura(fig, 'dj_km_estendido', 'Com o seguimento estendido, as curvas mantêm a ordem, e a distância entre o Controle e os grupos com AC aumenta',
       secao='8.4.3', fonte=FONTE_DJ, nota='IC 95% (Greenwood); marcas = censuras. Eventos e tempos da planilha mantidos; '
       'só os censurados em 07/10/2026 foram atualizados pelo DataJud.')
''')

code(r'''
def dj_linha_res(r):
    lin = {'Análise': r['rotulo'], 'Sentenças': r['n_eventos'], 'Censurados': r['n_censurados']}
    for g in ORDEM_GRUPO:
        lin[f'Mediana {g} (dias)'] = r[f'mediana_{g}']
    for g in ('Presencial', 'Remota'):
        lo, hi = r[f'HR_{g}_ic']
        lin[f'HR {g} (IC 95%)'] = f"{fmt_br(r[f'HR_{g}'], 2)} ({fmt_br(lo, 2)}–{fmt_br(hi, 2)}); p = {fmt_p(r[f'HR_{g}_p'])}"
    for g in ('Presencial', 'Remota'):
        lo, hi = r[f'dRMST_{g}_ic']
        lin[f'ΔRMST180 {g} (dias)'] = f"{fmt_br(r[f'dRMST_{g}'], 1)} ({fmt_br(lo, 1)} a {fmt_br(hi, 1)}); p = {fmt_p(r[f'dRMST_{g}_p'])}"
    lin['Log-rank (3 grupos)'] = f"χ² = {fmt_br(r['lr_chi2'], 2)}; p = {fmt_p(r['lr_p'])}"
    return lin


comp_ext = pd.DataFrame([dj_linha_res(res_base), dj_linha_res(res_ext)]).set_index('Análise').T
tabela(comp_ext.rename_axis('Medida'), 'dj_comparacao_estendido',
       'Parte IV × seguimento estendido: medianas, Cox (b) e ΔRMST(180) por grupo (Controle = referência)', secao='8.4.3',
       fonte=FONTE_DJ, nota='Cox (b): grupo + mês de distribuição + origem externa (Efron). ΔRMST: IC percentil bootstrap estratificado '
       '(2.000); p pela aproximação normal. Valores divulgados na Parte IV: medianas 81/96/95 dias; HR 0,87 e 0,81; ΔRMST180 6,5 e 10,7 dias.')

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
pos = np.arange(2)
for j, (r, cor_r, nome) in enumerate([(res_base, CINZA, 'Parte IV (07/10)'), (res_ext, TINTA, f'Estendido ({DJ_CORTE:%d/%m})')]):
    hr = [r[f'HR_{g}'] for g in ('Presencial', 'Remota')]
    lo = [r[f'HR_{g}_ic'][0] for g in ('Presencial', 'Remota')]
    hi = [r[f'HR_{g}_ic'][1] for g in ('Presencial', 'Remota')]
    xx = pos + (j - 0.5) * 0.3
    axs[0].errorbar(xx, hr, yerr=[np.subtract(hr, lo), np.subtract(hi, hr)], fmt='o', color=cor_r, capsize=4, label=nome, ms=7)
    for xi, h in zip(xx, hr):
        axs[0].annotate(fmt_br(h, 2), (xi, h), xytext=(8, 0), textcoords='offset points', va='center', fontsize=8.5)
    dr = [r[f'dRMST_{g}'] for g in ('Presencial', 'Remota')]
    dlo = [r[f'dRMST_{g}_ic'][0] for g in ('Presencial', 'Remota')]
    dhi = [r[f'dRMST_{g}_ic'][1] for g in ('Presencial', 'Remota')]
    axs[1].bar(xx, dr, width=0.28, color=cor_r, label=nome)
    axs[1].errorbar(xx, dr, yerr=[np.subtract(dr, dlo), np.subtract(dhi, dr)], fmt='none', ecolor=TINTA, capsize=4)
    for xi, d, h_ in zip(xx, dr, dhi):
        axs[1].annotate(fmt_br(d, 1), (xi, h_), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8.5)
axs[0].axhline(1, color=TINTA_2, lw=1, ls='--')
axs[0].set_xticks(pos, ['AC presencial', 'AC remota'])
axs[0].set_xlim(-0.6, 1.6)
axs[0].set_ylabel('HR de sentença vs. Controle (IC 95%)')
axs[0].set_title('Cox (b): HR < 1 = sentença mais lenta')
axs[1].axhline(0, color=TINTA_2, lw=1)
axs[1].set_xticks(pos, ['AC presencial', 'AC remota'])
axs[1].set_ylabel('ΔRMST até 180 dias vs. Controle (dias; IC 95%)')
axs[1].set_title('Dias a mais sem sentença nos primeiros 180 dias')
for ax in axs:
    ax.grid(axis='x', visible=False)
    legenda_abaixo(ax, ncol=2)
anotar_teste(axs[0], texto_teste('Wald (Cox)', extra=f"Remota: p = {fmt_p(res_base['HR_Remota_p'])} → {fmt_p(res_ext['HR_Remota_p'])}"),
             loc='upper right')
anotar_teste(axs[1], texto_teste('Bootstrap (2.000)', extra=f"Remota: p = {fmt_p(res_base['dRMST_Remota_p'])} → {fmt_p(res_ext['dRMST_Remota_p'])}"),
             loc='upper left')
figura(fig, 'dj_efeitos_estendido', f"Com o seguimento estendido, o efeito da AC remota se fortalece: HR {fmt_br(res_base['HR_Remota'], 2)} → "
       f"{fmt_br(res_ext['HR_Remota'], 2)}; ΔRMST180 {fmt_br(res_base['dRMST_Remota'], 1)} → {fmt_br(res_ext['dRMST_Remota'], 1)} dias", secao='8.4.3',
       fonte=FONTE_DJ, nota='Cinza = base da Parte IV; preto = seguimento estendido pelo DataJud.')
''')

interp('dj_estendido')

# =====================================================================================
md(r'''
## 8.5 VIII-C — As regras TPU reproduzem as variáveis da pesquisa?

A seção 8.3 validou a planilha **variável por variável**. A pergunta agora é outra: se o estudo tivesse sido feito **só com o DataJud**, sem a planilha, as variáveis de análise (tempo, evento, tipo de desfecho, AC) e os **resultados** seriam os mesmos? Essa é a condição para aplicar as mesmas regras à população dos JECs de Natal (8.6), onde não há planilha.

**Construção.** Para os processos vinculados: tempo zero = 1º movimento no 4º JEC; evento = 1º julgamento (R1) até 07/10/2026 e antes da saída da unidade; censura na saída ou em 07/10/2026; grupo = o do sorteio (que só a planilha tem). **Critério pré-fixado** para "reproduz bem": κ ≥ 0,80 para o evento e para o tipo de desfecho; pelo menos 90% dos tempos com diferença ≤ 1 dia entre os processos com evento nas duas fontes; e HR e ΔRMST do DataJud dentro do IC 95% da planilha.
''')

code(r'''
vc = v.copy()
_s = vc['dj_sent_dt'].dt.normalize()
_x = vc['dj_saida_dt'].dt.normalize()
ev_dj = _s.notna() & (_s <= DATA_CORTE)
sai_dj = ~ev_dj & _x.notna() & (_x <= DATA_CORTE)
t0 = vc['dj_entrada'].dt.normalize()
vc['T_dj'] = np.where(ev_dj, (_s - t0).dt.days, np.where(sai_dj, (_x - t0).dt.days, (DATA_CORTE - t0).dt.days)).astype(float)
vc['E_dj'] = ev_dj.astype(int)
vc['dT'] = np.where((vc['E_dj'] == 1) & (vc['evento'].astype(int) == 1), vc['T_dj'] - vc['tempo'].astype(float), np.nan)

k_ev = dj_kappa(vc['evento'].astype(int), vc['E_dj'])
k_tp = kap_desf['R1']
dT = vc['dT'].dropna()
s_pl = dj_base_sob(vc, 'tempo', 'evento')
s_dj = dj_base_sob(vc, 'T_dj', 'E_dj')
r_pl = dj_analise_sob(s_pl, 'Planilha (vinculados)')
r_dj = dj_analise_sob(s_dj, 'Só DataJud (regras TPU)')

fig, axs = plt.subplots(1, 2, figsize=(13.5, 5.6), gridspec_kw={'width_ratios': [1.6, 1]})
ax = axs[0]
for g in ORDEM_GRUPO:
    for s_, ls, rot in [(s_pl, '-', 'planilha'), (s_dj, '--', 'DataJud')]:
        sg = s_[s_.grupo == g]
        km = KaplanMeierFitter().fit(sg['T'], sg['E'])
        sf = km.survival_function_.iloc[:, 0]
        ax.step(sf.index, sf.values, where='post', color=CORES_GRUPO[g], ls=ls, lw=2 if ls == '-' else 1.6,
                label=f'{g} — {rot} (mediana {fmt_br(km.median_survival_time_, 0)} d)')
ax.set_xlabel(ROTULOS['dias'])
ax.set_ylabel(ROTULOS['S'])
ax.set_ylim(0, 1.02)
ax.set_title('Kaplan-Meier: planilha (contínua) × só DataJud (tracejada)')
ax.legend(fontsize=7.5, loc='upper right')
anotar_teste(ax, texto_teste('Log-rank (3 grupos)', f'planilha p = {fmt_p(r_pl["lr_p"])}', extra=f'DataJud p = {fmt_p(r_dj["lr_p"])}'),
             loc='lower left')
fx = dj_faixa(dT)
barras_verticais(axs[1], FAIXAS_DIF, fx.values, cores=[TINTA if f == '0' else CINZA for f in FAIXAS_DIF],
                 ylabel='Processos', xlabel='Tempo DataJud − tempo planilha (dias)')
axs[1].set_title('Diferença do tempo até a sentença')
anotar_teste(axs[1], texto_teste('Evento: kappa', f'κ = {fmt_br(k_ev[0], 3)}', efeito=f'tempos iguais: {pct_br((dT == 0).mean())}',
                                 extra=f'|dif.| ≤ 1 dia: {pct_br((dT.abs() <= 1).mean())}'), loc='upper left')
figura(fig, 'dj_regras_km', 'Só com os movimentos do DataJud, as curvas de sobrevivência dos três grupos são praticamente as mesmas',
       secao='8.5', fonte=FONTE_DJ, nota='Processos vinculados; corte em 07/10/2026 nas duas fontes. DataJud: 1º julgamento (R1), '
       'tempo zero = 1º movimento no 4º JEC, censura na saída da unidade.')

crit = pd.DataFrame([
    {'Critério': 'κ do evento (sentença até 07/10)', 'Valor': fmt_br(k_ev[0], 3), 'Limiar': '≥ 0,80', 'Atende': k_ev[0] >= 0.8},
    {'Critério': 'κ do tipo de desfecho (R1)', 'Valor': fmt_br(k_tp[0], 3), 'Limiar': '≥ 0,80', 'Atende': k_tp[0] >= 0.8},
    {'Critério': 'Tempos com |dif.| ≤ 1 dia', 'Valor': pct_br((dT.abs() <= 1).mean()), 'Limiar': '≥ 90%',
     'Atende': (dT.abs() <= 1).mean() >= 0.9},
] + [{'Critério': f'HR {g} (DataJud) no IC da planilha', 'Valor': f"{fmt_br(r_dj[f'HR_{g}'], 2)} vs. {fmt_br(r_pl[f'HR_{g}'], 2)} "
      f"({fmt_br(r_pl[f'HR_{g}_ic'][0], 2)}–{fmt_br(r_pl[f'HR_{g}_ic'][1], 2)})", 'Limiar': 'dentro do IC',
      'Atende': r_pl[f'HR_{g}_ic'][0] <= r_dj[f'HR_{g}'] <= r_pl[f'HR_{g}_ic'][1]} for g in ('Presencial', 'Remota')]
  + [{'Critério': f'ΔRMST180 {g} (DataJud) no IC da planilha', 'Valor': f"{fmt_br(r_dj[f'dRMST_{g}'], 1)} vs. {fmt_br(r_pl[f'dRMST_{g}'], 1)} "
      f"({fmt_br(r_pl[f'dRMST_{g}_ic'][0], 1)} a {fmt_br(r_pl[f'dRMST_{g}_ic'][1], 1)})", 'Limiar': 'dentro do IC',
      'Atende': r_pl[f'dRMST_{g}_ic'][0] <= r_dj[f'dRMST_{g}'] <= r_pl[f'dRMST_{g}_ic'][1]} for g in ('Presencial', 'Remota')])
DJ_REGRAS_OK = bool(crit['Atende'].all())
tabela(crit, 'dj_criterios', 'Critérios pré-fixados para aplicar as regras TPU à população', secao='8.5', fonte=FONTE_DJ,
       destaque=~crit['Atende'], nota=f'Linhas em destaque = critério não atendido. Decisão: '
       f'{"aplicar as regras à população (8.6)" if DJ_REGRAS_OK else "aplicar com ressalvas"}.')
print('Regras TPU reproduzem a planilha:', DJ_REGRAS_OK)
''')

interp('dj_regras')

# =====================================================================================
md(r'''
## 8.6 VIII-D — O 4º JEC entre os Juizados Cíveis de Natal

### 8.6.1 A população e o desenho

**População.** Processos de **classe 436** (Procedimento do Juizado Especial Cível), ou de classe 156 (Cumprimento de sentença) com o movimento 14739 de evolução de classe (o mesmo processo, já na fase de cumprimento), cujo **1º movimento** foi lançado em um dos 14 JECs cíveis de Natal, ajuizados de 01/01 a 03/08 de **2025** (antes) e de **2026** (durante o experimento), mesma janela do calendário. A unidade de cada processo é o juizado do 1º movimento (a distribuição); quem saiu depois continua contado na unidade de origem, censurado na saída, como na Parte IV. As regras de 8.2 são as mesmas para todas as unidades.

**Desfechos com horizonte fixo, por coorte mensal.** Comparar tempos de unidades ou anos com seguimentos diferentes mistura o efeito com o tempo de observação (o artefato da entrada escalonada; seção 2.5). Por isso, cada processo é acompanhado **só nos primeiros 90 dias**, e cada coorte mensal de ajuizamento tem o mesmo horizonte:

- **P90**: proporção sentenciada até 90 dias, 1 − Ŝ(90) de Kaplan-Meier (saída da unidade = censura);
- **RMST90**: dias, em média, sem sentença nos primeiros 90 dias;
- **% sem mérito até 90 dias** e **% homologação até 90 dias**: proporções simples.

**Diferenças em diferenças (DiD).** Para cada unidade *u*, Δ_u = Y_u,2026 − Y_u,2025; o DiD do 4º JEC é Δ_4º − média de Δ dos outros 13. Com 14 unidades, a inferência não pode tratar processos como independentes (os processos de uma unidade compartilham juiz, cartório e pauta); usa-se a **inferência por permutação entre unidades** (placebo): o mesmo DiD é calculado fingindo que cada um dos outros 13 juizados foi o "tratado", e o p-valor é a posição do 4º JEC entre os 14 (o menor p possível é 1/14 ≈ 0,071). O DiD supõe **tendências paralelas** antes de 2026, verificadas no gráfico mensal de 2025.

**Leitura.** É uma comparação **observacional** do efeito do **experimento sobre a unidade** (os três braços somados, mais o que mudou na rotina por causa dele: pauta de audiências, reatividade, o juiz-pesquisador), e não do efeito do rito.
''')

code(r'''
DJ_JAN_AGO = {2025: (pd.Timestamp('2025-01-01'), pd.Timestamp('2025-08-03')),
              2026: (pd.Timestamp('2026-01-01'), pd.Timestamp('2026-08-03'))}
H_DJ = 90
pop = pd.DataFrame()
if DJ_POP4_OK:
    _linhas = []
    for x in dj_pop_regs.values():
        if x.get('grau') != 'JE':
            continue
        movs = sorted(x.get('movimentos') or [], key=lambda m: m['dataHora'])
        if not movs:
            continue
        un = next((dj_oj(m) for m in movs if dj_oj(m)), '')
        if un not in JECS_NATAL:
            continue
        cl = (x.get('classe') or {}).get('codigo')
        evo = any(int(m['codigo']) == 14739 for m in movs)
        if not (cl == 436 or (cl == 156 and evo)):
            continue
        r = dj_derivar(x, un)
        r['numero'] = x['numeroProcesso']
        _linhas.append(r)
    pop = pd.DataFrame(_linhas).drop_duplicates('numero')
    pop['jec'] = pop['unidade'].map(JECS_NATAL)
    pop['quarto'] = pop['unidade'] == COD_4JEC
    pop['ano'] = pop['ajuizamento'].dt.year
    pop['coorte'] = pop['ajuizamento'].dt.to_period('M')
    pop['janela'] = [(a in DJ_JAN_AGO) and (DJ_JAN_AGO[a][0] <= d <= DJ_JAN_AGO[a][1]) for a, d in zip(pop['ano'], pop['ajuizamento'])]
    print(f'População: {len(pop):,} processos; por ano de ajuizamento:', pop['ano'].value_counts().sort_index().to_dict())
else:
    print('Coleta da população dos JECs de Natal ainda não disponível no cache (datajud_sondagem/natal/).')
    DJ_CORTE_POP = DJ_CORTE
''')

code(r'''
if DJ_POP4_OK:
    vol_pop = dj_volume_diario(dj_pop_regs.values(), '2026-08-15', max(x.get('dataHoraUltimaAtualizacao', '')[:10] for x in dj_pop_regs.values()))
    DJ_CORTE_POP, nivel_pop, queda_pop = dj_corte_confiavel(vol_pop, DATA_CORTE - pd.Timedelta(days=28), DATA_CORTE)
    t0p = pop['entrada'].dt.normalize()
    _s = pop['sent_dt'].dt.normalize()
    _x = pop['saida_dt'].dt.normalize()
    evp = _s.notna() & (_s <= DJ_CORTE_POP)
    saip = ~evp & _x.notna() & (_x <= DJ_CORTE_POP)
    pop['T'] = np.where(evp, (_s - t0p).dt.days, np.where(saip, (_x - t0p).dt.days, (DJ_CORTE_POP - t0p).dt.days)).astype(float)
    pop['E'] = evp.astype(int)
    pop['tipo'] = np.where(evp, pop['sent_tipo'], np.where(saip, 'Redistribuição', 'Ativo'))
    pop = pop[pop['T'] >= 0].copy()
    pop['sm90'] = (pop['tipo'] == 'Sem mérito') & (pop['T'] <= H_DJ)
    pop['hom90'] = (pop['tipo'] == 'Homologação') & (pop['T'] <= H_DJ)

    # cobertura da amostra
    p4 = pop[pop['quarto'] & pop['janela'] & (pop['ano'] == 2026)]
    na_pop = dj['numero'].isin(p4['numero'])
    def _motivo(n):
        x = _principal.get(n)
        if x is None:
            return 'sem registro de juizado no DataJud'
        movs = sorted(x.get('movimentos') or [], key=lambda m: m['dataHora'])
        cl = (x.get('classe') or {}).get('codigo')
        if not (cl == 436 or (cl == 156 and any(int(m['codigo']) == 14739 for m in movs))):
            return f'outra classe ({cl} {(x.get("classe") or {}).get("nome") or ""})'.strip()
        if movs and dj_oj(movs[0]) != COD_4JEC:
            return '1º movimento em outro órgão (chegou por redistribuição)'
        if not ('20260101' <= str(x.get('dataAjuizamento'))[:8] <= '20260803'):
            return 'ajuizado fora de 01/01 a 03/08/2026'
        return 'outro'
    mot = dj.loc[~na_pop, 'numero'].map(_motivo).value_counts()
    cob = pd.DataFrame([['População DataJud: 4º JEC, 2026 (01/01 a 03/08)', len(p4)],
                        ['   dos quais estão na planilha', int(p4['numero'].isin(dj['numero']).sum())],
                        ['   não estão na planilha', int((~p4['numero'].isin(dj['numero'])).sum())],
                        ['Planilha (938 processos)', len(dj)],
                        ['   dos quais estão na população DataJud', int(na_pop.sum())]]
                       + [[f'   fora da população: {k}', int(v)] for k, v in mot.items()], columns=['Conjunto', 'Processos'])
    tabela(cob, 'dj_cobertura', 'A definição de população recupera quase todos os processos do experimento', secao='8.6.1', fonte=FONTE_DJ,
           nota='População = classe 436 (ou 156 com evolução de classe), 1º movimento no juizado, ajuizamento na janela. '
                'Motivos de exclusão avaliados no registro principal do processo (8.3.1).')

if DJ_POP_OK:
    npop = pop[pop['janela']].groupby(['jec', 'ano']).size().unstack().reindex([JECS_NATAL[c] for c in JECS_NATAL])
    fig, ax = plt.subplots(figsize=(12, 4.8))
    barras_agrupadas(ax, npop.rename(columns=str), cores={'2025': CINZA, '2026': TINTA}, ylabel='Processos ajuizados (01/01 a 03/08)')
    ax.set_xticks(range(len(npop)), [f'{j} JEC' for j in npop.index], fontsize=8.5)
    ax.set_title('Processos da população por juizado e ano (mesma janela do calendário)')
    legenda_abaixo(ax, ncol=2)
    _o = npop[2026].values; _e = np.full_like(_o, _o.mean(), dtype=float)
    chi_n, p_n = stats.chisquare(_o, _e)
    anotar_teste(ax, texto_teste('Qui-quadrado de aderência (2026)', f'χ² = {fmt_br(chi_n, 2)} (13 gl)', p_n,
                                 'H₀: distribuição igual entre os 14'), loc='lower right')
    figura(fig, 'dj_pop_n', 'A distribuição por sorteio divide os processos quase igualmente entre os 14 JECs', secao='8.6.1',
           fonte=FONTE_DJ_POP, nota=f'Classe 436 (ou 156 com evolução de classe); unidade = juizado do 1º movimento. Corte do índice: {DJ_CORTE_POP:%d/%m/%Y}.')
''')

interp('dj_populacao')

md(r'''
### 8.6.2 Os 14 JECs por consultas agregadas (plano B)

Como a API rejeitava as consultas que devolvem documentos (a fase *fetch* do Elasticsearch), os outros 13 juizados foram consultados por **agregações** (`size: 0`), que só devolvem contagens e passaram na primeira tentativa (scripts `contagens_mensais.py` e `contagens_desfecho.py`; caches `natal_contagens_*.json`). As agregações dão duas informações por juizado:

1. o **volume mensal de ajuizamentos** (classe 436/156), de 01/2025 a 03/08/2026;
2. para as janelas de 01/01 a 03/08 de 2025 e de 2026, quantos processos têm, **na data da coleta**, algum movimento de **sentença**, de **mérito**, **sem mérito** e de **homologação**, pelos mesmos códigos TPU de 8.2.

**O que muda em relação ao desenho de 8.6.1.** Não há tempos: a medida é a proporção de processos com cada tipo de movimento **até a coleta** (novembro de 2026), e não até 90 dias. Os processos de 2025 tiveram mais tempo de observação que os de 2026, mas essa diferença é **a mesma para todos os juizados** (mesmas janelas de ajuizamento, mesma data de coleta), e por isso se cancela na diferença em diferenças. As categorias não são exclusivas (um processo pode ter extinção sem mérito e, depois, um acordo homologado), e a unidade é o órgão **atual** do registro (quem foi redistribuído conta no destino). A inferência é a mesma de 8.6.1: **permutação entre unidades** (placebo), com p mínimo de 1/14.
''')

code(r'''
DJ_AGG_VOL = DJ_PASTA / 'natal_contagens_mensais.json'
DJ_AGG_DESF = DJ_PASTA / 'natal_contagens_desfecho.json'
DJ_AGG_OK = DJ_AGG_VOL.exists() and DJ_AGG_DESF.exists()
if DJ_AGG_OK:
    agv = json.loads(DJ_AGG_VOL.read_text(encoding='utf-8'))
    agd = json.loads(DJ_AGG_DESF.read_text(encoding='utf-8'))
    # ---- volume mensal
    vol = pd.DataFrame({JECS_NATAL[o]: pd.Series(m) for o, m in agv['orgaos'].items()}).fillna(0).sort_index()
    vol = vol.loc[[k for k in vol.index if '202501' <= k <= '202607']]
    fig, ax = plt.subplots(figsize=(12, 5))
    xs = np.arange(len(vol))
    for j in vol.columns:
        if j != '4º':
            ax.plot(xs, vol[j], color=COR_OUTROS, lw=0.9, alpha=0.7)
    ax.plot(xs, vol.drop(columns='4º').mean(axis=1), color=TINTA_2, lw=3, alpha=0.6, label='média dos outros 13 JECs')
    ax.plot(xs, vol['4º'], color=COR_4JEC, lw=2.2, marker='o', ms=4, label='4º JEC')
    ax.axvline(11.5, color=DESTAQUE, ls='--', lw=1)
    ax.text(11.6, ax.get_ylim()[1] * 0.98, 'início do experimento', color=DESTAQUE, fontsize=8, va='top')
    ax.set_xticks(xs, [f"{MESES_PT[int(k[4:]) - 1]}/{k[2:4]}" for k in vol.index], rotation=45, fontsize=8)
    ax.set_ylabel('Processos ajuizados no mês')
    ax.set_title('Ajuizamentos mensais por juizado (classe 436/156; órgão atual)')
    ax.legend(loc='lower right', fontsize=8)
    j26 = pd.Series({JECS_NATAL[o]: d['2026']['n'] for o, d in agd['orgaos'].items()})
    chi_v2, p_v2 = stats.chisquare(j26.values)
    anotar_teste(ax, texto_teste('Qui-quadrado de aderência (jan.–ago./2026)', f'χ² = {fmt_br(chi_v2, 2)} (13 gl)', p_v2,
                                 'H₀: os 14 recebem o mesmo volume'), loc='upper left', tamanho=8)
    figura(fig, 'dj_agg_volume', 'O distribuidor divide a entrada igualmente entre os 14 juizados, antes e durante o experimento',
           secao='8.6.2', fonte=FONTE_DJ_POP, nota=f'Consulta agregada (size 0) de {agv["coletado_em"][:10]}; agosto/2026 omitido (só 1º a 3).')

    # ---- desfechos por juizado e ano
    linhas = []
    for o, d in agd['orgaos'].items():
        for a in ('2025', '2026'):
            r = d[a]
            linhas.append({'jec': JECS_NATAL[o], 'ano': int(a), 'n': r['n'], 'Sentença': r['sentenca'] / r['n'],
                           'Mérito': r.get('merito', 0) / r['n'], 'Sem mérito': r.get('sem_merito', 0) / r['n'],
                           'Homologação': r.get('homologacao', 0) / r['n']})
    agt = pd.DataFrame(linhas)
    DESF_AGG = ['Sentença', 'Mérito', 'Sem mérito', 'Homologação']
    wa = agt.pivot(index='jec', columns='ano', values=DESF_AGG)
    did_agg, rows = {}, []
    for y in DESF_AGG:
        delta = wa[(y, 2026)] - wa[(y, 2025)]
        did = pd.Series({u: delta[u] - delta.drop(u).mean() for u in delta.index})
        did_agg[y] = did
        obs = did['4º']
        rows.append({'Movimento (até a coleta)': y, '4º JEC 2025': 100 * wa.loc['4º', (y, 2025)], '4º JEC 2026': 100 * wa.loc['4º', (y, 2026)],
                     'Outros 2025': 100 * wa[(y, 2025)].drop('4º').mean(), 'Outros 2026': 100 * wa[(y, 2026)].drop('4º').mean(),
                     'DiD (p.p.)': 100 * obs, 'Posição |DiD| (1 = maior)': int((did.abs() >= abs(obs) - 1e-12).sum()),
                     'p (permutação)': float(np.mean(did.abs() >= abs(obs) - 1e-12))})
    did_agg_tab = pd.DataFrame(rows)
    tabela(did_agg_tab, 'dj_agg_did', 'Diferenças em diferenças por consultas agregadas: 4º JEC × outros 13 JECs, 2025 × 2026',
           secao='8.6.2', fonte=FONTE_DJ_POP, destaque='p (permutação)', casas=1,
           nota='Percentual de processos ajuizados de 01/01 a 03/08 de cada ano com algum movimento do tipo até a coleta (nov./2026). '
                '"Outros" = média simples das 13 unidades. p = proporção das 14 unidades com |DiD placebo| ≥ |DiD do 4º JEC|.')
    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    for ax, y in zip(axs.flat, DESF_AGG):
        s_ = (100 * did_agg[y]).sort_values()
        ax.bar(range(len(s_)), s_.values, color=[COR_4JEC if u == '4º' else COR_OUTROS for u in s_.index])
        ax.axhline(0, color=TINTA_2, lw=1)
        ax.set_xticks(range(len(s_)), list(s_.index), fontsize=8)
        ax.set_xlabel('Juizado (ordenado pelo DiD)')
        ax.set_ylabel('DiD (p.p.)')
        ax.set_title(f'Com movimento de {y.lower()}' if y != 'Sentença' else 'Com sentença (qualquer tipo)')
        ax.grid(axis='x', visible=False)
        lin = did_agg_tab[did_agg_tab['Movimento (até a coleta)'] == y].iloc[0]
        anotar_teste(ax, texto_teste('Permutação entre unidades', f"DiD 4º JEC = {fmt_br(lin['DiD (p.p.)'], 1)} p.p.", lin['p (permutação)'],
                                     f"posição {lin['Posição |DiD| (1 = maior)']} de 14"), loc='upper left', tamanho=8)
    figura(fig, 'dj_agg_did', ('De 2025 para 2026, a sentença de mérito caiu no 4º JEC mais do que em qualquer outro juizado'
                               if did_agg_tab.set_index('Movimento (até a coleta)').loc['Mérito', 'Posição |DiD| (1 = maior)'] == 1
                               else 'Diferenças em diferenças entre os 14 juizados (placebo por permutação)'),
           secao='8.6.2', fonte=FONTE_DJ_POP, nota='Cada barra = DiD calculado como se aquela unidade fosse a tratada; preto = 4º JEC.')

    # ---- tipicidade em 2025 (antes do experimento)
    fig, axs = plt.subplots(1, 2, figsize=(13, 5))
    for ax, y in zip(axs, ['Sem mérito', 'Mérito']):
        s25 = wa[(y, 2025)].sort_values()
        xs = np.arange(len(s25))
        cor = [COR_4JEC if u == '4º' else COR_OUTROS for u in s25.index]
        ax.bar(xs - 0.2, 100 * s25.values, width=0.4, color=cor, label='2025')
        ax.bar(xs + 0.2, 100 * wa.loc[s25.index, (y, 2026)].values, width=0.4, color=cor, alpha=0.45, hatch='//',
               edgecolor='white', label='2026')
        ax.set_xticks(xs, list(s25.index), fontsize=8.5)
        ax.set_xlabel('Juizado (ordenado por 2025)')
        ax.set_ylabel(f'Processos com movimento de {y.lower()} (%)')
        ax.set_title(f'{y}: cheias = 2025; hachuradas = 2026')
        ax.grid(axis='x', visible=False)
        ct = np.array([[agd['orgaos'][o]['2025'][{'Sem mérito': 'sem_merito', 'Mérito': 'merito'}[y]],
                        agd['orgaos'][o]['2025']['n'] - agd['orgaos'][o]['2025'][{'Sem mérito': 'sem_merito', 'Mérito': 'merito'}[y]]]
                       for o in agd['orgaos']])
        chi_t, p_t, gl_t, _ = stats.chi2_contingency(ct)
        pos = int((s25 > s25['4º']).sum()) + 1
        anotar_teste(ax, texto_teste('Homogeneidade entre os 14 (2025)', f'χ² = {fmt_br(chi_t, 1)} ({gl_t} gl)', p_t,
                                     f'4º JEC: {pos}º maior de 14 em 2025'), loc='upper left', tamanho=8)
        legenda_abaixo(ax, ncol=2)
    figura(fig, 'dj_agg_tipicidade', 'Já em 2025 o 4º JEC extinguia mais processos sem mérito e julgava menos o mérito que a maioria dos juizados',
           secao='8.6.2', fonte=FONTE_DJ_POP, nota='Proporção de processos ajuizados de 01/01 a 03/08 com algum movimento do tipo até a coleta; '
           'categorias não exclusivas; órgão atual do registro.')
    tabela((agt.assign(**{c: 100 * agt[c] for c in DESF_AGG}).pivot(index='jec', columns='ano', values=['n'] + DESF_AGG)
            .pipe(lambda t: t.set_axis([f'{a} {b}' for a, b in t.columns], axis=1))
            .loc[[JECS_NATAL[c] for c in JECS_NATAL]].rename_axis('Juizado')),
           'dj_agg_juizados', 'Volume e percentual de processos com cada tipo de movimento, por juizado e ano (consultas agregadas)',
           secao='8.6.2', fonte=FONTE_DJ_POP, casas=1, formatos={'n 2025': 'int', 'n 2026': 'int'},
           destaque=lambda df: df.index == '4º', nota='Percentuais até a coleta (nov./2026); janelas de 01/01 a 03/08.')
else:
    print('Consultas agregadas ainda não disponíveis (contagens_mensais.py, contagens_desfecho.py).')
''')

interp('dj_agregado')

md(r'''
### 8.6.3 Tendências mensais e o pressuposto das tendências paralelas

O gráfico mostra o P90 de cada coorte mensal: o 4º JEC em preto e os outros 13 em cinza (a linha cinza grossa é a média deles). A linha vertical marca o início do experimento. **Teste das tendências paralelas (2025):** regressão do P90 mensal de cada unidade no mês, com interação mês × 4º JEC; H₀: a inclinação do 4º JEC em 2025 é igual à dos demais.
''')

code(r'''
def dj_resumo(sub, h=H_DJ):
    T, E = sub['T'].values, sub['E'].values
    S = dj_km_grade(T, E, h)
    return pd.Series({'n': len(sub), 'P90': 1 - S[h], 'RMST90': S[:h].sum(), 'SM90': sub['sm90'].mean(), 'HOM90': sub['hom90'].mean()})


if DJ_POP_OK:
    ult_coorte = (DJ_CORTE_POP - pd.Timedelta(days=H_DJ)).to_period('M')
    mens = (pop[(pop['coorte'] >= pd.Period('2025-01', 'M')) & (pop['coorte'] <= min(ult_coorte, pd.Period('2026-07', 'M')))]
            .groupby(['jec', 'coorte']).apply(dj_resumo).reset_index())
    mens['quarto'] = mens['jec'] == '4º'
    mens['t'] = (mens['coorte'] - pd.Period('2025-01', 'M')).apply(lambda d: d.n)
    T_GRADE = np.arange(int(mens['t'].max()) + 1)
    fig, axs = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
    for ax, (col, ylab) in zip(axs, [('P90', 'Sentenciados até 90 dias (%)'), ('SM90', 'Sem mérito até 90 dias (%)')]):
        for j, sub in mens.groupby('jec'):
            if j == '4º':
                continue
            ss = sub.set_index('t')[col].reindex(T_GRADE)          # meses sem coleta ficam em branco
            ax.plot(T_GRADE, 100 * ss.values, color=COR_OUTROS, lw=0.8, alpha=0.6)
        med = mens[~mens['quarto']].groupby('t')[col].mean().reindex(T_GRADE)
        ax.plot(T_GRADE, 100 * med.values, color=TINTA_2, lw=3, alpha=0.6, label='média dos outros 13 JECs')
        q = mens[mens['quarto']].set_index('t')[col].reindex(T_GRADE)
        ax.plot(T_GRADE, 100 * q.values, color=COR_4JEC, lw=2.2, marker='o', ms=4, label='4º JEC')
        ax.axvline(11.5, color=DESTAQUE, ls='--', lw=1)
        ax.text(11.6, ax.get_ylim()[1] * 0.97, 'início do experimento', color=DESTAQUE, fontsize=8, va='top')
        ax.set_ylabel(ylab)
        ax.legend(loc='lower left', fontsize=8)
    pre = mens[mens['coorte'].dt.year == 2025].copy()
    pre['quarto_i'] = pre['quarto'].astype(int)
    m_pt = smf.wls('P90 ~ t * quarto_i', data=pre, weights=pre['n']).fit(cov_type='HC1')
    anotar_teste(axs[0], texto_teste('Tendências paralelas (2025, WLS)', f"Δ inclinação = {fmt_br(100 * m_pt.params['t:quarto_i'], 2)} p.p./mês",
                                     m_pt.pvalues['t:quarto_i']), loc='lower right')
    rot = [f"{MESES_PT[(k) % 12]}/{25 + k // 12}" for k in range(int(mens['t'].max()) + 1)]
    axs[1].set_xticks(range(len(rot)), rot, rotation=45, fontsize=8)
    axs[0].set_title('Proporção sentenciada até 90 dias, por coorte mensal de ajuizamento')
    axs[1].set_title('Proporção extinta sem mérito até 90 dias')
    figura(fig, 'dj_tendencias', 'Antes de 2026, o 4º JEC seguia a tendência dos outros juizados; em 2026, afastou-se dela',
           secao='8.6.3', fonte=FONTE_DJ_POP, nota=f'Coortes com 90 dias completos até o corte do índice ({DJ_CORTE_POP:%d/%m/%Y}). '
           'Teste: regressão ponderada pelo n da coorte, erros HC1; H₀: mesma inclinação em 2025.')
''')

interp('dj_tendencias')

md(r'''
### 8.6.4 Diferenças em diferenças e permutação entre unidades
''')

code(r'''
DJ_DESF = {'P90': ('Sentenciados até 90 dias', 'p.p.', 100), 'RMST90': ('RMST até 90 dias', 'dias', 1),
           'SM90': ('Sem mérito até 90 dias', 'p.p.', 100), 'HOM90': ('Homologação até 90 dias', 'p.p.', 100)}
if DJ_POP_OK:
    jan = pop[pop['janela']]
    up = jan.groupby(['jec', 'ano']).apply(dj_resumo).reset_index()
    wide = up.pivot(index='jec', columns='ano', values=list(DJ_DESF))
    did_rows, did_all = [], {}
    for y in DJ_DESF:
        delta = wide[(y, 2026)] - wide[(y, 2025)]
        did = {u: delta[u] - delta.drop(u).mean() for u in delta.index}
        did_all[y] = pd.Series(did)
        obs = did['4º']
        p_perm = np.mean([abs(d) >= abs(obs) - 1e-12 for d in did.values()])
        rank = int((pd.Series(did).abs() >= abs(obs) - 1e-12).sum())
        nome, un, esc = DJ_DESF[y]
        did_rows.append({'Desfecho': nome, '4º JEC 2025': wide.loc['4º', (y, 2025)] * esc, '4º JEC 2026': wide.loc['4º', (y, 2026)] * esc,
                         'Outros 2025': wide[(y, 2025)].drop('4º').mean() * esc, 'Outros 2026': wide[(y, 2026)].drop('4º').mean() * esc,
                         f'DiD': obs * esc, 'Unidade': un, 'Posição |DiD| (1 = maior)': rank, 'p (permutação)': p_perm})
    did_tab = pd.DataFrame(did_rows)
    tabela(did_tab, 'dj_did', 'Diferenças em diferenças: 4º JEC × outros 13 JECs, 2025 × 2026 (01/01 a 03/08)', secao='8.6.4',
           fonte=FONTE_DJ_POP, destaque='p (permutação)', formatos={'4º JEC 2025': 1, '4º JEC 2026': 1, 'Outros 2025': 1, 'Outros 2026': 1,
                                                                     'DiD': 1, 'Unidade': 'texto'},
           nota='Proporções em %; DiD em pontos percentuais (p.p.) ou dias. "Outros" = média simples das 13 unidades. '
                'p = proporção das 14 unidades com |DiD placebo| ≥ |DiD do 4º JEC| (mínimo 1/14 = 0,071).')

    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    for ax, y in zip(axs.flat, DJ_DESF):
        nome, un, esc = DJ_DESF[y]
        s_ = (did_all[y] * esc).sort_values()
        cores = [COR_4JEC if u == '4º' else COR_OUTROS for u in s_.index]
        ax.bar(range(len(s_)), s_.values, color=cores)
        ax.axhline(0, color=TINTA_2, lw=1)
        ax.set_xticks(range(len(s_)), [f'{u}' for u in s_.index], fontsize=8)
        ax.set_xlabel('Juizado (ordenado pelo DiD)')
        ax.set_ylabel(f'DiD ({un})')
        ax.set_title(nome)
        ax.grid(axis='x', visible=False)
        lin = did_tab[did_tab['Desfecho'] == nome].iloc[0]
        anotar_teste(ax, texto_teste('Permutação entre unidades', f"DiD 4º JEC = {fmt_br(lin['DiD'], 1)} {un}", lin['p (permutação)'],
                                     f"posição {lin['Posição |DiD| (1 = maior)']} de 14"), loc='upper left', tamanho=8)
    figura(fig, 'dj_did', 'Entre os 14 juizados, o 4º JEC é o que mais mudou de 2025 para 2026?', secao='8.6.4', fonte=FONTE_DJ_POP,
           nota='Cada barra = DiD calculado como se aquela unidade fosse a tratada (placebo); preto = 4º JEC.')
''')

interp('dj_did')

md(r'''
### 8.6.5 O experimento mudou a unidade? O grupo Controle de 2026 e o 4º JEC de 2025

Se o rito atual de 2026 (grupo Controle) fosse igual ao do 4º JEC de 2025, as duas curvas coincidiriam. Uma diferença indicaria que **a unidade mudou durante o experimento** (pauta ocupada pelas audiências obrigatórias, reatividade do cartório e do juiz), e que o Controle **não** representa o "rito atual" fora do experimento. Para comparar o mesmo com o mesmo, as quatro curvas do 4º JEC usam as **regras TPU** (o tempo de 2026 vem da seção 8.5, só DataJud) e todas são truncadas em 180 dias. O painel da direita mostra os outros 13 JECs nos mesmos dois anos: é o contrafactual de tendência da capital.

**Testes.** Log-rank 4º JEC 2025 × Controle 2026 (H₀: mesma curva até 180 dias) e, à direita, outros 13 JECs 2025 × 2026.
''')

code(r'''
if DJ_POP4_OK:
    TRUNC = 180

    def dj_trunc(T, E, tau=TRUNC):
        T = np.asarray(T, float); E = np.asarray(E, int)
        return np.minimum(T, tau), np.where(T > tau, 0, E)

    _grp = dict(zip(dj['numero'], dj['grupo'].astype(str)))
    q25 = pop[pop['quarto'] & pop['janela'] & (pop['ano'] == 2025)]
    q26 = pop[pop['quarto'] & pop['janela'] & (pop['ano'] == 2026)].copy()
    q26['grupo'] = q26['numero'].map(_grp)
    q26s = q26[q26['grupo'].notna()]
    comp4 = pd.concat([pd.DataFrame({'T': q25['T'], 'E': q25['E'], 'serie': '4º JEC 2025'}),
                       pd.DataFrame({'T': q26s['T'], 'E': q26s['E'], 'serie': q26s['grupo'] + ' 2026'})], ignore_index=True)
    comp4['T'], comp4['E'] = dj_trunc(comp4['T'], comp4['E'])
    cores4 = {'4º JEC 2025': TINTA, 'Controle 2026': CORES_GRUPO['Controle'], 'Presencial 2026': CORES_GRUPO['Presencial'],
              'Remota 2026': CORES_GRUPO['Remota'], 'Outros 13 JECs 2025': TINTA, 'Outros 13 JECs 2026': CINZA}
    dois = DJ_POP_OK
    fig, axs = plt.subplots(1, 2 if dois else 1, figsize=(14, 6.4) if dois else (9, 6.4))
    axs = np.atleast_1d(axs)
    ORD4 = [k for k in ['4º JEC 2025', 'Controle 2026', 'Presencial 2026', 'Remota 2026'] if (comp4.serie == k).any()]
    plot_km(axs[0], comp4, tempo='T', evento='E', grupo='serie', ordem=ORD4,
            cores=cores4, passo=30, tmax=TRUNC, ic=True, censuras=False)
    a_ = comp4[comp4.serie.isin(['4º JEC 2025', 'Controle 2026'])]
    lr4 = logrank_test(a_.loc[a_.serie == '4º JEC 2025', 'T'], a_.loc[a_.serie == 'Controle 2026', 'T'],
                       a_.loc[a_.serie == '4º JEC 2025', 'E'], a_.loc[a_.serie == 'Controle 2026', 'E'])
    rm = {s_: dj_rmst(g_['T'].values.astype(int), g_['E'].values, TRUNC) for s_, g_ in comp4.groupby('serie')}
    anotar_teste(axs[0], texto_teste('Log-rank: 4º JEC 2025 × Controle 2026', f'χ² = {fmt_br(lr4.test_statistic, 2)}', lr4.p_value,
                                     f"RMST180: {fmt_br(rm['4º JEC 2025'], 1)} × {fmt_br(rm['Controle 2026'], 1)} dias"), loc='center right', tamanho=8)
    axs[0].set_title('4º JEC: 2025 (antes) e os três braços de 2026')
    tab_ad = pd.DataFrame([{'Série': k, 'n': int((comp4.serie == k).sum()), 'RMST180 (dias)': rm[k],
                            'Sentenciados até 90 dias': 1 - dj_km_grade(comp4.loc[comp4.serie == k, 'T'].values.astype(int),
                                                                         comp4.loc[comp4.serie == k, 'E'].values, 90)[90]}
                           for k in ORD4])
    if dois:
        o25 = pop[~pop['quarto'] & pop['janela'] & (pop['ano'] == 2025)]
        o26 = pop[~pop['quarto'] & pop['janela'] & (pop['ano'] == 2026)]
        compo = pd.concat([pd.DataFrame({'T': o25['T'], 'E': o25['E'], 'serie': 'Outros 13 JECs 2025'}),
                           pd.DataFrame({'T': o26['T'], 'E': o26['E'], 'serie': 'Outros 13 JECs 2026'})], ignore_index=True)
        compo['T'], compo['E'] = dj_trunc(compo['T'], compo['E'])
        plot_km(axs[1], compo, tempo='T', evento='E', grupo='serie', ordem=['Outros 13 JECs 2025', 'Outros 13 JECs 2026'], cores=cores4,
                passo=30, tmax=TRUNC, ic=True, censuras=False)
        lro = logrank_test(compo.loc[compo.serie.str.endswith('2025'), 'T'], compo.loc[compo.serie.str.endswith('2026'), 'T'],
                           compo.loc[compo.serie.str.endswith('2025'), 'E'], compo.loc[compo.serie.str.endswith('2026'), 'E'])
        rmo = {s_: dj_rmst(g_['T'].values.astype(int), g_['E'].values, TRUNC) for s_, g_ in compo.groupby('serie')}
        anotar_teste(axs[1], texto_teste('Log-rank: 2025 × 2026', f'χ² = {fmt_br(lro.test_statistic, 2)}', lro.p_value,
                                         f"RMST180: {fmt_br(rmo['Outros 13 JECs 2025'], 1)} × {fmt_br(rmo['Outros 13 JECs 2026'], 1)} dias"),
                     loc='center right', tamanho=8)
        axs[1].set_title('Outros 13 JECs cíveis de Natal: 2025 e 2026')
        tab_ad = pd.concat([tab_ad, pd.DataFrame([{'Série': k, 'n': int((compo.serie == k).sum()), 'RMST180 (dias)': rmo[k],
                                                   'Sentenciados até 90 dias': 1 - dj_km_grade(compo.loc[compo.serie == k, 'T'].values.astype(int),
                                                                                               compo.loc[compo.serie == k, 'E'].values, 90)[90]}
                                                  for k in ['Outros 13 JECs 2025', 'Outros 13 JECs 2026']])], ignore_index=True)
    for ax in axs:
        ax.legend(loc='upper right', fontsize=7.5)
    figura(fig, 'dj_antes_durante', ('O grupo Controle de 2026 reproduz o 4º JEC de 2025: o rito atual não mudou durante o experimento'
                                  if lr4.p_value >= 0.05 else 'O grupo Controle de 2026 difere do 4º JEC de 2025: a unidade mudou durante o experimento'),
       secao='8.6.5', fonte=FONTE_DJ_POP,
           nota=f'Todas as curvas pelas regras TPU (DataJud), corte do índice em {DJ_CORTE_POP:%d/%m/%Y}, truncadas em 180 dias; '
                'ajuizamentos de 01/01 a 03/08 de cada ano. 2026 no 4º JEC: processos da população que estão na planilha, pelo grupo sorteado.')
    tabela(tab_ad, 'dj_antes_durante', 'Antes × durante: RMST até 180 dias e proporção sentenciada até 90 dias (regras TPU)',
           secao='8.6.5', fonte=FONTE_DJ_POP, formatos={'Sentenciados até 90 dias': 'pct', 'RMST180 (dias)': 1, 'n': 'int'})
''')

interp('dj_antes_durante')

md(r'''
### 8.6.6 O 4º JEC é típico entre os 14? (questão 2.10)

Em 2025, antes do experimento, as 14 unidades recebiam processos sorteados pelo mesmo distribuidor; diferenças entre elas refletem juiz, cartório e pauta. O gráfico ordena os juizados pelo P90 de 2025 e mostra o de 2026 ao lado. **Teste:** qui-quadrado de homogeneidade da proporção sentenciada até 90 dias entre as 14 unidades em 2025 (todas as coortes de 2025 têm os 90 dias completos, de modo que a proporção simples não sofre censura, a não ser pela saída da unidade).
''')

code(r'''
if DJ_POP_OK:
    p90 = wide['P90'].sort_values(2025)
    fig, ax = plt.subplots(figsize=(12, 5.2))
    xs = np.arange(len(p90))
    ax.bar(xs - 0.2, 100 * p90[2025], width=0.4, color=[COR_4JEC if u == '4º' else COR_OUTROS for u in p90.index], label='2025')
    ax.bar(xs + 0.2, 100 * p90[2026], width=0.4, color=[COR_4JEC if u == '4º' else COR_OUTROS for u in p90.index], alpha=0.45,
           hatch='//', edgecolor='white', label='2026')
    ax.set_xticks(xs, [f'{u} JEC' for u in p90.index], fontsize=8.5)
    ax.set_ylabel('Sentenciados até 90 dias (%)')
    ax.set_title('P90 por juizado: barras cheias = 2025; hachuradas = 2026; preto = 4º JEC')
    ax.grid(axis='x', visible=False)
    j25 = jan[jan['ano'] == 2025]
    ct = pd.crosstab(j25['jec'], (j25['E'] == 1) & (j25['T'] <= H_DJ))
    chi_h, p_h, gl_h, _ = stats.chi2_contingency(ct.values)
    pos4 = int((p90[2025] > p90.loc['4º', 2025]).sum()) + 1
    anotar_teste(ax, texto_teste('Qui-quadrado de homogeneidade (2025)', f'χ² = {fmt_br(chi_h, 1)} ({gl_h} gl)', p_h,
                                 f'4º JEC: {pos4}º maior P90 de 14 em 2025'), loc='upper left')
    legenda_abaixo(ax, ncol=2)
    figura(fig, 'dj_tipicidade', 'O 4º JEC entre os 14 Juizados Cíveis de Natal, antes e durante o experimento', secao='8.6.6',
           fonte=FONTE_DJ_POP, nota='P90 = 1 − Ŝ(90) de Kaplan-Meier (saída = censura). Ajuizamentos de 01/01 a 03/08 de cada ano.')
    tip = (up.assign(**{c: up[c] * DJ_DESF[c][2] for c in DJ_DESF})
           .pivot(index='jec', columns='ano', values=['n'] + list(DJ_DESF)))
    tip.columns = [f'{a} {b}' for a, b in tip.columns]
    tabela(tip.loc[p90.index].rename_axis('Juizado'), 'dj_tipicidade', 'Desfechos com horizonte de 90 dias por juizado, 2025 e 2026',
           secao='8.6.6', fonte=FONTE_DJ_POP, casas=1, formatos={'n 2025': 'int', 'n 2026': 'int'},
           destaque=lambda df: df.index == '4º', nota='P90, SM90 e HOM90 em %; RMST90 em dias.')
''')

interp('dj_tipicidade')

md(r'''
### 8.6.7 Os "106,8 dias" do período anterior

O projeto do experimento cita, como duração média do 4º JEC antes da intervenção, **106,8 dias** (painel GPS-Jus, consulta de 17/12/2025), e a comparação do pesquisador opõe esse número à média de ~75 dias dos sentenciados de 2026. O GPS-Jus mede a duração média **dos processos que receberam sentença em um período**, olhando para trás (do ajuizamento à sentença). A célula reproduz essa medida com o DataJud: 4º JEC, processos com o 1º julgamento entre 17/12/2024 e 17/12/2025 (12 meses), média de dias desde a entrada; e a **mesma medida** para os sentenciados de 2026 até 07/10/2026. Essa média "dos sentenciados" depende de quanto tempo a janela olha para trás: numa janela que começa com o experimento, só entram processos novos, e a média cai por construção (seção 2.5, artefato da entrada escalonada). Por isso a comparação justa é a de horizonte fixo (8.6.4–8.6.5).
''')

code(r'''
if DJ_POP4_OK:
    tem_2024 = DJ_4JEC_2024_2025
    q4 = pop[pop['quarto'] & (pop['E'] == 1)].copy()
    q4['dt_s'] = q4['entrada'].dt.normalize() + pd.to_timedelta(q4['T'], unit='D')
    jan1 = q4[(q4['dt_s'] > '2024-12-17') & (q4['dt_s'] <= '2025-12-17')]
    if not tem_2024:
        jan1 = jan1[jan1['ano'] >= 2025]          # 2024 incompleto não entra (subconjunto não aleatório)
    jan2 = q4[(q4['dt_s'] >= '2026-01-01') & (q4['dt_s'] <= DATA_CORTE)]
    sent_pl = dados[dados['evento'].astype(int) == 1]['tempo'].astype(float)
    g106 = pd.DataFrame([
        ['GPS-Jus (citado no projeto, 17/12/2025)', 106.8, np.nan, np.nan],
        ['DataJud: sentenciados de 17/12/2024 a 17/12/2025' + ('' if tem_2024 else ' (só ajuizados em 2025: limite inferior)'),
         jan1['T'].mean(), jan1['T'].median(), len(jan1)],
        ['DataJud: sentenciados de 01/01 a 07/10/2026', jan2['T'].mean(), jan2['T'].median(), len(jan2)],
        ['Planilha: sentenciados até 07/10/2026 (média ingênua)', sent_pl.mean(), sent_pl.median(), len(sent_pl)],
    ], columns=['Medida', 'Média (dias)', 'Mediana (dias)', 'n'])
    tabela(g106, 'dj_106', 'A "média anterior" de 106,8 dias e a mesma medida calculada no DataJud', secao='8.6.7', fonte=FONTE_DJ_POP,
           casas=1, formatos={'n': 'int'},
           nota='Média dos dias da entrada no 4º JEC ao 1º julgamento, entre os sentenciados na janela. '
                + ('Inclui ajuizamentos de 2024 e 2025; processos ajuizados antes de 2024 e sentenciados na 1ª janela não foram coletados.'
                   if tem_2024 else 'ATENÇÃO: a coleta de 2024 do 4º JEC não terminou (API sobrecarregada); a 1ª janela inclui só os ajuizados em 2025, '
                   'e a sua média é um limite inferior da medida do GPS-Jus.'))
    fig, ax = plt.subplots(figsize=(10, 5))
    _cats = [quebra(t, 22) + (f'\n(n = {fmt_int(n)})' if pd.notna(n) else '') for t, n in zip(g106['Medida'], g106['n'])]
    barras_verticais(ax, _cats, g106['Média (dias)'], cores=[DESTAQUE, TINTA, '#5B7389', CINZA], ylabel='Média (dias)', quebrar=40)
    ax.set_title('Média "dos sentenciados na janela" (medida do GPS-Jus)')
    u_ = stats.mannwhitneyu(jan1['T'], jan2['T'])
    anotar_teste(ax, texto_teste('Mann-Whitney (janela 2025 × 2026)', f'U = {fmt_br(u_.statistic, 0)}', u_.pvalue,
                                 'medida condicional ao encerramento: não é efeito'), loc='upper right', tamanho=8)
    figura(fig, 'dj_106', f"A mesma medida dá {fmt_br(jan1['T'].mean(), 0)} dias antes e {fmt_br(jan2['T'].mean(), 0)} durante o experimento; "
       f"a queda para {fmt_br(sent_pl.mean(), 0)} dias é artefato da janela da planilha",
           secao='8.6.7', fonte=FONTE_DJ_POP, nota='A média dos sentenciados numa janela que começa com o experimento só inclui '
           'processos novos (censura à direita ignorada).')
''')

interp('dj_106')

md(r'''
## 8.7 Síntese da Parte VIII
''')

interp('dj_sintese')
