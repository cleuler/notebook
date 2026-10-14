# Seção 22 — Etapa 2: a população de inquéritos de CVLI do Estado (DataJud/CNJ).
# Trecho incluído por build_rafaelcc_ed1.py (usa md, code e interp de lá).

# =====================================================================
md(r'''
---

# ETAPA 2 (PARTE V): A POPULAÇÃO DO ESTADO NO DATAJUD

## 22. Os Inquéritos de CVLI de Goiás na Base Nacional do Poder Judiciário

### 22.1 Por que complementar e o que o DataJud permite

A Etapa 1 deixou quatro lacunas que a amostra não resolve:

| Lacuna da amostra | O que o DataJud oferece | Limite |
|---|---|---|
| Truncamento: só entram IPs que chegaram ao Projudi em 2022–2025 | Todos os processos eletrônicos, com a **data de ajuizamento** e o movimento de **conversão de autos físicos**, que permite separar os nativos digitais (sem truncamento) dos convertidos | Processos físicos encerrados antes da digitalização não estão na base |
| n = 218 e categorias raras | Cerca de 37 mil processos de CVLI no Estado | Só dados estruturados (classe, assunto, órgão, movimentos) |
| Seis comarcas | Todos os municípios, para comparar as comarcas-alvo com o restante do Estado | — |
| Sem identificação dos processos | — | A amostra não tem o número CNJ, e o vínculo individual só é possível por aproximação (22.11) |

**O que não vem do DataJud:** delegacia, arma de fogo, número de vítimas e de indiciados, texto das diligências e datas do fato e da instauração. A comparação se faz pelas variáveis que **as duas bases** têm, ou que podem ser aproximadas pelos movimentos da Tabela Processual Unificada (TPU) do CNJ.

**Coleta.** O script `src/coleta_datajud.py` consulta a API pública e grava um cache local (`dat/datajud/`), que este notebook lê sem depender da API. Ele busca dois conjuntos no TJGO:

- **(A)** inquéritos policiais e autos de prisão em flagrante (classes 279 e 280);
- **(B)** ações penais (classes 282 e 283) que nasceram de inquérito e **mudaram de classe com a denúncia** (movimento 14739, "Evolução da Classe Processual", mesmo número de processo);
- **(C)** ações penais que tiveram a mesma mudança registrada como "Retificação de Classe Processual" (14738), sem o movimento de evolução.

Sem (B) e (C), os inquéritos que viraram ação penal sumiriam da base, e a taxa de denúncia seria subestimada. Na coorte de 2022 em diante, (B) e (C) cobrem 95% das ações penais de CVLI (5.617 de 5.928). As 311 restantes foram distribuídas já como ação penal, sem o histórico do inquérito no mesmo número. Como não têm o marco de início do inquérito, ficam fora da análise do tempo.

**O que se mede.** O DataJud registra o inquérito **a partir da sua chegada ao Judiciário** (o ajuizamento). A data de instauração pela polícia não existe na base. Por isso, a comparação com a amostra se faz pela **fase judicial**, que tem o mesmo marco inicial nas duas bases (22.4).
''')

code(r'''
PASTA_DATAJUD = PASTA_ESTUDO / 'dat' / 'datajud'
PASTA_IBGE = PASTA_ESTUDO / 'dat' / 'ibge'
ARQUIVO_MANIFESTO = PASTA_DATAJUD / 'manifesto.json'
if ARQUIVO_MANIFESTO.exists():
    manifesto = json.loads(ARQUIVO_MANIFESTO.read_text(encoding='utf-8'))
    print(f"Fonte: {manifesto['fonte']}")
    print(f"Coleta: {manifesto['inicio_coleta_utc'][:16]} a {manifesto['fim_coleta_utc'][:16]} (UTC)")
    display(pd.DataFrame({'Coletados': manifesto['processos'], 'Soma das fatias na API': manifesto['total_api_fatias'],
                          'Total sem fatiar na API': manifesto['total_api_sem_fatiar']}))
else:  # coleta ainda em andamento: usa o que já está no cache e a data de modificação mais recente
    ultima = max(a.stat().st_mtime for a in PASTA_DATAJUD.glob('*.jsonl.gz'))
    manifesto = {'fim_coleta_utc': pd.Timestamp(ultima, unit='s').isoformat()}
    print('ATENÇÃO: coleta incompleta (sem manifesto). Resultados provisórios.')
estados = pd.DataFrame({a.name.replace('.estado.json', ''): json.loads(a.read_text(encoding='utf-8'))
                        for a in PASTA_DATAJUD.glob('*.estado.json')}).T
print(f"Fatias concluídas: {int(estados['fim'].astype(bool).sum())} de {len(estados)}; "
      f"processos no cache: {int(estados['n'].sum()):,} de {int(pd.to_numeric(estados['total_api'], errors='coerce').sum()):,} informados pela API")

registros = []
for arquivo in sorted(PASTA_DATAJUD.glob('*.jsonl.gz')):
    segmento = arquivo.name.split('__')[0]
    try:
        with gzip.open(arquivo, 'rt', encoding='utf-8') as f:
            for linha in f:
                try:
                    r = json.loads(linha)
                except json.JSONDecodeError:  # linha final incompleta durante a coleta
                    continue
                r['segmento'] = segmento
                registros.append(r)
    except (EOFError, OSError):  # bloco gzip ainda sendo gravado
        pass
print(f'{len(registros):,} registros lidos de {len(list(PASTA_DATAJUD.glob("*.jsonl.gz")))} fatias')
''')

md(r'''
### 22.2 Curadoria dos dados do DataJud

A curadoria segue o mesmo rigor da Etapa 1:

1. **Duplicidade:** um processo pode aparecer em mais de um grau ou sistema. Mantém-se um registro por número CNJ: o de 1º grau com mais movimentos;
2. **Datas:** `dataAjuizamento` vem como texto `aaaammddhhmmss` (às vezes com 8 dígitos ou em ISO). A conversão tolera os três formatos, e datas impossíveis viram `NaT` e são registradas;
3. **Município e comarca:** o código IBGE do órgão julgador é traduzido pelo cadastro do IBGE (`dat/ibge/`), e as seis comarcas da amostra são marcadas;
4. **Assuntos:** o processo pode ter vários. A partir deles constroem-se três atributos (22.3);
5. **Movimentos:** cada movimento da TPU vira data de evento ou indicador (22.4).
''')

code(r'''
def data_datajud(valor):
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return pd.NaT
    texto = re.sub(r'\D', '', str(valor))
    for formato, tamanho in (('%Y%m%d%H%M%S', 14), ('%Y%m%d', 8)):
        if len(texto) >= tamanho:
            data = pd.to_datetime(texto[:tamanho], format=formato, errors='coerce')
            if pd.notna(data) and pd.Timestamp('1950-01-01') <= data <= pd.Timestamp('2027-12-31'):
                return data
    return pd.NaT


def lista_assuntos(r):
    codigos = []
    for a in r.get('assuntos') or []:
        for item in (a if isinstance(a, list) else [a]):
            if isinstance(item, dict) and item.get('codigo') is not None:
                codigos.append(int(item['codigo']))
    return codigos


municipios_ibge = pd.DataFrame([{'Codigo_IBGE': int(m['id']), 'Municipio': m['nome'],
                                 'Mesorregiao': (m.get('microrregiao') or {}).get('mesorregiao', {}).get('nome')}
                                for m in json.loads((PASTA_IBGE / 'municipios_go.json').read_text(encoding='utf-8'))])
populacao = json.loads((PASTA_IBGE / 'populacao_censo2022_go.json').read_text(encoding='utf-8'))[0]['resultados'][0]['series']
municipios_ibge = municipios_ibge.merge(pd.DataFrame([{'Codigo_IBGE': int(s['localidade']['id']), 'Populacao_2022': int(s['serie']['2022'])}
                                                      for s in populacao]), on='Codigo_IBGE', how='left').set_index('Codigo_IBGE')
CODIGO_IBGE_COMARCA = {'Goiânia': 5208707, 'Aparecida de Goiânia': 5201405, 'Anápolis': 5201108, 'Senador Canedo': 5220454,
                       'Luziânia': 5212501, 'Águas Lindas de Goiás': 5200258}

linhas = []
for r in registros:
    orgao = r.get('orgaoJulgador') or {}
    movimentos = r.get('movimentos') or []
    linhas.append({
        'Numero_processo': str(r.get('numeroProcesso')), 'Segmento': r['segmento'], 'Grau': r.get('grau'),
        'Sistema': (r.get('sistema') or {}).get('nome'), 'Classe': (r.get('classe') or {}).get('codigo'),
        'Classe_nome': (r.get('classe') or {}).get('nome'), 'Orgao': orgao.get('nome'),
        'Codigo_IBGE': pd.to_numeric(orgao.get('codigoMunicipioIBGE'), errors='coerce'),
        'Ajuizamento_bruto': r.get('dataAjuizamento'), 'Data_ajuizamento': data_datajud(r.get('dataAjuizamento')),
        'Assuntos': lista_assuntos(r), 'N_movimentos': len(movimentos), 'Movimentos': movimentos,
        'Ultima_atualizacao': pd.to_datetime(r.get('dataHoraUltimaAtualizacao'), errors='coerce', utc=True),
    })
pop = pd.DataFrame(linhas)
n_bruto = len(pop)
pop = (pop.assign(_g1=pop['Grau'].eq('G1'))
          .sort_values(['Numero_processo', '_g1', 'N_movimentos'], ascending=[True, False, False])
          .drop_duplicates('Numero_processo').drop(columns='_g1').set_index('Numero_processo'))
pop['Municipio'] = pop['Codigo_IBGE'].map(municipios_ibge['Municipio'])
pop['Mesorregiao'] = pop['Codigo_IBGE'].map(municipios_ibge['Mesorregiao'])
pop['Comarca_alvo'] = pop['Codigo_IBGE'].map({v: k for k, v in CODIGO_IBGE_COMARCA.items()}).fillna('Demais municípios')

DATA_COLETA_DJ = pd.Timestamp(manifesto['fim_coleta_utc'][:10])
curadoria_dj = pd.DataFrame([
    ('Registros lidos', n_bruto), ('Duplicados removidos (mesmo número CNJ)', n_bruto - len(pop)),
    ('Processos únicos', len(pop)), ('Sem data de ajuizamento válida', int(pop['Data_ajuizamento'].isna().sum())),
    ('Ajuizamento posterior à coleta', int((pop['Data_ajuizamento'] > DATA_COLETA_DJ).sum())),
    ('Sem município (código IBGE)', int(pop['Municipio'].isna().sum())),
    ('Sem nenhum movimento', int(pop['N_movimentos'].eq(0).sum())),
], columns=['Verificação', 'Processos']).set_index('Verificação')
display(curadoria_dj)
display(pd.crosstab(pop['Classe_nome'], pop['Segmento'], margins=True, margins_name='Total'))
''')

