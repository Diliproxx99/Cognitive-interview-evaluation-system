from django.shortcuts import render, redirect
from PyPDF2 import PdfReader
from docx import Document

from .question_engine import generate_questions


# ---------------- WELCOME ----------------
def welcome(request):
    return render(request, "interview_app/welcome.html")


# ---------------- RESUME UPLOAD ----------------
def resume_upload(request):
    return render(request, "interview_app/resume_upload.html")


# ---------------- RESUME ANALYSIS ----------------
def analyze_resume(request):

    if request.method != "POST":
        return redirect("resume_upload")

    resume_file = request.FILES.get("resume")
    if not resume_file:
        return redirect("resume_upload")

    text = ""

    if resume_file.name.endswith(".pdf"):
        reader = PdfReader(resume_file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    elif resume_file.name.endswith(".docx"):
        doc = Document(resume_file)
        for p in doc.paragraphs:
            text += p.text

    text = text.lower()

    skill_db = [
        "python", "java", "c", "sql", "django",
        "html", "css", "javascript",
        "communication", "teamwork", "leadership"
    ]

    extracted = [s.upper() for s in skill_db if s in text]

    if len(extracted) >= 8:
        level = "Advanced"
    elif len(extracted) >= 4:
        level = "Intermediate"
    else:
        level = "Beginner"

    request.session["skills"] = extracted
    request.session["level"] = level

    return render(request, "interview_app/analysis_result.html", {
        "skills": extracted,
        "level": level
    })


# ---------------- INTERVIEW SETUP ----------------
def interview_setup(request):
    return render(request, "interview_app/interview_setup.html", {
        "level": request.session.get("level", "Beginner")
    })


# ---------------- START INTERVIEW ----------------
def start_interview(request):

    if request.method != "POST":
        return redirect("interview_setup")

    questions = generate_questions(
        interview_type=request.POST.get("interview_type"),
        level=request.POST.get("difficulty"),
        language=request.POST.get("language")
    )

    request.session["questions"] = questions
    request.session["current_index"] = 0
    request.session["answers"] = []
    request.session["mode"] = request.POST.get("mode")

    return redirect("countdown")


# ---------------- COUNTDOWN ----------------
def countdown(request):
    return render(request, "interview_app/countdown.html")


# ---------------- INTERVIEW QUESTION ----------------
def interview_question(request):

    questions = request.session.get("questions", [])
    index = request.session.get("current_index", 0)
    answers = request.session.get("answers", [])
    mode = request.session.get("mode", "text")

    if not questions or index >= len(questions):
        return redirect("interview_complete")

    question = questions[index]

    if request.method == "POST":

        answer = request.POST.get("answer", "").strip()

        # Voice validation
        if mode == "voice" and len(answer.split()) < 3:
            return render(request, "interview_app/interview_question.html", {
                "question": question,
                "number": index + 1,
                "mode": mode,
                "error": "Please speak clearly (minimum 3 words)."
            })

        answers.append({
            "question": question,
            "answer": answer
        })

        request.session["answers"] = answers
        request.session["current_index"] = index + 1

        return redirect("interview_question")

    return render(request, "interview_app/interview_question.html", {
        "question": question,
        "number": index + 1,
        "mode": mode
    })


# ---------------- INTERVIEW COMPLETE ----------------
def interview_complete(request):

    questions = request.session.get("questions", [])
    answers = request.session.get("answers", [])

    total = len(questions)
    answered = len(answers)

    total_score = 0
    detailed_feedback = []

    for item in answers:

        answer = item["answer"]

        # ✅ SIMPLE LOGIC (NO ERROR NOW)

        if answer.strip() == "":
            score = 0
            comment = "Not attempted"

        elif len(answer.split()) > 8:
            score = 1
            comment = "Good answer"

        elif len(answer.split()) > 3:
            score = 0.5
            comment = "Average answer"

        else:
            score = 0
            comment = "Too short"

        total_score += score

        detailed_feedback.append({
            "question": item["question"],
            "answer": answer,
            "score": score,
            "comment": comment
        })

    percentage = round((total_score / total) * 100, 2) if total else 0

    confidence = (
        "High" if percentage >= 75 else
        "Medium" if percentage >= 40 else
        "Low"
    )

    return render(request, "interview_app/interview_complete.html", {
        "total": total,
        "answered": answered,
        "score": round(total_score, 1),
        "percentage": percentage,
        "confidence": confidence,
        "feedback": detailed_feedback
    })