"""Matplotlib charts used by the dashboard."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")   # no display needed (works on servers and in tests)
import matplotlib.pyplot as plt

from .config import CHART_COLOR, POSSIBLE_COVERAGE, STRONG_COVERAGE


def _style(ax):
    ax.grid(axis="x", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)


def coverage_chart(results: list):
    """Job keyword coverage per candidate, coloured by verdict, with the two thresholds."""
    n = max(len(results), 1)
    fig, ax = plt.subplots(figsize=(9, 0.45 * n + 1.4))
    names = [r.name for r in results]
    ax.barh(names, [r.coverage for r in results], color=[CHART_COLOR[r.verdict] for r in results], height=0.6)
    ax.axvline(POSSIBLE_COVERAGE, color=CHART_COLOR["Possible match"], ls="--", lw=1)
    ax.axvline(STRONG_COVERAGE, color=CHART_COLOR["Strong match"], ls="--", lw=1)
    ax.text(POSSIBLE_COVERAGE + 0.5, -0.9, "Possible", fontsize=7, color=CHART_COLOR["Possible match"])
    ax.text(STRONG_COVERAGE + 0.5, -0.9, "Strong", fontsize=7, color=CHART_COLOR["Strong match"])
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    ax.set_xlabel("Job keyword coverage (%)", fontsize=8)
    ax.tick_params(labelsize=8)
    _style(ax)
    fig.tight_layout()
    return fig


def category_chart(result):
    """Top-3 predicted categories for one resume."""
    fig, ax = plt.subplots(figsize=(4.5, 1.8))
    cats = [c for c, _ in result.top3]
    ax.barh(cats, [p for _, p in result.top3], color="#1f4e9c", height=0.55)
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    ax.set_xlabel("Model confidence (%)", fontsize=8)
    ax.tick_params(labelsize=8)
    _style(ax)
    fig.tight_layout()
    return fig
