AI Resume Analyser
A resume analyser that compares your resume against a job description using NLP and gives instant feedback.
Features

Upload resume (PDF)
Paste job description
Get match score (%) using TF-IDF + cosine similarity
See matched & missing skills (40+ tech skills covered)
Strengths and improvement suggestions
Rule-based summary

Setup

Install dependencies:

pip install -r requirements.txt

Run the app:

python app.py

Open browser: http://localhost:5000

Tech Stack

Python + Flask (backend)
TF-IDF + Cosine Similarity (scikit-learn)
pdfplumber (PDF extraction)
HTML/CSS/JS (frontend)

## Project Structure
```
resume-analyzer/
├── app.py              # Main Flask app (all backend logic)
├── templates/
│   └── index.html      # Frontend UI
├── requirements.txt
└── README.md
```