md(r'''
### 22.3 Operacionalização de CVLI e MVI

**O conceito no material da disciplina.** A Tabela 01 do estudo de caso seleciona os municípios do **Pronasci II** no Centro-Oeste pela **taxa de Mortes Violentas Intencionais (MVI)** de 2022 (FBSP/MJSP). As seis comarcas da amostra são justamente os municípios goianos dessa lista. Há dois indicadores oficiais:

- **CVLI (Crimes Violentos Letais Intencionais, Senasp/MJSP):** homicídio doloso (inclusive o feminicídio), latrocínio e lesão corporal seguida de morte;
- **MVI (FBSP):** CVLI mais as **mortes decorrentes de intervenção policial**.

**Tradução para a TPU.** O assunto do processo vira três atributos, cada um uma partição:

| Atributo | Regra | Categorias |
|---|---|---|
| `Tipo_cvli` | assunto mais específico presente, na ordem feminicídio → latrocínio → homicídio qualificado → privilegiado → simples → homicídio (n.e.) → lesão corporal seguida de morte | 7 tipos |
| `Modalidade` | **culposo** se houver o assunto "Crime Culposo" (5865) ou "Crimes de Trânsito" (3632); **tentado** se houver "Crime Tentado" (5555); senão **consumado** | consumado, tentado, culposo |
| `Categoria_indicador` | consumado → **CVLI**; tentado → **tentativa de CVLI**; culposo → **fora do indicador** | 3 classes |

As **mortes por intervenção policial** não têm assunto próprio na TPU e não podem ser separadas no DataJud. Por isso o DataJud mede CVLI, e não MVI. Na amostra, o indício textual de intervenção estatal (14 casos) faz essa ponte. A amostra inclui tentativas (42 casos); para comparar, a população é filtrada da mesma forma: consumados mais tentados, sem os culposos.
''')

code(r'''
TIPOS_CVLI = [('Feminicídio', {12091}), ('Latrocínio', {5567, 11159}), ('Homicídio qualificado', {3372, 9638}),
              ('Homicídio privilegiado', {3371, 9637}), ('Homicídio simples', {3370, 9636}),
              ('Homicídio (espécie não especificada)', {11243}), ('Lesão corporal seguida de morte', {3387, 9643})]
CULPOSO, TENTADO = {5865, 3632}, {5555}


def tipo_cvli(codigos):
    codigos = set(codigos)
    return next((nome for nome, conjunto in TIPOS_CVLI if codigos & conjunto), None)


pop['Tipo_cvli'] = para_categoria(pop['Assuntos'].map(tipo_cvli), {n: n for n, _ in TIPOS_CVLI}, [n for n, _ in TIPOS_CVLI])
pop['Modalidade'] = para_categoria(pop['Assuntos'].map(
    lambda c: 'Culposo' if set(c) & CULPOSO else 'Tentado' if set(c) & TENTADO else 'Consumado'),
    {m: m for m in ['Consumado', 'Tentado', 'Culposo']}, ['Consumado', 'Tentado', 'Culposo'])
pop['Categoria_indicador'] = para_categoria(pop['Modalidade'].astype(str),
                                            {'Consumado': 'CVLI', 'Tentado': 'Tentativa de CVLI', 'Culposo': 'Fora do indicador (culposo)'},
                                            ['CVLI', 'Tentativa de CVLI', 'Fora do indicador (culposo)'])
display(verificar_particao(pop['Tipo_cvli']))
display(verificar_particao(pop['Categoria_indicador']))
display(pd.crosstab(pop['Tipo_cvli'], pop['Categoria_indicador'], margins=True, margins_name='Total'))
''')

md(r'''
### 22.4 A linha do tempo do inquérito no DataJud: início, retorno da polícia, manifestação do MP e decisão

Cada ato do processo é registrado com um código da Tabela Processual Unificada (TPU) do CNJ. A API pública **não informa quem praticou o ato**: polícia, MP ou juízo. Por isso, os marcos do inquérito são reconstruídos a partir de **movimentos característicos**. A análise exploratória dos 13,5 mil processos de 2022 em diante sustenta estas definições:

| Marco | Definição operacional | Por que tem sentido no negócio |
|---|---|---|
| **Início** | data de ajuizamento: a **distribuição do IP ao juízo** | coincide com o primeiro movimento em 99,9% dos casos. É o mesmo marco do "recebimento no Projudi" da amostra |
| **Retorno da polícia** (proxy do fim da investigação) | último movimento 15000, "**Finalizada** tramitação direta entre MP e autoridade policial", antes do desfecho | marca a volta dos autos da polícia ao sistema judicial. Só existe nos IPs com tramitação direta |
| **Manifestação final do MP** | última petição do tipo **Denúncia**, **Parecer**, **Parecer de mérito (MP)** ou **Parecer falta de interesse (MP)** antes do desfecho | é o equivalente da "conclusão no MP" da amostra: o promotor oferece denúncia ou pede o arquivamento |
| **Desfecho judicial** (evento principal) | primeiro entre: recebimento da denúncia (391) ou mudança para ação penal (evolução 14739; retificação 14738 no segmento C); determinação de arquivamento (1063), arquivamento (12430) ou arquivamento definitivo (246); extinção da punibilidade por prescrição (11878) ou morte do agente (1042) | é o ato que **encerra** a fase investigativa. É objetivo e está presente em todos os processos encerrados |

A partir desses marcos, três durações são medidas:

- **Fase judicial** = início → desfecho judicial. É o desfecho principal, comparável à fase judicial da amostra. Nos casos sem desfecho até a coleta, é censurada;
- **Até o MP** = início → manifestação final do MP. É o análogo direto da medida da amostra, mas só existe quando a petição do MP está registrada;
- **Fase policial (proxy)** = início → retorno da polícia, só nos IPs com tramitação direta.

**Diferença em relação à amostra.** O evento da amostra é a manifestação do MP; aqui, o principal é o ato judicial que a acolhe. Por isso, cada comparação informa a defasagem entre os dois. Um arquivamento seguido de desarquivamento é uma **reabertura**: a análise usa o primeiro encerramento e conta as reaberturas.
''')

