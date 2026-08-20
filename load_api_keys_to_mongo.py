from pymongo import MongoClient
from datetime import datetime

MONGO_URI="mongodb+srv://kumardaspritam972_db_user:x4mLbdrWdZigu952@ai-voice-system.xm0qrh1.mongodb.net/?appName=ai-voice-system"

client = MongoClient(MONGO_URI)
db = client["ai_voice_db"]
api_keys_col = db["api_keys"]

# OPTIONAL: purane keys hata do (first time clean insert)
api_keys_col.delete_many({})

api_keys = [
    "sk_eb5431472cbdd8b94851db4180cf877e74592c37fd71064d",
    "sk_863ff38c6d50dc136bfb6e32a35da2c502fff64df6e29bcd"
]

docs = []

for key in api_keys:
    docs.append({
        "provider": "elevenlabs",
        "api_key": key,
        "active": True,
        "used_count": 0,
        "last_used": None,
        "created_at": datetime.utcnow()
    })

api_keys_col.insert_many(docs)

print("✅ API keys successfully saved to MongoDB")
