import streamlit as st
import requests

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

HF_TOKEN = st.secrets["HF_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

WHISPER_API = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
SUMMARY_API = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
QUIZ_API = "https://api-inference.huggingface.co/models/google/flan-t5-base"

# ---------------- FUNCTIONS ---------------- #

def transcribe_audio(audio_bytes):
    response = requests.post(
        WHISPER_API,
        headers=HEADERS,
        data=audio_bytes
    )
    return response.json()["text"]


def summarize_text(text):
    response = requests.post(
        SUMMARY_API,
        headers=HEADERS,
        json={"inputs": text}
    )
    return response.json()[0]["summary_text"]


def generate_quiz(text):
    prompt = f"""
Generate 5 multiple choice questions from the text below.
Each question should have 4 options and clearly mention the correct answer.

Text:
{text}
"""
    response = requests.post(
        QUIZ_API,
        headers=HEADERS,
        json={"inputs": prompt}
    )
    return response.json()[0]["generated_text"]


# ---------------- UI ---------------- #

st.title("🎧 AI Lecture Notes Generator")
st.markdown("### Convert lecture audio into notes & quizzes using AI")
st.divider()

audio_file = st.file_uploader("📤 Upload lecture audio (mp3 / wav)", type=["mp3", "wav"])
difficulty = st.selectbox("📘 Select difficulty level", ["Easy", "Medium", "Hard"])

generate_btn = st.button("🚀 Generate Notes")

if generate_btn:

    if audio_file is None:
        st.error("❌ Please upload an audio file.")
    else:
        audio_bytes = audio_file.read()

        with st.spinner("🔄 Transcribing audio..."):
            transcript = transcribe_audio(audio_bytes)

        st.subheader("📝 Transcribed Text")
        st.write(transcript)

        with st.spinner("🧠 Generating summary..."):
            summary = summarize_text(transcript)

        st.subheader("📘 AI Generated Notes")
        st.success(summary)

        with st.spinner("🧩 Generating quiz..."):
            quiz = generate_quiz(summary)

        st.subheader("🧠 Quiz From Lecture")
        st.write(quiz)

        st.success("✅ Done Successfully!")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Hugging Face API")
