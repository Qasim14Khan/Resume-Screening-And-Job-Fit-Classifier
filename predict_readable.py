"""Predict a resume's field using ONLY models/resume_model_readable.py (plain Python numbers).

Run:  python predict_readable.py                 (uses a demo resume)
      python predict_readable.py resume.txt      (uses your text file)
No scikit-learn and no joblib are used for the prediction itself. If the joblib model exists, the result
is compared with it, to show both give the same answer.
"""
import math
import re
import sys

sys.path.insert(0, "models")
import resume_model_readable as M            # the plain-Python model

from src.text import clean_text              # same cleaning as training

TOKEN = re.compile(r"(?u)\b\w\w+\b")          # same word pattern as scikit-learn's TfidfVectorizer


def predict(text, top=3):
    words = TOKEN.findall(clean_text(text))
    lo, hi = M.NGRAM_RANGE
    grams = [" ".join(words[i:i + n]) for n in range(lo, hi + 1) for i in range(len(words) - n + 1)]
    index = {w: i for i, w in enumerate(M.VOCABULARY)}
    counts = {}
    for g in grams:
        if g in index:
            counts[index[g]] = counts.get(index[g], 0) + 1
    # TF-IDF: (1 + log count) * idf, then scale so the vector has length 1
    x = {i: ((1 + math.log(c)) if M.SUBLINEAR_TF else c) * M.IDF[i] for i, c in counts.items()}
    norm = math.sqrt(sum(v * v for v in x.values())) or 1.0
    x = {i: v / norm for i, v in x.items()}
    scores = [sum(row[i] * v for i, v in x.items()) + b for row, b in zip(M.COEF, M.INTERCEPT)]
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    probs = [e / sum(exps) for e in exps]
    best = sorted(range(len(probs)), key=lambda k: -probs[k])[:top]
    return [(M.CLASSES[k], probs[k]) for k in best]


DEMO = ("Python developer with pandas, numpy, machine learning, statistics and tensorflow. "
        "Built models in scikit-learn and wrote SQL reports. Degree in computer science.")
if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8", errors="ignore").read() if len(sys.argv) > 1 else DEMO
    print("Prediction from the plain-Python model file:")
    for name, p in predict(text):
        print(f"  {name:28s} {100 * p:5.1f}%")
    try:
        import joblib
        from sklearn.metrics import accuracy_score  # noqa: F401  (only to check scikit-learn exists)
        pipe = joblib.load("models/resume_model.joblib")
        proba = pipe["model"].predict_proba([clean_text(text)])[0]
        best = proba.argmax()
        print(f"Same text with the joblib model: {pipe['label_encoder'].classes_[best]} {100 * proba[best]:.1f}%")
    except Exception as e:  # joblib model or scikit-learn not available: that is fine
        print("(joblib comparison skipped:", type(e).__name__, ")")