code(r'''
MOVIMENTOS_INTERESSE = {
    # código: (papel, descrição)
    14732: ('conversao', 'Conversão de autos físicos em eletrônicos'),
    14999: ('td_inicio', 'Iniciada tramitação direta MP–polícia'),
    15000: ('retorno_policia', 'Finalizada tramitação direta MP–polícia (retorno dos autos da polícia)'),
    1063: ('arquivamento', 'Determinação de arquivamento de procedimento investigatório'),
    12430: ('arquivamento', 'Arquivamento'),
    246: ('arquivamento', 'Arquivamento definitivo'),
    893: ('desarquivamento', 'Desarquivamento (reabertura)'),
    391: ('denuncia', 'Recebimento da denúncia'),
    14739: ('denuncia', 'Evolução da classe processual (IP → ação penal)'),
    11878: ('extincao', 'Extinção da punibilidade: prescrição'),
    1042: ('extincao', 'Extinção da punibilidade: morte do agente'),
    12332: ('prorrogacao', 'Prorrogado o prazo de conclusão do inquérito'),
    12742: ('custodia', 'Audiência de custódia'),
    12140: ('preventiva', 'Conversão do flagrante em preventiva'),
    818: ('liberdade_provisoria', 'Liberdade provisória'),
    85: ('peticao', 'Petição (o tipo vem no complemento)'),
    14738: ('retificacao_classe', 'Retificação da classe processual (nas ações penais do segmento C, marca a denúncia)'),
}
PETICOES_MP = {'Denúncia', 'Parecer', 'Parecer de Mérito (MP)', 'Parecer Falta de Interesse (MP)'}
PAPEIS_FIM = ('denuncia', 'arquivamento', 'extincao')


def linha_do_tempo(movimentos, retificacao_e_denuncia=False):
    """Datas dos marcos do inquérito a partir dos movimentos (datas como texto aaaa-mm-dd, para rapidez)."""
    datas = defaultdict(list)
    for m in movimentos:
        papel = MOVIMENTOS_INTERESSE.get(m.get('codigo'), (None,))[0]
        if papel == 'retificacao_classe':
            papel = 'denuncia' if retificacao_e_denuncia else None
        data = (m.get('dataHora') or '')[:10]
        if papel is None or len(data) != 10:
            continue
        if papel == 'peticao':
            tipos = {c.get('nome') for c in m.get('complementosTabelados') or []}
            if tipos & PETICOES_MP:
                datas['peticao_mp'].append(data)
            continue
        datas[papel].append(data)
        if m.get('codigo') == 11878:
            datas['prescricao'].append(data)
    fins = {p: min(datas[p]) for p in PAPEIS_FIM if datas[p]}
    fim = min(fins.values()) if fins else None
    tipo_fim = min(fins, key=fins.get) if fins else None
    antes = lambda lista: max([d for d in lista if fim is None or d <= fim], default=None)
    return {'Data_fim': fim, 'Papel_fim': tipo_fim, 'Data_conversao': min(datas['conversao'], default=None),
            'Data_retorno_policia': antes(datas['retorno_policia']), 'Data_manifestacao_mp': antes(datas['peticao_mp']),
            'Data_desarquivamento': min(datas['desarquivamento'], default=None),
            **{f'N_{p}': len(datas[p]) for p in ['td_inicio', 'retorno_policia', 'arquivamento', 'desarquivamento', 'denuncia',
                                                 'extincao', 'prescricao', 'prorrogacao', 'custodia', 'preventiva',
                                                 'liberdade_provisoria', 'peticao_mp']}}


eventos_dj = pd.DataFrame([linha_do_tempo(movs, seg == 'acao_penal_retificada') for movs, seg in zip(pop['Movimentos'], pop['Segmento'])],
                          index=pop.index)
for c in [c for c in eventos_dj if c.startswith('Data_')]:
    eventos_dj[c] = pd.to_datetime(eventos_dj[c], errors='coerce')
pop = pop.join(eventos_dj)

presenca = pd.DataFrame([{'Código TPU': c, 'Papel': p, 'Descrição': d,
                          'Processos com o movimento (%)': 100 * pop['Movimentos'].map(lambda ms, c=c: any(m.get('codigo') == c for m in ms)).mean()}
                         for c, (p, d) in MOVIMENTOS_INTERESSE.items()]).set_index('Código TPU')
display(presenca.round(1))

MAPA_FIM = {'denuncia': 'Denúncia', 'arquivamento': 'Arquivamento', 'extincao': 'Extinção da punibilidade'}
pop['Tipo_fim'] = para_categoria(pop['Papel_fim'].map(MAPA_FIM).fillna('Em curso'),
                                 {k: k for k in ['Arquivamento', 'Denúncia', 'Extinção da punibilidade', 'Em curso']},
                                 ['Arquivamento', 'Denúncia', 'Extinção da punibilidade', 'Em curso'])
pop['Evento_fim'] = pop['Data_fim'].notna()
pop['Convertido'] = pop['Data_conversao'].notna()
pop['Fim_observado'] = pop['Data_fim'].fillna(DATA_COLETA_DJ)
pop['Tempo_judicial_dj'] = (pop['Fim_observado'] - pop['Data_ajuizamento'].dt.normalize()).dt.days
pop['Tempo_ate_mp_dj'] = (pop['Data_manifestacao_mp'] - pop['Data_ajuizamento'].dt.normalize()).dt.days
pop['Tempo_policial_proxy_dj'] = (pop['Data_retorno_policia'] - pop['Data_ajuizamento'].dt.normalize()).dt.days
pop['Defasagem_mp_decisao'] = (pop['Data_fim'] - pop['Data_manifestacao_mp']).dt.days
pop['Ano_ajuizamento'] = pop['Data_ajuizamento'].dt.year
pop['APF'] = pop['Classe'].eq(280)  # classe de origem; nas ações penais evoluídas a origem se perde (não usada em modelos)
pop['Tramitacao_direta_dj'] = pop['N_td_inicio'].gt(0)
pop['Indicio_prisao'] = pop[['N_custodia', 'N_preventiva', 'N_liberdade_provisoria']].sum(axis=1).gt(0)
pop['Houve_prorrogacao'] = pop['N_prorrogacao'].gt(0)
pop['Reaberto'] = pop['N_desarquivamento'].gt(0)

incoerencias_dj = pd.DataFrame([
    ('Desfecho anterior ao ajuizamento', int((pop['Data_fim'] < pop['Data_ajuizamento'].dt.normalize()).sum())),
    ('Manifestação do MP anterior ao ajuizamento', int((pop['Data_manifestacao_mp'] < pop['Data_ajuizamento'].dt.normalize()).sum())),
    ('Conversão anterior ao ajuizamento', int((pop['Data_conversao'] < pop['Data_ajuizamento'].dt.normalize()).sum())),
    ('Ação penal (segmentos B e C) sem marco de denúncia', int((pop['Segmento'].isin(['acao_penal_evoluida', 'acao_penal_retificada'])
                                                                & ~pop['Papel_fim'].eq('denuncia')).sum())),
    ('Encerrados sem manifestação do MP registrada', int((pop['Evento_fim'] & pop['Data_manifestacao_mp'].isna()).sum())),
], columns=['Regra de coerência', 'Processos']).set_index('Regra de coerência')
display(incoerencias_dj)

validos_dj = (pop['Data_ajuizamento'].notna() & (pop['Data_ajuizamento'] <= DATA_COLETA_DJ) & (pop['Tempo_judicial_dj'] >= 0)
              & pop['Municipio'].notna())
pop_cvli = pop[validos_dj & pop['Categoria_indicador'].ne('Fora do indicador (culposo)')].copy()
print(f'Processos analisáveis (CVLI consumado ou tentado, datas coerentes): {len(pop_cvli):,} de {len(pop):,}')
''')

md(r'''
### 22.5 A janela de tempo e o recorte que reproduz o estudo

Os processos **convertidos** são o estoque físico que sobreviveu até a digitalização e, como na amostra, sofrem truncamento. Os **nativos digitais** formam uma coorte **sem truncamento**, acompanhada desde o ajuizamento.

**O recorte que reproduz o estudo.** A amostra reúne IPs que tramitaram no Projudi de 2022 em diante. Por isso a população é recortada nos **inquéritos de CVLI ajuizados de 2022 a 2026**, no Estado inteiro, com as seis comarcas destacadas.

O gráfico da direita mostra por que os IPs antigos não podem ser identificados pela data de digitalização: o TJGO converteu quase todos os autos físicos em 2020–2021, antes da janela da amostra. A data de "recebimento no Projudi" dos IPs antigos da amostra é outro marco: a volta do inquérito à tramitação.
''')

code(r'''
por_ano = pd.crosstab(pop_cvli['Ano_ajuizamento'], pop_cvli['Convertido'].map({False: 'Nativo digital', True: 'Convertido'}))
por_ano['% nativos'] = 100 * por_ano.get('Nativo digital', 0) / por_ano.drop(columns='% nativos', errors='ignore').sum(axis=1)
fig, axes = plt.subplots(1, 2, figsize=(16, 4.6))
anos_plot = por_ano.loc[por_ano.index >= 2005]
axes[0].bar(anos_plot.index, anos_plot.get('Convertido', 0), color=COR_DESTAQUE, label='Convertido (autos físicos digitalizados)')
axes[0].bar(anos_plot.index, anos_plot.get('Nativo digital', 0), bottom=anos_plot.get('Convertido', 0), color=COR_PRINCIPAL, label='Nativo digital')
axes[0].set_xlabel('ano de ajuizamento')
axes[0].set_ylabel('processos de CVLI (consumado ou tentado)')
axes[0].set_title('Processos baixados por ano de ajuizamento')
axes[0].legend()
conversoes = pop_cvli.loc[pop_cvli['Convertido'], 'Data_conversao'].dt.to_period('M').value_counts().sort_index()
axes[1].bar(conversoes.index.to_timestamp(), conversoes.values, width=25, color=COR_DESTAQUE)
axes[1].axvspan(pd.Timestamp('2022-01-01'), pd.Timestamp('2025-06-30'), color=COR_SECUNDARIA, alpha=0.3, label='janela da amostra')
axes[1].set_title('Quando os autos físicos foram convertidos')
axes[1].set_ylabel('conversões no mês')
axes[1].legend()
plt.tight_layout()
plt.show()

antigos = pop_cvli[pop_cvli['Ano_ajuizamento'] < 2022]
print(f'Ajuizados antes de 2022 e convertidos: {int(antigos["Convertido"].sum()):,}; '
      f'{100 * antigos["Data_conversao"].dt.year.le(2021).sum() / max(antigos["Convertido"].sum(), 1):.0f}% digitalizados até 2021')
ANO_INICIO_COORTE = 2022
coorte_dj = pop_cvli[pop_cvli['Ano_ajuizamento'].ge(ANO_INICIO_COORTE) & ~pop_cvli['Convertido']].copy()
coorte_dj['Porte_municipio'] = pd.cut(coorte_dj['Codigo_IBGE'].map(municipios_ibge['Populacao_2022']).astype(float),
                                      [0, 50_000, 200_000, 1_000_000, np.inf],
                                      labels=['até 50 mil', '50–200 mil', '200 mil–1 milhão', 'mais de 1 milhão'], ordered=True)
coorte_dj['Ano_ajuizamento_cat'] = pd.Categorical(coorte_dj['Ano_ajuizamento'], ordered=True)
coorte_dj['Comarca_alvo'] = pd.Categorical(coorte_dj['Comarca_alvo'], categories=list(CODIGO_IBGE_COMARCA) + ['Demais municípios'])
coorte_dj['Mesorregiao'] = coorte_dj['Mesorregiao'].astype('category')
coorte_dj['Modalidade'] = coorte_dj['Modalidade'].cat.remove_unused_categories()
for v in ['Indicio_prisao', 'Tramitacao_direta_dj', 'Houve_prorrogacao']:
    coorte_dj[v] = coorte_dj[v].astype('boolean')
ROTULOS_BOOLEANOS.update({'Indicio_prisao': ('Sem indício de prisão', 'Com indício de prisão'),
                          'Tramitacao_direta_dj': ('Sem TD', 'Com TD'), 'Houve_prorrogacao': ('Sem prorrogação', 'Com prorrogação')})
print(f'Coorte 2022–{DATA_COLETA_DJ.year} (nativa digital): {len(coorte_dj):,} processos; {int(coorte_dj["Evento_fim"].sum()):,} '
      f'com desfecho; coleta em {DATA_COLETA_DJ:%d/%m/%Y}')
display(pd.crosstab(coorte_dj['Comarca_alvo'], coorte_dj['Tipo_fim'], margins=True, margins_name='Total'))
''')

