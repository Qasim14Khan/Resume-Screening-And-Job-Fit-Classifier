"""Rules that turn scores into plain-language next steps for the recruiter.

Every action says what we see, and what to do. This is DECISION SUPPORT: a human decides.
"""
from __future__ import annotations

from dataclasses import dataclass

from .config import LOW_CONFIDENCE, STUFFING_DENSITY


@dataclass
class Action:
    severity: str   # "red" | "yellow" | "info" | "green"
    title: str
    detail: str
    action: str


def generate_actions(results: list) -> list:
    """Build the 'What to do now' list for a screened batch (results are sorted best first)."""
    acts: list[Action] = []
    strong = [r for r in results if r.verdict == "Strong match" and not r.stuffed]
    possible = [r for r in results if r.verdict == "Possible match" and not r.stuffed]

    for r in strong[:3]:
        acts.append(Action(
            "green", f"Shortlist: {r.name}",
            f"Covers {r.coverage:.0f}% of the job's keywords. Predicted field: {r.category} ({r.confidence:.0f}% confidence).",
            ("Invite for an interview. " + (f"Ask about: {', '.join(r.missing[:4])}." if r.missing else
                                            "No important keywords are missing."))))
    for r in possible[:3]:
        acts.append(Action(
            "yellow", f"Review manually: {r.name}",
            f"Covers {r.coverage:.0f}% of the job's keywords; missing: {', '.join(r.missing[:5]) or 'none'}.",
            "Read the resume yourself. The candidate may describe the same skills with different words."))
    for r in results:
        if r.stuffed:
            acts.append(Action(
                "red", f"Possible keyword stuffing: {r.name}",
                f"{100 * r.stuffing_density:.0f}% of this resume's words are job keywords (alert level {100 * STUFFING_DENSITY:.0f}%).",
                "Read it manually. The score may be inflated by repeating the job's words."))
    for r in results:
        if r.unsure:
            acts.append(Action(
                "info", f"Model unsure about the field: {r.name}",
                f"Best guess {r.category} at only {r.confidence:.0f}% confidence (next: {r.top3[1][0]}).",
                "Check the resume yourself. It may mix several fields."))
    if results and not strong and not possible:
        acts.append(Action(
            "info", "No candidate matches this job well",
            f"The best coverage is {results[0].coverage:.0f}%.",
            "Check whether the job description uses different wording from the resumes. "
            "The system matches exact words only."))
    order = {"red": 0, "green": 1, "yellow": 2, "info": 3}
    return sorted(acts, key=lambda a: order[a.severity])
