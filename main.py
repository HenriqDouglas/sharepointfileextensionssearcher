import os
import requests
import json
from msal import ConfidentialClientApplication
from tqdm import tqdm
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações do aplicativo
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
SCOPES = [os.getenv('GRAPH_API_SCOPES')]
BASE_URL = os.getenv('BASE_URL')

# Validação das variáveis de ambiente
if not all([CLIENT_ID, CLIENT_SECRET, TENANT_ID, SCOPES, BASE_URL]):
    raise EnvironmentError("Variáveis de ambiente não configuradas corretamente. Verifique o arquivo .env.")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Função para obter o ID de um site pelo nome
def obter_site_id(nome_site):
    headers = {'Authorization': f'Bearer {get_access_token()}'}
    
    # Consultar sites
    search_url = f"{BASE_URL}/sites?search={nome_site}"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao buscar sites: {response.status_code} {response.text}")
    
    sites = response.json().get('value', [])
    for site in sites:
        if site['name'] == nome_site:
            return site['id']
    
    raise Exception(f"Site {nome_site} não encontrado.")

# Função para autenticar e obter o token de acesso
def get_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    token_response = app.acquire_token_for_client(scopes=SCOPES)
    access_token = token_response.get('access_token')

    if not access_token:
        raise Exception("Falha ao obter o token de acesso.")
    return access_token

# Função para buscar arquivos em um único site do SharePoint
def buscar_arquivos_em_site(site_id, extensions):
    headers = {'Authorization': f'Bearer {get_access_token()}'}

    # Função recursiva para percorrer subpastas
    def buscar_em_pasta(folder_id):
        search_url = f"{BASE_URL}/sites/{site_id}/drive/items/{folder_id}/children"
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Erro ao buscar arquivos na pasta {folder_id}: {response.status_code} {response.text}")

        items = response.json().get('value', [])
        arquivos_encontrados = []

        for item in tqdm(items, desc=f'Buscando na pasta {folder_id}', unit='item'):
            if item.get('folder'):  # Se for uma pasta, chamamos a função recursiva
                arquivos_encontrados.extend(buscar_em_pasta(item['id']))
            else:  # Se for um arquivo, verifica a extensão
                file_name = item['name']
                if any(file_name.endswith(ext) for ext in extensions):
                    arquivos_encontrados.append({
                        'file_name': file_name,
                        'web_url': item['webUrl']
                    })
        
        return arquivos_encontrados

    # Inicia a busca a partir da raiz do diretório
    return buscar_em_pasta('root')

# Função para salvar resultados em um arquivo JSON
def salvar_resultados(resultados, arquivo='resultados.json'):
    try:
        with open(arquivo, 'w') as f:
            json.dump(resultados, f, indent=4)
        print(f"Resultados salvos com sucesso no arquivo: {arquivo}")
    except Exception as e:
        print(f"Erro ao salvar resultados: {e}")

# Função principal
if __name__ == "__main__":

    site_id = obter_site_id('tecinov')  # Substitua pelo nome do seu site
    extensoes = ['.zip', '.rar']

    try:
        arquivos_encontrados = buscar_arquivos_em_site(site_id, extensoes)

        # Mostrar os resultados
        #for arquivo in arquivos_encontrados:
        #    print(f"Arquivo: {arquivo['file_name']}, URL: {arquivo['web_url']}")

        # Salvar os resultados
        salvar_resultados(arquivos_encontrados)
    except Exception as e:
        print(f"Erro durante a execução: {e}")