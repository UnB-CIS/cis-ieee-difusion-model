"""
Script principal para treinamento do modelo SR3.
"""

from typing import Tuple, Optional
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from models.unet import SR3UNET
from models.diffusion import DiffusionSR
from data.dataset import SR3Dataset

def plot_results(
    model: tf.keras.Model, 
    test_images: Tuple[tf.Tensor, tf.Tensor], 
    save_path: Optional[str] = None
) -> None:
    """
    Plota e opcionalmente salva os resultados do modelo.
    
    Args:
        model: Modelo treinado
        test_images: Tupla de (imagens HR, imagens LR)
        save_path: Caminho para salvar o plot. Se None, apenas exibe
        
    Raises:
        ValueError: Se test_images não tiver o formato correto
        ValueError: Se save_path não for um caminho válido
        RuntimeError: Se houver erro ao gerar ou salvar o plot
    """
    if not isinstance(test_images, tuple) or len(test_images) != 2:
        raise ValueError("test_images deve ser uma tupla de (HR, LR)")
    if save_path and not os.path.isdir(os.path.dirname(save_path)):
        raise ValueError(f"Diretório inválido para save_path: {save_path}")
        
    try:
        hr_images, lr_images = test_images
        predictions = model.predict(lr_images)
        
        plt.figure(figsize=(15, 5))
        
        for i in range(3):  # Plota 3 exemplos
            # Imagem original HR
            plt.subplot(3, 3, i*3 + 1)
            plt.imshow(hr_images[i])
            plt.title('Original HR')
            plt.axis('off')
            
            # Imagem LR upscaled
            plt.subplot(3, 3, i*3 + 2)
            plt.imshow(lr_images[i])
            plt.title('LR Upscaled')
            plt.axis('off')
            
            # Predição do modelo
            plt.subplot(3, 3, i*3 + 3)
            plt.imshow(predictions[i])
            plt.title('Predicted HR')
            plt.axis('off')
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
            
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar/salvar plot: {str(e)}")

def train_model(
    data_dir: str,
    epochs: int = 100,
    batch_size: int = 16,
    learning_rate: float = 0.0008,
    max_images: Optional[int] = None,
    save_dir: Optional[str] = None
) -> tf.keras.Model:
    """
    Treina o modelo SR3.
    
    Args:
        data_dir: Diretório com as imagens de treino
        epochs: Número de épocas de treinamento
        batch_size: Tamanho do batch
        learning_rate: Taxa de aprendizado
        max_images: Número máximo de imagens para treino
        save_dir: Diretório para salvar checkpoints e resultados
        
    Returns:
        Modelo treinado
        
    Raises:
        ValueError: Se os parâmetros de treinamento forem inválidos
        NotADirectoryError: Se data_dir ou save_dir não existirem
        RuntimeError: Se houver erro durante o treinamento
        MemoryError: Se não houver memória suficiente
    """
    # Validação de parâmetros
    if epochs < 1:
        raise ValueError("epochs deve ser maior que 0")
    if batch_size < 1:
        raise ValueError("batch_size deve ser maior que 0")
    if learning_rate <= 0:
        raise ValueError("learning_rate deve ser maior que 0")
    if not os.path.isdir(data_dir):
        raise NotADirectoryError(f"Diretório de dados não encontrado: {data_dir}")
    if save_dir and not os.path.isdir(save_dir):
        raise NotADirectoryError(f"Diretório de salvamento não encontrado: {save_dir}")
        
    try:
        # Configuração do GPU
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        
        # Carregamento dos dados
        dataset = SR3Dataset(data_dir, max_images=max_images)
        train_ds = dataset.create_tf_dataset(batch_size=batch_size)
        
        # Inicialização do modelo e processo de difusão
        model = SR3UNET()
        diffusion = DiffusionSR()
        
        # Compilação do modelo
        model.compile_model(learning_rate=learning_rate)
        
        # Callbacks
        callbacks = []
        if save_dir:
            checkpoint_path = os.path.join(save_dir, 'checkpoints/model_{epoch:02d}.h5')
            os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
            callbacks.append(
                tf.keras.callbacks.ModelCheckpoint(
                    checkpoint_path,
                    save_best_only=True,
                    monitor='loss'
                )
            )
        
        # Treinamento
        history = model.fit(
            train_ds,
            epochs=epochs,
            callbacks=callbacks
        )
        
        # Salva resultados finais
        if save_dir:
            model.save(os.path.join(save_dir, 'modelo_final.h5'))
            
            # Plota e salva curva de perda
            plt.figure(figsize=(10, 5))
            plt.plot(history.history['loss'])
            plt.title('Curva de Perda do Modelo')
            plt.xlabel('Época')
            plt.ylabel('Perda')
            plt.savefig(os.path.join(save_dir, 'curva_perda.png'))
        
        return model
        
    except tf.errors.ResourceExhaustedError:
        raise MemoryError("Memória insuficiente durante o treinamento")
    except Exception as e:
        raise RuntimeError(f"Erro durante o treinamento: {str(e)}")

if __name__ == '__main__':
    try:
        # Diretórios de dados e salvamento
        DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
        SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'resultados')
        
        # Cria diretório de salvamento se não existir
        os.makedirs(SAVE_DIR, exist_ok=True)
        
        # Treina o modelo
        model = train_model(
            data_dir=DATA_DIR,
            epochs=100,
            batch_size=16,
            save_dir=SAVE_DIR
        )
        
        print("Treinamento concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
        raise
