# Busca de Arquivos no OneDrive

Este projeto tem como objetivo realizar a busca de arquivos com extensões específicas (como `.zip`, `.rar`, etc.) em um site do OneDrive, incluindo arquivos dentro de subpastas. A busca é feita através da API do Microsoft Graph.

## Requisitos

- Python 3.x
- Bibliotecas necessárias:
  - `requests`: Para fazer as requisições HTTP para a API do Microsoft Graph.

## Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/yourusername/seu-repositorio.git
   cd seu-repositorio

2. Instale as dependências:
    pip install -r requirements.txt

3. Configure as variáveis de ambiente e autenticação:

    Para acessar a API do Microsoft Graph, você precisará de um token de acesso (Bearer token). Isso pode ser obtido através do processo de autenticação da API do Microsoft Graph. Consulte a documentação do Microsoft Graph para mais informações.

4. Execute o script para buscar arquivos em um site específico:
    site_id = 'seu_site_id_aqui'  # Substitua pelo seu site ID
    extensions = ['.zip', '.rar']  # Extensões dos arquivos a serem buscados
    arquivos = buscar_arquivos_em_site(site_id, extensions)
    print(arquivos)

