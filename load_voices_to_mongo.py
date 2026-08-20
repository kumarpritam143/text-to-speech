import json
from pymongo import MongoClient

MONGO_URI="mongodb+srv://kumardaspritam972_db_user:x4mLbdrWdZigu952@ai-voice-system.xm0qrh1.mongodb.net/?appName=ai-voice-system"

JSON_PATH = r"C:\Users\91628\Dropbox\PC\Downloads\Realtime-Streaming-website-main\Realtime-Streaming-website-main\elevenlabs_voices.json"

client = MongoClient(MONGO_URI)
db = client["ai_voice_db"]
voices_col = db["voices"]

# Load JSON file
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 🔥 Clear old data (optional but recommended)
voices_col.delete_many({})

# 🔥 DIRECT INSERT (AS-IS)
voices_col.insert_one(data)

print("✅ JSON file saved directly into MongoDB (no modification)")
