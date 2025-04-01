
import os
import argparse
from pathlib import Path
from onedrive_client import OneDriveClient


def main(interactive=True):
    """
    Função principal que demonstra o uso da classe OneDriveClient para
    baixar arquivos do OneDrive.
    """
    client = OneDriveClient()
    
    try:
        client.authenticate(interactive=interactive)
        
        folder_id = os.getenv('FOLDER_ID')
        target_dir = Path('src/data/onedrive_dataset')
        
        target_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n=== Iniciando download de arquivos ===\n")
        count = client.download_folder_files(folder_id, target_dir)
        print(f"\n=== {count} arquivos baixados com sucesso ===\n")
        
    except Exception as e:
        print(f'Erro: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Baixar arquivos do OneDrive via Microsoft Graph API')
    parser.add_argument('--noninteractive', action='store_true', 
                      help='Usar autenticação não interativa (client credentials flow). '
                           'Requer TENANT_ID definido no .env e permissões de aplicativo configuradas no Azure.')
    args = parser.parse_args()
    
    main(interactive=not args.noninteractive)
