from flask import request, jsonify
from fine_tuning.AI import callGpt
import os
import threading
from pymongo import MongoClient
from bson.objectid import ObjectId 

def receive_letter():
    data = request.json
    title = data.get('title')  
    letter = data.get('letter')
    mail = data.get('mail')
    database_url = os.getenv('MONGO_URI')
    #'title'과 'letter' 있는지 확인
    
    if not title or not letter or not mail:
        return jsonify({"error": "데이터가 충분하지 않습니다."}), 400

    else:
        client = MongoClient(database_url)
        db = client.monoletter
        collection = db['users'] 
        # 이메일로 사용자 찾기
        user = collection.find_one({"email": mail})
        if user:
            detail = user['detail']
            print(detail)
            feedback = callGpt(letter, title,detail)
            print(feedback)
            return jsonify(feedback)
        else:
            print("User not found.")
            return jsonify({"error": "User not found."}), 404


