import streamlit as st
import requests

# ================= CONFIG ================= #

st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

HF_TOKEN = st.secrets["HF_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

WHISPER_API = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
SUMMARY_API = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
QUIZ_API = "https://router.huggingface.co/hf-inference/models/google/flan-t5-base"

# ================= FUNCTIONS ================= #

def transcribe_audio(audio_bytes):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "audio/wav"
    }

    response = requests.post(
        WHISPER_API,
        headers=headers,
        data=audio_bytes
    )

    if response.status_code != 200:
        st.error("❌ Whisper API Error")
        st.code(response.text)
        return ""

    return response.json().get("text", "")


def summarize_text(text):
    response = requests.post(
        SUMMARY_API,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        },
        json={"inputs": text}
    )

    if response.status_code != 200:
        st.error("❌ Summary API Error")
        st.code(response.text)
        return ""

    return response.json()[0]["summary_text"]


def generate_quiz(text):
    prompt = f"""
Generate 5 multiple choice questions.
Each question should have 4 options and mention the correct answer.

Text:
{text}
"""

    response = requests.post(
        QUIZ_API,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        },
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        st.error("❌ Quiz API Error")
        st.code(response.text)
        return ""

    return response.json()[0]["generated_text"]


# ================= UI ================= #

st.title("🎧 AI Lecture Notes Generator")
st.markdown("### Convert lecture audio into notes and quizzes using AI")
st.divider()

audio_file = st.file_uploader("📤 Upload Lecture Audio (MP3 / WAV)", type=["mp3", "wav"])
generate_btn = st.button("🚀 Generate Notes")

if generate_btn:
    if not audio_file:
        st.error("❌ Please upload an audio file.")
    else:
        audio_bytes = audio_file.read()

        with st.spinner("🔄 Transcribing audio..."):
            transcript = transcribe_audio(audio_bytes)

        if transcript:
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

            st.success("✅ Completed Successfully!")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Hugging Face")
