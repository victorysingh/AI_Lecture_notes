import streamlit as st
import requests

st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

HF_TOKEN = st.secrets["HF_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ✅ WORKING MODELS
ASR_API = "https://router.huggingface.co/hf-inference/models/facebook/wav2vec2-base-960h"
SUMMARY_API = "https://router.huggingface.co/hf-inference/models/t5-small"
QUIZ_API = "https://router.huggingface.co/hf-inference/models/google/flan-t5-small"


# ---------- FUNCTIONS ----------

def transcribe_audio(audio_bytes):
    files = {
        "file": ("audio.wav", audio_bytes)
    }

    response = requests.post(
        ASR_API,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        files=files
    )

    if response.status_code != 200:
        st.error("Speech-to-Text Error")
        st.code(response.text)
        return ""

    return response.json()["text"]


def summarize_text(text):
    response = requests.post(
        SUMMARY_API,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": text}
    )

    if response.status_code != 200:
        st.error("Summary Error")
        st.code(response.text)
        return ""

    return response.json()[0]["generated_text"]


def generate_quiz(text):
    prompt = f"""
Create 5 multiple choice questions from the text below.
Each question must have 4 options and clearly mention the correct answer.

Text:
{text}
"""

    response = requests.post(
        QUIZ_API,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        st.error("Quiz Error")
        st.code(response.text)
        return ""

    return response.json()[0]["generated_text"]


# ---------- UI ----------

st.title("🎧 AI Lecture Notes Generator")
st.markdown("Convert lecture audio into notes and quizzes using AI")
st.divider()

audio_file = st.file_uploader("Upload lecture audio", type=["wav", "mp3"])

if st.button("Generate Notes"):
    if not audio_file:
        st.error("Please upload an audio file.")
    else:
        audio_bytes = audio_file.read()

        with st.spinner("🎧 Transcribing audio..."):
            transcript = transcribe_audio(audio_bytes)

        if transcript:
            st.subheader("📝 Transcript")
            st.write(transcript)

            with st.spinner("📘 Summarizing..."):
                summary = summarize_text(transcript)

            st.subheader("📘 Summary")
            st.success(summary)

            with st.spinner("🧠 Generating Quiz..."):
                quiz = generate_quiz(summary)

            st.subheader("🧠 Quiz")
            st.write(quiz)

            st.success("✅ Done Successfully!")
