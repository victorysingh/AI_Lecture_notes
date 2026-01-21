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

# ---------------- SPEECH TO TEXT ---------------- #

def transcribe_audio(audio_bytes):
    headers = {
        "Authorization": ASSEMBLY_API_KEY
    }

    # Upload audio
    upload = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=audio_bytes
    ).json()

    audio_url = upload["upload_url"]

    # Request transcription
    transcript = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": audio_url}
    ).json()

    transcript_id = transcript["id"]

    # Poll result
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

# ---------------- SUMMARIZATION ---------------- #

def summarize_text(text):
    text = text[:3500]  # Important for HF limit

    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        headers={
            "Authorization": f"Bearer {HF_TOKEN}"
        },
        json={"inputs": text}
    )

    data = response.json()
    return data[0].get("summary_text", "Summary failed.")

# ---------------- QUIZ GENERATION ---------------- #

def generate_quiz(text):
    prompt = f"""
Generate 5 multiple choice questions with answers based on the text below:

{text}
"""

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-base",
        headers={
            "Authorization": f"Bearer {HF_TOKEN}"
        },
        json={"inputs": prompt}
    )

    data = response.json()
    return data[0].get("generated_text", "Quiz generation failed.")

# ---------------- UI ---------------- #

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

        with st.spinner("📘 Generating summary..."):
            summary = summarize_text(transcript)

        st.subheader("📘 Summary")
        st.success(summary)

        with st.spinner("🧠 Generating quiz..."):
            quiz = generate_quiz(summary)

        st.subheader("🧠 Quiz")
        st.write(quiz)

        st.success("✅ Completed Successfully")
