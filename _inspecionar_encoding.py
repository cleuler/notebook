# -*- coding: utf-8 -*-
"""
Inspeciona o encoding real das saídas armazenadas no notebook
e verifica se os scripts de validação têm o problema de encode no terminal.
"""
import io
import json
import sys

# ── Forçar UTF-8 no stdout do terminal Windows ───────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print(f'stdout encoding original : {sys.stdout.encoding}')
print(f'filesystem encoding      : {sys.getfilesystemencoding()}')
print()

with open('estcaso_lide_pred.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

# ── 1. Inspecionar bytes reais dos caracteres especiais nos outputs ───────────
print('=== Caracteres nao-ASCII nas saidas do notebook (Secao 6) ===')
encontrou = False
for i, cell in enumerate(nb['cells']):
    for out in cell.get('outputs', []):
        if out.get('output_type') != 'stream':
            continue
        texto = ''.join(out.get('text', []))
        if 'frequ' not in texto.lower() and 'tabela' not in texto.lower():
            continue
        chars_especiais = [(j, ch) for j, ch in enumerate(texto) if ord(ch) > 127]
        if chars_especiais:
            encontrou = True
            print(f'\nCelula {i} — trecho: {repr(texto[:80])}')
            print('  Caracteres nao-ASCII encontrados:')
            for pos, ch in chars_especiais[:10]:
                utf8_hex = ch.encode('utf-8').hex()
                print(f'    pos={pos:>3}  char={ch!r}  U+{ord(ch):04X}  UTF-8={utf8_hex}')

if not encontrou:
    print('Nenhum caractere nao-ASCII encontrado nas saidas — outputs sao ASCII puro.')

# ── 2. Testar impressao de acentos com e sem o fix ───────────────────────────
print()
print('=== Teste de impressao com UTF-8 forcado ===')
print('Texto com acentos: frequencias, ocorrencias, validacao')
print('Simbolos: OK - PASS - FAIL')

# ── 3. Verificar prints dentro das celulas do secao06 ─────────────────────────
print()
print('=== Strings com acentos nos code() de secao06_frequencias.py ===')
with open('src/estcaso_lide_pred/secao06_frequencias.py', encoding='utf-8') as f:
    src = f.read()

import re
# Encontrar todos os print() com caracteres acentuados
prints = re.findall(r"print\([^)]*[àáâãäéêëíîïóôõöúûüçñÀÁÂÃÄÉÊËÍÎÏÓÔÕÖÚÛÜÇÑ][^)]*\)", src)
if prints:
    print(f'  {len(prints)} print() com acentos encontrados:')
    for p in prints:
        print(f'    {p[:80]}')
else:
    print('  Nenhum print() com acento encontrado em secao06_frequencias.py')
    print('  (os acentos aparecem apenas em strings de dados/rotulos, nao em print())')
