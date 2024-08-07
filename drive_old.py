from __future__ import print_function
import httplib2
import os
import platform

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import HttpAccessTokenRefreshError

import io
from googleapiclient.http import MediaIoBaseDownload

from datetime import datetime
import re
import unicodedata
from util import resource_path
import shutil
from error import *

CREDENTIAL_DIR = resource_path('./googlefile')
CREDENTIAL_FILENAME = 'drive-python-download.json'

CLIENT_SECRET_FILE = resource_path('./googlefile/client_secret.json')
APPLICATION_NAME = 'Google Drive File Export Example'

SCOPES = 'https://www.googleapis.com/auth/drive.readonly'


def get_credentials():
    credential_dir = CREDENTIAL_DIR
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, CREDENTIAL_FILENAME)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def find_file_id_by_name(service, folder_id, file_name):
    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print('No files found in the folder.')
        return None

    for file in files:
        if file['name'] == file_name:
            return file['id']

    print(f'File "{file_name}" not found in the folder.')
    return None

def find_folder_id_by_name(service, parent_folder_id, folder_name):
    results = service.files().list(q=f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'", fields="files(id, name)").execute()
    folders = results.get('files', [])

    if not folders:
        print('No folders found in the parent folder.')
        return None

    for folder in folders:
        if folder['name'] == folder_name:
            return folder['id']

    print(f'Folder "{folder_name}" not found in the parent folder.')
    return None


def download_file(service, file_id, file_name, save_directory=None, save_as_name=None):
    request = service.files().get_media(fileId=file_id)

    # 수정된 부분: 저장 디렉토리와 파일명이 주어진 경우 사용
    save_directory = save_directory or '.'  # 기본값은 현재 디렉토리로 설정
    save_as_name = save_as_name or file_name

    # 저장 경로 생성
    save_path = os.path.join(save_directory, save_as_name)

    fh = io.FileIO(save_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print('Download %d%%.' % int(status.progress() * 100))

def download(file_name, TO_NAME=None, save_directory=None, FOLDER_ID='root'):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # 수정된 부분: 파일명으로 파일 ID 찾기
    file_id = find_file_id_by_name(service, FOLDER_ID, file_name)

    if file_id:
        print(f'File ID for "{file_name}": {file_id}')
        # 파일 다운로드, 저장 디렉토리와 파일명이 주어지면 그렇지 않으면 다운로드된 파일명 그대로 사용
        download_file(service, file_id, file_name, save_directory=save_directory, save_as_name=TO_NAME)

# 예시: "jinha.txt" 파일을 다운로드하고 특정 디렉토리에 저장
# download("jinha.txt", TO_NAME='aa.txt', save_directory='/path/to/your/directory')

def getStockxl(save_directory):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # 파일명 패턴 정의
    file_pattern = re.compile(r'^재고관리표M\((\d{6})\)RT\.xlsm$')

    # 모든 파일 목록 가져오기
    results = service.files().list().execute()
    files = results.get('files', [])

    # 매칭되는 파일 목록 출력
    matching_files = []

    for file_info in files:
        file_name = file_info['name']
        match = file_pattern.match(file_name)

        if match:
            matching_files.append(file_name)

    if matching_files:
        print('Matching Files:')
        for matching_file in matching_files:
            print(matching_file)
        
        # 최신 파일 정보 초기화
        latest_file_info = None

        for file_info in files:
            file_name = file_info['name']
            if file_name in matching_files:
                # 파일명에서 날짜 추출
                date_str = re.match(r'^재고관리표M\((\d{6})\)RT\.xlsm$', file_name).group(1)
                date_format = "%y%m%d"
                file_date = datetime.strptime(date_str, date_format)

                # 최신 파일인지 확인
                if not latest_file_info or file_date > latest_file_info['date']:
                    latest_file_info = {'name': file_name, 'date': file_date, 'id': file_info['id']}

        if latest_file_info:
            print(f'\nLatest Stock File: "{latest_file_info["name"]}", Date: {latest_file_info["date"]}')
            download_file(service, latest_file_info['id'], latest_file_info['name'], save_directory=resource_path(save_directory), save_as_name="DB.xlsm")
        else:
            print('\nNo matching files found.')
    else:
        print('No matching files found.')

# 예시: 특정 디렉토리에 최신 Stock 파일 다운로드
# getStockxl('/path/to/your/directory')
        

def get_latest_named_folder_id(service, parent_folder_id):
    results = service.files().list(
        q=f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)",
        orderBy="name desc"
    ).execute()

    folders = results.get('files', [])

    if not folders:
        print('No folders found in the parent folder.')
        return None

    latest_named_folder = folders[0]['id']  # 가장 최신 폴더의 ID로 초기화
    latest_name = folders[0]['name']

    for folder in folders[1:]:
        if folder['name'] > latest_name:
            latest_name = folder['name']
            latest_named_folder = folder['id']

    return latest_named_folder, latest_name

def JsonKeyDrive2Temp(directory):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # 'GoogleDriveKeys' 폴더의 ID를 찾기
    drive_keys_folder_id = find_folder_id_by_name(service, 'root', 'GoogleDriveKeys')

    if drive_keys_folder_id:
        # 최신 폴더명으로 폴더 선택
        latest_named_folder = get_latest_named_folder_id(service, drive_keys_folder_id)
        latest_named_folder_name = latest_named_folder[1]
        latest_named_folder_id = latest_named_folder[0]

        if latest_named_folder_id:
            # 'drive-python-download.json' 파일 ID 찾기
            json_file_id = find_file_id_by_name(service, latest_named_folder_id, 'drive-python-download.json')

            if json_file_id:
                # 파일 다운로드
                download_file(service, json_file_id, 'drive-python-download.json', save_directory=directory)
                print(f'Updated drive-python-download.json by version {latest_named_folder_name}')
            else:
                print('No "drive-python-download.json" file found in the latest named folder.')
        else:
            print('No folder found in "GoogleDriveKeys" folder.')
    else:
        print('No "GoogleDriveKeys" folder found in the root directory.')


def JsonKeyAppdata2Temp():
    # AppData 경로 설정
    if os.name == "nt":  # Windows
        appdata_path = os.path.join(os.path.expandvars("%APPDATA%"), "Local", "PHOretail")
    elif os.name == "posix":  # Mac
        appdata_path = os.path.join(os.path.expanduser("~/Library/Application Support"), "PHOretail")
    else:
        print("Unsupported operating system.")
        return

    # PHOretail 폴더 생성 (없을 경우)
    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)
        print("Made PHOretail folder in appdata")

    # JSON 파일 경로 설정
    json_file_path = os.path.join(appdata_path, "drive-python-download.json")

    # Temp 폴더 경로 설정
    temp_folder_path = resource_path("googlefile")

    # JSON 파일 존재 여부 확인
    if os.path.exists(json_file_path):
        # JSON 파일을 Temp 폴더로 복사
        shutil.copy(json_file_path, temp_folder_path)
        print(f"drive-python-download.json copied to: {temp_folder_path}")
    else:
        print("There is no drive-python-download.json in appdata.")

