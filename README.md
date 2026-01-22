📘 AI Lecture Notes Generator
📌 Problem Statement

Students often struggle to take proper notes during lectures. Important concepts may be missed, and revising long audio recordings is time-consuming. There is a need for an intelligent system that can automatically convert lecture audio into structured notes and generate quizzes for effective learning.

💡 Solution

This project uses Artificial Intelligence and Natural Language Processing (NLP) to:

Convert lecture audio into text

Generate concise, easy-to-understand summaries

Automatically create quiz questions

Provide a clean and interactive web interface

The system is cloud-based, lightweight, and does not require local ML model installation.

🛠️ Technologies Used
Technology	Purpose
Python	Core programming
Streamlit	Web interface
AssemblyAI API	Speech-to-Text
Hugging Face API	Text summarization & quiz generation
BART	Lecture summarization
FLAN-T5	Quiz generation
Requests	API communication
⚙️ Features

✔ Upload lecture audio (MP3 / WAV)
✔ Convert speech to text automatically
✔ Generate AI-based lecture summary
✔ Create quiz questions from content
✔ Simple and clean UI
✔ Works on Streamlit Cloud
✔ No heavy ML installation required

🧠 System Architecture
Audio Input
     ↓
Speech-to-Text (AssemblyAI)
     ↓
Text Processing
     ↓
Summarization (BART - Hugging Face)
     ↓
Quiz Generation (FLAN-T5)
     ↓
Streamlit Web Interface

🚀 How to Run the Project
🔹 Step 1: Clone the Repository
git clone https://github.com/your-username/AI_Lecture_notes.git
cd AI_Lecture_notes

🔹 Step 2: Install Dependencies
pip install streamlit requests

🔹 Step 3: Create API Keys
✅ AssemblyAI Key

Go to: https://www.assemblyai.com/

Create an account

Copy API key

✅ Hugging Face Token

Go to: https://huggingface.co/settings/tokens

Create Read Access Token

🔹 Step 4: Add Secrets (Streamlit Cloud)

In Streamlit → Manage App → Secrets, add:

ASSEMBLY_API_KEY = "your_assemblyai_key"
HF_TOKEN = "your_huggingface_token"

🔹 Step 5: Run the App
streamlit run app.py

📸 Screenshots (Add in PPT / README)

📌 Recommended screenshots:

Home screen

Audio upload screen

Transcript output

Summary output

Quiz generation

(Add these in Results / Output slide)

📈 Future Enhancements

🔹 Download notes as PDF
🔹 Multi-language support
🔹 Topic-wise quizzes
🔹 User authentication
🔹 Progress tracking
🔹 Deployment on Hugging Face Spaces

👨‍💻 Author

Jaipreet Singh
AI & ML Internship Project