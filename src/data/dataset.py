"""
Módulo para manipulação e carregamento de dados para o modelo SR3.
"""

from typing import Tuple, Optional, List
import os
import cv2
import numpy as np
import tensorflow as tf

class SR3Dataset:
    """
    Classe para gerenciamento do dataset para super resolução.
    """
    
    def __init__(
        self, 
        base_dir: str, 
        hr_size: int = 128, 
        lr_size: int = 32, 
        max_images: Optional[int] = None
    ) -> None:
        """
        Inicializa o gerenciador de dataset.
        
        Args:
            base_dir: Diretório base contendo as imagens
            hr_size: Tamanho desejado para imagens de alta resolução
            lr_size: Tamanho para downscaling das imagens de baixa resolução
            max_images: Número máximo de imagens para carregar
            
        Raises:
            ValueError: Se hr_size ou lr_size forem menores que 1
            ValueError: Se max_images for menor que 1
            NotADirectoryError: Se base_dir não existir ou não for um diretório
        """
        if hr_size < 1 or lr_size < 1:
            raise ValueError("Dimensões das imagens devem ser maiores que 0")
        if max_images is not None and max_images < 1:
            raise ValueError("max_images deve ser maior que 0")
        if not os.path.isdir(base_dir):
            raise NotADirectoryError(f"Diretório não encontrado: {base_dir}")
            
        self.base_dir = base_dir
        self.hr_size = hr_size
        self.lr_size = lr_size
        self.max_images = max_images
        
    def load_images(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Carrega e processa as imagens do diretório.
        
        Returns:
            Tupla contendo (imagens HR, imagens LR upscaled)
            
        Raises:
            RuntimeError: Se nenhuma imagem for encontrada no diretório
            IOError: Se houver erro ao ler alguma imagem
            ValueError: Se alguma imagem estiver corrompida ou em formato inválido
        """
        hr_images: List[np.ndarray] = []
        lr_images: List[np.ndarray] = []
        
        try:
            # Percorre o diretório de imagens
            for person in os.listdir(self.base_dir):
                person_dir = os.path.join(self.base_dir, person)
                
                if os.path.isdir(person_dir):
                    for image_file in os.listdir(person_dir):
                        try:
                            image_path = os.path.join(person_dir, image_file)
                            
                            # Carrega e processa a imagem
                            img = cv2.imread(image_path)
                            if img is None:
                                raise ValueError(f"Imagem inválida ou corrompida: {image_path}")
                                
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img_rgb = img_rgb / 255.0  # Normalização
                            
                            # Gera versão HR
                            hr = cv2.resize(img_rgb, (self.hr_size, self.hr_size), 
                                          interpolation=cv2.INTER_CUBIC)
                            
                            # Gera versão LR e faz upscaling
                            lr = cv2.resize(img_rgb, (self.lr_size, self.lr_size), 
                                          interpolation=cv2.INTER_CUBIC)
                            lr = cv2.resize(lr, (self.hr_size, self.hr_size), 
                                          interpolation=cv2.INTER_CUBIC)
                            
                            hr_images.append(hr)
                            lr_images.append(lr)
                            
                            if self.max_images and len(hr_images) >= self.max_images:
                                break
                        except IOError as e:
                            raise IOError(f"Erro ao ler imagem {image_path}: {str(e)}")
                        except Exception as e:
                            raise ValueError(f"Erro ao processar imagem {image_path}: {str(e)}")
                
                if self.max_images and len(hr_images) >= self.max_images:
                    break
                    
            if not hr_images:
                raise RuntimeError(f"Nenhuma imagem encontrada em {self.base_dir}")
            
            return np.array(hr_images), np.array(lr_images)
            
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar imagens: {str(e)}")
    
    def create_tf_dataset(
        self, 
        batch_size: int = 32, 
        shuffle: bool = True
    ) -> tf.data.Dataset:
        """
        Cria um tf.data.Dataset para treinamento.
        
        Args:
            batch_size: Tamanho do batch
            shuffle: Se deve embaralhar os dados
            
        Returns:
            Dataset pronto para treinamento
            
        Raises:
            ValueError: Se batch_size for menor que 1
            RuntimeError: Se houver erro ao criar o dataset
            MemoryError: Se não houver memória suficiente para carregar os dados
        """
        if batch_size < 1:
            raise ValueError("batch_size deve ser maior que 0")
            
        try:
            hr_images, lr_images = self.load_images()
            
            dataset = tf.data.Dataset.from_tensor_slices((hr_images, lr_images))
            
            if shuffle:
                dataset = dataset.shuffle(buffer_size=len(hr_images))
                
            dataset = dataset.batch(batch_size)
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
            
            return dataset
            
        except tf.errors.ResourceExhaustedError:
            raise MemoryError("Memória insuficiente para criar o dataset")
        except Exception as e:
            raise RuntimeError(f"Erro ao criar dataset: {str(e)}")
