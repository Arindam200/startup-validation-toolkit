#!/usr/bin/env python3
"""Deterministic momentum scoring for the competitor-teardown skill.

Reads a competitors.json file (schema documented in references/scoring-rubric.md)
and prints a 0-100 momentum score, per-dimension breakdown, and band for each
competitor as markdown, sorted highest-momentum first.

Usage:
    python3 momentum_score.py path/to/competitors.json
"""
import json
import sys


def score_hiring(open_roles) -> tuple[int, str]:
    n = open_roles if isinstance(open_roles, (int, float)) else 0
    if n <= 0:
        return 2, "0 open roles found"
    if n <= 3:
        return 8, f"{int(n)} open role(s) — modest"
    if n <= 10:
        return 14, f"{int(n)} open roles — real hiring push"
    return 20, f"{int(n)} open roles — aggressive scaling"


def score_recency(days_ago) -> tuple[int, str]:
    if days_ago is None:
        return 2, "no funding/news mention found"
    d = days_ago
    if d <= 30:
        return 20, f"last substantive mention {int(d)}d ago"
    if d <= 90:
        return 14, f"last substantive mention {int(d)}d ago"
    if d <= 365:
        return 8, f"last substantive mention {int(d)}d ago"
    return 3, f"last mention {int(d)}d ago — gone quiet"


def score_reviews(review_count, review_rating) -> tuple[int, str]:
    n = review_count if isinstance(review_count, (int, float)) else 0
    rating = review_rating
    if n <= 0:
        return 0, "no reviews found"
    volume_confidence = "low" if n < 20 else ("medium" if n < 200 else "high")
    if rating is None:
        return 6, f"{int(n)} review(s) found, rating unknown ({volume_confidence} confidence)"
    rating_points = max(0, min(int(round((rating / 5) * 16)), 16))
    volume_bonus = {"low": 0, "medium": 2, "high": 4}[volume_confidence]
    total = min(rating_points + volume_bonus, 20)
    return total, f"{int(n)} review(s), {rating}/5 avg ({volume_confidence} confidence)"


def score_social(social_followers) -> tuple[int, str]:
    n = social_followers if isinstance(social_followers, (int, float)) else 0
    if n <= 0:
        return 0, "no social presence found"
    if n < 1_000:
        return 5, f"{int(n)} followers"
    if n < 10_000:
        return 10, f"{int(n)} followers"
    if n < 100_000:
        return 15, f"{int(n)} followers"
    return 20, f"{int(n)} followers"


def score_team_scale(signal: str) -> tuple[int, str]:
    points = {
        "unknown": 2,
        "1-10": 6,
        "11-50": 11,
        "51-200": 15,
        "201-1000": 18,
        "1000+": 20,
    }.get(signal or "unknown", 2)
    return points, f"employee_count_signal={signal or 'unknown'}"


def band_for(score: int) -> str:
    if score >= 80:
        return "Aggressive Growth"
    if score >= 55:
        return "Steady"
    if score >= 25:
        return "Stalling"
    return "Dormant"


def main():
    if len(sys.argv) != 2:
        print("Usage: momentum_score.py <path-to-competitors.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    results = []
    for c in data.get("competitors", []):
        dims = [
            ("Hiring velocity", score_hiring(c.get("open_roles"))),
            ("News/funding recency", score_recency(c.get("last_funding_or_news_days_ago"))),
            ("Review volume & rating", score_reviews(c.get("review_count"), c.get("review_rating"))),
            ("Social reach", score_social(c.get("social_followers"))),
            ("Team-scale signal", score_team_scale(c.get("employee_count_signal"))),
        ]
        total = sum(points for _, (points, _) in dims)
        results.append((c.get("name", "(unnamed)"), c.get("url", ""), total, band_for(total), dims))

    results.sort(key=lambda r: r[2], reverse=True)

    print("# Competitor momentum scorecard\n")
    print("| Rank | Competitor | Score | Band |")
    print("|---|---|---|---|")
    for i, (name, url, total, band, _) in enumerate(results, 1):
        print(f"| {i} | {name} | {total}/100 | {band} |")

    for name, url, total, band, dims in results:
        print(f"\n## {name} — {total}/100 ({band})")
        if url:
            print(f"{url}\n")
        print("| Dimension | Score | Why |")
        print("|---|---|---|")
        for dim_name, (points, why) in dims:
            print(f"| {dim_name} | {points}/20 | {why} |")


if __name__ == "__main__":
    main()
