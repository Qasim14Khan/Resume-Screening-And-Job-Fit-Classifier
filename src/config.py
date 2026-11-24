"""Thresholds in one place. All of these are HEURISTICS (not learned from hiring data)."""

STRONG_COVERAGE = 50.0      # % of the job's keyword weight found in the resume -> "Strong match"
POSSIBLE_COVERAGE = 25.0    # ... -> "Possible match"; below this -> "Weak match"
STUFFING_DENSITY = 0.30     # share of resume words that are job keywords; above this looks like keyword stuffing
LOW_CONFIDENCE = 40.0       # % model confidence below which we ask for a manual check

STATUS_ORDER = ["Strong match", "Possible match", "Weak match"]
STATUS_COLOR = {"Strong match": "green", "Possible match": "orange", "Weak match": "gray"}   # Streamlit colors
CHART_COLOR = {"Strong match": "#2ca02c", "Possible match": "#f0a500", "Weak match": "#9aa0a6"}
