from pymongo import MongoClient
from datetime import datetime

# MongoDB 클라이언트 생성
uri = "mongodb+srv://jinha12345:mU3PiT5P1VrRvOYH@jinha.8og9mva.mongodb.net/?retryWrites=true&w=majority&appName=jinha"
client = MongoClient(uri)

def addtoMongoDB(message, id):
    global uri, client

    # 데이터베이스 선택
    db = client.Fproject

    # 컬렉션 선택
    collection = db.chat

    # 새로운 문서 추가
    new_message = {"id": id, "message": message, "created_at": datetime.utcnow()}
    result = collection.insert_one(new_message)
    
    # 추가된 문서의 ID 반환
    return result.inserted_id

def getLatestMessage(n):
    messages = client.Fproject.chat.find().sort("created_at", -1).limit(n)
    messages = list(messages)[::-1]
    return messages

#latest_messages = getLatestMessage(10)

#for message in latest_messages:
#    print(message)