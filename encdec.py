import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


def encrypt_file_to_string(file_path: str, key_str: str) -> str:
    # 문자열 키를 바이트로 변환하고 길이를 32바이트로 맞춤
    key = key_str.encode('utf-8').ljust(32)[:32]
    
    # Initialization Vector (IV) 생성
    iv = os.urandom(16)
    
    # 파일 읽기
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # AES 패딩 추가
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()
    
    # AES 암호화 설정
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # 데이터 암호화
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # IV와 암호화된 데이터를 base64로 인코딩
    encrypted_string = base64.b64encode(iv + encrypted_data).decode('utf-8')
    return encrypted_string



def decrypt_string_to_file(encrypted_string: str, key_str: str, output_file_path: str):
    # 문자열 키를 바이트로 변환하고 길이를 32바이트로 맞춤
    key = key_str.encode('utf-8').ljust(32)[:32]
    
    # base64로 인코딩된 데이터를 디코딩
    encrypted_data = base64.b64decode(encrypted_string)
    
    # Initialization Vector (IV)와 암호화된 데이터 분리
    iv = encrypted_data[:16]
    encrypted_file_data = encrypted_data[16:]
    
    # AES 복호화 설정
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # 데이터 복호화
    padded_data = decryptor.update(encrypted_file_data) + decryptor.finalize()
    
    # AES 패딩 제거
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    file_data = unpadder.update(padded_data) + unpadder.finalize()
    
    # 복호화된 데이터를 파일에 저장
    with open(output_file_path, 'wb') as f:
        f.write(file_data)

# 키 문자열
# key_str = "Wlsend99Js##"

# 파일 암호화
# encrypted_string = encrypt_file_to_string('drive-python-download_old.json', key_str)
# print(encrypted_string)
# encrypted_string = 'AUKCLpF1CYXnBzuuo59O55dO/+VhFkRKgVja2KKKF65PQ3HHR+XAK1lReup3Vjb3Nbb6vw49jNDOf27GpSbVv4xEE5ApndNUC3/TZlBRVyFFxAXnUEOJxbhklvRm/M4zPGaRtqiWQfWA2f/tXWT5nwppt9isPS/uyt81SQ1fCyYtufzxPHy2N/bkw8hMNqtFAsekGW5UekRDPTlDVHdt0eIuOOmImF92PMba7T+jQWWuKthzAD3mmVEqgR0fpJ+71GJroQ2ZW6p1tA/2Os3+ANE34eaqYzyQXxmXlSxKtgIXsaAMcNjkHGEizr66MRmxYNfeQ4syENS8HJ9vU1J2WjfzerVjSc85aag22D86dPExdu2V4P5N6d6GOkyltCGhwZFnye2RvguRY+ibP5bzIE+0zh8Mzm9SMiuEa9IcD8seQJfztmEiSZuj4ME7Pg3/YN9ab9KLMWI7RArbd/IpO1O77DgV4s5e9Ey52vO6UTWgVRKGgAAyGIvv83txI/BcQjDXi9Woa4t6bKeHcOAJJHGyGGDF77X3M6Jbpr/Z0sZhQ72mjTI/Z5qaISQo2k2MofiFrbDMaQqXZjg994xRAzc1QpDUk/CNLNl3F/i+D36W0v1M325PkKjoj0pSrglqR8cCH6FEOCjxK+MA1FqkCu+TvYFwZjIaF4GRD2eE0K452qgCStVaOLly8ln4vfRxpnn0ky6S3sMdLtUnRkaDmaAXUU1hjrCW7dd4xpoEcndxvaxK8htmk0BRrR+P4c9GvNXgHIa+51m4KHrYeK9iI7Eis507IKDm6Q0tw/W7C/hEsL5eCeL6WuOvLyWvdMQ1mbNmfUcjcbHN7tEr6cR1KlUxoA0HDHQEfx271wGkXBHhdSXmvBvnz8OZRQY47oF+tomwru5Y78TsU3Rln3m0OPeLXczpvv3Yon2KUH1XqOF9ZYcYLhcB44OS/i8hI0UUETao9TPlcR88cJ1rv0LZKxpLkgduAqzVJwU3OwcDIplFoWvGkY+Mf0O8YeTkKMm/Vh2dDQ+sV6zL2GSG09QcFM08yz7mMqN4awj08K4RlTH08RjK5xTitP+yAROnbSQjZXrhJ1Iwt8hBShWuZFVYRuPMzHItjnv4GK8zBl8W6yFBXBRL6mZCdBK8w7o1KDg+aHIwObVaqSggS0MPAhGc+5LfQLz4NQFHBGsnUvXpSvcvQs8Io+B+rG2kp9k6WjBa4+ZPD8FXbD85DELabVSuWOKwYtos0whmiem/xIYMGUgo7vmmus8cy2IOyl16cxSB0vPvMWISHNiEuutlI6CadQzROHIFQka6XSypxFeSvqZhBUfE5IVK22aiJ2wz7Nad7Aksr6W9pe6WwGYF+kpPmLPcdk+Z9w00cd0EwMGsbJ4GExpe1Lq1NVa4rrFSa8pq+B/EPMFW9DUREGLCND5wdPX4o4bAkQimkD+4pEWfP3fuWyKYsZppMrKl9qT5EtZ+aFl2kKFDbVZ/miFIOQ9QbS4ZGvFiIUgYbpBpEBJT7O4wSVVyqsUKAMDUUyygOZG7akP8k+Lc7EpngmPcqHbA4uRzsTl/CZq0Fb22n5eaNd3RFwB/DIPj1WFnKZW+q94a4E4L2ybgTqfU3cSXRgSFttnz+cbveIirmtX/1QMdPd+9QbhyuaYUDQRphhWyyjiSIJSYPkqyv80TfhMygVBfCDCrM6Kvxa2RMcmHHXbZFA//e9CAR/VuHAd3WBbVKzi16nbsKws9QXGblm5J+5KYKJ+DbcVUlsfEJHnFdNKOuhSuoUx+HaCQzcaXXZTZQ+hty2ORt3hN89NN66QHGy/2xIk5PU9c3k6lOOLuGy6JKh0HJH+cK2ypAZXZYG8u+n8IQOf+8u9fl9+Nq2Vfz+8TPjhA+8YeFwjaffF1jGntQi31w9nQlel7Lf7AZzuN0T6O'

# 복호화된 파일 저장 경로
# output_file_path = './googlefile/drive-python-download.json'

# 암호화된 문자열 복호화 및 파일 저장
# decrypt_string_to_file(encrypted_string, key_str, output_file_path)
# print(f'파일이 {output_file_path}에 성공적으로 복호화되었습니다.')

