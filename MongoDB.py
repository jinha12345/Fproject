from pymongo import MongoClient

# MongoDB 클라이언트 생성
uri = "mongodb+srv://jinha12345:mU3PiT5P1VrRvOYH@jinha.8og9mva.mongodb.net/?retryWrites=true&w=majority&appName=jinha"
client = MongoClient(uri)

def getonefromMongoDB(database_name, collection_name, query_field, query_value, target_field):
    global uri, client

    # 데이터베이스 선택
    db = client[database_name]

    # 컬렉션 선택
    collection = db[collection_name]

    # 조건에 맞는 첫 번째 문서 조회
    query = {query_field: query_value}  # 조건 생성
    document = collection.find_one(query)

    # 문서에서 지정한 필드 값 반환
    return document[target_field] if document and target_field in document else None

def UploadToMongoDB(database_name, collection_name, field):
    global uri, client

    # 데이터베이스 선택
    db = client[database_name]

    # 컬렉션 선택
    collection = db[collection_name]

    # field가 딕셔너리 형태인지 확인
    if not isinstance(field, dict):
        raise ValueError("field는 반드시 딕셔너리 형태여야 합니다.")

    try:
        # 데이터 삽입
        result = collection.insert_one(field)
        print(f"데이터가 성공적으로 업로드되었습니다. 문서 ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"데이터 업로드 중 오류 발생: {e}")
        return None

def get_all_data(database_name, collection_name):
    global uri, client

    # 데이터베이스 및 컬렉션 선택
    db = client[database_name]
    collection = db[collection_name]

    # 컬렉션의 모든 문서 가져오기
    documents = collection.find()

    # 모든 데이터를 리스트로 반환
    data_list = list(documents)

    return data_list