interp('dj_janela')

md(r'''
### 22.6 Descrição e normalidade na população

Mesma sequência da Etapa 1, agora na coorte estadual:

- **descrição** dos marcos, incluindo os tempos das três etapas;
- **normalidade:** Shapiro-Wilk em uma subamostra de 5 mil, porque o teste é definido até esse tamanho, e D'Agostino-Pearson na base inteira.

Com milhares de casos, qualquer desvio da normal é detectado. Por isso o gráfico Q-Q é o que mostra a **magnitude** do afastamento.
''')

code(r'''
concl_dj = coorte_dj[coorte_dj['Evento_fim']].copy()
DESFECHOS_DJ = {'Tempo_judicial_dj': 'Fase judicial (ajuizamento → desfecho judicial)',
                'Tempo_ate_mp_dj': 'Até o MP (ajuizamento → manifestação final do MP)',
                'Tempo_policial_proxy_dj': 'Fase policial, proxy (ajuizamento → retorno da polícia)'}
display(pd.DataFrame({r: descrever(concl_dj[v]) for v, r in DESFECHOS_DJ.items()}).round(1))
print(f"Defasagem manifestação do MP → decisão judicial (dias): mediana = {concl_dj['Defasagem_mp_decisao'].median():.0f}; "
      f"Q1–Q3 = {concl_dj['Defasagem_mp_decisao'].quantile(0.25):.0f}–{concl_dj['Defasagem_mp_decisao'].quantile(0.75):.0f}")

x_dj = concl_dj['Tempo_judicial_dj'].astype(float).to_numpy() + 0.5
sub_sw = RNG.choice(x_dj, size=min(len(x_dj), 5000), replace=False)
print(f'Normalidade da fase judicial (encerrados): Shapiro-Wilk (subamostra de {len(sub_sw):,}) W = {stats.shapiro(sub_sw).statistic:.3f}, '
      f'p = {stats.shapiro(sub_sw).pvalue:.1e}; D\'Agostino p = {stats.normaltest(x_dj).pvalue:.1e}; assimetria = {stats.skew(x_dj):.2f}')

fig, axes = plt.subplots(1, 4, figsize=(21, 4.8), gridspec_kw={'width_ratios': [2, 1, 1.4, 1.4]})
axes[0].hist(x_dj, bins=60, color=COR_PRINCIPAL, edgecolor='white')
axes[0].axvline(np.median(x_dj), color=TINTA, linestyle='--', label=f'mediana = {np.median(x_dj):.0f} dias')
axes[0].axvline(x_dj.mean(), color=COR_DESTAQUE, label=f'média = {x_dj.mean():.0f} dias')
axes[0].set_xlabel('dias')
axes[0].set_ylabel('processos')
axes[0].set_title('Fase judicial na população (encerrados)')
axes[0].legend()
axes[1].boxplot(x_dj, widths=0.5, patch_artist=True, boxprops={'facecolor': COR_SECUNDARIA}, medianprops={'color': TINTA, 'linewidth': 2})
axes[1].set_xticks([1], ['encerrados'])
axes[1].set_ylabel('dias')
axes[1].set_title('boxplot')
axes[1].grid(axis='x', visible=False)
(osm, osr), (a, b, _) = stats.probplot(sub_sw, dist='norm')
axes[2].scatter(osm, osr, s=6, color=COR_PRINCIPAL)
axes[2].plot(osm, a * osm + b, color=COR_DESTAQUE)
axes[2].set_xlabel('quantis teóricos da normal')
axes[2].set_ylabel('dias')
axes[2].set_title('Q-Q normal (subamostra)')
etapas = concl_dj[['Tempo_policial_proxy_dj', 'Tempo_ate_mp_dj', 'Tempo_judicial_dj']].astype(float)
axes[3].boxplot([etapas[c].dropna() for c in etapas], showfliers=False, patch_artist=True, widths=0.55,
                boxprops={'facecolor': COR_SECUNDARIA}, medianprops={'color': TINTA, 'linewidth': 2})
axes[3].set_xticks([1, 2, 3], ['até retorno\nda polícia', 'até manifestação\ndo MP', 'até decisão\njudicial'])
axes[3].set_ylabel('dias desde o ajuizamento')
axes[3].set_title('As três etapas (encerrados)')
axes[3].grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
''')

interp('dj_descricao')

md(r'''
### 22.7 Testes de hipóteses na população

As mesmas famílias de testes da seção 17, agora com milhares de casos:

1. **Tipo de desfecho × variáveis:** qui-quadrado de independência, com V de Cramér e barras empilhadas. Com n grande, p pequeno é quase certo, e é o **V** que diz se a associação é relevante;
2. **Fase judicial × grupos:** Mann-Whitney e Kruskal-Wallis nos encerrados, com tamanho de efeito, boxplots e post-hoc de Dunn.

**Variáveis disponíveis na população:**

- comarca (as seis da amostra e os demais municípios), mesorregião e porte do município (Censo 2022);
- tipo de CVLI e modalidade (consumado ou tentado);
- indício de prisão (custódia, preventiva, liberdade provisória);
- ano de ajuizamento;
- tramitação direta e prorrogação de prazo, que acontecem **durante** o procedimento e são lidas como descrição, não como efeito.

A classe de origem **APF** não é usada: nos IPs que viraram ação penal, a classe muda para 282/283 e a origem em flagrante se perde. O indício de prisão a substitui.
''')

code(r'''
VARIAVEIS_DJ = ['Comarca_alvo', 'Mesorregiao', 'Porte_municipio', 'Tipo_cvli', 'Modalidade', 'Indicio_prisao', 'Ano_ajuizamento_cat',
                'Tramitacao_direta_dj', 'Houve_prorrogacao']
CORES_DESFECHO.update({'Extinção da punibilidade': CORES[3], 'Em curso': CORES[2]})
assoc_dj, tabelas_dj = [], {}
for v in VARIAVEIS_DJ:
    x = serie_exibicao(coorte_dj, v)
    validos = x.notna()
    tabela, resultado = teste_associacao(x[validos].astype(str), coorte_dj.loc[validos, 'Tipo_fim'].astype(str), n_perm=2_000)
    tabelas_dj[v] = tabela
    assoc_dj.append({'Variável': v, **resultado})
assoc_dj = pd.DataFrame(assoc_dj).set_index('Variável')
assoc_dj['p BH'] = multipletests(assoc_dj['p-valor'], method='fdr_bh')[1]
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(assoc_dj.sort_values('V de Cramér', ascending=False))
fig, axes = plt.subplots(1, 3, figsize=(20, 5.6))
for ax, v in zip(axes, ['Comarca_alvo', 'Tipo_cvli', 'Indicio_prisao']):
    barras_verticais_empilhadas(ax, tabelas_dj[v].reindex(columns=['Arquivamento', 'Denúncia', 'Extinção da punibilidade', 'Em curso'],
                                                          fill_value=0), CORES_DESFECHO)
    ax.set_title(f'{v}: V de Cramér = {assoc_dj.loc[v, "V de Cramér"]:.2f}; p = {assoc_dj.loc[v, "p-valor"]:.2g}', fontsize=9.5)
axes[0].legend(fontsize=8, loc='lower left')
plt.suptitle('População (coorte 2022+): tipo de desfecho por grupo', fontweight='bold')
plt.tight_layout()
plt.show()

testes_dj = []
for v in VARIAVEIS_DJ:
    r = comparar_grupos(concl_dj.assign(**{v: serie_exibicao(concl_dj, v)}), 'Tempo_judicial_dj', v)
    if r:
        testes_dj.append({'Variável': v, **r})
testes_dj = pd.DataFrame(testes_dj).set_index('Variável')
testes_dj['p BH'] = multipletests(testes_dj['p-valor'], method='fdr_bh')[1]
with pd.option_context('display.float_format', lambda v: f'{v:.4g}', 'display.max_colwidth', 140):
    display(testes_dj.sort_values('Efeito', ascending=False))
fig, axes = plt.subplots(2, 3, figsize=(19, 11))
for ax, v in zip(axes.flat, ['Comarca_alvo', 'Tipo_cvli', 'Modalidade', 'Indicio_prisao', 'Porte_municipio', 'Ano_ajuizamento_cat']):
    boxplot_grupos(ax, concl_dj, 'Tempo_judicial_dj', v)
for ax in axes[:, 0]:
    ax.set_ylabel('dias (fase judicial)')
plt.suptitle('População: fase judicial por grupo (encerrados; letras = Dunn–Holm)', fontweight='bold')
plt.tight_layout()
plt.show()
''')

