# CIS - IEEE Difusion Model

## Tecnologias Utilizadas

- [Docker](hhttps://www.docker.com/)
- [Tensforflow](https://www.tensorflow.org/)

## Pré-Requisitos

- Ter o docker instalado
- Ajustar direção do volume no arquivo `docker-compose.yml` para o diretório onde se encontra o modelo de difusão

## Estrutura do projeto (draft)

```bash
├── src
│   └── main-cpu.py # Script principal para execução do modelo de difusão (para o tensor flow rodar em CPU)
├── docs
│   ├── bib.md # Referências bibliográficas
│   └── main-cpu.md  # Documentação do script main-cpu.py
```

## Como rodar o projeto

```bash
docker-compose up
```

## Branchs principais

### Dev

Branch de ambiente de desenvolvimento da equipe. 

Toda nova funcionalidade ou correção deve primeiro ser implementada na branch `dev`.

### Main

Branch principal do repositório e representa o ambiente de produção do projeto.

## Boas Práticas de GitHub

### Novas branchs

Procure criar branchs a partir da versão dev, caso vá desenvolver alguma alteração visual ou funcional do software.

### Nomenclatura de novas branchs

Ao criar a nova branch, procure trazer significado a ela desde a sua nomeação, e aqui seguem algumas boas práticas:

#### Prefixo

Coloque um prefixo na branch, a fim de esclarecer sua intenção. Alguns exemplos abaixo:

- `feat/`: implementação de uma nova funcionalidade do software;
- `fix/`: implementação de uma correção no software;
- `docs/`: documentação de parte ou trecho do software;
- `refactor/`: refatoração de parte ou trecho do software.

#### Nome

Após o prefixo, coloque um nome declarativo ou explicativo do objetivo da branch, ou seja, um nome que diga
o que será implementado na branch. Procure escrever na convenção "kebab-case".

#### Sufixo

Após o nome, adicione um sufixo numérico, explicitando qual a issue do projeto a que se refere a nova branch.

#### Exemplo

- `feat/data-fetching-23`
- `fix/tensorflow-implementation-12`
- `refactor/extract-component-5`

### Novas issues no Project

É necessário tomar algumas atenções quanto às issues do GitHub.

#### Integração Contínua

Focando-se na boa prática de integração contínua, faz-se necessário particionar pendências e novas funcionalidades
o máximo possível, enquanto houver sentido, afim de se criar issues com menores responsabilidades, promovendo
branchs menores, PRs menores, merges mais frequentes e um código-fonte com atualizações constantes.

