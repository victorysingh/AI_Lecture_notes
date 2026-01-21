import streamlit as st
import requests

st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

HF_TOKEN = st.secrets["HF_TOKEN"]

SUMMARY_API = "https://router.huggingface.co/hf-inference/models/t5-small"
QUIZ_API = "https://router.huggingface.co/hf-inference/models/google/flan-t5-small"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ---------------- FUNCTIONS ---------------- #

def summarize_text(text):
    response = requests.post(
        SUMMARY_API,
        headers=HEADERS,
        json={"inputs": text}
    )
    return response.json()[0]["generated_text"]

def generate_quiz(text):
    prompt = f"""
Create 5 multiple choice questions from the following text.
Each question should have 4 options and mention the correct answer.

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
st.markdown("### Convert lecture content into notes & quizzes using AI")

st.divider()

lecture_text = st.text_area(
    "📘 Paste your lecture content here:",
    height=250,
    placeholder="Paste lecture text here..."
)

if st.button("Generate Notes"):
    if not lecture_text.strip():
        st.error("Please enter lecture text")
    else:
        with st.spinner("🧠 Generating summary..."):
            summary = summarize_text(lecture_text)

        st.subheader("📘 AI Generated Notes")
        st.success(summary)

        with st.spinner("🧩 Generating quiz..."):
            quiz = generate_quiz(summary)

        st.subheader("🧠 Quiz")
        st.write(quiz)

        st.success("✅ Successfully Generated")
