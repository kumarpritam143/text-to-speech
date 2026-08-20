import streamlit as st
import requests
from pymongo import MongoClient

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Voice Generator", layout="centered")
st.title("🎙️ AI Voice Generator (MongoDB Powered)")

# =========================
# MONGO CONFIG
# =========================
MONGO_URI = st.secrets["MONGO_URI"]

import certifi
from pymongo import MongoClient

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=False
)

db = client["ai_voice_db"]

voices_col = db["voices"]
api_keys_col = db["api_keys"]

# =========================
# GET API KEY (ROUND ROBIN READY)
# =========================
def get_api_key():
    key_doc = api_keys_col.find_one({"active": True})
    if not key_doc:
        st.error("No active API key found in MongoDB")
        st.stop()
    return key_doc["api_key"]

# =========================
# GET VOICES FROM MONGO
# =========================
def get_all_voices():
    doc = voices_col.find_one({})
    if not doc:
        return []
    return doc["voices"][0]["voices"]  # 🔥 exact structure

voices = get_all_voices()

if not voices:
    st.error("No voices found in MongoDB")
    st.stop()

# =========================
# PREPARE FILTER OPTIONS
# =========================
genders = sorted(set(
    v.get("labels", {}).get("gender")
    for v in voices
    if v.get("labels", {}).get("gender")
))

languages = sorted(set(
    lang.get("language")
    for v in voices
    for lang in v.get("verified_languages", [])
    if lang.get("language")
))

# =========================
# UI FILTERS
# =========================
gender = st.selectbox("Select Gender", [""] + genders)
language = st.selectbox("Select Language", [""] + languages)

filtered_voices = voices

if gender:
    filtered_voices = [
        v for v in filtered_voices
        if v.get("labels", {}).get("gender") == gender
    ]

if language:
    filtered_voices = [
        v for v in filtered_voices
        if any(
            l.get("language") == language
            for l in v.get("verified_languages", [])
        )
    ]

voice_names = [v["name"] for v in filtered_voices]
voice_name = st.selectbox("Select Voice", [""] + voice_names)

selected_voice = next(
    (v for v in filtered_voices if v["name"] == voice_name),
    None
)

# =========================
# SHOW VOICE DETAILS
# =========================
if selected_voice:
    st.markdown("---")
    st.markdown("### 🎧 Selected Voice Details")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"**🧑 Voice Name:** {selected_voice.get('name')}")
        st.markdown(
            f"**📝 Description:** {selected_voice.get('description', 'No description available')}"
        )
        st.markdown(
            f"**🎯 Use Case:** {selected_voice.get('labels', {}).get('use_case')}"
        )

    with col2:
        st.markdown(
            f"**🌍 Language:** {selected_voice.get('labels', {}).get('language')}"
        )
        st.markdown(
            f"**🗣️ Accent:** {selected_voice.get('labels', {}).get('accent')}"
        )
        st.markdown(
            f"**🎂 Age:** {selected_voice.get('labels', {}).get('age')}"
        )
        st.markdown(
            f"**🚻 Gender:** {selected_voice.get('labels', {}).get('gender')}"
        )

# =========================
# TEXT INPUT
# =========================
text = st.text_area(
    "Enter Text",
    placeholder="Type your text here...",
    height=150
)


# =========================
# GENERATE VOICE
# =========================
if st.button("🎧 Generate Voice"):
    if not selected_voice:
        st.error("Please select a voice first")
        st.stop()

    if not text.strip():
        st.error("Please enter some text")
        st.stop()

    api_key = get_api_key()
    voice_id = selected_voice["voice_id"]

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.8
        }
    }

    with st.spinner("Generating voice..."):
        r = requests.post(url, headers=headers, json=payload)

    if r.status_code != 200:
        st.error("❌ Voice generation failed")
        try:
            st.json(r.json())
        except:
            st.write(r.text)
    else:
        st.success("✅ Voice generated successfully")
        st.audio(r.content, format="audio/mp3")
