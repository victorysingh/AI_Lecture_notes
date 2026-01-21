import streamlit as st
import requests
import time
from openai import OpenAI

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

ASSEMBLY_API_KEY = st.secrets["ASSEMBLY_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------- SPEECH TO TEXT ---------------- #

def transcribe_audio(audio_file):
    headers = {
        "authorization": ASSEMBLY_API_KEY
    }

    # Upload audio
    upload_response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=audio_file
    ).json()

    audio_url = upload_response["upload_url"]

    # Request transcription
    transcript_response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": audio_url}
    ).json()

    transcript_id = transcript_response["id"]

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

# ---------------- OPENAI FUNCTIONS ---------------- #

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the lecture clearly in student-friendly language."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


def generate_quiz(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Create 5 multiple choice questions with answers."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


# ---------------- UI ---------------- #

st.title("🎧 AI Lecture Notes Generator")
st.markdown("Convert lecture audio into notes and quizzes using AI")

audio_file = st.file_uploader("Upload Lecture Audio", type=["wav", "mp3"])

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