interp('dj_testes')

md(r'''
### 22.8 Que distribuição descreve o tempo na população?

O mesmo procedimento da seção 18, aplicado aos encerrados da coorte:

1. ajuste das seis famílias;
2. AIC e BIC;
3. teste da razão de verossimilhança;
4. **FDA empírica × FDA teórica**, com os parâmetros.

A aderência por bootstrap usa uma subamostra aleatória de mil processos. Com dezenas de milhares, o KS rejeitaria qualquer modelo por diferenças irrelevantes.
''')

code(r'''
x_fit = concl_dj['Tempo_judicial_dj'].astype(float).to_numpy() + 0.5
ajustes_conc_dj, tabela_conc_dj = ajustar_scipy(x_fit)
display(tabela_conc_dj.round(3))
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(razao_verossimilhanca_scipy(tabela_conc_dj))
sub_fit = RNG.choice(x_fit, size=min(len(x_fit), 1000), replace=False)
aderencia_dj = pd.DataFrame({n: aderencia_bootstrap(sub_fit, n, n_boot=100) for n in tabela_conc_dj.index[:3]}).T
print('Aderência (subamostra de 1.000; 100 réplicas):')
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(aderencia_dj)

xs = np.sort(x_fit)
ecdf = np.arange(1, len(xs) + 1) / len(xs)
grade = np.linspace(0.5, np.percentile(xs, 99.5), 600)
fig, axes = plt.subplots(1, 2, figsize=(17, 5))
axes[0].step(xs, ecdf, where='post', color=TINTA, linewidth=2, label='FDA empírica (encerrados)')
for nome, cor in zip(tabela_conc_dj.index[:3], [COR_PRINCIPAL, COR_DESTAQUE, CORES[2]]):
    dist, params = ajustes_conc_dj[nome]
    forma = ', '.join(f'{p:.2f}' for p in params[:-2])
    axes[0].plot(grade, dist.cdf(grade, *params), color=cor, linewidth=1.8,
                 label=f'{nome} ({"forma " + forma + "; " if forma else ""}escala {params[-1]:,.0f})')
axes[0].set_xlim(0, grade.max())
axes[0].set_xlabel('dias')
axes[0].set_ylabel('F(t)')
axes[0].set_title('População: FDA empírica × FDA teórica (3 melhores por AIC)')
axes[0].legend(fontsize=8.5, loc='lower right')
axes[1].hist(xs[xs <= grade.max()], bins=60, density=True, color=COR_SECUNDARIA, edgecolor='white', label='histograma')
for nome, cor in zip(tabela_conc_dj.index[:3], [COR_PRINCIPAL, COR_DESTAQUE, CORES[2]]):
    dist, params = ajustes_conc_dj[nome]
    axes[1].plot(grade, dist.pdf(grade, *params), color=cor, linewidth=1.8, label=nome)
axes[1].set_xlabel('dias')
axes[1].set_ylabel('densidade')
axes[1].set_title('Histograma × densidade ajustada')
axes[1].legend()
plt.tight_layout()
plt.show()
''')

interp('dj_distribuicao')

md(r'''
### 22.9 Regressões logísticas: denúncia e prescrição

Com milhares de desfechos, os modelos que a amostra não comportava (6 denúncias, 10 prescrições) são estimados aqui:

1. **Denúncia × arquivamento:** o que se associa à responsabilização?
2. **Extinção da punibilidade × arquivamento:** o que se associa a o Estado perder o prazo ou o objeto?

Em ambos entram comarca, tipo de CVLI, tentativa, indício de prisão, porte do município e ano de ajuizamento. As medidas de ajuste são razões de chance, pseudo-R² de McFadden e AUC.
''')

code(r'''
REFERENCIAS.update({'Comarca_modelo': 'Goiânia', 'Tipo_modelo': 'Homicídio simples', 'Ano_ajuizamento_cat': int(coorte_dj['Ano_ajuizamento'].min())})
coorte_dj['Comarca_modelo'] = coorte_dj['Comarca_alvo'].astype(str)
coorte_dj['Tipo_modelo'] = coorte_dj['Tipo_cvli'].astype(str).replace(
    {'Homicídio privilegiado': 'Outros', 'Homicídio (espécie não especificada)': 'Outros', 'Lesão corporal seguida de morte': 'Outros'})
X_dj = matriz_desenho(coorte_dj, ['Comarca_modelo', 'Tipo_modelo', 'Ano_ajuizamento_cat'], ['Indicio_prisao'], [])
X_dj['Tentado'] = coorte_dj['Modalidade'].eq('Tentado').astype(float)
X_dj['Log10_populacao'] = np.log10(coorte_dj['Codigo_IBGE'].map(municipios_ibge['Populacao_2022']).astype(float))


def logistica_populacao(alvo, base, titulo):
    sub = coorte_dj[coorte_dj['Tipo_fim'].isin([alvo, base])]
    X = sm.add_constant(X_dj.loc[sub.index].astype(float))
    X = X.loc[:, (X.std() > 0) | (X.columns == 'const')]
    y = sub['Tipo_fim'].eq(alvo).astype(int)
    modelo = sm.Logit(y, X).fit(disp=False, maxiter=300)
    p = modelo.predict()
    auc = stats.mannwhitneyu(p[y == 1], p[y == 0]).statistic / ((y == 1).sum() * (y == 0).sum())
    print(f'{titulo}: n = {int(modelo.nobs):,}; eventos = {int(y.sum()):,} ({100 * y.mean():.1f}%); pseudo-R² de McFadden = '
          f'{modelo.prsquared:.3f}; AUC = {auc:.3f}; LR χ² = {modelo.llr:.0f} (p = {modelo.llr_pvalue:.2g})')
    tabela = pd.DataFrame({'OR': np.exp(modelo.params), 'IC 2,5%': np.exp(modelo.conf_int()[0]),
                           'IC 97,5%': np.exp(modelo.conf_int()[1]), 'p-valor': modelo.pvalues}).drop('const')
    display(tabela.round(3))
    grafico_floresta(tabela.rename(columns={'OR': 'HR'}), titulo, rotulo_x='razão de chances (log) — IC 95%')
    return modelo, tabela


logit_den_dj, or_den_dj = logistica_populacao('Denúncia', 'Arquivamento', 'Chance de denúncia (× arquivamento) na coorte estadual')
logit_ext_dj, or_ext_dj = logistica_populacao('Extinção da punibilidade', 'Arquivamento',
                                             'Chance de extinção da punibilidade (× arquivamento) na coorte estadual')
''')

interp('dj_logistica')

md(r'''
### 22.10 Sobrevivência na população: Kaplan-Meier, log-rank, Cox e modelos paramétricos

A coorte é acompanhada **desde o ajuizamento**, sem truncamento, e os processos sem desfecho até a coleta entram como censurados. A sequência repete a da seção 20:

- curva geral;
- curvas por grupo, com log-rank e a razão de riscos (HR) do Cox univariado;
- Cox multivariável com teste dos riscos proporcionais e curvas ajustadas;
- famílias paramétricas com censura e modelo AFT.
''')

code(r'''
T_DJ = coorte_dj['Tempo_judicial_dj'].astype(float).to_numpy() + 0.5
E_DJ = coorte_dj['Evento_fim'].astype(int).to_numpy()
km_dj = KaplanMeierFitter().fit(T_DJ, E_DJ, label='Coorte estadual 2022+')
m, li, ls = mediana_ic(km_dj)
fig, ax = plt.subplots(figsize=(12, 5))
km_dj.plot_survival_function(ax=ax, color=COR_PRINCIPAL, linewidth=2.4)
for comarca_grupo, cor in [('Demais municípios', CORES[2])]:
    m_g = coorte_dj['Comarca_alvo'].eq(comarca_grupo).to_numpy()
    KaplanMeierFitter().fit(T_DJ[m_g], E_DJ[m_g], label='Demais municípios').plot_survival_function(ax=ax, color=cor, ci_show=False)
m_alvo = ~coorte_dj['Comarca_alvo'].eq('Demais municípios').to_numpy()
KaplanMeierFitter().fit(T_DJ[m_alvo], E_DJ[m_alvo], label='6 comarcas da amostra').plot_survival_function(ax=ax, color=COR_DESTAQUE, ci_show=False)
ax.axhline(0.5, color=TINTA_2, linestyle='--', linewidth=1)
ax.set_ylim(0, 1.02)
ax.set_xlabel('dias desde o ajuizamento')
ax.set_ylabel('S(t): proporção sem desfecho')
ax.set_title(f'População: mediana de Kaplan-Meier da fase judicial = {m:.0f} dias (IC {li:.0f}–{ls:.0f}); n = {len(T_DJ):,}')
plt.tight_layout()
plt.show()

km_dj_var = grade_km(coorte_dj, T_DJ, E_DJ, [v for v in VARIAVEIS_DJ if v != 'Mesorregiao'],
                     'População: Kaplan-Meier por variável (log-rank e HR do Cox univariado)', colunas=4)
logrank_dj = km_dj_var.groupby('Variável', sort=False)['p log-rank'].first().to_frame()
logrank_dj['p BH'] = multipletests(logrank_dj['p log-rank'], method='fdr_bh')[1]
display(logrank_dj.round(5))
with pd.option_context('display.max_rows', 120):
    display(km_dj_var.drop(columns='p log-rank').set_index(['Variável', 'Grupo']).round(0))
''')

