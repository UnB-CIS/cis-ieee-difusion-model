"""
Módulo de difusão para o modelo SR3.
Implementa o processo de difusão e desdifusão para super resolução de imagens.
"""

from typing import Tuple, Union
import numpy as np
import tensorflow as tf

class DiffusionSR:
    """
    Classe que implementa o processo de difusão para super resolução.
    
    Attributes:
        timesteps (int): Número total de passos de tempo para o processo de difusão
        beta (np.ndarray): Cronograma de variância do ruído
        alpha (np.ndarray): 1 - beta
        alpha_bar (np.ndarray): Produto cumulativo de alpha
    """
    
    def __init__(self, timesteps: int = 1000, beta_start: float = 0.0001, beta_end: float = 0.02) -> None:
        """
        Inicializa o processo de difusão.
        
        Args:
            timesteps: Número de passos de tempo
            beta_start: Valor inicial de beta
            beta_end: Valor final de beta
            
        Raises:
            ValueError: Se timesteps for menor que 1
            ValueError: Se beta_start for menor ou igual a 0
            ValueError: Se beta_end for menor que beta_start
        """
        if timesteps < 1:
            raise ValueError("timesteps deve ser maior que 0")
        if beta_start <= 0:
            raise ValueError("beta_start deve ser maior que 0")
        if beta_end <= beta_start:
            raise ValueError("beta_end deve ser maior que beta_start")
            
        self.timesteps = timesteps
        
        # Criação do cronograma de beta linear
        self.beta: np.ndarray = np.linspace(beta_start, beta_end, timesteps)
        
        # Cálculo dos parâmetros alpha
        self.alpha: np.ndarray = 1 - self.beta
        self.alpha_bar: np.ndarray = np.cumprod(self.alpha, 0)
        self.alpha_bar = np.concatenate((np.array([1.]), self.alpha_bar[:-1]), axis=0)
        
        # Raiz quadrada dos parâmetros para uso eficiente
        self.sqrt_alpha_bar: np.ndarray = np.sqrt(self.alpha_bar)
        self.one_minus_sqrt_alpha_bar: np.ndarray = np.sqrt(1 - self.alpha_bar)
    
    def add_noise(self, x_0: Union[np.ndarray, tf.Tensor], t: np.ndarray) -> Tuple[tf.Tensor, tf.Tensor]:
        """
        Adiciona ruído à imagem de acordo com o passo de tempo especificado.
        
        Args:
            x_0: Imagem original
            t: Índices dos passos de tempo
            
        Returns:
            Tupla contendo (imagem com ruído, ruído adicionado)
            
        Raises:
            ValueError: Se x_0 tiver formato inválido
            ValueError: Se t contiver valores fora do intervalo [0, timesteps-1]
            RuntimeError: Se houver erro durante a adição de ruído
        """
        if not isinstance(x_0, (np.ndarray, tf.Tensor)):
            raise ValueError("x_0 deve ser um array numpy ou tensor tensorflow")
        if t.min() < 0 or t.max() >= self.timesteps:
            raise ValueError(f"Valores de t devem estar entre 0 e {self.timesteps-1}")
            
        try:
            noise = np.random.normal(size=x_0.shape)
            sqrt_alpha_bar_t = np.reshape(np.take(self.sqrt_alpha_bar, t), [-1, 1, 1, 1])
            one_minus_sqrt_alpha_bar_t = np.reshape(
                np.take(self.one_minus_sqrt_alpha_bar, t), [-1, 1, 1, 1]
            )
            
            noisy_img = sqrt_alpha_bar_t * x_0 + one_minus_sqrt_alpha_bar_t * noise
            return tf.convert_to_tensor(noisy_img), tf.convert_to_tensor(noise)
            
        except Exception as e:
            raise RuntimeError(f"Erro ao adicionar ruído: {str(e)}")
    
    def ddim_sample(
        self, 
        x_t: tf.Tensor, 
        pred_noise: tf.Tensor, 
        t: int, 
        step_size: int
    ) -> tf.Tensor:
        """
        Implementa a amostragem DDIM (Denoising Diffusion Implicit Models).
        
        Args:
            x_t: Imagem com ruído no tempo t
            pred_noise: Ruído predito pelo modelo
            t: Passo de tempo atual
            step_size: Tamanho do passo para amostragem
            
        Returns:
            Imagem com menos ruído
            
        Raises:
            ValueError: Se t for menor que step_size
            ValueError: Se x_t e pred_noise tiverem formatos diferentes
            ValueError: Se step_size for maior que t
            RuntimeError: Se houver erro durante a amostragem
        """
        if not isinstance(x_t, tf.Tensor) or not isinstance(pred_noise, tf.Tensor):
            raise ValueError("x_t e pred_noise devem ser tensores tensorflow")
        if x_t.shape != pred_noise.shape:
            raise ValueError("x_t e pred_noise devem ter o mesmo formato")
        if t < step_size:
            raise ValueError("t deve ser maior ou igual a step_size")
            
        try:
            alpha_t_bar = np.reshape(np.take(self.alpha_bar, t), [-1, 1, 1, 1])
            alpha_t_minus_one = np.reshape(
                np.take(self.alpha_bar, t-step_size), [-1, 1, 1, 1]
            )
            
            # Predição da imagem menos ruidosa
            pred = (x_t - ((1 - alpha_t_bar) ** 0.5) * pred_noise) / (alpha_t_bar ** 0.5)
            pred = (alpha_t_minus_one ** 0.5) * pred
            
            # Adição do ruído predito
            pred = pred + ((1 - alpha_t_minus_one) ** 0.5) * pred_noise
            return pred
            
        except Exception as e:
            raise RuntimeError(f"Erro durante a amostragem DDIM: {str(e)}")
