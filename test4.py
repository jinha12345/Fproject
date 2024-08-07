from cryptography.fernet import Fernet
import base64
import os

# 주어진 문자열을 Base64로 인코딩하여 유효한 Fernet 키 생성
def create_key_from_string(s):
    # 문자열을 바이트로 변환하고 Base64로 인코딩
    key = base64.urlsafe_b64encode(s.ljust(32).encode())
    return key

# 문자열을 복호화하기
def decrypt_string(encrypted_string, key):
    fernet = Fernet(key)
    decrypted_string = fernet.decrypt(encrypted_string).decode()
    return decrypted_string

# 암호화된 파일을 복호화하고 JSON 파일로 저장
def save_decrypted_file(decrypted_data, filename):
    with open(filename, "w") as dec_file:
        dec_file.write(decrypted_data)

# 예제 실행
if __name__ == "__main__":
    # 1. 복호화에 사용할 키 설정
    key_string = "7Q8x2nsP5P9YNVemEY-cXnaT_1VcmwNfb94R_kDjixk="
    key = base64.urlsafe_b64decode(key_string)

    # 2. 암호화된 데이터를 Base64로 디코딩
    encrypted_data_base64 = (
        "gAAAAABmsp_vPMtcR-EBgsZwwXHXXkWqJthEkHF-9b_WwOnQjccfI-Hadd-GOBEMObvcNBsLuI4LS22QnUc00CZQvb8jQXHO90GVyZ69vwEHpookgLgAsr1AKBRxkIErR-8Yv94hMl4tdW6lzdkS_tM-5wellqRl-mumgX8NdQnQOummTrpHljNCUoG0SfoEQVwAH1OtvHsW-c-ucpI7maaeqzgIGbZc61P04FaGwwgElAodWZr_Io5Yg9zcrDDTsQbOTVyGbSJFpeldnXyxhN95xliiSUl3fqZwPwjGvqXA-3S-bGNeDvQCyBtNo7OR79uDXlSKVCklME-8JD_x-v5r91rp7thfA2VjHwlwncdH7J2XBmmYjALLp-mgln3T94O8YJQk4zeLb4CfiLECR3MlEJjA6IqzKsOqo3dcvBZ-Aen5rmne550qJxCbPUmY6wiL0aSidiRnHiZtwOPB8g4iYg8NtrB2_t21cHAgfZTWCeHjTog7eagnhPj79zITHQDJQWSWFWgtw8IXs0-qXVPD46ZGtzh9Qdkn90L2o0VgEwtg3CDfjmQlAYVwBvVaTy0zygJC4mOz1TiczZXuwpfy6Dun1Xzr_FkVUoDhR5IUmFwNpJleUqXehsrbuYG01aOGiJcpD_Z4N0w8sp_ZnMU_70EZtAfAVNk95v65-wGcCvm5MaK5zzUa8dMbtJtqReu2UjP64BhfRHhoNDp2pzd3ReSElwJ1_0EkiAy3oI_KVgXLgI6ctrhoKAfKaFyLFrS1fG0GFdB2Kcp4tUgc6k1ckftsFqcQW-axHcEX2p9kfMNwx0fe4jRNHPhiJVgpuc-tYsnLRRv01jmpGXhyng4NZWmuVaR5_dkvP9k1pDQASoc5esS55nJYoKzUqloJLdeSxDR_q9HG0OLmXMiNnZD4-QSvEVeedBQ3dY02uZ9d7tpiMJIp2pXvkxeDPP8teOxhC3CIA7q4MVxyKLvmAevpFDF2snNwfB_crlsd4XZBH3dyffQOgVuEhOo4bKPm72yGdIWj2fIxS0DpaE1f4YgQ_BEDcE_oErbIC8oPlucTd0VdfFE6cfxslrx6mp_xlFmCdWsrW_DruWrGnHQIY1Y_ipRXQx3nRed9oWIkm96S1cSxwR2VO4D3uGw-mXAT5wbPojURXqO_qNcV-7AF-MylNHJe9PD9TrZRqbX9vIHD_5i2u_DvbqAJk-lPf0ljYVIXhkNAadM86c7z5pElH9NfP8MLYTIQ2mKfBN6GMvUFuGyjoSDjh3wPde17YtXC7vYaMcj5kVx_a0Ojh29Qw9WpwfTkhQdzoywxXi5EWYhVePGg12vkl-U4F5G8ELSEEZ98W0EUX_f3ucwFYzSSI0L2IWkpYxuphH5Rw6sIM8AUokGssQh0iz4zIbYtu0Xqms7GDDdkgnfuYblawaDRVAHWN4qEoJVauvKGvJHP4T2zfouVtnGlhiJzwsMAtpeY630jeVxlrYsXhYla94mJ5aJrvvEASTAnr7I_lQg6L5lWHShmNxy98wxm00VTYKT6qhEPRQSxtEbGCQCekBcoREvdThRXDgRhI6wx9BsWGD7JCbpSWDgBteWdbtRDme6nX3NE3Q7Xn43O8jAudTthB735yvYNtPA0e39sHQ-g4A2Gy2AtA0ZvWar4qOqTrfoTHg8bc9ZkcVYhhPdWs19fxQVDs7dm3a6hbRb1xg7wckaxSBFHPT-4QgCDTa3Oqfyr8nfuQnjngNU6fZ-E4WwW14oyXHCDO6qQ4ZPwoUQXrV17Hvf3dovgBaAlJ8-W5j_uRt6yD5Zf9ZHSMdvHl3Go4wfMQtCBHHxSuBeKKfeGd278PGNXim69EZmVkZEXhlPZNz_X-bMXDP-fQRboI44EgFOw2JAfeMyO9_IunDk5peqD5qcg3atbAJnjCDwbktev_xdb6a4ScIoNw-LYNzkASz0ZZE19JWYz90jY1uUQERUDmWOVcZ5HTDc="
    )
    
    # 패딩이 올바른지 확인하고 추가
    padded_encrypted_data_base64 = encrypted_data_base64 + '=' * (-len(encrypted_data_base64) % 4)

    # 3. 암호화된 데이터를 Base64로 디코딩
    encrypted_data = base64.b64decode(padded_encrypted_data_base64)

    # 4. 암호화된 데이터를 복호화
    decrypted_data = decrypt_string(encrypted_data, key)

    # 5. 복호화된 데이터를 ./dec 폴더에 저장
    if not os.path.exists('./dec'):
        os.makedirs('./dec')
    save_decrypted_file(decrypted_data, './dec/decrypted_file.json')

    print("Decryption complete. Decrypted file saved as './dec/decrypted_file.json'.")
