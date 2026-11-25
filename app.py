"""Resume Screening & Job-Fit Classifier - Streamlit dashboard.

Run with:  streamlit run app.py
"""
import glob
import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.charts import category_chart, coverage_chart
from src.config import POSSIBLE_COVERAGE, STRONG_COVERAGE
from src.model import load_bundle, screen_all
from src.presets import JOB_PRESETS
from src.recommend import generate_actions
from src.text import extract_text

st.set_page_config(page_title="Resume Screening & Job-Fit", page_icon="📄", layout="wide")

MODEL_PATH = "models/resume_model.joblib"
SAMPLE_DIR = "sample_resumes"


@st.cache_resource
def get_bundle():
    return load_bundle(MODEL_PATH)


def true_category(file_name: str) -> str:
    """Sample files are named like Data_Science_1.txt, so the true field is in the name (demo mode only)."""
    return file_name.rsplit(".", 1)[0].rsplit("_", 1)[0].replace("_", " ")


def add_resume():
    """Callback for the 'Add a resume' form."""
    name = st.session_state["new_name"].strip() or f"Pasted resume {len(st.session_state.get('extra', [])) + 1}"
    text = st.session_state["new_text"]
    if text.strip():
        st.session_state.setdefault("extra", []).append((name, text))
        st.session_state["added_msg"] = f"'{name}' added and screened."


if not os.path.exists(MODEL_PATH):
    st.error("Model not found (models/resume_model.joblib). Open a terminal in this folder and run:  python train.py")
    st.info("train.py reads Data/UpdatedResumeDataSet.csv, trains the model and saves it. Then refresh this page.")
    st.stop()
bundle = get_bundle()

# ---------------------------------------------------------------- sidebar
st.sidebar.title("📄 Resume Screening")
st.sidebar.caption("Rank resumes against a job and see what to do next")
preset = st.sidebar.selectbox("Job title", list(JOB_PRESETS))
jd = JOB_PRESETS[preset]
st.sidebar.text_area("Job description", value=jd, height=170, disabled=True, key=f"jd_{preset}")
use_samples = st.sidebar.checkbox("Also include the sample resumes", value=False,
                                  help="Loads the PDF/DOCX/TXT resumes from the sample_resumes folder so the dashboard is never empty.")
demo_mode = st.sidebar.checkbox("Demo mode: show true field from file name", value=False,
                                help="For the sample files only. Lets you check the model's predicted field against the truth.")
st.sidebar.info("Decision support only. A human recruiter makes the final decision.")

st.title("Resume Screening & Job-Fit Classifier")
st.write("**Upload a resume** (PDF, DOCX or TXT). Pick the job in the sidebar. You get the predicted field, "
         "how well the resume fits the job, what is missing, and what to do next.")
