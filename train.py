"""Train the resume classifier from the CSV and save everything the dashboard needs.

Run:  python train.py
Reads  Data/UpdatedResumeDataSet.csv  (columns: Category, Resume)
Writes models/resume_model.joblib, results/metrics.json, results/per_category_report.csv
This is the same pipeline as the notebook, as a script, so the dashboard works without re-running the notebook.
"""
import glob
import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, adjusted_rand_score, classification_report,
                             normalized_mutual_info_score, precision_recall_fscore_support, silhouette_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from src.text import clean_text

SEED = 42


def find_csv():
    for pattern in ("Data/*.csv", "data/*.csv", "*.csv"):
        for path in sorted(glob.glob(pattern)):
            if "own_resumes" in path:
                continue
            cols = pd.read_csv(path, nrows=1).columns
            if {"Category", "Resume"} <= set(cols):
                return path
    sys.exit("Could not find the dataset. Put UpdatedResumeDataSet.csv in a folder called Data next to train.py.")


path = find_csv()
df = pd.read_csv(path)[["Category", "Resume"]].dropna()
n0 = len(df)
df = df.drop_duplicates(subset="Resume").reset_index(drop=True)
df["clean"] = df["Resume"].map(clean_text)
df = df[df["clean"].str.len() > 0].reset_index(drop=True)
print(f"{path}: {n0} rows -> {len(df)} unique resumes, {df['Category'].nunique()} categories")

le = LabelEncoder()
y = le.fit_transform(df["Category"])
X_tr, X_te, y_tr, y_te = train_test_split(df["clean"], y, test_size=0.2, stratify=y, random_state=SEED)


def make(clf):
    return Pipeline([("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), sublinear_tf=True)), ("clf", clf)])


models = {
    "Logistic Regression": (make(LogisticRegression(max_iter=1000)), {"clf__C": [0.1, 1, 10]}),
    "Naive Bayes": (make(MultinomialNB()), {"clf__alpha": [0.1, 0.5, 1.0]}),
}
min_class = int(np.bincount(y_tr).min())
cv = max(2, min(5, min_class))   # every fold needs at least one resume of each category
print(f"Smallest category in training: {min_class} resumes -> using {cv}-fold cross-validation")
res, best_est = {}, {}
for name, (pipe, grid) in models.items():
    before = accuracy_score(y_te, pipe.fit(X_tr, y_tr).predict(X_te))
    gs = GridSearchCV(pipe, grid, cv=cv, scoring="accuracy", n_jobs=-1).fit(X_tr, y_tr)
    est = gs.best_estimator_
    p = est.predict(X_te)
    pr, rc, f1, _ = precision_recall_fscore_support(y_te, p, average="macro", zero_division=0)
    res[name] = dict(best_params={k.split("__")[1]: v for k, v in gs.best_params_.items()},
                     cv_accuracy=round(float(gs.best_score_), 4), acc_before_tuning=round(before, 4),
                     acc_after_tuning=round(accuracy_score(y_te, p), 4),
                     train_accuracy=round(accuracy_score(y_tr, est.predict(X_tr)), 4),
                     precision=round(pr, 4), recall=round(rc, 4), f1=round(f1, 4))
    best_est[name] = est
    print(f"{name:20s} CV {res[name]['cv_accuracy']}  test {res[name]['acc_after_tuning']}")

best_name = max(res, key=lambda m: res[m]["cv_accuracy"])
best = best_est[best_name]

# Logistic Regression and Naive Bayes both give real class probabilities, so no calibration is needed.
final, final_name = best, best_name

# Top words per category (Logistic Regression coefficients)
lr = best_est["Logistic Regression"]
vocab = np.array(lr["tfidf"].get_feature_names_out())
top_words = {str(le.classes_[i]): vocab[np.argsort(lr["clf"].coef_[i])[-8:][::-1]].tolist()
             for i in range(len(le.classes_))}

# K-Means skill clusters
tf = TfidfVectorizer(max_features=3000, stop_words="english", sublinear_tf=True)
Xall = tf.fit_transform(df["clean"])
terms = np.array(tf.get_feature_names_out())
Ks = list(range(2, min(31, len(df))))
sil = [silhouette_score(Xall, KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(Xall)) for k in Ks]
best_k = Ks[int(np.argmax(sil))]
km = KMeans(n_clusters=best_k, n_init=10, random_state=SEED).fit(Xall)
cluster_terms = {c: terms[np.argsort(km.cluster_centers_[c])[-8:][::-1]].tolist() for c in range(best_k)}

os.makedirs("models", exist_ok=True)
os.makedirs("results", exist_ok=True)
joblib.dump(dict(model=final, label_encoder=le, tfidf=tf, kmeans=km, cluster_terms=cluster_terms,
                 model_name=final_name), "models/resume_model.joblib")
metrics = dict(n_resumes=len(df), n_categories=int(df["Category"].nunique()), removed_duplicates_or_empty=n0 - len(df),
               cv_folds=cv, classification=res, best_model=best_name, deployed_model=final_name,
               deployed_test_accuracy=round(accuracy_score(y_te, final.predict(X_te)), 4),
               top_words_per_category=top_words,
               clustering=dict(best_k=best_k, silhouette=round(max(sil), 4),
                               kmeans_ARI=round(adjusted_rand_score(y, km.labels_), 4),
                               kmeans_NMI=round(normalized_mutual_info_score(y, km.labels_), 4)))
json.dump(metrics, open("results/metrics.json", "w"), indent=2, default=str)
rep = classification_report(y_te, final.predict(X_te), labels=range(len(le.classes_)),
                            target_names=le.classes_, output_dict=True, zero_division=0)
pd.DataFrame(rep).T.round(3).to_csv("results/per_category_report.csv")
print("Saved models/resume_model.joblib and results/metrics.json. Deployed model:", final_name)
