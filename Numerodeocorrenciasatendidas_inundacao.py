import requests
import pandas as pd
from io import StringIO
import json

# URL do arquivo CSV
file_url = 'https://observasampa.prefeitura.sp.gov.br/arquivo.php?cd_indicador=237'

print("Iniciando o download...")

try:
    # Realiza a requisição HTTP para baixar o arquivo
    response = requests.get(file_url)
    response.raise_for_status()  # Levanta um erro se o download não for bem-sucedido
    
    print(f"Download concluído com sucesso. Status code: {response.status_code}")

    # Verifique se o conteúdo realmente contém dados
    if len(response.content) > 0:
        print("Conteúdo recebido, processando o CSV...")

        try:
            # Usa StringIO para tratar o conteúdo como um arquivo em memória
            file_content = StringIO(response.text)
            
            # Especifica o delimitador como ponto e vírgula
            data_df = pd.read_csv(file_content, delimiter=';')
            
            # Remove a coluna "Unnamed: 0" se ela existir
            if 'Unnamed: 0' in data_df.columns:
                data_df = data_df.drop(columns=['Unnamed: 0'])
            
            # Converte as colunas que contêm números no formato "número,0" para float
            for col in data_df.columns:
                # Tenta converter para float removendo a vírgula e o zero, se possível
                try:
                    data_df[col] = data_df[col].str.replace(',', '.').astype(float)
                except ValueError:
                    # Se não for possível converter (coluna de texto, por exemplo), continue
                    continue
            
            print(f"DataFrame criado com {len(data_df)} linhas e {len(data_df.columns)} colunas.")
            print("Cabeçalho do CSV:")
            print(data_df.columns)  # Exibe o cabeçalho do CSV
            
            # Converte para JSON
            data_dict = data_df.to_dict(orient='list')
            json_output = json.dumps(data_dict, ensure_ascii=False, indent=4)
            print("JSON gerado:")
            print(json_output)  # Imprime o JSON completo
        except Exception as e:
            print(f"Erro ao processar o arquivo CSV: {e}")
    else:
        print("Aviso: O conteúdo baixado está vazio.")
except requests.exceptions.RequestException as e:
    print(f"Erro ao tentar baixar o arquivo: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")















