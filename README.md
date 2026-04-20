# AI Resume Analyser

An AI-powered resume analyser that compares your resume against a job description and gives instant feedback.

## Features
- Upload resume (PDF)
- Paste job description
- Get match score (%)
- See matched & missing skills
- Strengths and improvement suggestions
- AI-generated summary

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set your Anthropic API key:
```
# Windows
set ANTHROPIC_API_KEY=your_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_key_here
```

3. Run the app:
```
python app.py
```

4. Open browser: `http://localhost:5000`

## Tech Stack
- Python + Flask (backend)
- Claude AI API (analysis)
- pdfplumber (PDF extraction)
- HTML/CSS/JS (frontend)

## Project Structure
```
resume-analyzer/
├── app.py              # Main Flask app (all backend logic)
├── templates/
│   └── index.html      # Frontend UI
├── requirements.txt
└── README.md
```
