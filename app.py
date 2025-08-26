import streamlit as st
import requests
import os

st.title("English/Hindi Text-to-Speech")

# -----------------------------
# 1️⃣ Enter your ElevenLabs API Key
API_KEY = "sk_207165fe77e3ff79843fe8085c0ece631a88aa0d42e48958"
# -----------------------------

# 2️⃣ Choose voice gender
voice_gender = st.radio("Select Voice Gender", ("male", "female"))

# 3️⃣ Set Voice IDs (replace with your voice IDs from ElevenLabs)
voice_ids = {
    "male": "qSV5UqvHBC0Widy71Esh",
    "female": "H6QPv2pQZDcGqLwDTIJQ"
}

VOICE_ID = voice_ids.get(voice_gender)

# 4️⃣ Enter text and upload file
text_input = st.text_area("Enter English or Hindi Text")
uploaded_file = st.file_uploader("Upload you text/Pdf file")

# 5️⃣ Generate Speech
if st.button("Generate Speech"):
    if not API_KEY:
        st.warning("Please enter your ElevenLabs API Key!")
    else:
        # Get text from input or file
        if uploaded_file:
            text = str(uploaded_file.read(), "utf-8")
        elif text_input:
            text = text_input
        else:
            st.warning("Please enter text or upload a text file!")
            st.stop()
        
        # Optional: warn if text is very long
        if len(text) > 10000:
            st.warning("Text is very long! Consider splitting into smaller files for free API usage.")
        
        # ElevenLabs TTS request
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.3,
                "similarity_boost": 0.8
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            audio_file = "output.mp3"
            with open(audio_file, "wb") as f:
                f.write(response.content)
            st.success("✅ Audio generated successfully!")
            st.audio(audio_file, format="audio/mp3")
        else:
            st.error(f"❌ Failed to generate speech: {response.status_code}, {response.text}")
