from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -------------------------------
# Lazy load model (VERY IMPORTANT)
# -------------------------------
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading semantic model (first time only)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# --------------------------------
# Main Evaluation Function
# --------------------------------
def evaluate_answer(user_answer, correct_answer):
    model = get_model()

    # Generate embeddings
    embeddings = model.encode([user_answer, correct_answer])

    # Cosine similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # Convert numpy.float32 → normal float (VERY IMPORTANT)
    score = float(round(float(similarity) * 100, 2))

    # Feedback Logic
    if score >= 85:
        feedback = "Excellent answer. Strong technical understanding."
    elif score >= 70:
        feedback = "Very good answer. Minor improvements possible."
    elif score >= 55:
        feedback = "Good attempt. Try to explain more clearly."
    elif score >= 40:
        feedback = "Average answer. Add more technical depth."
    else:
        feedback = "Answer needs improvement. Revise the concept properly."

    return score, feedback