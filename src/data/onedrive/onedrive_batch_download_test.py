import os
import time
import argparse
from pathlib import Path
from onedrive_client import OneDriveClient

def mock_process_images(file_paths):
    """
    Função de mock para simular processamento de imagens.
    Neste exemplo, apenas lê os arquivos e imprime informações básicas.
    """
    print(f"\n[MOCK PROCESSOR] Iniciando processamento de {len(file_paths)} arquivos...")
    
    for i, file_path in enumerate(file_paths):
        # Simula processamento que leva tempo
        print(f"[MOCK PROCESSOR] Processando arquivo {i+1}/{len(file_paths)}: {file_path.name}")
        
        # Obtém o tamanho do arquivo
        file_size = file_path.stat().st_size
        
        # Simula leitura do arquivo
        with open(file_path, 'rb') as f:
            # Apenas lê os primeiros bytes para confirmar acesso
            first_bytes = f.read(100)
            print(f"[MOCK PROCESSOR] Arquivo lido: {file_path.name}, tamanho: {file_size} bytes")
        
        # Simula um processamento que demora
        print(f"[MOCK PROCESSOR] Aplicando transformações em {file_path.name}...")
        time.sleep(0.5)  # Simula processamento que leva tempo
        
        print(f"[MOCK PROCESSOR] Concluído processamento de {file_path.name}")
    
    print(f"[MOCK PROCESSOR] Processamento de todos os arquivos concluído!")
    
    # Simula criação de um resultado
    result_file = Path('./batch_processing_result.txt')
    with open(result_file, 'a') as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp}: Processados {len(file_paths)} arquivos\n")
        for path in file_paths:
            f.write(f"  - {path.name}\n")
    
    print(f"[MOCK PROCESSOR] Resultados salvos em {result_file.absolute()}")
    return True


def main(interactive=True, batch_size=3):
    """
    Função principal que demonstra o uso de download em batches.
    """
    client = OneDriveClient()
    
    try:
        client.authenticate(interactive=interactive)
        
        folder_id = os.getenv('FOLDER_ID')
        if not folder_id:
            raise ValueError("FOLDER_ID não configurado no arquivo .env")
            
        target_dir = Path('src/data/onedrive_temp')
        
        print("\n=== Iniciando download de arquivos em batches ===\n")
        print(f"Tamanho do batch: {batch_size} arquivos")
        print(f"Pasta de download temporário: {target_dir}")
        print(f"Folder ID no OneDrive: {folder_id}")
        
        # Cria um arquivo para registrar o resultado total
        result_log = Path('./batch_processing_result.txt')
        if result_log.exists():
            result_log.unlink()
        
        with open(result_log, 'w') as f:
            f.write(f"=== LOG DE PROCESSAMENTO EM BATCHES ===\n")
            f.write(f"Início: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Inicia o processo de download em batches
        total_processed = client.download_folder_files_in_batches(
            folder_id=folder_id,
            target_dir=target_dir,
            batch_size=batch_size,
            process_func=mock_process_images
        )
        
        with open(result_log, 'a') as f:
            f.write(f"\nFim: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de arquivos processados: {total_processed}\n")
        
        print(f"\n=== {total_processed} arquivos baixados e processados em batches ===")
        print(f"Log completo salvo em: {result_log.absolute()}")
        
    except Exception as e:
        print(f'Erro: {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Baixar e processar arquivos do OneDrive em batches')
    parser.add_argument('--noninteractive', action='store_true', 
                      help='Usar autenticação não interativa (não recomendado para este tenant)')
    parser.add_argument('--batch-size', type=int, default=10,
                      help='Número de arquivos para baixar e processar em cada batch')
    args = parser.parse_args()
    
    main(interactive=not args.noninteractive, batch_size=args.batch_size)
