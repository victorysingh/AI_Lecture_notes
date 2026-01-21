import streamlit as st
import os
from transformers import pipeline
@st.cache_resource
def load_whisper_model():
 return pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)
@st.cache_resource 
def load_summarizer():
   return pipeline("summarization",model="facebook/bart-large-cnn")
#title
st.set_page_config(
    page_title="AI Lecture Notes Generator",
    page_icon="🎧",
    layout="centered"
)

st.title("🎧 AI Lecture Notes Generator")
st.markdown("### Convert lecture audio into smart notes and quizzes using AI")
st.markdown("---")


st.divider()

#file upload
audio_file = st.file_uploader(("Upload lecture audio(mp3/WAV)"),
type=["mp3",'wav']
)

#Difficulty selector
difficulty = st.selectbox("Select difficulty level:" ,["Easy","Medium","Hard"])

# Action Buttton
generate_btn = st.button("Generate Notes")
@st.cache_resource
def load_quiz_generator():
   return pipeline("text2text-generation", model="google/flan-t5-base")
if generate_btn:

    if audio_file is None:
        st.error("❌ Please upload an audio file before generating notes.")
    
    else:
        # Save file safely
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())

        st.success("✅ Audio uploaded successfully!")
        
 #load model
        st.info("🔄 Transcribing audio...")
        st.success("✅ Audio processed successfully")
        st.info("🧠 Generating summary and quiz...")

        whisper_model = load_whisper_model()
 # #transcribe
         
        result = whisper_model("temp_audio.wav")
        transcript = result["text"]
        st.subheader("📝 Transcribed Text")
        st.write(transcript)
#load summarizer
        st.info("🧠 Generating summary...")
        summarizer = load_summarizer()

#adjust summary length based on difficulty 
        if difficulty == "Easy":
           max_len = 80
           min_len = 40
        elif difficulty == "Medium":
           max_len = 150
           min_len =80
        else:
           max_len = 250
           min_len = 120
        summary = summarizer(
           transcript,
           max_length=max_len,
           min_length=min_len,
           do_sample=False
   )  
        st.subheader("📘 AI Generated Notes")
        st.write(summary[0]["summary_text"]) 
    #genrate quiz
        st.subheader("🧠 Quiz Generated from Lecture")
        quiz_model=load_quiz_generator()
        quiz_prompt = f"""
        Generate 5 multiple choice questions based on the following text.
        Each question should have 4 options and indicate the correct answer.

        Text:
        {summary[0]["summary_text"]}
        """

        quiz = quiz_model(quiz_prompt, max_length=512)

        st.write(quiz[0]["generated_text"]) 
        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit and Hugging Face")
