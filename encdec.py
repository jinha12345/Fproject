import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


key_str = "Wlsend99Js##"


def encrypt_file_to_string(file_path: str) -> str:
    global key_str

    # 문자열 키를 바이트로 변환하고 길이를 32바이트로 맞춤
    key = key_str.encode('utf-8').ljust(32)[:32]
    
    # Initialization Vector (IV) 생성
    iv = os.urandom(16)
    
    # 파일명과 파일 데이터 읽기
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # 파일명과 파일 데이터 결합 (파일명 길이를 먼저 추가)
    file_name_bytes = file_name.encode('utf-8')
    file_name_length = len(file_name_bytes).to_bytes(4, 'big')
    combined_data = file_name_length + file_name_bytes + file_data
    
    # AES 패딩 추가
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(combined_data) + padder.finalize()
    
    # AES 암호화 설정
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # 데이터 암호화
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # IV와 암호화된 데이터를 base64로 인코딩
    encrypted_string = base64.b64encode(iv + encrypted_data).decode('utf-8')
    return encrypted_string


def decrypt_string_to_file(encrypted_string: str, output_dir: str = './'):
    global key_str

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
    combined_data = unpadder.update(padded_data) + unpadder.finalize()
    
    # 파일명 길이 추출 및 파일명과 파일 데이터 분리
    file_name_length = int.from_bytes(combined_data[:4], 'big')
    file_name = combined_data[4:4 + file_name_length].decode('utf-8')
    file_data = combined_data[4 + file_name_length:]
    
    # 파일명과 데이터를 사용해 파일 저장
    output_file_path = os.path.join(output_dir, file_name)
    with open(output_file_path, 'wb') as f:
        f.write(file_data)
    
    return output_file_path

# 사용 예시:
# 암호화된 문자열 생성
# encrypted_string = encrypt_file_to_string('your_file_path_here')
# print(encrypted_string)

# 복호화 및 파일 저장
# output_path = decrypt_string_to_file(encrypted_string, './output_dir/')
# print(f'파일이 {output_path}에 성공적으로 복호화되었습니다.')

#encrypted_string = encrypt_file_to_string('./app.py')
#print(encrypted_string)

#output_path = decrypt_string_to_file(encrypted_string, './test/')
#print(f'파일이 {output_path}에 성공적으로 복호화되었습니다.')