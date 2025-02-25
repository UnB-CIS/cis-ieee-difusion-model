import os
from pathlib import Path
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL
from list_folder_and_files import list_folder_children

FOLDER_ID = 'test_id'

def download_file(headers, file_id, file_name):
    """
    Baixa um arquivo do OneDrive usando a API Microsoft Graph.
    
    Esta função faz uma requisição para a API Microsoft Graph para baixar um arquivo
    do OneDrive. Ela trata a resposta de redirecionamento 302 que é típica para downloads
    de arquivos do OneDrive, e salva o arquivo no local especificado.
    
    Args:
        headers (dict): Cabeçalhos de autorização contendo o token de acesso.
                        Formato: {'Authorization': 'Bearer <access_token>'}
        file_id (str): O identificador único do arquivo no OneDrive.
        file_name (str ou Path): O caminho onde o arquivo baixado será salvo.
                                Pode ser uma string ou um objeto Path.
    
    Returns:
        None
    
    Raises:
        HTTPError: Se a requisição para a API Microsoft Graph falhar.
        IOError: Se houver um problema ao escrever o arquivo no disco.

    """
    url = f'{MS_GRAPH_BASE_URL}/me/drive/items/{file_id}/content'
    response = httpx.get(url, headers=headers)
    
    if response.status_code == 302:
        download_location = response.headers['location']
        response_file_download = httpx.get(download_location)
        with open(file_name, 'wb') as file:
            file.write(response_file_download.content)
            print(f'Arquivo "{file_name}" baixado com sucesso')
    else:
        print(f'Falha ao baixar arquivo com id {file_id}')
        print('Descrição:')
        print(response.json())

def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ['User.Read', 'Files.ReadWrite.All']
    
    try:
        access_token = get_access_token(
            application_id=APPLICATION_ID,
            client_secret=CLIENT_SECRET,
            scopes=SCOPES
        )
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        folder_id = FOLDER_ID
        target_dir = Path('onedrive_dataset')
        files = list_folder_children(headers, folder_id)
        for file in files:
            if 'file' in file:
                file_id = file['id']
                download_file(headers, file_id, target_dir / file['name'])
    except Exception as e:
        print(f'Erro: {e}')

if __name__ == "__main__":
    main()