code(r'''
base_dj = X_dj.assign(T=T_DJ, E=E_DJ).dropna()
base_dj = base_dj.loc[:, (base_dj.std() > 0) | base_dj.columns.isin(['T', 'E'])]
cox_dj = CoxPHFitter(penalizer=1e-4).fit(base_dj, 'T', 'E')
resumo_cox_dj = cox_dj.summary[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].set_axis(['HR', 'IC 2,5%', 'IC 97,5%', 'p-valor'], axis=1)
ll0 = cox_dj.log_likelihood_ - cox_dj.log_likelihood_ratio_test().test_statistic / 2
print(f'Cox na coorte: n = {len(base_dj):,}; eventos = {int(base_dj["E"].sum()):,}; C = {cox_dj.concordance_index_:.3f}; '
      f'pseudo-R² de Nagelkerke = {nagelkerke(cox_dj.log_likelihood_, ll0, len(base_dj))[1]:.3f}')
ph_dj = proportional_hazard_test(cox_dj, base_dj, time_transform='rank').summary['p']
display(resumo_cox_dj.assign(**{'p PH (Schoenfeld)': ph_dj}).round(4))
grafico_floresta(resumo_cox_dj, 'Cox — população (HR > 1 = desfecho mais rápido)')

fig, axes = plt.subplots(1, 3, figsize=(19, 4.8), sharey=True)
perfil = base_dj.drop(columns=['T', 'E']).mean().to_frame().T
for ax, (coluna, valores, rotulos) in zip(axes, [('Comarca_modelo=Aparecida de Goiânia', [0, 1], ['Goiânia (ref.)', 'Aparecida']),
                                                 ('Indicio_prisao', [0, 1], ['Sem indício de prisão', 'Com indício de prisão']),
                                                 ('Tipo_modelo=Homicídio qualificado', [0, 1], ['Homicídio simples', 'Homicídio qualificado'])]):
    if coluna not in perfil:
        continue
    perfis = pd.concat([perfil.assign(**{coluna: v}) for v in valores], ignore_index=True)
    curvas = cox_dj.predict_survival_function(perfis, times=np.linspace(0, np.percentile(T_DJ, 99), 300))
    for (_, curva), rotulo, cor in zip(curvas.items(), rotulos, CORES):
        ax.plot(curvas.index, curva, color=cor, linewidth=2.2, label=rotulo)
    hr = resumo_cox_dj.loc[coluna]
    ax.set_title(f'{quebrar(coluna, 34)}\nHR = {hr["HR"]:.2f} (IC {hr["IC 2,5%"]:.2f}–{hr["IC 97,5%"]:.2f})', fontsize=9.5)
    ax.axhline(0.5, color=TINTA_2, linestyle='--', linewidth=0.8)
    ax.set_xlabel('dias desde o ajuizamento')
    ax.legend(fontsize=8)
axes[0].set_ylabel('S(t) prevista pelo Cox')
plt.suptitle('População: curvas ajustadas pelo modelo de Cox', fontweight='bold')
plt.tight_layout()
plt.show()

ajustes_dj, tabela_dj = ajustar_familias(T_DJ, E_DJ)
display(tabela_dj.round(2))
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(razao_verossimilhanca(ajustes_dj))
diagnostico_sobrevivencia(T_DJ, E_DJ, ajustes_dj, km_dj, 'População (com censura)')

base_aft_dj = base_dj.copy()
base_aft_dj.columns = [re.sub(r'\W+', '_', unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode()).strip('_') for c in base_aft_dj.columns]
nomes_aft_dj = dict(zip(base_aft_dj.columns, base_dj.columns))
aft_dj = GeneralizedGammaRegressionFitter(penalizer=1e-4).fit(
    base_aft_dj, 'T', 'E', regressors={'mu_': ' + '.join(c for c in base_aft_dj if c not in ('T', 'E')), 'sigma_': '1', 'lambda_': '1'})
s = aft_dj.summary.loc['mu_'].drop(index='Intercept', errors='ignore')
tr_dj = pd.DataFrame({'TR': np.exp(s['coef']), 'IC 2,5%': np.exp(s['coef lower 95%']), 'IC 97,5%': np.exp(s['coef upper 95%']),
                      'p-valor': s['p']}).rename(index=nomes_aft_dj)
print(f'AFT gama generalizada na população: AIC = {aft_dj.AIC_:.0f}')
display(tr_dj.round(3))
''')

interp('dj_sobrevivencia')

md(r'''
### 22.11 A amostra diante da população: mesmas comarcas, mesma janela

Fecha-se o círculo comparando a amostra com a população **no mesmo recorte**: as seis comarcas, com ajuizamento de 2022 em diante. Em dois níveis:

1. **Amostra instaurada a partir de 2022** (recorte equivalente, n = 89);
2. **Amostra inteira**, para ver o que o estoque antigo muda no perfil.

**Testes:**

- **Proporções:** **binomial exato** da proporção da amostra contra a da população. A coorte é o censo do recorte, e sua proporção funciona como valor conhecido p₀;
- **Distribuição das comarcas:** **qui-quadrado de aderência**;
- **Tempo:** a **fase judicial** da amostra (recebimento no Projudi → conclusão no MP) contra a da população (ajuizamento → manifestação do MP ou → decisão judicial), por Kaplan-Meier e log-rank.
''')

code(r'''
coorte_alvo = coorte_dj[coorte_dj['Comarca_alvo'].ne('Demais municípios')].copy()
recente = dados[dados['Ano_instauracao'].ge(2022)]
populacao_cmp = pd.DataFrame({
    'Réu preso / indício de prisão': coorte_alvo['Indicio_prisao'].astype(bool), 'Tentado': coorte_alvo['Modalidade'].eq('Tentado'),
    'Homicídio qualificado': coorte_alvo['Tipo_cvli'].isin(['Homicídio qualificado', 'Feminicídio']),
    'Tramitação direta': coorte_alvo['Tramitacao_direta_dj'].astype(bool), 'Denúncia': coorte_alvo['Tipo_fim'].eq('Denúncia'),
})


def indicadores_amostra(df):
    return pd.DataFrame({'Réu preso / indício de prisão': df['Reu_preso'].astype(bool), 'Tentado': df['Tentativa'].astype(bool),
                         'Homicídio qualificado': df['Assunto_resumido'].isin(['Homicídio qualificado', 'Feminicídio']),
                         'Tramitação direta': df['Tramitacao_direta'].astype(bool), 'Denúncia': df['Desfecho'].eq('Denúncia oferecida')})


comparacao = []
for nivel, df in [('Amostra ≥ 2022 (recorte equivalente)', recente), ('Amostra inteira', dados)]:
    ind = indicadores_amostra(df)
    for v in ind:
        k, n, p0 = int(ind[v].sum()), len(ind), float(populacao_cmp[v].mean())
        teste = stats.binomtest(k, n, p0)
        ic = teste.proportion_ci(method='exact')
        comparacao.append({'Nível': nivel, 'Indicador': v, 'Amostra': f'{k}/{n}', '% amostra': 100 * k / n, 'IC 2,5%': 100 * ic.low,
                           'IC 97,5%': 100 * ic.high, '% população = p₀': 100 * p0, 'p-valor (binomial exato)': teste.pvalue})
comparacao = pd.DataFrame(comparacao)
comparacao['p BH'] = comparacao.groupby('Nível')['p-valor (binomial exato)'].transform(lambda p: multipletests(p, method='fdr_bh')[1])
with pd.option_context('display.float_format', lambda v: f'{v:.4g}'):
    display(comparacao.set_index(['Nível', 'Indicador']))

fig, axes = plt.subplots(1, 2, figsize=(18, 5.2), sharey=True)
for ax, (nivel, tab) in zip(axes, comparacao.groupby('Nível', sort=False)):
    x = np.arange(len(tab))
    props = tab['% amostra'].to_numpy()
    ax.bar(x - 0.18, props, width=0.36, color=COR_DESTAQUE, label='amostra (IC 95% exato)')
    ax.errorbar(x - 0.18, props, yerr=[props - tab['IC 2,5%'].to_numpy(), tab['IC 97,5%'].to_numpy() - props], fmt='none', ecolor=TINTA, capsize=4)
    ax.bar(x + 0.18, tab['% população = p₀'], width=0.36, color=COR_PRINCIPAL, label='população (p₀)')
    for xi, pv in zip(x, tab['p BH']):
        ax.text(xi, 102, f'p BH\n{pv:.2g}', ha='center', fontsize=8)
    ax.set_xticks(x, [quebrar(i, 14) for i in tab['Indicador']], fontsize=8.5)
    ax.set_ylim(0, 115)
    ax.set_title(f'{nivel} × população 2022+ (6 comarcas)', fontsize=10)
    ax.grid(axis='x', visible=False)
axes[0].set_ylabel('%')
axes[0].legend(loc='upper left', fontsize=8.5)
plt.suptitle('Teste binomial exato: proporção da amostra contra a da população', fontweight='bold')
plt.tight_layout()
plt.show()

observado = recente['Comarca'].value_counts().reindex(dados['Comarca'].cat.categories)
proporcao_pop = coorte_alvo['Comarca_alvo'].astype(str).value_counts(normalize=True).reindex(observado.index).fillna(0)
esperado = proporcao_pop * observado.sum()
aderencia_comarca = stats.chisquare(observado, esperado)
display(pd.DataFrame({'Amostra ≥ 2022': observado, 'Esperado pela população': esperado.round(1),
                      '% amostra': (100 * observado / observado.sum()).round(1), '% população': (100 * proporcao_pop).round(1),
                      'Resíduo de Pearson': ((observado - esperado) / np.sqrt(esperado)).round(2)}))
print(f'Qui-quadrado de aderência (comarcas): χ² = {aderencia_comarca.statistic:.2f}; gl = {len(observado) - 1}; '
      f'p = {aderencia_comarca.pvalue:.3g}; menor frequência esperada = {esperado.min():.1f}')
''')

