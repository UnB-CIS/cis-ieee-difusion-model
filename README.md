# SR3: Super Resolution via Diffusion Model

Este projeto implementa um modelo de super resolução de imagens baseado em difusão, inspirado no artigo [Image Super-Resolution via Iterative Refinement](https://arxiv.org/abs/2104.07636).

## Estrutura do Projeto

```
src/
├── data/
│   └── dataset.py      # Gerenciamento e pré-processamento de dados
├── models/
│   ├── diffusion.py    # Processo de difusão
│   └── unet.py         # Arquitetura U-NET
├── utils/
│   └── visualization.py # Funções de visualização
└── train.py            # Script principal de treinamento
```

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

2. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/cis-ieee-difusion-model.git
cd cis-ieee-difusion-model
```

3. Instale as dependências:
```bash
poetry install
```

4. Ative o ambiente virtual:
```bash
poetry shell
```

### Opção 2: Usando pip

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/cis-ieee-difusion-model.git
cd cis-ieee-difusion-model
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Preparação dos Dados

1. Estruture seus dados no diretório `data/`:
```
data/
└── imagens/
    ├── pessoa1/
    │   ├── foto1.jpg
    │   └── foto2.jpg
    └── pessoa2/
        ├── foto1.jpg
        └── foto2.jpg
```

2. Requisitos das imagens:
   - Formato: JPG ou PNG
   - Resolução mínima: 128x128 pixels
   - Recomendado: imagens faciais bem iluminadas e centralizadas

### Treinamento do Modelo

1. Treinamento básico:
```bash
python src/train.py
```

2. Com parâmetros personalizados:
```bash
python src/train.py --data_dir data/imagens --epochs 100 --batch_size 16 --save_dir resultados
```

3. Parâmetros disponíveis:
   - `--data_dir`: Diretório com as imagens de treino (default: data/)
   - `--epochs`: Número de épocas de treinamento (default: 100)
   - `--batch_size`: Tamanho do batch (default: 16)
   - `--learning_rate`: Taxa de aprendizado (default: 0.0008)
   - `--max_images`: Limite de imagens para treino (opcional)
   - `--save_dir`: Diretório para salvar resultados (default: resultados/)

### Visualização dos Resultados

1. Durante o treinamento:
   - Curvas de perda são salvas em `resultados/curva_perda.png`
   - Checkpoints do modelo em `resultados/checkpoints/`

2. Após o treinamento:
   - Modelo final salvo em `resultados/modelo_final.h5`
   - Exemplos de super resolução em `resultados/exemplos/`

### Inferência

1. Para super resolução de uma única imagem:
```bash
python src/inference.py --input imagem.jpg --output resultado.png
```

2. Para processar um diretório:
```bash
python src/inference.py --input_dir pasta_imagens/ --output_dir resultados/
```

## Desenvolvimento

O projeto usa várias ferramentas de desenvolvimento:

- **Black**: Formatação de código
  ```bash
  poetry run black .
  ```

- **isort**: Ordenação de imports
  ```bash
  poetry run isort .
  ```

- **mypy**: Checagem de tipos
  ```bash
  poetry run mypy src/
  ```

- **pylint**: Análise estática
  ```bash
  poetry run pylint src/
  ```

Para executar todas as verificações de uma vez:
```bash
poetry run pre-commit run --all-files
```

## Testes

1. Executar todos os testes:
```bash
poetry run pytest
```

2. Apenas testes unitários:
```bash
poetry run pytest -m "unit"
```

3. Apenas testes de integração:
```bash
poetry run pytest -m "integration"
```

4. Com cobertura de código:
```bash
poetry run pytest --cov=src tests/
```

## Solução de Problemas

### Erros Comuns

1. **Memória GPU insuficiente**:
   - Reduza o batch_size
   - Diminua a resolução das imagens
   - Use mixed precision training

2. **Imagens não carregam**:
   - Verifique o formato das imagens
   - Confirme as permissões dos arquivos
   - Valide a estrutura do diretório

3. **Treinamento instável**:
   - Ajuste a taxa de aprendizado
   - Aumente o número de épocas
   - Verifique a qualidade dos dados

### Otimização de Performance

1. **GPU**:
   - Use CUDA para aceleração
   - Monitore o uso de memória
   - Ajuste os parâmetros de batch

2. **Dados**:
   - Use TFRecords para I/O eficiente
   - Implemente data augmentation
   - Cache os dados em memória

3. **Modelo**:
   - Ative a compilação XLA
   - Use mixed precision quando possível
   - Otimize o pipeline de dados

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Citação

Se você usar este código em sua pesquisa, por favor cite:

```bibtex
@article{sr3_2021,
  title={Image Super-Resolution via Iterative Refinement},
  author={Saharia, Chitwan and Ho, Jonathan and Chan, William and Sumer, Tim and Fleet, David and Norouzi, Mohammad},
  journal={arXiv preprint arXiv:2104.07636},
  year={2021}
}
