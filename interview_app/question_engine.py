import random
from .question_bank import QUESTION_BANK

TOTAL_QUESTIONS = 10


def generate_questions(interview_type, level, language=None):
    """
    Generate 10 random interview questions dynamically
    """

    interview_type = interview_type.lower()
    level = level.lower()

    # ---------------- TECHNICAL ----------------
    if interview_type == "technical":
        if not language:
            raise ValueError("Language is required for technical interview")

        language = language.lower()
        pool = QUESTION_BANK["technical"][language][level]

    # ---------------- HR ----------------
    elif interview_type == "hr":
        pool = QUESTION_BANK["hr"]["general"][level]

    # ---------------- FUNDAMENTALS ----------------
    elif interview_type == "fundamentals":
        pool = QUESTION_BANK["fundamentals"]["general"][level]

    else:
        raise ValueError("Invalid interview type")

    # Safety check
    if len(pool) < TOTAL_QUESTIONS:
        raise ValueError("Not enough questions available")

    return random.sample(pool, TOTAL_QUESTIONS)