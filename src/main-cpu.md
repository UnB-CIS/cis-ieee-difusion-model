# Possivel plano de ação

## 1. Preparação de Dados (Pipeline)
- Carregar e pré-processar a base de dados: funções para carregar, redimensionar e normalizar as imagens. Isso inclui a criação de um *pipeline de dados que possa lidar com a divisão em treinamento, validação.

## 2. Augmentação de dados:
- Adicionar transformações como rotação, corte e redimensionamento para melhorar a robustez do modelo.

- Construção de pares de imagens de baixa e alta resolução: Crie uma função para degradar imagens de alta resolução, gerando pares que servirão para o treinamento do modelo de *super-resolução.

...