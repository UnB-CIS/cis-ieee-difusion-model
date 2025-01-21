"""
Módulo de visualização para o modelo SR3.
Fornece funções para visualizar o processo de difusão e resultados da super resolução.
"""

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

class DiffusionVisualizer:
    """
    Classe para visualização do processo de difusão e resultados do SR3.
    """
    
    @staticmethod
    def plot_diffusion_steps(images, noise_steps, num_samples=5, figsize=(15, 5)):
        """
        Plota o processo de difusão em diferentes passos de tempo.
        
        Args:
            images (np.ndarray): Imagens originais
            noise_steps (list): Lista de passos de tempo para visualizar
            num_samples (int): Número de imagens para mostrar
            figsize (tuple): Tamanho da figura
        """
        fig, axes = plt.subplots(num_samples, len(noise_steps), figsize=figsize)
        
        for i in range(num_samples):
            for j, step in enumerate(noise_steps):
                if num_samples > 1:
                    ax = axes[i, j]
                else:
                    ax = axes[j]
                    
                ax.imshow(images[i, step])
                ax.set_title(f'Step {step}')
                ax.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_sr_comparison(sr_images, hr_images, lr_images, num_samples=4, figsize=(15, 20)):
        """
        Plota comparação entre imagens SR, HR e LR.
        
        Args:
            sr_images (np.ndarray): Imagens geradas pelo modelo SR3
            hr_images (np.ndarray): Imagens originais em alta resolução
            lr_images (np.ndarray): Imagens em baixa resolução com upscaling
            num_samples (int): Número de amostras para visualizar
            figsize (tuple): Tamanho da figura
        """
        fig, axes = plt.subplots(num_samples, 3, figsize=figsize)
        
        titles = ['SR3 Super Resolution', 'Ground Truth (HR)', 'Bicubic Upscaled']
        images = [sr_images, hr_images, lr_images]
        
        for i in range(num_samples):
            for j in range(3):
                axes[i, j].imshow(images[j][i])
                axes[i, j].set_title(titles[j])
                axes[i, j].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_training_progress(model_outputs, target_images, timesteps, num_samples=2, figsize=(15, 10)):
        """
        Plota o progresso do treinamento em diferentes timesteps.
        
        Args:
            model_outputs (list): Lista de saídas do modelo em diferentes timesteps
            target_images (np.ndarray): Imagens alvo (ground truth)
            timesteps (list): Lista dos timesteps correspondentes
            num_samples (int): Número de amostras para visualizar
            figsize (tuple): Tamanho da figura
        """
        fig, axes = plt.subplots(num_samples, len(timesteps) + 1, figsize=figsize)
        
        for i in range(num_samples):
            # Plota a imagem alvo
            if num_samples > 1:
                ax = axes[i, 0]
            else:
                ax = axes[0]
            
            ax.imshow(target_images[i])
            ax.set_title('Target')
            ax.axis('off')
            
            # Plota as saídas do modelo
            for j, (output, step) in enumerate(zip(model_outputs, timesteps)):
                if num_samples > 1:
                    ax = axes[i, j+1]
                else:
                    ax = axes[j+1]
                
                ax.imshow(output[i])
                ax.set_title(f'Step {step}')
                ax.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_attention_maps(attention_weights, input_image, num_heads=4, figsize=(15, 5)):
        """
        Plota mapas de atenção do modelo.
        
        Args:
            attention_weights (np.ndarray): Pesos de atenção do modelo
            input_image (np.ndarray): Imagem de entrada
            num_heads (int): Número de cabeças de atenção para visualizar
            figsize (tuple): Tamanho da figura
        """
        fig, axes = plt.subplots(1, num_heads + 1, figsize=figsize)
        
        # Plota a imagem original
        axes[0].imshow(input_image)
        axes[0].set_title('Input Image')
        axes[0].axis('off')
        
        # Plota os mapas de atenção
        for i in range(num_heads):
            attention_map = attention_weights[i]
            axes[i+1].imshow(attention_map, cmap='viridis')
            axes[i+1].set_title(f'Attention Head {i+1}')
            axes[i+1].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    # @staticmethod
    # def save_image_grid(images, filename, nrow=8, padding=2):
    #     """
    #     Salva uma grade de imagens em um arquivo.
        
    #     Args:
    #         images (np.ndarray): Array de imagens para salvar
    #         filename (str): Nome do arquivo de saída
    #         nrow (int): Número de imagens por linha
    #         padding (int): Padding entre as imagens
    #     """
    #     # Calcula o número de linhas necessário
    #     if isinstance(images, list):
    #         images = np.stack(images)
        
    #     if len(images.shape) == 3:
    #         images = images[..., np.newaxis]
            
    #     nmaps = images.shape[0]
    #     xmaps = min(nrow, nmaps)
    #     ymaps = int(np.ceil(float(nmaps) / xmaps))
        
    #     # Cria a grade de imagens
    #     grid = np.ones(
    #         (
    #             padding + ymaps * (images.shape[1] + padding),
    #             padding + xmaps * (images.shape[2] + padding),
    #             images.shape[3]
    #         )
    #     )
        
    #     k = 0
    #     for y in range(ymaps):
    #         for x in range(xmaps):
    #             if k >= nmaps:
    #                 break
                    
    #             grid[
    #                 y * (images.shape[1] + padding) + padding:(y + 1) * (images.shape[1] + padding),
    #                 x * (images.shape[2] + padding) + padding:(x + 1) * (images.shape[2] + padding)
    #             ] = images[k]
    #             k += 1
                
    #     # Salva a imagem
    #     plt.imsave(filename, grid.squeeze())
