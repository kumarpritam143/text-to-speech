from pymongo import MongoClient
from datetime import datetime

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)
db = client["ai_voice_db"]
api_keys_col = db["api_keys"]

# OPTIONAL: purane keys hata do (first time clean insert)
api_keys_col.delete_many({})



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
