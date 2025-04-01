import os
import webbrowser
import msal
from dotenv import load_dotenv

MS_GRAPH_BASE_URL = 'https://graph.microsoft.com/v1.0'

def get_access_token_interactive(client_id, client_secret, scopes):
    """
    Adquire token via MSAL usando fluxo de código de autorização (interativo).
    """
    authority_url = 'https://login.microsoftonline.com/common'

    client = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority_url
    )

    auth_request_url = client.get_authorization_request_url(scopes)
    try:
        firefox = webbrowser.get('firefox')
        firefox.open(auth_request_url)
    except webbrowser.Error:
        print(f"Abra o seguinte URL no seu navegador para autorizar o aplicativo:\n{auth_request_url}")
        
    authorization_code = input("Entre com o código de autorização: ")

    token_response = client.acquire_token_by_authorization_code(
        authorization_code,
        scopes=scopes
    )
    
    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        raise Exception("Falha ao adquirir token:  " + str(token_response))
        
def get_access_token_client_credentials(client_id, client_secret, tenant_id, scopes=None):
    """
    Adquire token via MSAL usando fluxo de credenciais de cliente (não interativo).
    """
    if scopes is None:
        # Para client credentials, precisa usar o escopo .default
        scopes = ['https://graph.microsoft.com/.default']
        
    # Para client credentials, a autoridade deve ser específica do tenant
    authority_url = f'https://login.microsoftonline.com/{tenant_id}'

    client = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority_url
    )

    # Adquire token diretamente com as credenciais do cliente
    token_response = client.acquire_token_for_client(scopes=scopes)
    
    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        raise Exception("Falha ao adquirir token:  " + str(token_response))

def get_access_token(client_id, client_secret, scopes=None, tenant_id=None, interactive=True):
    """
    Função unificada para obter token de acesso, permitindo escolher entre métodos interativos e não interativos.
    """
    if interactive:
        if scopes is None:
            scopes = ['User.Read', 'Files.ReadWrite.All']
        return get_access_token_interactive(client_id, client_secret, scopes)
    else:
        if tenant_id is None:
            raise ValueError("O tenant_id é obrigatório para autenticação não interativa")
        return get_access_token_client_credentials(client_id, client_secret, tenant_id, scopes)
    

def main():
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ['https://graph.microsoft.com/.default']

    try:
        access_token = get_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,scopes=SCOPES)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        print(headers)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()