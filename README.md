🧠 AI Lecture Notes Generator
📌 Problem Statement

Students often struggle to take proper notes during lectures. Important concepts may be missed, and revising long audio recordings is time-consuming. There is a need for an intelligent system that can automatically convert lecture audio into structured notes and generate quizzes for effective learning.

💡 Solution

This project uses Artificial Intelligence and Natural Language Processing (NLP) to:

Convert lecture audio into text

Summarize the lecture into clear notes

Automatically generate quiz questions

Provide an easy-to-use web interface

The system uses Hugging Face Inference APIs, making it lightweight and cloud-deployable without heavy ML installations.

🛠️ Technologies Used
Technology	Purpose
Python	Core programming language
Streamlit	Web application framework
Hugging Face API	AI model inference
Whisper	Speech-to-text conversion
BART	Text summarization
FLAN-T5	Quiz generation
Requests	API communication
⚙️ Features

✔ Upload lecture audio (MP3/WAV)
✔ Convert speech to text
✔ Generate AI-based summary
✔ Automatically generate quiz questions
✔ Simple and clean UI
✔ Works on Streamlit Cloud
✔ No local ML model installation required

🧠 System Architecture
Audio Input
     ↓
Speech-to-Text (Whisper API)
     ↓
Text Processing
     ↓
Summarization (BART API)
     ↓
Quiz Generation (FLAN-T5 API)
     ↓
Streamlit Web Interface

🚀 How to Run the Project
🔹 Step 1: Clone the Repository
git clone https://github.com/your-username/AI_Lecture_notes.git
cd AI_Lecture_notes

🔹 Step 2: Install Dependencies
pip install streamlit requests

🔹 Step 3: Create Hugging Face Token

Go to: https://huggingface.co/settings/tokens

Create a Read Access Token

Copy the token

🔹 Step 4: Add Token to Streamlit

In Streamlit Cloud → Manage App → Secrets, add:

HF_TOKEN = "your_huggingface_token"

🔹 Step 5: Run the App
streamlit run app.py

📈 Future Enhancements

🔹 Download notes as PDF
🔹 Language translation
🔹 Topic-wise quiz generation
🔹 User login system
🔹 Progress tracking
🔹 Deployment on Hugging Face Spaces

👨‍💻 Author

Jaipreet Singh
AI & ML Internship Project