import pytest
from PIL import Image
from src.data.data_extract import (
    ImageDataExtractor,
    DIV2K_TRAIN,
    DIV2K_VALID,
    FLICKR2K
)

BASE_URL = "https://1drv.ms/f/c/4a433beb13092d5e/El4tCRPrO0MggEo9XQAAAAABVMTS8lLqv5YfVBIpYW0fDA"

@pytest.fixture
def extractor():
    """Fixture que fornece uma instância do ImageDataExtractor."""
    return ImageDataExtractor(BASE_URL)

@pytest.mark.parametrize("dataset_config,start_index", [
    (DIV2K_TRAIN, 1),
    (DIV2K_VALID, 800),
    (FLICKR2K, 1)
])

def test_single_image_download(extractor, dataset_config, start_index):
    """Testa o download de uma única imagem de cada dataset."""
    image, temp_path = extractor.get_image(dataset_config, start_index)
    
    try:
        # Verifica se a imagem foi carregada corretamente
        assert isinstance(image, Image.Image), "A imagem não é uma instância válida de PIL.Image"
        assert image.size[0] > 0 and image.size[1] > 0, "A imagem tem dimensões inválidas"
        
    finally:
        # Limpa o arquivo temporário
        extractor.cleanup_temp_file(temp_path)

@pytest.mark.parametrize("dataset_config,start_index,num_images", [
    (DIV2K_TRAIN, 1, 5),
    (DIV2K_VALID, 800, 5),
    (FLICKR2K, 1, 5)
])

def test_multiple_images_iterator(extractor, dataset_config, start_index, num_images):
    """Testa o download de múltiplas imagens usando o iterador do dataset."""
    temp_files = []
    count = 0
    
    try:
        for idx, (image_number, image, temp_path) in enumerate(extractor.iterate_dataset(dataset_config)):
            if idx >= num_images:
                break
                
            assert isinstance(image, Image.Image), f"A imagem {image_number} não é uma instância válida de PIL.Image"
            assert image.size[0] > 0 and image.size[1] > 0, f"A imagem {image_number} tem dimensões inválidas"
            temp_files.append(temp_path)
            count += 1
            
        assert count == num_images, f"Esperava {num_images} imagens, mas obteve {count}"
        
    finally:
        # Limpa todos os arquivos temporários
        for temp_path in temp_files:
            extractor.cleanup_temp_file(temp_path)

def test_invalid_image_number(extractor):
    """Testa o comportamento com números de imagem inválidos."""
    with pytest.raises(ValueError):
        extractor.get_image(DIV2K_TRAIN, 0)  # Índice menor que o início