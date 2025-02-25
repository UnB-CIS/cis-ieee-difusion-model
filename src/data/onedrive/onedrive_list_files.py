import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL

def list_root_folder(headers):
    url = f'{MS_GRAPH_BASE_URL}/me/drive/root/children'
    response = httpx.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return [item for item in data['value']]
    else:
        print(f'Failed to list root folder: {response.status_code}')
        return []

def list_folder_children(headers, folder_id):
    url = f'{MS_GRAPH_BASE_URL}/me/drive/items/{folder_id}/children'
    response = httpx.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return [item for item in data['value']]
    else:
        print(f'Failed to list children of folder {folder_id}: {response.status_code}')
        return []

def list_root_folder_metadata(root_folder):
    for folder in root_folder:
        if 'folder' in folder:
            print(f'Folder id: {folder["id"]}')
            print(f'Folder name: {folder["name"]}')
            print(f'Folder web url: {folder["webUrl"]}')
            print(f'Folder size: {folder["size"]}')
            print(f'Folder created date: {folder["createdDateTime"]}')
            print(f'Created by: {folder["createdBy"]["user"]["displayName"]}')
            print(f'Folder modified date: {folder["lastModifiedDateTime"]}')
            print(f'Last modified by: {folder["lastModifiedBy"]["user"]["displayName"]}')
            print(f'Folder parent id: {folder["parentReference"]["id"]}')
            print(f'Item Count: {folder["folder"]["childCount"]}')
            print('-' * 50)
        elif 'file' in folder:
            print(f'File id: {folder["id"]}')
            print(f'File name: {folder["name"]}')
            print(f'File web url: {folder["webUrl"]}')
            print(f'File size (in KB): {folder["size"] / 1024:.2f}')
            print(f'File created date: {folder["createdDateTime"]}')
            print(f'Created by: {folder["createdBy"]["user"]["displayName"]}')
            print(f'File modified date: {folder["lastModifiedDateTime"]}')
            print(f'Last modified by: {folder["lastModifiedBy"]["user"]["displayName"]}')
            print(f'File parent id: {folder["parentReference"]["id"]}')
            print(f'File Mime type: {folder["file"]["mimeType"]}')
            print('-' * 50)

def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ['User.Read', 'Files.ReadWrite.All']
    
    try:
        access_token = get_access_token(
            client_id=APPLICATION_ID,
            client_secret=CLIENT_SECRET,
            scopes=SCOPES
        )
        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        root_folder = list_root_folder(headers)
        list_root_folder_metadata(root_folder)

        # folder_id = "7ADBC4F93D2ED730!21805"
        # list_children = list_folder_children(headers, folder_id)
        # for child in list_children:
        #     if 'folder' in child:
        #         print(f'Folder id: {child["id"]}')
        #         print(f'Folder name: {child["name"]}')
        #         print(f'Folder web url: {child["webUrl"]}')
        #         print(f'Folder size: {child["size"]}')
        #         print(f'Folder created date: {child["createdDateTime"]}')
        #         print(f'Created by: {child["createdBy"]["user"]["displayName"]}')
        #         print(f'Folder modified date: {child["lastModifiedDateTime"]}')
        #         print(f'Last modified by: {child["lastModifiedBy"]["user"]["displayName"]}')
        #         print(f'Folder parent id: {child["parentReference"]["id"]}')
        #         print(f'Item Count: {child["folder"]["childCount"]}')
        #         print('-' * 50)
        #     elif 'file' in child:
        #         print(f'File id: {child["id"]}')
        #         print(f'File name: {child["name"]}')
        #         print(f'File web url: {child["webUrl"]}')
        #         print(f'File size (in KB): {child["size"] / 1024:.2f}')
        #         print(f'File created date: {child["createdDateTime"]}')
        #         print(f'Created by: {child["createdBy"]["user"]["displayName"]}')
        #         print(f'File modified date: {child["lastModifiedDateTime"]}')
        #         print(f'Last modified by: {child["lastModifiedBy"]["user"]["displayName"]}')
        #         print(f'File parent id: {child["parentReference"]["id"]}')
        #         print(f'File Mime type: {child["file"]["mimeType"]}')
        #         print('-' * 50)
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()
