from flask import Flask, request, jsonify, render_template
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# -------- SKILLS --------
SKILL_KEYWORDS = {
    "python", "java", "sql", "html", "css", "javascript", "flask", "django",
    "react", "nodejs", "mysql", "postgresql", "mongodb", "git", "linux",
    "docker", "aws", "rest", "api", "machine learning", "deep learning",
    "tensorflow", "pandas", "numpy", "excel", "tableau", "c", "c++",
    "spring", "hibernate", "selenium", "jira", "agile", "scrum", "networking","oop", "jdbc", "debugging", "troubleshooting",
"dns", "tcp", "ip", "servicenow"
}

# -------- CORE FUNCTIONS --------

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def clean_text(text):
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())

def get_match_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([clean_text(resume_text), clean_text(jd_text)])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 1)

def get_keywords(text):
    text = clean_text(text)
    found = set()

    for skill in SKILL_KEYWORDS:
        skill_clean = skill.replace(" ", "")
        text_clean = text.replace(" ", "")

        if skill in text or skill_clean in text_clean:
            found.add(skill)

    return found
def keyword_analysis(resume_text, jd_text):
    resume_skills = get_keywords(resume_text)
    jd_skills = get_keywords(jd_text)
    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    return matched, missing

def get_final_score(resume_text, jd_text):
    tfidf_score = get_match_score(resume_text, jd_text)
    matched, missing = keyword_analysis(resume_text, jd_text)

    if len(matched) + len(missing) == 0:
        keyword_score = 0
    else:
        keyword_score = (len(matched) / (len(matched) + len(missing))) * 100

    final_score = (0.3 * tfidf_score) + (0.7 * keyword_score)
    return round(final_score, 1)

# -------- RULE-BASED SUGGESTIONS --------

def get_suggestions(score, matched, missing, resume_text):
    strengths = []
    improvements = []

    if len(matched) >= 5:
        strengths.append(f"Strong skill alignment — {len(matched)} matching skills found")
    elif len(matched) >= 2:
        strengths.append(f"Partial skill match — {len(matched)} relevant skills present")

    if score >= 60:
        strengths.append("Resume content closely aligns with job requirements")

    if "python" in matched or "java" in matched:
        strengths.append("Core programming language matches the JD")

    if "sql" in matched:
        strengths.append("Database skills (SQL) are relevant")

    if "git" in matched:
        strengths.append("Version control (Git) experience is a plus")

    if not strengths:
        strengths.append("Resume has some relevant keywords")

    # Improvements
    if missing:
        improvements.append(f"Add missing skills: {', '.join(missing[:4])}")

    if score < 40:
        improvements.append("Resume needs strong alignment with JD")
    elif score < 65:
        improvements.append("Improve wording using JD keywords")

    if "git" in missing:
        improvements.append("Learn Git basics")

    if "sql" in missing:
        improvements.append("Add SQL project experience")

    if not improvements:
        improvements.append("Fine-tune resume content")

    # Summary
    if score >= 70:
        summary = f"Strong match ({score}%). Apply confidently."
    elif score >= 40:
        summary = f"Moderate match ({score}%). Improve skills and wording."
    else:
        summary = f"Weak match ({score}%). Needs improvement."

    return strengths[:3], improvements[:3], summary

# -------- ROUTES --------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyse", methods=["POST"])
def analyse():
    try:
        file = request.files.get("resume")
        jd = request.form.get("jd", "").strip()

        if not file or not jd:
            return jsonify({"error": "Upload resume and enter JD"}), 400

        if not file.filename.endswith(".pdf"):
            return jsonify({"error": "Only PDF allowed"}), 400

        resume_text = extract_text(file)

        if not resume_text.strip():
            return jsonify({"error": "PDF text not readable"}), 400

        # Step 1: keyword analysis
        matched, missing = keyword_analysis(resume_text, jd)

        # Step 2: debug prints
        tfidf_score = get_match_score(resume_text, jd)
        print("TF-IDF Score:", tfidf_score)
        print("Matched Skills:", matched)
        print("Missing Skills:", missing)

        # Step 3: final score
        score = get_final_score(resume_text, jd)

        # Step 4: suggestions
        strengths, improvements, summary = get_suggestions(score, matched, missing, resume_text)

        return jsonify({
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "strengths": strengths,
            "improvements": improvements,
            "summary": summary
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

# -------- RUN --------

if __name__ == "__main__":
    app.run(debug=True)