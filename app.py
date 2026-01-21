import streamlit as st
import requests
import time

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

ASSEMBLY_API_KEY = st.secrets["ASSEMBLY_API_KEY"]
HF_TOKEN = st.secrets["HF_TOKEN"]

SUMMARY_API = "https://router.huggingface.co/hf-inference/models/t5-small"
QUIZ_API = "https://router.huggingface.co/hf-inference/models/google/flan-t5-small"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ---------------- SPEECH TO TEXT ---------------- #

def transcribe_audio(audio_file):
    headers = {"authorization": ASSEMBLY_API_KEY}

    upload = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=audio_file
    )

    audio_url = upload.json()["upload_url"]

    transcript_req = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        json={"audio_url": audio_url},
        headers=headers
    )

    transcript_id = transcript_req.json()["id"]

    while True:
        result = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=headers
        ).json()

        if result["status"] == "completed":
            return result["text"]

        if result["status"] == "error":
            return "Transcription failed"

        time.sleep(3)

# ---------------- NLP ---------------- #

def summarize_text(text):
    r = requests.post(
        SUMMARY_API,
        headers=HEADERS,
        json={
            "inputs": text,
            "options": {"wait_for_model": True}
        }
    )

    if r.status_code != 200:
        st.error("Summary API Error")
        st.code(r.text)
        return ""

    data = r.json()
    return data[0]["generated_text"]


def generate_quiz(text):
    prompt = f"""
Create 5 multiple choice questions from the text.
Each question must have 4 options and clearly indicate the correct answer.

Text:
{text}
"""

    r = requests.post(
        QUIZ_API,
        headers=HEADERS,
        json={
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }
    )

    if r.status_code != 200:
        st.error("Quiz API Error")
        st.code(r.text)
        return ""

    data = r.json()
    return data[0]["generated_text"]

# ---------------- UI ---------------- #

st.title("🎧 AI Lecture Notes Generator")
st.markdown("Convert lecture audio into notes and quizzes using AI")

audio_file = st.file_uploader("Upload Lecture Audio", type=["wav", "mp3"])

if st.button("Generate Notes"):
    if not audio_file:
        st.error("Please upload an audio file")
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
