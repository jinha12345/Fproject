import os
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import threading

def getImage(model, image_path):
    time.sleep(10)
    URL_init = 'https://lsco.scene7.com/is/image/lsco/'
    if len(model) != 10 or model[5] != '-':
        return 0
    URL_model = model[:5] + model[6:]
    URL_first = ['-back', '-front', '-side', '-detail', '-dynamic1', '-alt1', '-detail1', '-alt2', '-alt3', '-alt4']
    URL_second = ['-pdp']
    URL_third = ['-lse', '-ld', '']

    URL_remainders = ['-front-gstk']

    URL_command = '?resMode=bisharp&fit=crop&wid=1000'

    URLs = []
    for i in URL_first:
        for j in URL_second:
            for k in URL_third:
                URLs.append(URL_init + URL_model + i + j + k + URL_command)
    for i in URL_remainders:
        URLs.append(URL_init + URL_model + i + URL_command)

    start_time = time.time()
    # ThreadPoolExecutor를 사용하여 다중 스레딩으로 이미지 다운로드
    successful_downloads = download_images_parallel(URLs, image_path)

    # 종료 시간 기록 및 소요된 시간 출력
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"전체 실행 시간: {elapsed_time:.2f} 초")

    return successful_downloads

def download_image(url, folder_path, lock):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with lock:
                file_name = os.path.join(folder_path, f"{download_image.successful_downloads + 1}.jpg")
                download_image.successful_downloads += 1
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
            print(f"이미지 다운로드 완료: {file_name}")
            return True
        #else:
            #print(f"이미지 다운로드 실패. HTTP 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"에러 발생: {e}")
    return False

def download_images_parallel(urls, folder_path, num_threads=32):
    try:
        # 폴더가 없다면 생성
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 폴더 내 이미지 파일 제거
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        download_image.successful_downloads = 0  # 초기화
        lock = threading.Lock()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # download_image 함수를 사용하여 다중 스레딩으로 이미지 다운로드
            results = list(executor.map(download_image, urls, [folder_path] * len(urls), [lock] * len(urls)))

        successful_downloads = sum(results)

        return successful_downloads

    except Exception as e:
        print(f"에러 발생: {e}")
        return 0

# getImage 함수 호출
# print(getImage('18883-0107', 'image22s'))
