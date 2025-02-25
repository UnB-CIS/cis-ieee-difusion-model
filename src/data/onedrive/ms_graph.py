import os
import webbrowser
import msal
from dotenv import load_dotenv

MS_GRAPH_BASE_URL = 'https://graph.microsoft.com/v1.0'

def get_access_token(client_id, client_secret, scopes):
    """
    Acquire token via MSAL
    """
    authority_url = 'https://login.microsoftonline.com/common'

    client = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority_url
    )

    auth_request_url = client.get_authorization_request_url(scopes)
    firefox = webbrowser.get('firefox')
    firefox.open(auth_request_url)
    authorization_code = input("Enter the authorization code: ")

    token_response = client.acquire_token_by_authorization_code(
        authorization_code,
        scopes=scopes
    )
    
    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        return Exception("Failed to acquire token:  " + str(token_response))
    

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