def JsonKeyTemp2Appdata():
    # AppData 경로 설정
    if os.name == "nt":  # Windows
        appdata_path = os.path.join(os.path.expandvars("%APPDATA%"), "Local", "PHOretail")
    elif os.name == "posix":  # Mac
        appdata_path = os.path.join(os.path.expanduser("~/Library/Application Support"), "PHOretail")
    else:
        print("Unsupported operating system.")
        return

    # PHOretail 폴더 생성 (없을 경우)
    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)
        print("Made PHOretail folder in appdata")

    # JSON 파일 경로 설정
    json_file_path = os.path.join(resource_path("googlefile"), "drive-python-download.json")

    # JSON 파일 존재 여부 확인
    if os.path.exists(json_file_path):
        # JSON 파일을 Temp 폴더로 복사
        shutil.copy(json_file_path, appdata_path)
        print(f"drive-python-download.json copied to: {appdata_path}")
    else:
        print("There is no drive-python-download.json in temp.")

def JsonKeySync():
    try:
        JsonKeyDrive2Temp(resource_path("googlefile"))
        JsonKeyTemp2Appdata()
    except HttpAccessTokenRefreshError as e:
        try:
            print(f"임시 토큰 만료. 업데이트를 진행합니다.: {e}")
            JsonKeyAppdata2Temp()
            JsonKeyDrive2Temp(resource_path("googlefile"))
            JsonKeyTemp2Appdata()

        except HttpAccessTokenRefreshError as e:
            raise TokenExpireError