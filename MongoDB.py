from pymongo import MongoClient

# MongoDB 클라이언트 생성
uri = "mongodb+srv://jinha12345:mU3PiT5P1VrRvOYH@jinha.8og9mva.mongodb.net/?retryWrites=true&w=majority&appName=jinha"
client = MongoClient(uri)

def getfromMongoDB():
    global uri, client

    # 데이터베이스 선택
    db = client.my_database

    # 컬렉션 선택
    collection = db.my_collection

    # 첫 번째 문서 조회
    first_document = collection.find_one()

    return first_document['value']