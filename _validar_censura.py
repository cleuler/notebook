import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/estcaso_4jec_natal_rn.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell.get('id') == 'cod-tipagem':
        src = ''.join(cell['source'])
        print('=== SOURCE DA CÉLULA cod-tipagem ===')
        print(src)
        print()
        # Checar presença dos elementos-chave da alteração
        checks = {
            "passo 4 no cabeçalho"         : "# 4) Criar variável booleana 'censura'" in src,
            "passo 5 no cabeçalho"         : "# 5) Exibir dtypes" in src,
            "criação de dados['censura']"  : "dados['censura'] = dados['sentenca_std'].isna().astype(int)" in src,
            "verificação cruzada"           : "crosstab(dados['censura']" in src,
            "alerta de inconsistência"      : "inconsistentes" in src,
            "resumo de tipos mantido"       : "Tipos das variáveis após tipagem" in src,
            "estatísticas descritivas"      : "COLS_NUM].describe" in src,
        }
        print('=== VERIFICAÇÃO DE ELEMENTOS ===')
        for nome, ok in checks.items():
            status = 'OK' if ok else 'FALTANDO'
            print(f'  [{status}] {nome}')
        break
