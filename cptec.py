import requests
from bs4 import BeautifulSoup

# URL do banco de dados CPTEC
url = 'https://bancodedados.cptec.inpe.br/'

# Fazer uma requisição HTTP para obter o conteúdo da página
response = requests.get(url)
response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

# Parsear o HTML com BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar todos os links na página
links = soup.find_all('a', href=True)

# Filtrar links de interesse
data_links = [link['href'] for link in links if 'downloads.cptec.inpe.br' in link['href']]

print("Links de dados encontrados:")
for link in data_links:
    print(link)
    
    # Seguir o link e explorar mais profundamente
    if link.startswith('http'):
        sub_response = requests.get(link)
        sub_response.raise_for_status()
        sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
        
        # Adicionar lógica aqui para extrair dados da página interna

print("Extração de dados concluída.")



