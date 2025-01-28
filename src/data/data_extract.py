import os
import requests
from pathlib import Path
import tempfile
from PIL import Image
import logging
from dataclasses import dataclass
from typing import Optional, Iterator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatasetConfig:
    """Configuração para um conjunto de dados.
    
    Args:
        folder_name (str): Nome da pasta contendo as imagens (ex: 'DIV2K_train_HR')
        start_index (int): Índice inicial para numeração das imagens
        end_index (Optional[int]): Índice final para numeração das imagens (inclusivo), None se não houver fim
        image_format (str): Formato dos arquivos de imagem (ex: 'png', 'jpg')
        index_digits (int): Número de dígitos no índice da imagem (ex: 4 para '0001.png')
    """
    folder_name: str
    start_index: int
    end_index: Optional[int]
    image_format: str = 'png'
    index_digits: int = 4

class ImageDataExtractor:
    """Extrator genérico de dados de imagem para vários formatos de datasets."""
    
    def __init__(self, base_url: str):
        """Inicializa o ImageDataExtractor.
        
        Args:
            base_url (str): URL base para a pasta compartilhada do OneDrive
            
        Raises:
            ValueError: Se a base_url for inválida
        """
        self.base_url = base_url
        self.temp_dir = tempfile.gettempdir()
    
    def _get_image_url(self, config: DatasetConfig, image_number: int) -> str:
        """Constrói a URL para uma imagem específica.
        
        Args:
            config (DatasetConfig): Configuração do dataset
            image_number (int): Número da imagem
            
        Returns:
            str: URL completa para a imagem
            
        Raises:
            ValueError: Se o número da imagem for inválido para o dataset
        """
        if config.end_index and image_number > config.end_index:
            raise ValueError(f"O número da imagem {image_number} excede o intervalo do dataset")
        if image_number < config.start_index:
            raise ValueError(f"O número da imagem {image_number} é inferior ao índice inicial do dataset")
            
        image_name = f"{image_number:0{config.index_digits}d}.{config.image_format}"
        return f"{self.base_url}/{config.folder_name}/{image_name}"
    
    def get_image(self, config: DatasetConfig, image_number: int) -> tuple[Image.Image, str]:
        """Baixa e retorna uma imagem do dataset.
        
        Args:
            config (DatasetConfig): Configuração do dataset
            image_number (int): Número da imagem para download
            
        Returns:
            tuple: (Objeto PIL Image, caminho do arquivo temporário)
            
        Raises:
            requests.exceptions.RequestException: Se o download falhar ou ocorrer erro de rede
            PIL.UnidentifiedImageError: Se a imagem não puder ser aberta ou estiver corrompida
            ValueError: Se o número da imagem for inválido
            OSError: Se o arquivo temporário não puder ser criado ou escrito
        """
        url = self._get_image_url(config, image_number)
        temp_path = os.path.join(self.temp_dir, f"temp_image_{image_number:04d}.{config.image_format}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            image = Image.open(temp_path)
            return image, temp_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Falha ao baixar a imagem {image_number}: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao processar a imagem {image_number}: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
    
    def cleanup_temp_file(self, temp_path: str) -> None:
        """Remove o arquivo temporário de imagem.
        
        Args:
            temp_path (str): Caminho do arquivo temporário a ser removido
            
        Raises:
            OSError: Se o arquivo não puder ser removido ou permissão negada
            FileNotFoundError: Se o arquivo temporário não existir
        """
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                logger.debug(f"Arquivo temporário removido: {temp_path}")
        except Exception as e:
            logger.warning(f"Falha ao remover o arquivo temporário {temp_path}: {e}")
    
    def iterate_dataset(self, config: DatasetConfig) -> Iterator[tuple[int, Image.Image, str]]:
        """Itera através de todas as imagens em um dataset.
        
        Args:
            config (DatasetConfig): Configuração do dataset
            
        Yields:
            tuple: (número da imagem, objeto PIL Image, caminho do arquivo temporário)
            
        Raises:
            requests.exceptions.RequestException: Se o download falhar
            PIL.UnidentifiedImageError: Se a imagem não puder ser aberta
            OSError: Se as operações com arquivos temporários falharem
        """
        current_index = config.start_index
        while True:
            if config.end_index and current_index > config.end_index:
                break
                
            try:
                image, temp_path = self.get_image(config, current_index)
                yield current_index, image, temp_path
                current_index += 1
            except requests.exceptions.RequestException as e:
                if config.end_index is None:
                    # Se nenhum end_index for especificado, assume que chegamos ao fim
                    break
                raise

# Configurações predefinidas de datasets
DIV2K_TRAIN = DatasetConfig(
    folder_name="DIV2K_train_HR",
    start_index=1,
    end_index=None,
    image_format="png",
    index_digits=4
)

DIV2K_VALID = DatasetConfig(
    folder_name="DIV2K_valid_HR",
    start_index=800,
    end_index=None,
    image_format="png",
    index_digits=4
)

FLICKR2K = DatasetConfig(
    folder_name="Flickr2K/Flickr2K_HR",
    start_index=1,
    end_index=None, 
    image_format="png",
    index_digits=4
)