import os
from pathlib import Path
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL

class OneDriveClient:
    """
    Cliente para interagir com a API Microsoft Graph para OneDrive.
    """
    
    def __init__(self, client_id=None, client_secret=None, tenant_id=None):
        """
        Inicializa o cliente OneDrive.
        """

        if client_id is None or client_secret is None:
            load_dotenv()
            self.client_id = client_id or os.getenv('CLIENT_ID')
            self.client_secret = client_secret or os.getenv('CLIENT_SECRET')
            self.tenant_id = tenant_id or os.getenv('TENANT_ID')
        else:
            self.client_id = client_id
            self.client_secret = client_secret
            self.tenant_id = tenant_id
            
        self.scopes = ['User.Read', 'Files.ReadWrite.All']
        self.access_token = None
        self.headers = None
    
    def authenticate(self, scopes=None, interactive=True):
        """
        Autentica com a API Microsoft Graph.
        """
        if scopes:
            self.scopes = scopes
        

        if interactive:
            print("\nUsando autenticação interativa (requer interação do usuário)...")
            self.access_token = get_access_token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.scopes,
                interactive=True
            )
        else:
            if not self.tenant_id:
                raise ValueError("Para autenticação não interativa, é necessário fornecer o tenant_id")
                
            print("\nUsando autenticação não interativa (client credentials flow)...")
            self.access_token = get_access_token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                tenant_id=self.tenant_id,
                interactive=False
            )
        

        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        return self.access_token
    
    def list_root_folder(self):
        """
        Lista o conteúdo da pasta raiz do OneDrive.
        """
        if not self.headers:
            self.authenticate()
            
        url = f'{MS_GRAPH_BASE_URL}/me/drive/root/children'
        response = httpx.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return [item for item in data['value']]
        else:
            print(f'Falha ao listar pasta raiz: {response.status_code}')
            return []
    
    def get_folder_children(self, folder_id):
        """
        Obtém uma lista de itens filhos (arquivos e pastas) para um ID de pasta específico.
        """

        if not self.headers:
            self.authenticate()
            
        url = f'{MS_GRAPH_BASE_URL}/me/drive/items/{folder_id}/children'
        response = httpx.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return [item for item in data['value']]
        else:
            print(f'Falha ao listar conteúdo da pasta {folder_id}: {response.status_code}')
            return []
    
    def print_folder_children(self, folder_id):
        """
        Lista e exibe informações detalhadas sobre o conteúdo de uma pasta específica.
        """
        items = self.get_folder_children(folder_id)
        
        for item in items:
            if 'folder' in item:
                print(f'Folder id: {item["id"]}')
                print(f'Folder name: {item["name"]}')
                print(f'Folder web url: {item["webUrl"]}')
                print(f'Folder size: {item["size"]}')
                print(f'Folder created date: {item["createdDateTime"]}')
                print(f'Created by: {item["createdBy"]["user"]["displayName"]}')
                print(f'Folder modified date: {item["lastModifiedDateTime"]}')
                print(f'Last modified by: {item["lastModifiedBy"]["user"]["displayName"]}')
                print(f'Folder parent id: {item["parentReference"]["id"]}')
                print(f'Item Count: {item["folder"]["childCount"]}')
                print('-' * 50)
            elif 'file' in item:
                print(f'File id: {item["id"]}')
                print(f'File name: {item["name"]}')
                print(f'File web url: {item["webUrl"]}')
                print(f'File size (in KB): {item["size"] / 1024:.2f}')
                print(f'File created date: {item["createdDateTime"]}')
                print(f'Created by: {item["createdBy"]["user"]["displayName"]}')
                print(f'File modified date: {item["lastModifiedDateTime"]}')
                print(f'Last modified by: {item["lastModifiedBy"]["user"]["displayName"]}')
                print(f'File parent id: {item["parentReference"]["id"]}')
                print(f'File Mime type: {item["file"]["mimeType"]}')
                print('-' * 50)
                
        return items
    
    def print_items_metadata(self, items):
        """
        Exibe metadados detalhados de uma lista de itens.
        """
        for item in items:
            if 'folder' in item:
                print(f'Folder id: {item["id"]}')
                print(f'Folder name: {item["name"]}')
                print(f'Folder web url: {item["webUrl"]}')
                print(f'Folder size: {item["size"]}')
                print(f'Folder created date: {item["createdDateTime"]}')
                print(f'Created by: {item["createdBy"]["user"]["displayName"]}')
                print(f'Folder modified date: {item["lastModifiedDateTime"]}')
                print(f'Last modified by: {item["lastModifiedBy"]["user"]["displayName"]}')
                print(f'Folder parent id: {item["parentReference"]["id"]}')
                print(f'Item Count: {item["folder"]["childCount"]}')
                print('-' * 50)
            elif 'file' in item:
                print(f'File id: {item["id"]}')
                print(f'File name: {item["name"]}')
                print(f'File web url: {item["webUrl"]}')
                print(f'File size (in KB): {item["size"] / 1024:.2f}')
                print(f'File created date: {item["createdDateTime"]}')
                print(f'Created by: {item["createdBy"]["user"]["displayName"]}')
                print(f'File modified date: {item["lastModifiedDateTime"]}')
                print(f'Last modified by: {item["lastModifiedBy"]["user"]["displayName"]}')
                print(f'File parent id: {item["parentReference"]["id"]}')
                print(f'File Mime type: {item["file"]["mimeType"]}')
                print('-' * 50)
    
    def download_file(self, file_id, file_path):
        """
        Baixa um arquivo do OneDrive usando a API Microsoft Graph.
        """
        if not self.headers:
            self.authenticate()
            
        url = f'{MS_GRAPH_BASE_URL}/me/drive/items/{file_id}/content'
        response = httpx.get(url, headers=self.headers)
        
        if response.status_code == 302:
            download_location = response.headers['location']
            response_file_download = httpx.get(download_location)
            
            with open(file_path, 'wb') as file:
                file.write(response_file_download.content)
                print(f'Arquivo "{file_path}" baixado com sucesso')
            return True
        else:
            print(f'Falha ao baixar arquivo com id {file_id}')
            print('Descrição:')
            print(response.json())
            return False
    
    def download_folder_files(self, folder_id, target_dir='onedrive_dataset'):
        """
        Baixa todos os arquivos de uma pasta específica.
        """
        if not self.headers:
            self.authenticate()
            
        target_path = Path(target_dir)
        target_path.mkdir(exist_ok=True, parents=True)

        files = self.get_folder_children(folder_id)
        

        success_count = 0
        

        for file in files:
            if 'file' in file:
                file_id = file['id']
                file_name = file['name']
                file_path = target_path / file_name
                
                if self.download_file(file_id, file_path):
                    success_count += 1
        
        return success_count