code(r'''
# Fase judicial: amostra (Projudi → conclusão no MP) × população (ajuizamento → manifestação do MP; ajuizamento → decisão)
m_rec = dados['Ano_instauracao'].ge(2022).to_numpy()
T_POP = coorte_alvo['Tempo_judicial_dj'].astype(float) + 0.5
E_POP = coorte_alvo['Evento_fim'].astype(int)
mp_pop = coorte_alvo['Tempo_ate_mp_dj'].dropna().astype(float) + 0.5
curvas = [('Amostra ≥ 2022: Projudi → conclusão no MP', KaplanMeierFitter().fit(T_JUD[m_rec], EVENTO[m_rec]), COR_DESTAQUE),
          ('Amostra inteira: Projudi → conclusão no MP', KaplanMeierFitter().fit(T_JUD, EVENTO), CORES[4]),
          ('População 6 comarcas: ajuizamento → decisão judicial', KaplanMeierFitter().fit(T_POP, E_POP), COR_PRINCIPAL),
          ('População 6 comarcas: ajuizamento → manifestação do MP (com registro)', KaplanMeierFitter().fit(mp_pop), CORES[2])]
fig, axes = plt.subplots(1, 2, figsize=(18, 5.2))
for rotulo, km, cor in curvas:
    axes[0].step(km.survival_function_.index, km.survival_function_.iloc[:, 0], where='post', color=cor, linewidth=2,
                 label=f'{rotulo} (mediana {km.median_survival_time_:.0f} d)')
axes[0].axhline(0.5, color=TINTA_2, linestyle='--', linewidth=1)
axes[0].set_xlim(0, 1500)
axes[0].set_ylim(0, 1.02)
axes[0].set_xlabel('dias desde a chegada ao Judiciário')
axes[0].set_ylabel('S(t)')
teste_ap = logrank_test(T_JUD[m_rec], T_POP, EVENTO[m_rec], E_POP)
axes[0].set_title(f'Fase judicial: amostra × população (log-rank amostra ≥ 2022 × decisão: p = {teste_ap.p_value:.3g})')
axes[0].legend(fontsize=7.5, loc='upper right')

medianas_cmp = []
for comarca in dados['Comarca'].cat.categories:
    m_a = dados['Comarca'].eq(comarca).to_numpy()
    m_p = coorte_alvo['Comarca_alvo'].eq(comarca).to_numpy()
    medianas_cmp.append({'Comarca': comarca, 'n amostra': int(m_a.sum()),
                         'Mediana KM amostra (Projudi → MP)': KaplanMeierFitter().fit(T_JUD[m_a], EVENTO[m_a]).median_survival_time_,
                         'n população': int(m_p.sum()),
                         'Mediana KM população (→ decisão)': KaplanMeierFitter().fit(T_POP[m_p], E_POP[m_p]).median_survival_time_,
                         'Mediana população (→ MP)': coorte_alvo.loc[m_p, 'Tempo_ate_mp_dj'].median(),
                         'p log-rank (amostra × população)': logrank_test(T_JUD[m_a], T_POP[m_p], EVENTO[m_a], E_POP[m_p]).p_value})
medianas_cmp = pd.DataFrame(medianas_cmp).set_index('Comarca')
medianas_cmp['p BH'] = multipletests(medianas_cmp['p log-rank (amostra × população)'], method='fdr_bh')[1]
x = np.arange(len(medianas_cmp))
axes[1].bar(x - 0.27, medianas_cmp['Mediana KM amostra (Projudi → MP)'], width=0.27, color=COR_DESTAQUE, label='amostra (→ MP)')
axes[1].bar(x, medianas_cmp['Mediana população (→ MP)'], width=0.27, color=CORES[2], label='população (→ MP)')
axes[1].bar(x + 0.27, medianas_cmp['Mediana KM população (→ decisão)'], width=0.27, color=COR_PRINCIPAL, label='população (→ decisão)')
axes[1].set_xticks(x, [quebrar(c, 12) for c in medianas_cmp.index], fontsize=8.5)
axes[1].set_ylabel('mediana (dias)')
axes[1].set_title('Por comarca')
axes[1].legend(fontsize=8.5)
axes[1].grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
display(medianas_cmp.round(3))
lr_comarcas_pop = multivariate_logrank_test(T_POP, coorte_alvo['Comarca_alvo'].astype(str), E_POP)
print(f'Na população, as 6 comarcas diferem entre si? log-rank χ² = {lr_comarcas_pop.test_statistic:.1f}; p = {lr_comarcas_pop.p_value:.3g}')

# Vínculo individual (IPs recentes): comarca + ajuizamento = recebimento no Projudi (± 1 dia), candidato único
chave = coorte_alvo.reset_index()[['Numero_processo', 'Comarca_alvo', 'Data_ajuizamento', 'Data_manifestacao_mp', 'Data_fim', 'Tipo_fim']]
chave['Comarca_alvo'] = chave['Comarca_alvo'].astype(str)
vinculos = []
for n_ordem, linha in recente.iterrows():
    candidatos = chave[chave['Comarca_alvo'].eq(str(linha['Comarca']))
                       & ((chave['Data_ajuizamento'].dt.normalize() - linha['Data_recebimento_projudi']).dt.days.abs() <= 1)]
    vinculo = {'N_ordem': n_ordem, 'Candidatos': len(candidatos)}
    if len(candidatos) == 1:
        c = candidatos.iloc[0]
        vinculo.update({'MP DataJud − MP amostra (dias)': (c['Data_manifestacao_mp'] - linha['Data_conclusao_mp']).days
                        if pd.notna(c['Data_manifestacao_mp']) and pd.notna(linha['Data_conclusao_mp']) else np.nan,
                        'Decisão DataJud − MP amostra (dias)': (c['Data_fim'] - linha['Data_conclusao_mp']).days
                        if pd.notna(c['Data_fim']) and pd.notna(linha['Data_conclusao_mp']) else np.nan,
                        'Tipo_fim DataJud': c['Tipo_fim'], 'Desfecho amostra': str(linha['Desfecho']).split(':')[0]})
    vinculos.append(vinculo)
vinculos = pd.DataFrame(vinculos).set_index('N_ordem')
unicos = vinculos[vinculos['Candidatos'].eq(1)]
print(f'Vínculo individual: {len(unicos)} de {len(recente)} IPs recentes com candidato único '
      f'({100 * len(unicos) / max(len(recente), 1):.0f}%); distribuição de candidatos: {vinculos["Candidatos"].clip(upper=5).value_counts().sort_index().to_dict()}')
if len(unicos):
    display(unicos[['MP DataJud − MP amostra (dias)', 'Decisão DataJud − MP amostra (dias)']].describe().round(1))
    display(pd.crosstab(unicos['Desfecho amostra'], unicos['Tipo_fim DataJud']))
''')

interp('dj_comparacao')

md(r'''
### 22.12 Taxas por habitante: inquéritos de CVLI e MVI

Para ligar a análise ao critério do Pronasci II, calcula-se uma **taxa de processos de CVLI por 100 mil habitantes**, por município, e ela é comparada com a taxa de MVI de 2022 da Tabela 01 do estudo de caso. A definição precisa ser explícita:

| Elemento | Definição adotada |
|---|---|
| O que se conta | **processos** (inquéritos e APFs, inclusive os que viraram ação penal), não vítimas nem mortes |
| Assuntos | CVLI pela TPU: homicídio simples, qualificado, privilegiado ou não especificado, feminicídio, latrocínio e lesão corporal seguida de morte (códigos em 22.3) |
| Modalidade | versão principal: só **consumados** (o CVLI conta mortes). Sensibilidade: consumados + tentados. Culposos sempre fora |
| Período | ajuizamentos nativos digitais dos **anos completos** da coorte (2022 em diante, sem o ano da coleta) |
| Local | município do **órgão julgador** (sede da comarca) |
| Denominador | população do município sede (Censo 2022) |

**Ressalvas de robustez:**

1. **Unidade de contagem:** um fato com várias vítimas gera um processo, e um mesmo fato pode gerar mais de um processo (APF e IP, desmembramentos). A taxa mede **volume de procedimentos**, não de mortes;
2. **Comarca × município:** a comarca pode abranger municípios vizinhos sem fórum. O numerador incluiria esses casos, e o denominador só a sede, o que superestima a taxa das sedes;
3. **Momento:** o ajuizamento pode ocorrer meses depois do fato;
4. **Tamanho:** são só seis pontos, e a correlação com a MVI é **descritiva**.
''')

