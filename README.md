🧠 AI Lecture Notes Generator
📌 Problem Statement

Students often find it difficult to take notes during lectures. Important points may be missed, and revising long recordings is time-consuming. There is a need for an AI-based system that can automatically convert lecture audio into structured notes and quizzes.

💡 Solution

This project uses Artificial Intelligence and Natural Language Processing to:

Convert lecture audio into text

Summarize content into easy-to-understand notes

Generate quiz questions automatically

Allow difficulty-based learning

🛠️ Technologies Used

Python

Streamlit – UI

Hugging Face Transformers

Whisper (Speech-to-Text)

BART (Summarization)

Flan-T5 (Quiz Generation)

⚙️ Features

✔ Audio to text conversion
✔ AI-generated notes
✔ Difficulty levels (Easy / Medium / Hard)
✔ Quiz generation from lecture
✔ Simple and interactive UI

🧠 System Architecture
Audio Input
     ↓
Speech-to-Text (Whisper)
     ↓
Text Processing
     ↓
Summarization (BART)
     ↓
Quiz Generation (Flan-T5)
     ↓
Streamlit Output

🚀 How to Run the Project

Install dependencies:

pip install streamlit transformers torch torchaudio


Run the app:

streamlit run app.py


Upload an audio file and click Generate Notes

📈 Future Enhancements

PDF download of notes

Language translation

Topic-wise quizzes

User login system

Cloud deployment

👨‍💻 Author

Jaipreet singh
AI & ML Internship Project