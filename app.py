import streamlit as st
import requests
import time

# ================= CONFIG ================= #

st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

ASSEMBLY_API_KEY = st.secrets["ASSEMBLY_API_KEY"]
HF_TOKEN = st.secrets["HF_TOKEN"]

HF_HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ================= SPEECH TO TEXT ================= #

def transcribe_audio(audio_bytes):
    headers = {"authorization": ASSEMBLY_API_KEY}

    upload = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=audio_bytes
    ).json()

    transcript = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": upload["upload_url"]}
    ).json()

    transcript_id = transcript["id"]

    while True:
        result = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=headers
        ).json()

        if result["status"] == "completed":
            return result["text"]

        if result["status"] == "error":
            return "❌ Transcription failed."

        time.sleep(3)

# ================= SUMMARIZATION ================= #

def summarize_text(text):
    payload = {
        "inputs": text[:3500]
    }

    response = requests.post(
        "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn",
        headers=HF_HEADERS,
        json=payload
    )

    data = response.json()

    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]

    if "error" in data:
        return f"❌ HuggingFace Error: {data['error']}"

    return "❌ Summary generation failed"

# ================= QUIZ GENERATION ================= #

def generate_quiz(text):
    prompt = f"""
Create 5 multiple choice questions from the text below.
Each question must have 4 options and clearly show the correct answer.

Text:
{text}
"""

    payload = {"inputs": prompt}

    response = requests.post(
        "https://router.huggingface.co/hf-inference/models/google/flan-t5-base",
        headers=HF_HEADERS,
        json=payload
    )

    data = response.json()

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    if "error" in data:
        return f"❌ HuggingFace Error: {data['error']}"

    return "❌ Quiz generation failed"

# ================= UI ================= #

st.title("🎧 AI Lecture Notes Generator")
st.markdown("Convert lecture audio into notes and quizzes using AI")

audio_file = st.file_uploader("Upload Lecture Audio", type=["mp3", "wav"])

if st.button("Generate Notes"):

    if not audio_file:
        st.error("Please upload an audio file.")
    else:
        with st.spinner("🎧 Transcribing audio..."):
            transcript = transcribe_audio(audio_file.read())

        st.subheader("📝 Transcript")
        st.write(transcript)

        with st.spinner("📘 Generating Summary..."):
            summary = summarize_text(transcript)

        st.subheader("📘 Summary")
        st.success(summary)

        with st.spinner("🧠 Generating Quiz..."):
            quiz = generate_quiz(summary)

        st.subheader("🧠 Quiz")
        st.write(quiz)

        st.success("✅ Completed Successfully")
