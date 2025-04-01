# Integração de Dados do OneDrive

Este módulo fornece ferramentas para interagir com o OneDrive através da API Microsoft Graph, permitindo listar, navegar e baixar arquivos de pastas específicas.

## Pré-requisitos

- Python 3.8+
- Conta Microsoft com OneDrive
- Registro de aplicativo no Microsoft Azure com as permissões adequadas
- Variáveis de ambiente configuradas corretamente

## Configuração do Ambiente

1. Crie um arquivo `.env` na raiz do projeto ou copie do `.env.example` e preencha:

```env
# Obrigatório para ambos os métodos
CLIENT_ID=seu_id_de_aplicativo
CLIENT_SECRET=seu_segredo_de_cliente
FOLDER_ID=id_da_pasta_onedrive

# Obrigatório apenas para autenticação não interativa
TENANT_ID=seu_id_de_inquilino
```

## Métodos de Autenticação

A integração suporta dois métodos de autenticação:

### 1. Autenticação Interativa (Padrão)

```bash
python src/data/onedrive/onedrive_download_file.py
```

- **Compável com**: Contas Microsoft pessoais (Hotmail, Outlook.com) e contas corporativas (Microsoft 365)
- **Requer**: Interação manual do usuário para autorização no navegador
- **Ideal para**: Desenvolvimento, testes e uso pessoal
- **Processo**:
  1. O script abre uma URL no navegador
  2. Você faz login na conta Microsoft
  3. Você autoriza o aplicativo
  4. Você recebe um código que deve ser digitado no terminal

### 2. Autenticação Não Interativa (Client Credentials)

```bash
python src/data/onedrive/onedrive_download_file.py --noninteractive
```

- **Compatível com**: APENAS contas corporativas Microsoft 365/SharePoint (não funciona com contas pessoais)
- **Requer**: Assinatura Microsoft 365 Business/Enterprise (não é gratuito)
- **Ideal para**: Automação, ambientes headless, containers Docker
- **Configuração adicional**:
  1. O aplicativo no Azure Portal deve ter permissões de aplicativo (não delegadas)
  2. Um administrador do tenant deve conceder consentimento para essas permissões
  3. O TENANT_ID deve estar configurado no arquivo .env

## Scripts e Funções

### 1. Listando Arquivos do OneDrive

```bash
python src/data/onedrive/onedrive_list_files.py        # Modo interativo (padrão)
python src/data/onedrive/onedrive_list_files.py --noninteractive  # Modo não interativo
```

Este script exibe:

- Conteúdo da pasta raiz do OneDrive
- Detalhes de arquivos e pastas (ID, nome, tamanho, data de criação, etc.)

### 2. Baixando Arquivos

```bash
python src/data/onedrive/onedrive_download_file.py        # Modo interativo (padrão)
python src/data/onedrive/onedrive_download_file.py --noninteractive  # Modo não interativo
```

Este script:

- Obtém uma lista de arquivos da pasta especificada (`FOLDER_ID` no .env)
- Baixa cada arquivo para a pasta especificada (padrão: 'src/data/onedrive_dataset')
- Exibe o progresso conforme os arquivos são baixados

## IDs de Pasta

Ao usar esses scripts, você pode precisar especificar IDs de pasta:

- No código, use o formato: `7ADBC4F93D2ED730!21805`
- Em URLs, use o formato codificado: `7ADBC4F93D2ED730%2121805` (onde `!` é codificado como `%21`)

## Personalização

Para acessar uma pasta diferente do OneDrive:

1. Execute `onedrive_list_files.py` para ver todas as pastas disponíveis e seus IDs
2. Altere o valor de `FOLDER_ID` em `onedrive_download_file.py` para o ID da pasta desejada

## Solução de Problemas

- Se a autenticação falhar, verifique se suas variáveis de ambiente estão configuradas corretamente
- Verifique se o registro do seu aplicativo Azure tem as permissões necessárias (Files.ReadWrite.All)
- Para tokens expirados, simplesmente execute o script novamente para obter um novo token

## Exemplos de Uso

### Fluxo Interativo (para contas pessoais)

1. Execute: `python src/data/onedrive/onedrive_list_files.py`
2. Uma janela do navegador abrirá automaticamente (ou uma URL será exibida)
3. Faça login em sua conta Microsoft e autorize o aplicativo
4. Copie o código de autorização e cole no terminal
5. Veja a lista de arquivos e pastas com seus IDs
6. Para baixar arquivos: `python src/data/onedrive/onedrive_download_file.py`

### Fluxo Não Interativo (para contas corporativas)

1. Configure o arquivo .env com TENANT_ID e FOLDER_ID corretos
2. Registre seu aplicativo com permissões de aplicativo Files.Read.All e obtenha consentimento de administrador
3. Execute: `python src/data/onedrive/onedrive_download_file.py --noninteractive`
4. Os arquivos serão baixados automaticamente sem solicitar interação
