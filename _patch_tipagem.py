import json, sys

sys.stdout.reconfigure(encoding='utf-8')

nb_path = 'notebooks/estcaso_4jec_natal_rn.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Novo source completo para a célula cod-tipagem (seção 7)
novo_source = [
    "# ── Passo a passo desta célula ─────────────────────────────────────────────\n",
    "# 1) Converter colunas de data para datetime.\n",
    "# 2) Converter colunas de duração para numérico.\n",
    "# 3) Converter variáveis categóricas para o tipo 'category'.\n",
    "# 4) Criar variável booleana 'censura' (indicador de censura à direita).\n",
    "# 5) Exibir dtypes e estatísticas descritivas iniciais.\n",
    "# ───────────────────────────────────────────────────────────────────────────\n",
    "\n",
    "# ── Conversão de datas ──────────────────────────────────────────────────────\n",
    "COLS_DATA = [c for c in ['dt_distribuicao', 'dt_sentenca'] if c in dados.columns]\n",
    "for c in COLS_DATA:\n",
    "    dados[c] = pd.to_datetime(dados[c], errors='coerce')\n",
    "\n",
    "# ── Conversão de durações para int (aceita NaN via float64) ─────────────────\n",
    "COLS_NUM = [c for c in ['duracao_sent2', 'duracao_tecn', 'duracao_sort', 'duracao_proc']\n",
    "            if c in dados.columns]\n",
    "for c in COLS_NUM:\n",
    "    dados[c] = pd.to_numeric(dados[c], errors='coerce')\n",
    "\n",
    "# ── Conversão de categóricas ─────────────────────────────────────────────────\n",
    "COLS_CAT = [c for c in ['grupo', 'status_norm', 'hibrida', 'teve_acordo_na_ac',\n",
    "                        'teve_acordo_fora_da_ac', 'sentenca_std', 'tecnica']\n",
    "            if c in dados.columns]\n",
    "for c in COLS_CAT:\n",
    "    dados[c] = dados[c].astype('category')\n",
    "\n",
    "# ── Variável de censura à direita ─────────────────────────────────────────────\n",
    "# Definição: um processo é CENSURADO (censura = 1) quando NÃO possui sentença\n",
    "# registrada (sentenca_std é NaN), ou seja, seu tempo real de tramitação é\n",
    "# desconhecido pois o evento de interesse (encerramento com sentença) não ocorreu\n",
    "# dentro da janela de observação. Processos COM sentença registrada recebem\n",
    "# censura = 0 (evento observado). Convenção padrão em análise de sobrevivência:\n",
    "#   censura = 1  →  tempo incompleto (processo ainda ativo / sem sentença)\n",
    "#   censura = 0  →  evento ocorrido  (processo encerrado com sentença)\n",
    "if 'sentenca_std' in dados.columns:\n",
    "    dados['censura'] = dados['sentenca_std'].isna().astype(int)\n",
    "\n",
    "# Verificação cruzada com 'status_norm' para consistência interna\n",
    "# Espera-se que censura=1 coincida com status_norm='Ativo' e\n",
    "# censura=0 coincida com status_norm='Encerrado'.\n",
    "if {'censura', 'status_norm'}.issubset(dados.columns):\n",
    "    print('Distribuição da variável censura:')\n",
    "    print(dados['censura'].value_counts()\n",
    "          .rename({0: 'Evento observado  (censura = 0)',\n",
    "                   1: 'Censurado à direita (censura = 1)'})\n",
    "          .to_string())\n",
    "    print()\n",
    "    print('Tabela cruzada censura × status_norm (consistência):')\n",
    "    display(pd.crosstab(dados['censura'], dados['status_norm'],\n",
    "                        rownames=['censura'], colnames=['status_norm'],\n",
    "                        margins=True))\n",
    "    print()\n",
    "    # Alerta se houver linhas inconsistentes\n",
    "    inconsistentes = (\n",
    "        (dados['censura'] == 1) & (dados['status_norm'] == 'Encerrado') |\n",
    "        (dados['censura'] == 0) & (dados['status_norm'] == 'Ativo')\n",
    "    ).sum()\n",
    "    print(f'Linhas com censura inconsistente em relação ao status: {inconsistentes}')\n",
    "    msg = 'OK — censura alinhada ao status.' if inconsistentes == 0 else 'ATENÇÃO — revisar registros inconsistentes.'\n",
    "    print(msg)\n",
    "\n",
    "# ── Resumo de tipos ──────────────────────────────────────────────────────────\n",
    "print('\\nTipos das variáveis após tipagem:')\n",
    "print(dados.dtypes)\n",
    "\n",
    "print('\\nEstatísticas descritivas das variáveis de duração:')\n",
    "display(\n",
    "    dados[COLS_NUM].describe(percentiles=[.25, .5, .75, .9, .95]).round(1).T\n",
    ")"
]

# Aplicar o novo source na célula correta
for i, cell in enumerate(nb['cells']):
    if cell.get('id') == 'cod-tipagem':
        cell['source'] = novo_source
        print(f'Célula cod-tipagem (índice {i}) atualizada com sucesso.')
        break

# Salvar notebook em UTF-8
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Notebook salvo.')

