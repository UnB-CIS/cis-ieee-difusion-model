# SR3: Super Resolution via Diffusion Model

Este projeto implementa um modelo de super resolução de imagens baseado em difusão, inspirado no artigo [Image Super-Resolution via Iterative Refinement](https://arxiv.org/abs/2104.07636).

## Requisitos

- Python 3.8 ou superior
- Poetry (gerenciador de dependências)
- GPU com suporte a CUDA (recomendado)

## Instalação

Você pode escolher entre duas opções de instalação:

### Opção 1: Usando Poetry (Recomendado)

1. Instale o Poetry (se ainda não tiver):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2.Clone o repositório:

```bash
git clone https://github.com/seu-usuario/cis-ieee-difusion-model.git
cd cis-ieee-difusion-model
```

3.Instale as dependências:

```bash
poetry install
```

4.Ative o ambiente virtual:

```bash
poetry shell
```

### Opção 2: Usando pip

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/cis-ieee-difusion-model.git
cd cis-ieee-difusion-model
```

2.Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3.Instale as dependências:

```bash
pip install -r requirements.txt
```
