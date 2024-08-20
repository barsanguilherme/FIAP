import requests
import json
from datetime import datetime, timezone

# Substitua pela nova URL obtida
download_url = "https://sidra.ibge.gov.br/Ajax/JSon/Tabela/1/8535?versao=-1&_=1723749000561"

# Faz o download do arquivo JSON
response = requests.get(download_url)
response.raise_for_status()  # Verifica se o download foi bem-sucedido

# Converte o conteúdo para JSON
data = response.json()

# Verifica se os dados estão no formato esperado
if isinstance(data, list) and isinstance(data[0], dict):
    # Adiciona timestamp em cada item
    current_time_utc = datetime.now(timezone.utc).isoformat()
    for item in data:
        item['timestamp'] = current_time_utc
    
    # Salva o JSON ajustado
    with open('dados_ibge_8535.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Dados salvos em 'dados_ibge_8535.json'.")
else:
    # Salva o conteúdo original para inspeção
    with open('dados_ibge_8535_original.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Os dados não estão no formato esperado (lista de dicionários).")
    print("Dados originais salvos em 'dados_ibge_8535_original.json'.")
