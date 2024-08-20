import requests
import pandas as pd
import json
from datetime import datetime, timezone

# URL para o download dos dados
download_url = "https://sidra.ibge.gov.br/Ajax/JSon/Tabela/1/1764?versao=-1&_=1723748555262"

# Faz a requisição para obter os dados
response = requests.get(download_url)
response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

# Converte a resposta JSON para um dicionário Python
dados = response.json()

# Verifica se os dados estão no formato esperado
if isinstance(dados, list):
    # Adiciona o timestamp a cada registro
    current_time_utc = datetime.now(timezone.utc).isoformat()
    for item in dados:
        item['timestamp'] = current_time_utc

    # Converte os dados para JSON formatado
    json_data = json.dumps(dados, ensure_ascii=False, indent=4)

    # Salva o JSON em um arquivo
    with open('dados_ibge_1764.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    print("Dados salvos em 'dados_ibge_1764.json'.")
else:
    print("Os dados não estão no formato esperado (lista de dicionários).")
    # Salva os dados originais para análise
    with open('dados_ibge_1764_original.json', 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)
    print("Dados originais salvos em 'dados_ibge_1764_original.json'.")