uploads = st.file_uploader("Upload one or more resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)

resumes = []
if use_samples:
    for path in sorted(glob.glob(os.path.join(SAMPLE_DIR, "*.*"))):
        if path.lower().endswith((".pdf", ".docx", ".txt")):
            with open(path, "rb") as fh:
                resumes.append((os.path.basename(path), extract_text(fh.read(), path)))
resumes += [(f.name, extract_text(f.read(), f.name)) for f in uploads]
resumes += st.session_state.get("extra", [])

# ---------------------------------------------------------------- header
results = screen_all(bundle, resumes, jd) if resumes and jd.strip() else []
if resumes and len(results) < len(resumes):
    st.warning("Some files had no readable text (a scanned PDF is an image, not text). Use a text-based PDF, DOCX or TXT.")
st.caption(f"{preset} · {len(results)} resumes screened · model: {bundle.get('model_name', 'n/a')}")

tab_report, tab_overview, tab_cands, tab_insights, tab_add, tab_perf, tab_about = st.tabs(
    ["Resume report", "Overview", "Candidates", "Insights", "Add a resume", "Model performance", "About"])

# ---------------------------------------------------------------- resume report (one full report per resume)
with tab_report:
    if not results:
        st.info("Upload a resume above to see its report.")
    for r in results:
        with st.container(border=True):
            st.markdown(f"### {r.name}")
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown("**Verdict for this job**")
            c1.markdown(f"## :{r.color}[{r.verdict}]")
            c2.metric("Keyword coverage", f"{r.coverage:.0f}%")
            c3.metric("Fit score", f"{r.fit_score:.1f}%")
            c4.metric("Predicted field", r.category, f"{r.confidence:.0f}% confident", delta_color="off")
            left, right = st.columns(2)
            fig = category_chart(r)
            left.pyplot(fig)
            plt.close(fig)
            left.caption(f"Skill cluster C{r.cluster}: {', '.join(r.cluster_terms)}")
            right.markdown("**Skills that match the job**")
            right.write(", ".join(r.matched[:15]) or "none")
            right.markdown("**Important job keywords missing**")
            right.write(", ".join(r.missing) or "none")
            for a in generate_actions([r]):
                text = f"**{a.title}**  \n{a.detail}  \n**Action:** {a.action}"
                {"red": st.error, "yellow": st.warning, "green": st.success}.get(a.severity, st.info)(text)
            if demo_mode:
                truth = true_category(r.name)
                st.caption(f"True field from file name: {truth} " + ("✓ model correct" if truth == r.category else "✗ model differs"))

# ---------------------------------------------------------------- overview
with tab_overview:
    if not results:
        st.info("Upload a resume above (or tick 'Also include the sample resumes' in the sidebar).")
    else:
        actions = generate_actions(results)
        top = results[0]
        n_strong = sum(r.verdict == "Strong match" for r in results)
        n_possible = sum(r.verdict == "Possible match" for r in results)
        n_flags = sum(r.stuffed or r.unsure for r in results)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Resumes screened", len(results))
        c2.markdown("**Best candidate**")
        c2.markdown(f"## :{top.color}[{top.verdict}]")
        c2.caption(top.name)
        c3.metric("Strong matches", n_strong, f"{n_possible} possible", delta_color="off")
        c4.metric("Resumes to check by hand", n_flags, "keyword stuffing or unsure model", delta_color="off")

        st.subheader("Top candidates")
        cols = st.columns(min(3, len(results)))
        for col, r in zip(cols, results[:3]):
            with col:
                st.markdown(f"**{r.name}**")
                st.markdown(f"### :{r.color}[{r.verdict}]")
                st.caption(f"Keyword coverage {r.coverage:.0f}% · fit score {r.fit_score:.1f}%")
                st.caption(f"Predicted field: {r.category} ({r.confidence:.0f}%)")
                if r.matched:
                    st.caption("Matches: " + ", ".join(r.matched[:5]))

        st.subheader("What to do now")
        if not actions:
            st.success("Nothing needs attention.")
        for a in actions:
            text = f"**{a.title}**  \n{a.detail}  \n**Action:** {a.action}"
            {"red": st.error, "yellow": st.warning, "green": st.success}.get(a.severity, st.info)(text)

        st.subheader("Job keyword coverage by candidate")
        fig = coverage_chart(results)
        st.pyplot(fig)
        plt.close(fig)
        st.caption(f"Coverage = share of the job description's important words found in the resume. "
                   f"Strong ≥ {STRONG_COVERAGE:.0f}%, Possible ≥ {POSSIBLE_COVERAGE:.0f}% (heuristic thresholds).")

# ---------------------------------------------------------------- candidates
with tab_cands:
    if results:
        rows = []
        for i, r in enumerate(results):
            row = {"Rank": i + 1, "Candidate": r.name, "Verdict": r.verdict, "Keyword coverage %": round(r.coverage, 1),
                   "Fit score %": round(r.fit_score, 1), "Predicted field": r.category,
                   "Confidence %": round(r.confidence, 1),
                   "Skill cluster": f"C{r.cluster}: " + ", ".join(r.cluster_terms[:3])}
            if demo_mode:
                truth = true_category(r.name)
                row["True field (file name)"] = truth + (" ✓" if truth == r.category else " ✗")
            rows.append(row)
        table = pd.DataFrame(rows)
        st.dataframe(table, hide_index=True, use_container_width=True)
        st.download_button("Download ranking (CSV)", table.to_csv(index=False), "ranking.csv", "text/csv")
        for r in results:
            with st.expander(f"{r.name}: {r.verdict}, coverage {r.coverage:.0f}%"):
                c1, c2 = st.columns(2)
                fig = category_chart(r)
                c1.pyplot(fig)
                plt.close(fig)
                c1.markdown(f"**Skill cluster C{r.cluster}:** {', '.join(r.cluster_terms)}")
                c2.markdown("**Matching keywords**")
                c2.write(", ".join(r.matched[:15]) or "none")
                c2.markdown("**Important job keywords missing from this resume**")
                c2.write(", ".join(r.missing) or "none")
                c2.caption(f"Share of resume words that are job keywords: {100 * r.stuffing_density:.0f}%")
    else:
        st.info("No resumes to show yet.")

# ---------------------------------------------------------------- insights
with tab_insights:
    mpath = "results/metrics.json"
    metrics = json.load(open(mpath)) if os.path.exists(mpath) else {}
    st.subheader("Skill clusters found by K-Means")
    clusters = pd.DataFrame([{"Cluster": f"C{c}", "Top words": ", ".join(words)}
                             for c, words in bundle["cluster_terms"].items()])
    st.dataframe(clusters, hide_index=True, use_container_width=True)
    if os.path.exists("results/clusters_vs_categories.png"):
        st.image("results/clusters_vs_categories.png", caption="Job category vs K-Means cluster")
    top_words = metrics.get("top_words_per_category")
    if top_words:
        st.subheader("What the model looks for in each field")
        st.dataframe(pd.DataFrame([{"Category": c, "Strongest words": ", ".join(w)} for c, w in top_words.items()]),
                     hide_index=True, use_container_width=True)

# ---------------------------------------------------------------- add a resume
with tab_add:
    st.subheader("Add a resume")
    st.write("Paste a resume. It is added to the list and the whole dashboard updates.")
    if st.session_state.get("added_msg"):
        st.success(st.session_state.pop("added_msg"))
    with st.form("add_resume"):
        st.text_input("Candidate name or label", key="new_name")
        st.text_area("Resume text", height=220, key="new_text")
        st.form_submit_button("Add and screen", on_click=add_resume)
    if st.button("Remove pasted resumes"):
        st.session_state.pop("extra", None)
        st.rerun()

# ---------------------------------------------------------------- model performance
with tab_perf:
    mpath = "results/metrics.json"
    if not os.path.exists(mpath):
        st.info("Run the notebook to generate results/metrics.json.")
    else:
        m = json.load(open(mpath))
        st.write(f"**Dataset:** {m['n_resumes']} unique resumes, {m['n_categories']} categories. "
                 f"**Best model by cross-validation:** {m['best_model']}.")
        st.dataframe(pd.DataFrame(m["classification"]).T, use_container_width=True)
        cl = m.get("clustering", {})
        if cl:
            st.write(f"**K-Means:** K = {cl['best_k']}, silhouette = {cl['silhouette']}, "
                     f"agreement with true labels (ARI) = {cl['kmeans_ARI']}")
        if os.path.exists("results/per_category_report.csv"):
            with st.expander("Per-category precision, recall and F1"):
                st.dataframe(pd.read_csv("results/per_category_report.csv", index_col=0))
        for img, cap in [("tuning_effect.png", "Effect of tuning"), ("confusion_matrix.png", "Confusion matrix"),
                         ("elbow_silhouette.png", "Elbow and silhouette")]:
            if os.path.exists(f"results/{img}"):
                st.image(f"results/{img}", caption=cap)

# ---------------------------------------------------------------- about
with tab_about:
    st.subheader("The problem")
    st.write("A recruiter can receive hundreds of resumes for one job. Reading them all is slow and inconsistent, "
             "and good candidates can be missed.")
    st.subheader("How it works")
    st.markdown("""
1. **Clean** the text. Emails, phone numbers and links are removed, so the model cannot learn from identity.
2. **TF-IDF** turns each resume into numbers. Rare, useful words weigh more than common ones.
3. **Classifier** (Logistic Regression or Naive Bayes, chosen by cross-validation) predicts the resume's field.
4. **K-Means** groups resumes into skill clusters without labels.
5. **Fit score** (cosine similarity) and **keyword coverage** compare each resume with the job description.
6. **Rules** turn the scores into plain-language actions: shortlist, review by hand, or check for keyword stuffing.
    """)
    st.subheader("Data and limitations")
    st.markdown("""
- The dataset has 962 rows but only **166 unique resumes**, so results come from a small test set and can vary by a few points.
- The system matches **exact words only**. It does not understand synonyms, and keyword stuffing can fool it (the app flags it).
- Thresholds (Strong ≥ 50%, Possible ≥ 25%) are heuristics, not learned from hiring data.
- Historical resume data can carry bias. This is **decision support**: a human makes the final decision.
    """)
    st.caption("Parts of the code and documentation were written with help from Claude (Anthropic) and reviewed and tested by the team.")
