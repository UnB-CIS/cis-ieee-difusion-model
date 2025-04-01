
import os
from onedrive_client import OneDriveClient


def main():
    """
    Função principal que demonstra o uso da classe OneDriveClient para listar
    conteúdo do OneDrive.
    """
    client = OneDriveClient()
    
    try:
        client.authenticate()
        
        print("\n=== Conteúdo da pasta raiz ===\n")
        root_items = client.list_root_folder()
        client.print_items_metadata(root_items)
        
        folder_id = os.getenv('FOLDER_ID')
        print(f"\n=== Conteúdo da pasta {folder_id} ===\n")
        client.print_folder_children(folder_id)
        
    except Exception as e:
        print(f'Erro: {e}')

if __name__ == "__main__":
    main()
