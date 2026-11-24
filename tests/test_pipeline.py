"""Tests: does the screening logic behave sensibly? A tiny model is trained inside the test,
so these tests do not need your real dataset or models/resume_model.joblib."""
import random

import pytest
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from src.charts import category_chart, coverage_chart
from src.config import STUFFING_DENSITY
from src.model import analyze, screen_all, verdict
from src.recommend import generate_actions
from src.text import clean_text, extract_text

SKILLS = {
    "Data Science": "python pandas numpy machine learning statistics tensorflow sql visualization".split(),
    "HR": "recruitment onboarding payroll training interviewing talent policy employee".split(),
    "Java Developer": "java spring hibernate maven jsp servlet sql microservices rest".split(),
}
GENERIC = "team project experience responsible developed worked managed degree".split()
JD_DS = "Hiring a data scientist. Required: python pandas numpy machine learning statistics tensorflow sql"


@pytest.fixture(scope="module")
def bundle():
    rng = random.Random(0)
    texts, labels = [], []
    for cat, skills in SKILLS.items():
        for _ in range(12):
            words = rng.sample(skills, 5) + rng.choices(GENERIC, k=6)
            rng.shuffle(words)
            texts.append(" ".join(words))
            labels.append(cat)
    le = LabelEncoder().fit(labels)
    y = le.transform(labels)
    model = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression(max_iter=1000))]).fit(texts, y)
    tf = TfidfVectorizer(stop_words="english").fit([clean_text(t) for t in texts])
    km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(tf.transform([clean_text(t) for t in texts]))
    terms = tf.get_feature_names_out()
    cluster_terms = {c: terms[km.cluster_centers_[c].argsort()[-8:][::-1]].tolist() for c in range(3)}
    return dict(model=model, label_encoder=le, tfidf=tf, kmeans=km, cluster_terms=cluster_terms, model_name="test")


DS_RESUME = ("Python developer with pandas, numpy, machine learning, statistics and tensorflow. Worked on sql reports. "
             "Experience in a large team, responsible for several projects, developed dashboards for managers, "
             "completed a degree in computer science, presented results to clients and mentored new colleagues.")
HR_RESUME = "HR officer: recruitment, onboarding, payroll and training for the whole team."


def test_clean_text_removes_identifiers_and_stop_words():
    out = clean_text("Contact: ali@mail.com, +92 300 1234567, https://x.com/me. I know C++ and the Python!")
    assert "mail" not in out and "1234567" not in out and "https" not in out
    assert "c++" in out and "python" in out and "the" not in out.split()


def test_strong_and_weak_matches(bundle):
    ds = analyze(bundle, "ds", DS_RESUME, JD_DS)
    hr = analyze(bundle, "hr", HR_RESUME, JD_DS)
    assert ds.verdict == "Strong match" and ds.coverage >= 50
    assert hr.verdict == "Weak match" and hr.coverage == 0 and hr.fit_score == 0
    assert ds.category == "Data Science" and hr.category == "HR"


def test_scores_stay_in_range(bundle):
    a = analyze(bundle, "ds", DS_RESUME, JD_DS)
    assert 0 <= a.coverage <= 100 and 0 <= a.fit_score <= 100 and 0 <= a.confidence <= 100
    assert len(a.top3) == 3 and a.top3[0][0] == a.category


def test_ranking_is_best_first_and_skips_empty(bundle):
    res = screen_all(bundle, [("hr", HR_RESUME), ("empty", "!!! ..."), ("ds", DS_RESUME)], JD_DS)
    assert [r.name for r in res] == ["ds", "hr"]


def test_verdict_thresholds():
    assert verdict(80) == "Strong match" and verdict(30) == "Possible match" and verdict(5) == "Weak match"


def test_keyword_stuffing_is_flagged(bundle):
    stuffed = analyze(bundle, "stuffed", ("python pandas numpy machine learning statistics tensorflow sql " * 8), JD_DS)
    honest = analyze(bundle, "honest", DS_RESUME + " " + " ".join(GENERIC * 6), JD_DS)
    assert stuffed.stuffed and stuffed.stuffing_density >= STUFFING_DENSITY
    assert not honest.stuffed


def test_actions_shortlist_review_and_stuffing(bundle):
    res = screen_all(bundle, [("ds", DS_RESUME), ("hr", HR_RESUME),
                              ("stuffed", "python pandas numpy machine learning statistics tensorflow sql " * 8)], JD_DS)
    titles = [a.title for a in generate_actions(res)]
    assert any(t.startswith("Shortlist: ds") for t in titles)
    assert any("keyword stuffing" in t for t in titles)
    assert not any(t.startswith("Shortlist: stuffed") for t in titles)   # stuffed resumes are never shortlisted


def test_no_match_gives_guidance(bundle):
    res = screen_all(bundle, [("hr", HR_RESUME)], JD_DS)
    acts = generate_actions(res)
    assert any("No candidate matches" in a.title for a in acts)


def test_changing_the_job_changes_the_ranking(bundle):
    both = [("ds", DS_RESUME), ("hr", HR_RESUME)]
    jd_hr = "Hiring an HR executive: recruitment onboarding payroll training"
    assert screen_all(bundle, both, JD_DS)[0].name == "ds"
    assert screen_all(bundle, both, jd_hr)[0].name == "hr"


def test_extract_text_txt():
    assert extract_text(b"hello resume", "a.txt") == "hello resume"


def test_extract_text_docx():
    import io
    import docx
    d = docx.Document()
    d.add_paragraph("Python machine learning engineer")
    buf = io.BytesIO()
    d.save(buf)
    assert "machine learning" in extract_text(buf.getvalue(), "cv.docx")


def test_charts_render(bundle):
    res = screen_all(bundle, [("ds", DS_RESUME), ("hr", HR_RESUME)], JD_DS)
    assert coverage_chart(res) is not None and category_chart(res[0]) is not None
