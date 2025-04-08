# Microsoft Graph API - OneDrive Integration

Este módulo permite a integração com a API do Microsoft Graph para acessar arquivos no OneDrive.

## Métodos de Autenticação

### Autenticação Interativa

A autenticação interativa requer a interação do usuário através de um navegador web.

**Como funciona:**

1. O sistema gera uma URL de autorização
2. O navegador é aberto automaticamente (ou o usuário precisa copiar a URL)
3. O usuário faz login e autoriza o acesso
4. É gerado um código de autorização que o usuário deve informar no terminal
5. O sistema troca esse código por um token de acesso

**Requisitos:**

- CLIENT_ID (ID da aplicação no Azure AD)
- CLIENT_SECRET (Segredo do cliente da aplicação)
- Navegador web acessível
- Permissões delegadas configuradas no Azure AD (User.Read, Files.ReadWrite.All)

### Autenticação Não Interativa (Client Credentials)

A autenticação não interativa permite a execução automatizada sem intervenção do usuário.

**Como funciona:**

1. O sistema solicita um token diretamente usando as credenciais do cliente
2. Não há redirecionamento para navegador ou interação do usuário
3. O token é obtido através do fluxo de credenciais do cliente (client credentials flow)

**Requisitos:**

- CLIENT_ID (ID da aplicação no Azure AD)
- CLIENT_SECRET (Segredo do cliente da aplicação)
- TENANT_ID (ID do tenant do Azure AD)
- Permissões de aplicativo configuradas no Azure AD
- Licença SharePoint Online (SPO) ou Microsoft 365 E3/E5
- Certificado SharePoint configurado para aplicativos do SharePoint com permissões adequadas

## Configuração do Certificado SharePoint

Para que a autenticação não interativa funcione com acesso ao SharePoint/OneDrive:

1. É necessário configurar um certificado no Azure AD para a aplicação
2. O certificado deve ter permissões adequadas para acessar os recursos do SharePoint
3. A aplicação deve ser registrada com permissões adequadas no Azure AD
4. O tenant deve ter licenças SharePoint Online ativas

## Configuração de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
CLIENT_ID=seu-client-id
CLIENT_SECRET=seu-client-secret
TENANT_ID=seu-tenant-id
FOLDER_ID=id-da-pasta-onedrive (opcional)
```

## Execução

Para executar com autenticação interativa (padrão):

```bash
python onedrive_download_file.py
```

Para executar com autenticação não interativa:

```bash
python onedrive_download_file.py --noninteractive
```
