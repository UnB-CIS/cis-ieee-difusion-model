"""
Integração OneDrive DnCNN
--------------------------
Este módulo fornece funções para integrar o download em lotes do OneDrive
com o treinamento do modelo DnCNN usando autenticação interativa.
"""

import tensorflow as tf
import numpy as np
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Import OneDriveClient - assuming this is in a parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from onedrive_client import OneDriveClient

def authenticate_onedrive(interactive=True):
    """
    Autentica no OneDrive usando a abordagem interativa
    """
    client = OneDriveClient()
    client.authenticate(interactive=interactive)
    print("Autenticação bem-sucedida!")
    return client

def process_batch_for_dncnn(file_paths, model, noise_std=0.1, patch_size=50, patches_per_image=10):
    """
    Processa um lote de imagens para treinamento do DnCNN
    """
    print(f"\nProcessando lote de {len(file_paths)} imagens...")
    
    # Arrays para armazenar patches processados
    input_patches = []  # Patches ruidosos (entrada para o modelo)
    target_patches = []  # Resíduos de ruído (alvo para o modelo)
    
    for file_path in file_paths:
        # Pular arquivos que não são imagens
        if Path(file_path).suffix.lower() not in ['.jpg', '.jpeg', '.png']:
            continue
            
        # Carregar imagem
        try:
            img = tf.keras.utils.load_img(file_path, color_mode='rgb')
            img_array = tf.keras.utils.img_to_array(img)
            img_array = img_array / 255.0  # Normalizar para [0,1]
            
            # Pular imagens que são muito pequenas
            if img_array.shape[0] < patch_size or img_array.shape[1] < patch_size:
                print(f"Pulando {Path(file_path).name} - muito pequena")
                continue
                
            # Extrair patches aleatórios
            for _ in range(patches_per_image):
                h = np.random.randint(0, img_array.shape[0] - patch_size)
                w = np.random.randint(0, img_array.shape[1] - patch_size)
                patch = img_array[h:h+patch_size, w:w+patch_size]
                
                # Adicionar ruído para criar patch ruidoso
                noise = np.random.normal(0, noise_std, patch.shape)
                noisy_patch = np.clip(patch + noise, 0, 1)
                
                # Armazenar patches
                input_patches.append(noisy_patch)
                target_patches.append(noise)  # Para o DnCNN, o alvo é o ruído
                
        except Exception as e:
            print(f"Erro ao processar {Path(file_path).name}: {e}")
    
    # Treinar neste lote se tivermos patches
    if input_patches:
        x_batch = np.array(input_patches)
        y_batch = np.array(target_patches)
        
        # Treinar o modelo neste lote
        loss = model.train_on_batch(x_batch, y_batch)
        print(f"  Lote treinado - Perda: {loss:.6f}")
    
    return True

def train_dncnn_with_onedrive(
    model, 
    folder_id, 
    client=None, 
    epochs=5, 
    batch_size=16, 
    noise_std=0.1, 
    patch_size=50, 
    patches_per_image=10,
    interactive=True
):
    """
    Treina o modelo DnCNN usando imagens do OneDrive
    """
    # Criar cliente se não for fornecido
    if client is None:
        client = authenticate_onedrive(interactive=interactive)
    
    # Compilar modelo se ainda não estiver compilado
    if not hasattr(model, 'optimizer') or model.optimizer is None:
        print("Compilando modelo...")
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        loss_fn = tf.keras.losses.MeanSquaredError()
        model.compile(optimizer=optimizer, loss=loss_fn)
    
    # Diretório para downloads temporários
    temp_dir = Path('temp_downloads')
    temp_dir.mkdir(exist_ok=True, parents=True)
    
    # Criar uma função de processamento com referência ao modelo
    def process_batch(file_paths):
        return process_batch_for_dncnn(
            file_paths, 
            model, 
            noise_std=noise_std, 
            patch_size=patch_size, 
            patches_per_image=patches_per_image
        )
    
    # Treinar por múltiplas épocas
    for epoch in range(epochs):
        print(f"\n=== Época {epoch+1}/{epochs} ===")
        
        # Baixar e processar arquivos em lotes
        client.download_folder_files_in_batches(
            folder_id=folder_id,
            target_dir=str(temp_dir),
            batch_size=batch_size,
            process_func=process_batch
        )
        
        print(f"Época {epoch+1}/{epochs} concluída")
    
    return model

def test_dncnn_model(model, test_images, noise_std=0.1, save_path=None):
    """
    Testa o modelo DnCNN em uma lista de imagens de teste
    """
    import matplotlib.pyplot as plt
    
    # Número de imagens para exibir
    num_images = min(len(test_images), 3)
    
    # Criar figura
    plt.figure(figsize=(15, 5 * num_images))
    
    for i, image_path in enumerate(test_images[:num_images]):
        # Carregar e pré-processar imagem
        img = tf.keras.utils.load_img(image_path, color_mode='rgb')
        img_array = tf.keras.utils.img_to_array(img)
        img_array = img_array / 255.0  # Normalize
        
        # Add noise
        noise = np.random.normal(0, noise_std, img_array.shape)
        noisy_img = np.clip(img_array + noise, 0, 1)
        
        # Prever ruído usando o modelo
        predicted_noise = model.predict(np.expand_dims(noisy_img, 0))[0]
        
        # Imagem sem ruído
        denoised_img = np.clip(noisy_img - predicted_noise, 0, 1)
        
        # Exibir imagens
        plt.subplot(num_images, 3, i*3 + 1)
        plt.imshow(img_array)
        plt.title('Original')
        plt.axis('off')
        
        plt.subplot(num_images, 3, i*3 + 2)
        plt.imshow(noisy_img)
        plt.title(f'Com Ruído (σ={noise_std})')
        plt.axis('off')
        
        plt.subplot(num_images, 3, i*3 + 3)
        plt.imshow(denoised_img)
        plt.title('Sem Ruído')
        plt.axis('off')
    
    plt.tight_layout()
    
    # Salvar se o caminho for fornecido
    if save_path:
        plt.savefig(save_path)
        print(f"Resultados salvos em {save_path}")
    
    plt.show()
