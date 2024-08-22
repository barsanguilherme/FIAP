import json
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import os

# Nome do arquivo HTML
html_filename = 'Centro de Previsão de Tempo e Estudos Climáticos - INPE - Previsão Numérica.html'

# Verifica se o arquivo HTML existe no diretório atual
if not os.path.isfile(html_filename):
    print(f"Erro: Arquivo '{html_filename}' não encontrado no diretório atual.")
    print("Certifique-se de que o arquivo esteja no mesmo diretório do script ou forneça o caminho correto.")
else:
    # Carrega o HTML do arquivo fornecido
    with open(html_filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Inicializa um dicionário para armazenar os dados agrupados por data e hora
    dados_previsao = {}

    # Função para converter timestamps para datas e horas
    def timestamp_to_datetime(timestamp):
        return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

    # Função para extrair dados de gráficos do Highcharts
    def extrair_dados_highcharts(script_tag):
        chart_data = {}
        chart_js = script_tag.string

        if chart_js and "datasets" in chart_js:
            try:
                # Extrai a parte relevante do script que contém os dados
                json_start = chart_js.find('{"datasets":')
                json_end = chart_js.find("};", json_start) + 1
                json_content = chart_js[json_start:json_end]

                # Converte a string JSON para um dicionário Python
                chart_dict = json.loads(json_content)
                
                # Itera sobre cada dataset no dicionário
                for dataset in chart_dict['datasets']:
                    name = dataset['name']
                    data_points = dataset['data']

                    for point in data_points:
                        timestamp = point['x']
                        value = point['y']
                        datetime_str = timestamp_to_datetime(timestamp)
                        
                        if datetime_str not in dados_previsao:
                            dados_previsao[datetime_str] = {}
                        
                        dados_previsao[datetime_str][name] = value

            except Exception as e:
                print(f"Erro ao processar dados: {e}")
        return chart_data

    # Itera pelas tags <script> que contém os dados do Highcharts
    for script in soup.find_all('script'):
        if script.string and 'datasets' in script.string:
            print("Analisando script com 'datasets'...")

            # Extrai os dados
            extrair_dados_highcharts(script)

    # Adiciona o timestamp atual em UTC ao dicionário no formato ISO 8601
    current_time_utc = datetime.now(timezone.utc).isoformat()

    # Cria um dicionário final para armazenar os dados e o timestamp de extração
    dados_final = {
        'Extracted Timestamp': current_time_utc,
        'Previsao': dados_previsao
    }

    # Converte o dicionário final em um JSON formatado e exibe no terminal
    json_output = json.dumps(dados_final, ensure_ascii=False, indent=4)
    print(json_output)




