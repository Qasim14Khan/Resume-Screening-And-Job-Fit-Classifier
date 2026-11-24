"""Screening logic: predict the category, find the skill cluster, score the fit to a job."""
from __future__ import annotations

from dataclasses import dataclass, field

import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .config import (CHART_COLOR, LOW_CONFIDENCE, POSSIBLE_COVERAGE, STATUS_COLOR, STRONG_COVERAGE,
                     STUFFING_DENSITY)
from .text import clean_text

# Words that appear in almost every job ad but are not skills; they are ignored when reading the job description.
JD_FILLER = {"hiring", "required", "requirements", "looking", "seeking", "candidate", "responsibilities",
             "ability", "preferred", "must", "role", "position", "job", "join", "team"}


@dataclass
class Screening:
    """Result of screening ONE resume against ONE job description."""
    name: str
    category: str                 # model's guess of the resume's field (does not depend on the job)
    confidence: float             # % probability of that category
    top3: list                    # [(category, %), ...]
    cluster: int
    cluster_terms: list
    fit_score: float              # cosine similarity, %
    coverage: float               # % of the job's keyword weight found in the resume
    matched: list = field(default_factory=list)
    missing: list = field(default_factory=list)
    stuffing_density: float = 0.0
    verdict: str = "Weak match"

    @property
    def color(self) -> str:
        return STATUS_COLOR[self.verdict]

    @property
    def chart_color(self) -> str:
        return CHART_COLOR[self.verdict]

    @property
    def stuffed(self) -> bool:
        return self.stuffing_density >= STUFFING_DENSITY

    @property
    def unsure(self) -> bool:
        return self.confidence < LOW_CONFIDENCE


def load_bundle(path: str = "models/resume_model.joblib") -> dict:
    return joblib.load(path)


def verdict(coverage: float) -> str:
    """Plain-language label from job-keyword coverage (%)."""
    if coverage >= STRONG_COVERAGE:
        return "Strong match"
    if coverage >= POSSIBLE_COVERAGE:
        return "Possible match"
    return "Weak match"


def _probabilities(model, cleaned: str) -> np.ndarray:
    """Class probabilities. Uses predict_proba (LogReg, Naive Bayes, calibrated SVM) or a softmax fallback."""
    if hasattr(model, "predict_proba"):
        return model.predict_proba([cleaned])[0]
    d = model.decision_function([cleaned])[0]
    e = np.exp(d - d.max())
    return e / e.sum()


def analyze(bundle: dict, name: str, resume_text: str, jd_text: str):
    """Screen one resume. Returns None if the resume has no readable text."""
    model, le, tf, km = bundle["model"], bundle["label_encoder"], bundle["tfidf"], bundle["kmeans"]
    r = clean_text(resume_text)
    j = " ".join(w for w in clean_text(jd_text).split() if w not in JD_FILLER)
    if not r:
        return None
    p = _probabilities(model, r)
    top = np.argsort(p)[::-1][:3]
    v = tf.transform([r, j])
    terms = np.array(tf.get_feature_names_out())
    rv, jv = v[0].toarray()[0], v[1].toarray()[0]
    score = float(cosine_similarity(v[0], v[1])[0, 0]) * 100
    coverage = float(jv[rv > 0].sum() / jv.sum()) * 100 if jv.sum() > 0 else 0.0
    matched = terms[(rv > 0) & (jv > 0)].tolist()
    missing_idx = [i for i in np.argsort(jv)[::-1] if jv[i] > 0 and rv[i] == 0][:10]
    jd_words = set(j.split())
    words = r.split()
    density = sum(w in jd_words for w in words) / len(words)
    cl = int(km.predict(v[0])[0])
    return Screening(
        name=name, category=str(le.classes_[top[0]]), confidence=float(p[top[0]]) * 100,
        top3=[(str(le.classes_[i]), float(p[i]) * 100) for i in top],
        cluster=cl, cluster_terms=list(bundle["cluster_terms"][cl][:6]),
        fit_score=score, coverage=coverage, matched=matched, missing=terms[missing_idx].tolist(),
        stuffing_density=density, verdict=verdict(coverage),
    )


def screen_all(bundle: dict, resumes, jd_text: str) -> list:
    """resumes: list of (name, text). Returns Screenings sorted best first (coverage, then fit score)."""
    out = [a for name, text in resumes if (a := analyze(bundle, name, text, jd_text)) is not None]
    return sorted(out, key=lambda a: (-a.coverage, -a.fit_score))
