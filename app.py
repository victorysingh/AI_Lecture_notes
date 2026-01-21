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

WHISPER_API = "https://router.huggingface.co/hf-inference/models/openai/whisper-small"
SUMMARY_API = "https://router.huggingface.co/hf-inference/models/t5-small"
QUIZ_API = "https://router.huggingface.co/hf-inference/models/google/flan-t5-small"


# ---------------- FUNCTIONS ---------------- #

def transcribe_audio(audio_bytes):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "audio/wav"
    }

    r = requests.post(WHISPER_API, headers=headers, data=audio_bytes)
    if r.status_code != 200:
        st.error("Whisper Error")
        st.code(r.text)
        return ""

    return r.json().get("text", "")


def summarize_text(text):
    r = requests.post(
        SUMMARY_API,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": text}
    )

    if r.status_code != 200:
        st.error("Summary Error")
        st.code(r.text)
        return ""

    return r.json()[0]["generated_text"]


def generate_quiz(text):
    prompt = f"""
Create 5 MCQs from the text.
Each question must have 4 options and show the correct answer.

Text:
{text}
"""

    r = requests.post(
        QUIZ_API,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt}
    )

    if r.status_code != 200:
        st.error("Quiz Error")
        st.code(r.text)
        return ""

    return r.json()[0]["generated_text"]


# ---------------- UI ---------------- #

st.title("🎧 AI Lecture Notes Generator")
st.markdown("Convert lecture audio into notes and quizzes using AI")
st.divider()

audio_file = st.file_uploader("Upload Lecture Audio", type=["wav", "mp3"])
generate_btn = st.button("Generate Notes")

if generate_btn:
    if not audio_file:
        st.error("Please upload audio")
    else:
        audio_bytes = audio_file.read()

        with st.spinner("🎧 Transcribing..."):
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

            st.success("✅ Completed Successfully!")
