from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import io
from googleapiclient.http import MediaIoBaseDownload

from datetime import datetime
import re
import unicodedata
from util import resource_path

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

def normalize_filename(filename):
    return ''.join(c for c in unicodedata.normalize('NFD', filename) if unicodedata.category(c) != 'Mn')

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
        #file_name = normalize_filename(file_name)
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