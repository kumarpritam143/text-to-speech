from pymongo import MongoClient

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)
db = client["ai_voice_db"]

voices_col = db["voices"]
api_keys_col = db["api_keys"]

def get_all_voices():
    doc = voices_col.find_one({})
    if not doc:
        return []
    return doc["voices"][0]["voices"]   # 🔥 actual list
