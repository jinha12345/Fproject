from tkinter import Tk, filedialog
from PIL import Image
from io import BytesIO
from encdec import *

from tkinter import Tk, filedialog
from PIL import Image
import os
from util import *
from MongoDB import *

key_str = "Wlsend99Pr##"

def UploadProfileImage(id):

    # 1. 탐색기를 열어 사용자로부터 jpg 또는 png 파일 입력받기
    root = Tk()
    root.withdraw()  # Tkinter 창을 숨김
    file_path = filedialog.askopenfilename(
        title="이미지 파일 선택",
        filetypes=[("Image Files", "*.jpg *.png")]
    )
    
    if not file_path:  # 파일 선택이 취소된 경우
        return None

    # 2. 이미지를 32x32로 다운스케일링
    try:
        with Image.open(file_path) as img:
            # Pillow 10.0.0 이상에서는 Image.Resampling.LANCZOS 사용
            img_resized = img.resize((32, 32), Image.Resampling.LANCZOS)  # 32x32로 리사이즈
            # 리사이즈된 이미지를 임시 파일로 저장
            temp_file_path = resource_path("temp_resized_image.png")
            img_resized.save(temp_file_path, format="PNG")
    except Exception as e:
        print(f"이미지 처리 중 오류 발생: {e}")
        return None

    # 3. encrypt_file_to_string 함수를 사용하여 이미지를 문자열로 변환
    try:
        encrypted_string = encrypt_file_to_string(temp_file_path, key_str)
    except Exception as e:
        print(f"암호화 중 오류 발생: {e}")
        return None
    finally:
         #임시 파일 삭제
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    uri = "mongodb+srv://jinha12345:mU3PiT5P1VrRvOYH@jinha.8og9mva.mongodb.net/?retryWrites=true&w=majority&appName=jinha"
    client = MongoClient(uri)
    db = client["Fproject"]
    collection = db["ProfileImage"]
    collection.delete_one({"id": id})

    # 4. 암호화된 문자열 업로드
    UploadToMongoDB("Fproject", "ProfileImage", {"id" : id, "img" : encrypted_string})
    return None

def DownloadProfileImage():
    #getonefromMongoDB(database_name, collection_name, query_field, query_value, target_field)
    database_name = "Fproject"
    collection_name = "ProfileImage"
    data_list = get_all_data(database_name, collection_name)

    for data in data_list:
        encrypted_img = getonefromMongoDB(database_name, collection_name, "id", data["id"], "img")
        decrypt_string_to_file(encrypted_img, key_str, resource_path("./static/profileimage/" + data["id"] + ".png"))
    return None

#UploadProfileImage("jinha12345")
#DownloadProfileImage()