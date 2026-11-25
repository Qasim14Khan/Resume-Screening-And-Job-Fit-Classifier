"""Show what is inside models/resume_model.joblib (useful to explain the saved model in the viva).

Run:  python inspect_model.py
It prints the summary and also saves it as results/model_summary.txt, a readable file for GitHub.
"""
import builtins
import os

import joblib
import numpy as np

PATH = "models/resume_model.joblib"
_lines = []


def print(*args, **kwargs):          # print to the screen AND remember the text
    builtins.print(*args, **kwargs)
    _lines.append(" ".join(str(a) for a in args))


bundle = joblib.load(PATH)

print(f"File: {PATH}  ({os.path.getsize(PATH) / 1024:.0f} KB)")
print("\nThe file is ONE Python dictionary (saved with joblib) with these keys:")
for k, v in bundle.items():
    print(f"  {k:15s} -> {type(v).__name__}")

model, le = bundle["model"], bundle["label_encoder"]
print(f"\n1) model_name: {bundle['model_name']}")
print("\n2) model: a scikit-learn Pipeline with these steps:")
for name, step in model.named_steps.items():
    print(f"   - {name}: {step}")
tfidf, clf = model.named_steps["tfidf"], model.named_steps["clf"]
print(f"   TF-IDF vocabulary size: {len(tfidf.vocabulary_)} words/phrases")
if hasattr(clf, "coef_"):
    print(f"   Classifier weights shape: {clf.coef_.shape}  (categories x words)")

print(f"\n3) label_encoder: turns {len(le.classes_)} category names into numbers 0..{len(le.classes_) - 1}")
print("   Categories:", ", ".join(le.classes_))

if hasattr(clf, "coef_"):
    vocab = np.array(tfidf.get_feature_names_out())
    print("\n   Strongest words the model learned for 3 categories:")
    for cat in list(le.classes_)[:3]:
        i = list(le.classes_).index(cat)
        print(f"   {cat}: {', '.join(vocab[np.argsort(clf.coef_[i])[-6:][::-1]])}")

km = bundle["kmeans"]
print(f"\n4) kmeans: K-Means with {km.n_clusters} clusters (skill groups)")
print(f"5) tfidf (second one, for clustering and job-fit scoring): {len(bundle['tfidf'].vocabulary_)} words")
print("6) cluster_terms: top words of each cluster, for example")
for c in list(bundle["cluster_terms"])[:3]:
    print(f"   Cluster {c}: {', '.join(bundle['cluster_terms'][c][:6])}")

print("\nNote: the file holds learned numbers and vocabulary, NOT the training resumes.")

os.makedirs("results", exist_ok=True)
with open("results/model_summary.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(_lines) + "\n")
builtins.print("\nSaved results/model_summary.txt")
