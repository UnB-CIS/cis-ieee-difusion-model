# Documentação do Módulo de Transformação de Dados

## Classe DataTransformer

### Inicialização

A classe `DataTransformer` é inicializada com os seguintes parâmetros:

- `img_size`: Tamanho da imagem para redimensionamento (int)
- `resize_method`: Método de redimensionamento (default: tf.image.ResizeMethod.BILINEAR). Opções disponíveis:
  - `BILINEAR`: Interpolação bilinear - melhor para redução de tamanho
  - `NEAREST_NEIGHBOR`: Vizinho mais próximo - mais rápido, mas menor qualidade
  - `BICUBIC`: Interpolação bicúbica - melhor qualidade, mais lento
  - `AREA`: Baseado em área - bom para downscaling

### Métodos

#### `resize_image(image)`
Redimensiona a imagem para o tamanho especificado durante a inicialização.
- **Retorno**: Imagem redimensionada como tensor TensorFlow

#### `load_and_preprocess_image(image, label)`
Carrega e pré-processa a imagem, redimensionando-a e normalizando os valores dos pixels.
- **Retorno**: Tupla (imagem_processada, label)

#### `split_dataset(dataset, train_split, val_split)`
Divide o conjunto de dados em conjuntos de treinamento e validação.
- **Parâmetros**:
  - `dataset`: Dataset TensorFlow a ser dividido
  - `train_split`: Proporção para conjunto de treino (float entre 0 e 1)
  - `val_split`: Proporção para conjunto de validação (float entre 0 e 1)
- **Retorno**: Tupla (train_dataset, val_dataset)

#### `prepare_dataset(dataset, batch_size, train_split, val_split)`
Prepara o conjunto de dados, aplicando pré-processamento e dividindo em treino e validação.
- **Parâmetros**:
  - `dataset`: Dataset a ser preparado
  - `batch_size`: Tamanho do lote para treinamento
  - `train_split`: Proporção para conjunto de treino
  - `val_split`: Proporção para conjunto de validação
- **Retorno**: Tupla (train_dataset, val_dataset)

### Exemplo de Uso