"""Fecho metodológico: fontes indicadas, modelo com novos dados e dicionário."""

BLOCKS = [
    ("markdown", r"""
## 21. O desenho de pesquisa e o lugar de cada variável

Toshkov (2016, cap. 8, pp. 200–205) descreve o desenho observacional *Large-N* como a comparação de distribuições de variáveis em muitos casos. Aqui, a unidade é o **processo**, a moldura contém 50.320 processos e a amostra sorteada por ano contém 595. O fato de haver muitos casos permite estimar frequências e associações com precisão limitada pelo desenho; não transforma uma associação em efeito causal. A seleção da moldura, a codificação dos sinais e a disponibilidade dos documentos são partes do desenho, não detalhes posteriores ao teste.

As referências aos capítulos 7 e 11 exigem precisão: o **capítulo 7** trata de experimentos, ausentes neste estudo; a simulação computacional do fim do caderno é um ensaio do método e não randomização de processos reais. O **capítulo 11** trata de desenhos mistos e aninhados. A leitura dos autos na pesquisa de origem e o cruzamento com o DataJud para os mesmos processos compõem duas fontes em casos aninhados, mas a auditoria automática de códigos não equivale a uma nova leitura independente dos autos. O quadro abaixo documenta esta separação antes de qualquer interpretação substantiva.

| Elemento | Definição nesta análise | Consequência |
|---|---|---|
| unidade e moldura | processo distribuído nos JEC de Natal, 2022–2024, depois das exclusões documentadas | estimativas valem para a moldura depurada |
| sorteio | estratos por ano; JEC é domínio de análise, não estrato de sorteio | usar pesos e erro-padrão do desenho para prevalência |
| rótulo de pesquisa | F1–F3, com indício e certeza definidos pela regra de codificação | alvo operacional, não padrão jurídico independente |
| novas variáveis | movimentos, desfecho e tempos do DataJud após distribuição | úteis para associação e trajetória; não para prever o risco na distribuição |
| simulação | população artificial com parâmetros declarados | verifica comportamento do procedimento sob hipóteses, sem gerar evidência empírica nova |

Os exemplos de probabilidade condicional e Bayes das Seções 5–6 usam a amostra tratada, e não a planilha de casos novos como se fosse outra amostra de 595. Uma priori de 30% foi **atribuída como cenário** a partir do levantamento documental citado na revisão de escopo da Hadja; a revisão conceitual não estimou essa prevalência para Natal. A verossimilhança de cada desfecho vem da frequência na amostra vinculada ao DataJud. A probabilidade total soma os dois produtos `priori × verossimilhança`, porque H₀ e Hₐ foram definidos como complementares. A posteriori é a proporção do produto de Hₐ nessa soma. Reaproveitar a prevalência 17,65% simultaneamente como priori e como dado da verossimilhança contaria a mesma amostra duas vezes.

Friendly e Meyer (2016, cap. 6) orientam a análise de correspondência como visualização dos desvios de independência em tabelas categóricas. Os mapas já calculados na Seção 7 incluem inércia, massas, contribuições e qualidade de representação; pontos de linhas e colunas em mapa simétrico não têm distância euclidiana diretamente interpretável entre si. Categorias raras e células com frequência esperada pequena tornam a posição instável. Os sinais F3 entram na MCA apenas como suplementares, pois participam da própria regra que define a resposta.
"""),
    ("markdown", r"""
## 22. Quanto os desfechos novos conseguem distinguir as três categorias?

Os logitos multinomial, ordinal e de razão contínua da Seção 8 usam sinais F2 registrados pela pesquisa e, por isso, respondem principalmente como modelar **essa regra operacional**. Para medir a contribuição dos *dados novos*, ajustamos agora dois modelos simples com o desfecho TPU e três marcadores da trajetória administrativa. Os parâmetros são aprendidos em 2022–2023; as probabilidades são avaliadas nos processos de 2024, que não participaram do ajuste. A comparação inclui uma previsão que usa somente a frequência das classes no treino. A perda logarítmica e o Brier permitem ver se um modelo melhora sobre essa referência. A precisão global isolada seria enganosa, pois a classe majoritária domina a amostra.

Esses campos surgem depois do ajuizamento e não podem ser usados para alegar previsão no momento da distribuição. O desfecho TPU é proxy, e os rótulos da pesquisa são a referência disponível. Mesmo um ganho numérico neste confronto não estabeleceria acurácia jurídica nem autorizaria listas individuais de lides predatórias.
"""),
    ("code", r"""
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score

DJ_NOVO = dj.loc[dj.desfecho.notna()].copy()
_tr = DJ_NOVO.ano.astype(int).to_numpy() < 2024
_te = ~_tr
_cols = ['desfecho', 'houve_recurso', 'evoluiu_cumprimento', 'redistribuido']
_Z = DJ_NOVO[_cols].copy()
for _c in _cols:
    _Z[_c] = _Z[_c].astype(str)
_y = DJ_NOVO.classe3_cod.astype(int).to_numpy()
_enc = ColumnTransformer([('categorias', OneHotEncoder(handle_unknown='ignore'), _cols)])
_modelo = make_pipeline(_enc, LogisticRegression(max_iter=1000, C=1.0, random_state=2026))
_modelo.fit(_Z.loc[_tr], _y[_tr])
_pred = _modelo.predict_proba(_Z.loc[_te])
_base = np.tile(np.bincount(_y[_tr], minlength=3) / _tr.sum(), (_te.sum(), 1))
_linhas = []
for _nome, _p in [('frequência do treino', _base), ('logito multinomial, DataJud', _pred)]:
    _linhas.append({'modelo': _nome, 'n treino': int(_tr.sum()), 'n teste': int(_te.sum()),
                    'log-loss 2024': log_loss(_y[_te], _p, labels=[0, 1, 2]),
                    'Brier 2024': np.mean(np.sum((_p - np.eye(3)[_y[_te]]) ** 2, axis=1)),
                    'acurácia balanceada': balanced_accuracy_score(_y[_te], _p.argmax(1)),
                    'F1 macro': f1_score(_y[_te], _p.argmax(1), average='macro', zero_division=0)})
AVAL_DJ = pd.DataFrame(_linhas)
display(tabela_ptbr(AVAL_DJ, casas=4))
display(pd.crosstab(pd.Series(_y[_te], name='classe da pesquisa'),
                    pd.Series(_pred.argmax(1), name='classe prevista com DataJud')))
display(Markdown('A diferença de log-loss entre o modelo DataJud e a frequência do treino é **' +
                 fnum(AVAL_DJ.loc[1, 'log-loss 2024'] - AVAL_DJ.loc[0, 'log-loss 2024'], 4) +
                 '**. Valor negativo favorece o modelo com desfechos; a interpretação continua '
                 'limitada pela codificação dos rótulos e pela mudança de ano.'))
display(Markdown('No limiar da classe mais provável, o modelo atribuiu a categoria majoritária a **' +
                 str(int((_pred.argmax(1) == 0).sum())) + ' de ' + str(int(_te.sum())) +
                 '** casos. Assim, o pequeno ganho de log-loss não se traduz em distinção útil '
                 'das categorias minoritárias.'))
"""),
    ("markdown", r"""
## 23. Quadro de variáveis e dicionário para reutilização

O quadro informa **qual conceito cada coluna pretende representar**; o dicionário acrescenta **onde e quando ela foi medida**, quem entrou no denominador, como foi codificada e como a ausência deve ser tratada. Essa distinção é essencial no funil: F2 ausente em um excluído na Fase I significa “não avaliado”, enquanto `indicio = 0` nesse mesmo registro é uma decisão da regra de classificação ampla. As duas colunas não são observações equivalentes. O desfecho do DataJud, por sua vez, é posterior à distribuição e depende de registro administrativo. O arquivo exportado conserva os nomes e contagens do quadro original e acrescenta campos para que os colegas possam adaptar o modelo aos próprios projetos.
"""),
    ("code", r"""
_dic = QUADRO_TURMA.copy()
def _meta_variavel(nome):
    if nome in ('numero', 'ordem'):
        return ('moldura e vínculo', 'identificador', 'antes do sorteio', '595 processos da amostra',
                'não se aplica', 'não entra como preditor; serve à conferência do vínculo')
    if nome in ('jec', 'ano', 'classe_planilha'):
        return ('moldura / planilha', 'descrição ou domínio', 'na distribuição ou na coleta, conforme a coluna',
                '595 processos', 'ausência deve ser investigada na fonte', 'ano é estrato; JEC é domínio; classe da planilha pode ser posterior')
    if nome.startswith('F1_'):
        return ('planilha da pesquisa, leitura dos autos', 'critério de elegibilidade', 'fase I da pesquisa',
                '595 processos', 'NA: não informado; não converter automaticamente em Não', 'afeta quem pode alcançar F2')
    if nome.startswith('F2_'):
        return ('planilha da pesquisa, leitura dos autos', 'sinal de indício', 'fase II da pesquisa',
                '444 elegíveis', 'NA estrutural para os 151 excluídos na F1', 'não usar NA como ausência de sinal')
    if nome.startswith('F3_'):
        return ('planilha da pesquisa, leitura dos autos', 'critério de certeza', 'fase III da pesquisa',
                '233 que alcançaram F3', 'NA estrutural para quem não alcançou F3', 'participa da definição da classe3; não usar como preditor dela')
    if nome in ('desfecho', 't_desfecho', 'houve_recurso', 'classe_origem'):
        return ('DataJud / códigos TPU', 'trajetória ou desfecho operacional', 'após a distribuição',
                '593 com documento vinculado', 'sem documento para 2 da amostra; censura temporal é distinta de NA',
                'proxy administrativo; não usar para previsão no ajuizamento')
    return ('derivada da planilha F1–F3', 'resposta ou variável do funil', 'após codificação da pesquisa',
            '595 processos; conferir universo de origem das variáveis componentes',
            'zero pode ser efeito da regra do funil, não medição de F2/F3',
            'dependência mecânica com F1–F3; interpretar modelos como reprodução parcial da regra')

_meta = [_meta_variavel(x) for x in _dic.nome]
for _i, _col in enumerate(['fonte', 'papel analítico', 'momento', 'universo de medição',
                           'regra de ausência', 'restrição de interpretação']):
    _dic[_col] = [r[_i] for r in _meta]
_dic['regra operacional'] = _dic['descricao']
_dic['n_sem_medida'] = 595 - _dic.n_validos.astype(int)
assert (_dic.n_validos.astype(int) + _dic.n_sem_medida == 595).all()
_conceitos = pd.DataFrame([
    {'conceito': 'indício amplo', 'indicador': 'indicio', 'unidade': 'processo', 'fonte': 'F1–F3',
     'universo': '595 sorteados', 'limite': 'rótulo operacional da pesquisa'},
    {'conceito': 'certeza conforme regra', 'indicador': 'certeza', 'unidade': 'processo', 'fonte': 'F3',
     'universo': '595 sorteados; F3 observada em 233', 'limite': 'três sinais F3 simultâneos'},
    {'conceito': 'trajetória administrativa', 'indicador': 'desfecho, recurso, cumprimento, tempo',
     'unidade': 'processo', 'fonte': 'DataJud / TPU', 'universo': '593 vinculados',
     'limite': 'não identifica por si a predação jurídica'},
    {'conceito': 'prevalência na moldura', 'indicador': 'estimador estratificado de indicio',
     'unidade': 'processos da moldura', 'fonte': 'amostra + pesos por ano',
     'universo': '50.320 processos depurados', 'limite': 'estimativa, não contagem exata'},
])
with pd.ExcelWriter(TABELAS / 'quadro_dicionario_large_n.xlsx') as _xw:
    _conceitos.to_excel(_xw, sheet_name='Quadro conceitual', index=False)
    _dic.to_excel(_xw, sheet_name='Dicionário operacional', index=False)
    _sim[['prevalência na população simulada', 'estimativa estratificada sem erro',
          'estimativa com erro hipotético']].to_excel(_xw, sheet_name='Simulação do funil', index=False)
display(_conceitos)
display(_dic[['nome', 'fonte', 'papel analítico', 'universo de medição', 'regra de ausência',
              'restrição de interpretação']].head(12))
display(Markdown(f'O dicionário documenta **{len(_dic)} variáveis** e acompanha um exemplo '
                 'de simulação da população finita; as 300 réplicas são artificiais.'))
"""),
]
