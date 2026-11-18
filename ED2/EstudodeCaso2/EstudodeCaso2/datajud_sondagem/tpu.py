"""Consulta a Tabela Processual Unificada (TPU/CNJ) oficial, via serviço público do SGT
(https://gateway.cloud.pje.jus.br/tpu/api/v1/publico/consulta/detalhada/movimentos), com cache em tpu_movimentos.json.
Serve para conferir nome, item-pai (hierarquia), norma/artigo e glossário dos códigos de movimento."""
import json
import re
import time
from html import unescape
from pathlib import Path

import requests

AQUI = Path(__file__).resolve().parent
CACHE = AQUI / 'tpu_movimentos.json'
URL = 'https://gateway.cloud.pje.jus.br/tpu/api/v1/publico/consulta/detalhada/movimentos'
_cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}


def movimento(codigo):
    k = str(codigo)
    if k not in _cache:
        for i in range(5):
            try:
                r = requests.get(URL, params={'codigo': codigo}, timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
                r.encoding = 'utf-8'
                lst = r.json()
                break
            except (requests.RequestException, ValueError):
                time.sleep(3 * (i + 1))
        else:
            lst = []
        it = next((x for x in lst if x.get('id') == int(codigo)), lst[0] if lst else {})
        glos = re.sub(r'<[^>]+>', ' ', unescape(it.get('glossario') or ''))
        _cache[k] = {'nome': it.get('nome'), 'pai': it.get('cod_item_pai'), 'norma': it.get('norma'),
                     'artigo': it.get('artigo'), 'situacao': it.get('situacao'),
                     'jec': it.get('justica_estadual_juizado_especial'),
                     'complementos': {c.get('complementoDscComplemento'): [v.get('dscValorTabelado') for v in (c.get('complementoTabelado') or [])] for c in (it.get('complementos') or [])},
                     'glossario': ' '.join(glos.split())[:400]}
        CACHE.write_text(json.dumps(_cache, ensure_ascii=False, indent=1), encoding='utf-8')
        time.sleep(0.3)
    return _cache[k]


def cadeia(codigo):
    """Lista de códigos do próprio até a raiz (ex.: 219 -> 385 -> 193 -> 1)."""
    out, c = [], int(codigo)
    while c and c not in out and len(out) < 12:
        out.append(c)
        c = movimento(c).get('pai')
    return out
