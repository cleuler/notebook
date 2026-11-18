"""Cliente mínimo da API pública do DataJud (TJRN), no mesmo padrão de EstudodeCaso1/src/coleta_datajud.py.
Chave pública divulgada pelo CNJ em https://datajud-wiki.cnj.jus.br/api-publica/acesso"""
import time
import requests

URL = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrn/_search'
CHAVE_PUBLICA = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=='
CABECALHO = {'Authorization': f'APIKey {CHAVE_PUBLICA}', 'Content-Type': 'application/json',
             'User-Agent': 'Mozilla/5.0 (pesquisa academica; sondagem DataJud)'}
CHAMADAS = {'n': 0}


def consultar(corpo, tentativas=15, pausa=1.0):
    """POST com tentativas; só aceita resposta sem falha de shard."""
    ultimo = None
    for i in range(tentativas):
        try:
            CHAMADAS['n'] += 1
            r = requests.post(URL, headers=CABECALHO, json=corpo, timeout=180)
            j = r.json()
            if r.status_code == 200 and j.get('_shards', {}).get('failed', 0) == 0:
                time.sleep(pausa)
                return j
            if r.status_code == 400:
                raise ValueError(f'consulta inválida (HTTP 400): {str(j)[:400]}')
            ultimo = f'HTTP {r.status_code}; shards com falha: {j.get("_shards", {}).get("failed")}; {str(j)[:200]}'
        except requests.RequestException as erro:
            ultimo = repr(erro)[:160]
        except ValueError as erro:
            if 'HTTP 400' in str(erro):
                raise
            ultimo = repr(erro)[:160]
        espera = min(4 * (i + 1), 15)
        print(f'    {time.strftime("%H:%M:%S")} tentativa {i + 1} falhou ({ultimo}); nova tentativa em {espera}s', flush=True)
        time.sleep(espera)
    raise RuntimeError(f'API indisponível após {tentativas} tentativas: {ultimo}')
