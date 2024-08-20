import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import json
from io import BytesIO

# URL da página dos dados abertos
url = 'https://observasampa.prefeitura.sp.gov.br/index.php?page=dadosabertos'

# Fazer a requisição HTTP para obter o conteúdo da página
response = requests.get(url)
response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

# Parsear o HTML com BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar todos os links na página
download_buttons = soup.find_all('a', href=True)

# Filtrar apenas os links desejados (.csv)
csv_links = [button['href'] for button in download_buttons if button['href'].endswith('.csv')]

# Função para converter datas para ISO 8601 UTC
def convert_to_iso8601_utc(df):
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            df[column] = df[column].dt.tz_localize('UTC').dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return df

# Processar cada link encontrado
for link in csv_links:
    if not link.startswith('http'):
        link = 'https://observasampa.prefeitura.sp.gov.br/' + link

    # Fazer o download do arquivo
    file_response = requests.get(link)
    file_response.raise_for_status()

    # Determinar o nome do arquivo
    filename = os.path.basename(link)

    try:
        # Ler o arquivo CSV linha por linha
        df_iter = pd.read_csv(BytesIO(file_response.content), iterator=True, chunksize=1)
        
        for chunk in df_iter:
            # Converter datas para ISO 8601 e fuso UTC
            chunk = convert_to_iso8601_utc(chunk)

            # Filtrar dados para Zeladoria e Estado de São Paulo
            if 'Tema' in chunk.columns and 'Nível Região' in chunk.columns and 'Localidade' in chunk.columns:
                filtered_chunk = chunk[(chunk['Tema'].str.contains('Zeladoria', na=False)) & 
                                       (chunk['Nível Região'].str.contains('Estado', na=False)) & 
                                       (chunk['Localidade'].str.contains('São Paulo', na=False))]
                
                # Printar cada linha filtrada
                for _, row in filtered_chunk.iterrows():
                    print(row.to_dict())
    
    except pd.errors.ParserError as e:
        print(f"Erro ao processar o arquivo {filename}: {e}")
    except Exception as ex:
        print(f"Erro ao processar o arquivo {filename}: {ex}")











