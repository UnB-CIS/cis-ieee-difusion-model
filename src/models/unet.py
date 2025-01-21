"""
Módulo que implementa a arquitetura U-NET para o modelo SR3.
"""

from typing import Optional
import tensorflow as tf
from tensorflow.keras import layers, Model

class ConvBlock:
    """
    Bloco convolucional básico com condicionamento temporal.
    """
    
    def __init__(self, filters: int = 64) -> None:
        """
        Inicializa o bloco convolucional.
        
        Args:
            filters: Número de filtros para as camadas convolucionais
            
        Raises:
            ValueError: Se filters for menor que 1
        """
        if filters < 1:
            raise ValueError("Número de filtros deve ser maior que 0")
            
        self.filters = filters
        
    def __call__(self, x_img: tf.Tensor, x_ts: tf.Tensor) -> tf.Tensor:
        """
        Aplica as transformações do bloco.
        
        Args:
            x_img: Tensor da imagem de entrada
            x_ts: Tensor do embedding temporal
            
        Returns:
            Saída processada do bloco
            
        Raises:
            ValueError: Se x_img não for um tensor 4D (batch, height, width, channels)
            ValueError: Se x_ts não for um tensor 2D (batch, embedding_dim)
            RuntimeError: Se houver erro durante o processamento
        """
        if len(x_img.shape) != 4:
            raise ValueError("x_img deve ser um tensor 4D (batch, height, width, channels)")
        if len(x_ts.shape) != 2:
            raise ValueError("x_ts deve ser um tensor 2D (batch, embedding_dim)")
            
        try:
            # Processamento da imagem
            x_parameter = layers.Conv2D(self.filters, kernel_size=3, padding='same')(x_img)
            x_parameter = layers.Activation('relu')(x_parameter)

            # Processamento do tempo
            time_parameter = layers.Dense(self.filters)(x_ts)
            time_parameter = layers.Activation('relu')(time_parameter)
            time_parameter = layers.Reshape((1, 1, self.filters))(time_parameter)
            
            # Combinação dos features
            x_parameter = x_parameter * time_parameter
            
            # Processamento final
            x_out = layers.Conv2D(self.filters, kernel_size=3, padding='same')(x_img)
            x_out = x_out + x_parameter
            x_out = layers.LayerNormalization()(x_out)
            x_out = layers.Activation('relu')(x_out)
            
            return x_out
            
        except Exception as e:
            raise RuntimeError(f"Erro durante o processamento do bloco convolucional: {str(e)}")

class SR3UNET(Model):
    """
    Implementação da arquitetura U-NET para o modelo SR3.
    """
    
    def __init__(self) -> None:
        """
        Inicializa o modelo U-NET.
        
        Raises:
            RuntimeError: Se houver erro na inicialização do modelo
        """
        try:
            super(SR3UNET, self).__init__()
            self.conv_block = ConvBlock()
        except Exception as e:
            raise RuntimeError(f"Erro ao inicializar o modelo U-NET: {str(e)}")
        
    def build_model(self) -> Model:
        """
        Constrói a arquitetura do modelo.
        
        Returns:
            Modelo compilado
            
        Raises:
            RuntimeError: Se houver erro na construção do modelo
            ValueError: Se as dimensões dos tensores forem incompatíveis
            MemoryError: Se não houver memória suficiente para construir o modelo
        """
        try:
            # Entradas
            x1_ = x_input1 = layers.Input(shape=(128, 128, 3), name='x_input1')  # imagem com ruído
            x2_ = x_input2 = layers.Input(shape=(128, 128, 3), name='x_input2')  # imagem bicúbica
            
            # Concatenação das entradas
            x = tf.concat([x1_, x2_], axis=3)
            
            # Processamento do tempo
            x_ts = x_ts_input = layers.Input(shape=(1,), name='x_ts_input')
            x_ts = layers.Dense(64)(x_ts)
            x_ts = layers.LayerNormalization()(x_ts)
            x_ts = layers.Activation('relu')(x_ts)
            
            # Caminho descendente (encoder)
            x = x32 = self.conv_block(x, x_ts)
            x = layers.MaxPool2D(2)(x)
            
            x = x16 = self.conv_block(x, x_ts)
            x = layers.MaxPool2D(2)(x)
            
            x = x8 = self.conv_block(x, x_ts)
            
            # MLP Bridge
            x = layers.Flatten()(x)
            x = layers.Concatenate()([x, x_ts])
            x = layers.Dense(64)(x)
            x = layers.LayerNormalization()(x)
            x = layers.Activation('relu')(x)
            
            x = layers.Dense(32*32*64)(x)
            x = layers.LayerNormalization()(x)
            x = layers.Activation('relu')(x)
            x = layers.Reshape((32, 32, 64))(x)
            
            # Caminho ascendente (decoder)
            x = layers.Concatenate()([x, x8])
            x = self.conv_block(x, x_ts)
            x = layers.UpSampling2D(2)(x)
            
            x = layers.Concatenate()([x, x16])
            x = self.conv_block(x, x_ts)
            x = layers.UpSampling2D(2)(x)
            
            x = layers.Concatenate()([x, x32])
            x = self.conv_block(x, x_ts)
            
            # Concatenação final com entradas
            x = layers.Concatenate()([x, x1_, x2_])
            
            # Camada de saída
            x = layers.Conv2D(3, kernel_size=1, padding='same')(x)
            
            return Model([x_input1, x_input2, x_ts_input], x)
            
        except tf.errors.ResourceExhaustedError:
            raise MemoryError("Memória insuficiente para construir o modelo")
        except ValueError as e:
            raise ValueError(f"Erro nas dimensões dos tensores: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Erro ao construir o modelo: {str(e)}")
    
    def compile_model(self, learning_rate: float = 0.0008) -> None:
        """
        Compila o modelo com otimizador e função de perda.
        
        Args:
            learning_rate: Taxa de aprendizado para o otimizador
            
        Raises:
            ValueError: Se learning_rate for menor ou igual a 0
            RuntimeError: Se houver erro na compilação do modelo
        """
        if learning_rate <= 0:
            raise ValueError("learning_rate deve ser maior que 0")
            
        try:
            optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate)
            loss_func = tf.keras.losses.MeanSquaredError()
            self.compile(loss=loss_func, optimizer=optimizer)
        except Exception as e:
            raise RuntimeError(f"Erro ao compilar o modelo: {str(e)}")
