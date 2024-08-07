from cryptography.fernet import Fernet
import json

# 암호화에 사용할 키 생성
def generate_key():
    return Fernet.generate_key()

# 문자열을 암호화하기
def encrypt_string(string, key):
    fernet = Fernet(key)
    encrypted_string = fernet.encrypt(string.encode())
    return encrypted_string

# JSON 파일을 문자열로 읽기
def read_json_file(filename):
    with open(filename, "r") as json_file:
        return json_file.read()

# 예제 실행
if __name__ == "__main__":
    # 1. 암호화에 사용할 키 생성
    key = generate_key()

    # 2. JSON 파일을 읽어서 문자열로 변환
    json_string = read_json_file("drive-python-download_new.json")

    # 3. 문자열을 암호화
    encrypted_data = encrypt_string(json_string, key)

    # 4. 암호화된 문자열 출력
    print(f"Encryption key: {key.decode()}")
    print(f"Encrypted data (base64): {encrypted_data.decode()}")
