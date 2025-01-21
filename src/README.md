# Implementação do SR3 - Super Resolution via Diffusion Model

## Visão Geral

O SR3 (Super Resolution via Diffusion Model) é um modelo generativo especializado em super resolução de imagens. Este documento explica a implementação e os componentes principais do sistema.

## Estrutura do pasta src

``` bash
src/
├── data/
│   └── dataset.py       # Manipulação e carregamento de dados
├── models/
│   ├── unet.py         # Implementação da arquitetura U-NET
│   └── diffusion.py    # Lógica do processo de difusão
├── utils/
│   └── visualization.py # Funções de visualização
└── train.py            # Script principal de treinamento
```

## Componentes Principais

### 1. Processo de Difusão (`diffusion.py`)

- **Adição de Ruído**: Implementa o processo forward de adição de ruído Gaussiano
- **Escalonamento Beta**: Usa um cronograma linear de beta de 0.0001 a 0.02
- **Parâmetros Alpha**: Calcula os parâmetros alpha e alpha_bar necessários para o processo

### 2. Arquitetura U-NET (`unet.py`)

- **Bloco Base**: Implementa blocos convolucionais com:
  - Camadas convolucionais 2D
  - Normalização em lote
  - Ativação ReLU
  - Condicionamento temporal
- **Estrutura**:
  - Caminho descendente (codificador)
  - Ponte MLP
  - Caminho ascendente (decodificador)
  - Skip connections

### 3. Manipulação de Dados (`dataset.py`)

- Carregamento de imagens de alta resolução (HR)
- Geração de imagens de baixa resolução (LR)
- Upsampling bicúbico das imagens LR
- Normalização e pré-processamento

### 4. Visualização (`visualization.py`)

- Funções para plotagem de:
  - Processo de difusão
  - Resultados de super resolução
  - Comparações entre HR, LR e SR

## Detalhes de Implementação

### Processo de Treinamento

1. **Preparação dos Dados**:
   - Imagens HR (128x128)
   - Downscale para LR (32x32)
   - Upscale bicúbico para 128x128

2. **Adição de Ruído**:
   - 1000 passos de tempo
   - Ruído Gaussiano progressivo
   - Concatenação com imagem LR upscaled

3. **Treinamento do Modelo**:
   - Otimizador Adam (lr=0.0008)
   - Loss MSE
   - Checkpoints em intervalos estratégicos

### Inferência

1. Amostragem de ruído aleatório
2. Processo iterativo de denoising
3. Utilização de DDIM para amostragem eficiente

## Melhorias Possíveis

1. **Arquitetura**:
   - U-NET mais profunda
   - Mais parâmetros
   - Transformers para condicionamento temporal

2. **Dados**:
   - Treinamento com mais imagens
   - Augmentação de dados
   - Diferentes escalas de resolução

3. **Otimizações**:
   - Classifier-free guidance
   - Técnicas de amostragem mais eficientes
   - Fine-tuning adaptativo