code(r'''
MVI_2022 = pd.Series({'Águas Lindas de Goiás': 27.0, 'Anápolis': 18.1, 'Aparecida de Goiânia': 30.9, 'Goiânia': 16.7,
                      'Luziânia': 27.7, 'Senador Canedo': 34.1})  # Tabela 01 do estudo de caso (FBSP 2023; mortes/100 mil hab.)
anos_taxa = list(range(ANO_INICIO_COORTE, DATA_COLETA_DJ.year))
base_taxa = coorte_dj[coorte_dj['Ano_ajuizamento'].isin(anos_taxa)]
pop_municipio = municipios_ibge['Populacao_2022']


def taxa_por_municipio(df):
    t = (df.groupby('Codigo_IBGE').size() / len(anos_taxa)).rename('Processos por ano').to_frame()
    t = t.join(municipios_ibge[['Municipio', 'Populacao_2022']])
    t['Taxa por 100 mil hab./ano'] = 1e5 * t['Processos por ano'] / t['Populacao_2022']
    return t


taxa = taxa_por_municipio(base_taxa[base_taxa['Categoria_indicador'].eq('CVLI')])
taxa_com_tentados = taxa_por_municipio(base_taxa)
alvo = pd.DataFrame({
    'Processos de CVLI consumado/ano': taxa.set_index('Municipio').loc[list(MVI_2022.index), 'Processos por ano'],
    'Taxa CVLI consumado (por 100 mil)': taxa.set_index('Municipio').loc[list(MVI_2022.index), 'Taxa por 100 mil hab./ano'],
    'Taxa consumado + tentado (por 100 mil)': taxa_com_tentados.set_index('Municipio').loc[list(MVI_2022.index), 'Taxa por 100 mil hab./ano'],
    'MVI 2022 (FBSP)': MVI_2022})
taxa_estado = 1e5 * base_taxa['Categoria_indicador'].eq('CVLI').sum() / len(anos_taxa) / pop_municipio.sum()
print(f'Anos completos usados: {anos_taxa[0]}–{anos_taxa[-1]}; taxa estadual: {taxa_estado:.1f} processos de CVLI consumado por 100 mil hab./ano')
display(alvo.round(1))
for coluna in ['Taxa CVLI consumado (por 100 mil)', 'Taxa consumado + tentado (por 100 mil)']:
    print(f"Spearman ({coluna} × MVI 2022), 6 comarcas: {stats.spearmanr(alvo[coluna], alvo['MVI 2022 (FBSP)']).statistic:.2f}")
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(alvo['MVI 2022 (FBSP)'], alvo['Taxa CVLI consumado (por 100 mil)'], s=80, color=COR_DESTAQUE)
for m, linha in alvo.iterrows():
    ax.annotate(m, (linha['MVI 2022 (FBSP)'], linha['Taxa CVLI consumado (por 100 mil)']), textcoords='offset points', xytext=(6, 4), fontsize=9)
ax.set_xlabel('MVI 2022 (mortes por 100 mil hab., FBSP)')
ax.set_ylabel('processos de CVLI consumado por 100 mil hab./ano')
ax.set_title('Volume de inquéritos × violência letal registrada (6 comarcas)')
plt.tight_layout()
plt.show()
grandes = taxa[taxa['Populacao_2022'] >= 100_000].sort_values('Taxa por 100 mil hab./ano', ascending=False)
fig, ax = plt.subplots(figsize=(15, 5))
ax.bar(range(len(grandes)), grandes['Taxa por 100 mil hab./ano'],
       color=[COR_DESTAQUE if m in MVI_2022.index else COR_SECUNDARIA for m in grandes['Municipio']])
ax.axhline(taxa_estado, color=TINTA, linestyle='--', linewidth=1, label=f'Estado: {taxa_estado:.1f}')
ax.set_xticks(range(len(grandes)), [quebrar(m, 12) for m in grandes['Municipio']], fontsize=8, rotation=0)
ax.set_ylabel('processos de CVLI por 100 mil hab./ano')
ax.set_title('Municípios com 100 mil habitantes ou mais (laranja: comarcas da amostra)')
ax.legend()
ax.grid(axis='x', visible=False)
plt.tight_layout()
plt.show()
''')

interp('dj_taxas')

md(r'''
### 22.13 O que a população confirma

Cada achado da Etapa 1, o teste correspondente na população e o resultado.
''')

code(r'''
def hr_de(tabela, termo, coluna='HR'):
    return (tabela.loc[termo, coluna], tabela.loc[termo, 'p-valor']) if termo in tabela.index else (np.nan, np.nan)


def veredito(efeito_a, p_a, efeito_p, p_p, neutro=1.0):
    # confirma: mesmo sentido e significativo nas duas; contradiz: sentido oposto e significativo na população
    if np.isnan(efeito_p):
        return 'não testável'
    mesmo_sentido = np.sign(np.log(efeito_a / neutro)) == np.sign(np.log(efeito_p / neutro))
    if p_p < 0.05 and mesmo_sentido and p_a < 0.05:
        return 'confirma'
    if p_p < 0.05 and not mesmo_sentido:
        return 'contradiz'
    if p_p >= 0.05 and p_a < 0.05:
        return 'não se confirma'
    return 'mesmo sentido; significativo só na população' if mesmo_sentido else 'inconclusivo'


linhas = []
for rotulo, termo_a, termo_p in [('Aparecida de Goiânia × Goiânia (Cox)', 'Comarca=Aparecida de Goiânia', 'Comarca_modelo=Aparecida de Goiânia'),
                                 ('Flagrante/prisão (Cox): amostra APF × população indício de prisão',
                                  'Forma_instauracao=Auto de prisão em flagrante (APF)', 'Indicio_prisao'),
                                 ('Homicídio qualificado × simples (Cox)', 'Assunto_grupo=Homicídio qualificado', 'Tipo_modelo=Homicídio qualificado'),
                                 ('Tentado × consumado (Cox)', 'Tentativa', 'Tentado')]:
    (ha, pa), (hp, pp) = hr_de(resumo_cox, termo_a), hr_de(resumo_cox_dj, termo_p)
    linhas.append({'Achado': rotulo, 'Amostra': f'HR = {ha:.2f} (p = {pa:.2g})', 'População': f'HR = {hp:.2f} (p = {pp:.2g})',
                   'Veredito': veredito(ha, pa, hp, pp)})
or_apf = pd.DataFrame(resumo_2x2).set_index('Variável').loc['Forma_instauracao']
op, pp = hr_de(or_den_dj, 'Indicio_prisao', 'OR')
linhas.append({'Achado': 'Flagrante/prisão aumenta a chance de denúncia',
               'Amostra': f"OR (Fisher, APF) = {or_apf['OR']:.1f} (p = {or_apf['p (Fisher)']:.2g})",
               'População': f'OR (logística, indício de prisão) = {op:.1f} (p = {pp:.2g})',
               'Veredito': veredito(or_apf['OR'], or_apf['p (Fisher)'], op, pp)})
den = comparacao[comparacao['Indicador'].eq('Denúncia') & comparacao['Nível'].str.startswith('Amostra ≥')].iloc[0]
linhas.append({'Achado': 'Denúncia é rara', 'Amostra': f"{den['% amostra']:.1f}% (instaurados ≥ 2022)",
               'População': f"{den['% população = p₀']:.1f}% (6 comarcas, 2022+)",
               'Veredito': 'contradiz' if den['p BH'] < 0.05 else 'confirma'})
linhas.append({'Achado': 'O tempo não é normal (assimetria à direita)',
               'Amostra': f"W = {normalidade.loc[(DESFECHOS['Tempo_fase_judicial'], 'original (dias)'), 'Shapiro-Wilk W']:.3f}; assimetria = "
                          f"{normalidade.loc[(DESFECHOS['Tempo_fase_judicial'], 'original (dias)'), 'Assimetria']:.2f}",
               'População': f'W = {stats.shapiro(sub_sw).statistic:.3f}; assimetria = {stats.skew(x_dj):.2f}', 'Veredito': 'confirma'})
linhas.append({'Achado': 'Família da fase judicial (concluídos)', 'Amostra': f"melhor AIC: {tabelas_conc['Tempo_fase_judicial'].index[0]}",
               'População': f'melhor AIC: {tabela_conc_dj.index[0]}', 'Veredito': 'parcial: a forma depende da composição dos desfechos'})
confirmacao = pd.DataFrame(linhas).set_index('Achado')
with pd.option_context('display.max_colwidth', 120):
    display(confirmacao)
''')

interp('dj_confirmacao')
