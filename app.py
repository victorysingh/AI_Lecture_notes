import streamlit as st
import requests
import time

st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

ASSEMBLY_API_KEY = st.secrets["ASSEMBLY_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# ---------------- SPEECH TO TEXT ---------------- #

def transcribe_audio(audio_bytes):
    headers = {"Authorization": ASSEMBLY_API_KEY}

    upload = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=audio_bytes
    ).json()

    audio_url = upload["upload_url"]

    transcript = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": audio_url}
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
            return "Transcription failed"

        time.sleep(3)

# ---------------- OPENAI API ---------------- #

def call_openai(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful AI tutor."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=body
    )

    data = response.json()

    # ✅ SAFETY CHECK
    if "choices" not in data:
        return f"❌ OpenAI API Error:\n{data.get('error', {}).get('message', 'Unknown error')}"

    return data["choices"][0]["message"]["content"]


# ---------------- UI ---------------- #

st.title("🎧 AI Lecture Notes Generator")

audio_file = st.file_uploader("Upload lecture audio", type=["mp3", "wav"])

if st.button("Generate Notes"):
    if not audio_file:
        st.error("Upload an audio file")
    else:
        with st.spinner("🎧 Transcribing..."):
            transcript = transcribe_audio(audio_file.read())

        st.subheader("📝 Transcript")
        st.write(transcript)

        with st.spinner("📘 Generating summary..."):
            summary = call_openai(
                f"Summarize this lecture:\n\n{transcript}"
            )

        st.subheader("📘 Summary")
        st.success(summary)

        with st.spinner("🧠 Generating quiz..."):
            quiz = call_openai(
                f"Create 5 MCQs with answers from this:\n\n{summary}"
            )

        st.subheader("🧠 Quiz")
        st.write(quiz)

        st.success("✅ Done")
