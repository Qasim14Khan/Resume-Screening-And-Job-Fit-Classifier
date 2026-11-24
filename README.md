# Resume Screening & Job-Fit Classifier

🔗 **Live demo:** https://resume-screening-and-job-fit-classifier-2vxi8gtckgseiwlqfkyrxe.streamlit.app

A dashboard that ranks resumes against a job description and tells a recruiter **what to do next**: shortlist, review by hand, or check for keyword stuffing.

Built for AI-3202 Machine Learning Practical (DUET Karachi), Lab 14.
Team: Muhammad Qasim Khan (24F-AI-015), Muslim Zain (24F-AI-031), Muhammad Ismail (24F-AI-012), Talha Mazhar (24F-AI-022).
Instructor: Engr. Hamza Farooqui.

## What it does

- Predicts a resume's field (25 categories) with TF-IDF + Logistic Regression or Naive Bayes (Labs 3 and 9).
- Groups resumes into skill clusters with K-Means (Lab 10).
- Scores each resume against a job: **keyword coverage** and **cosine-similarity fit score**.
- Turns the scores into plain-language actions ("What to do now").
- Flags possible keyword stuffing and low model confidence.
- Demo mode: use the sample resumes, or upload PDF, DOCX or TXT files.

## Lab concepts used

| Lab | Concept | Where |
|---|---|---|
| Lab 1 | Data preprocessing | text cleaning, duplicate removal, label encoding, TF-IDF, stratified split |
| Lab 3 | Logistic Regression | classifier, `C` tuned with cross-validation |
| Lab 9 | Naive Bayes | classifier, `alpha` tuned with cross-validation |
| Lab 10 | K-Means | skill clusters, K chosen by elbow and silhouette |

## How to run

```bash
pip install -r requirements.txt
# 1. Put UpdatedResumeDataSet.csv in the Data folder.
# 2. Train and save the model (or choose Run All in the notebook, which does the same):
python train.py
# 3. Start the dashboard:
streamlit run app.py
```

Run the tests with `pytest`.

## Using the app

Upload a resume (PDF, DOCX or TXT), pick the job in the sidebar, and read the report: predicted field, fit to the job, matching and missing skills, and what to do next.

## Project structure

```
app.py              Streamlit dashboard
src/                text cleaning, model and scoring, recommendations, charts, job presets
tests/              pytest checks for the screening logic
Data/               put UpdatedResumeDataSet.csv here (not committed, see Data section)
models/             saved model bundle (created by the notebook)
results/            metrics and figures (created by the notebook)
sample_resumes/     12 fictional demo resumes (PDF) named like Data_Science_1.pdf
train.py            trains the model and saves models/ and results/
make_sample_resumes.py  regenerates the sample PDFs
```

## Results

Numbers come from `results/metrics.json`, produced by the notebook. The dataset has 962 rows but only 166 unique resumes after removing duplicates, split 132 train / 34 test. The best model is chosen by cross-validation (up to 5 folds; 2 folds here because the smallest category has only 2 training resumes) between Logistic Regression and Naive Bayes; exact numbers are in `results/metrics.json` after you run `python train.py`. Because the test set is small, one resume changes accuracy by about 3 points.

## Limitations

- Exact-word matching only. Synonyms are not understood.
- Keyword stuffing can fool the scores; the app flags it but cannot fully stop it.
- Coverage thresholds (Strong ≥ 50%, Possible ≥ 25%) are heuristics, not learned from hiring outcomes.
- Historical resume data can carry bias. This tool is decision support; a human makes the final decision.

## Data

UpdatedResumeDataSet.csv, originally published on Kaggle. Our copy came from the Hugging Face mirror `brackozi/Resume` (https://huggingface.co/datasets/brackozi/Resume). Download it and save it as `Data/UpdatedResumeDataSet.csv` before running `train.py`. It is not committed to this repository.

## Use of AI tools

Parts of the code and documentation were written with help from Claude (Anthropic). The team reviewed, ran and tested the work, and is responsible for it.
