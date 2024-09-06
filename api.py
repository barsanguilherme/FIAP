from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# URLs dos índices no Elasticsearch
ALAGAMENTOS_URL = 'https://elasticgrupogpt.pagekite.me/alagamentos/_search'
PREVISAO_TEMPO_URL = 'https://elasticgrupogpt.pagekite.me/dados_meterologicos_de_previsao_do_tempo/_search'

# Credenciais de autenticação
USERNAME = 'elastic'
PASSWORD = 'HAJhdvYdi2iJTmzUyYI9'

# Função auxiliar para fazer a requisição ao Elasticsearch com autenticação
def get_data_from_elasticsearch(url):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# Endpoint para buscar dados de alagamentos
@app.route('/alagamentos', methods=['GET'])
def get_alagamentos():
    data = get_data_from_elasticsearch(ALAGAMENTOS_URL)
    return jsonify(data), 200

# Endpoint para buscar dados de previsão do tempo
@app.route('/previsao_tempo', methods=['GET'])
def get_previsao_tempo():
    data = get_data_from_elasticsearch(PREVISAO_TEMPO_URL)
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)


