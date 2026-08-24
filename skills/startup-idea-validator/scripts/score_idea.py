#!/usr/bin/env python3
"""Deterministic scoring for the startup-idea-validator skill.

Reads a research.json file (schema documented in references/scoring-rubric.md)
and prints a 0-100 score, per-dimension breakdown, and verdict band as markdown.

Usage:
    python3 score_idea.py path/to/research.json
"""
import json
import sys


def score_demand(search_demand: dict) -> tuple[int, str]:
    strength = (search_demand or {}).get("signal_strength", "unknown")
    trend = (search_demand or {}).get("trend_direction", "unknown")

    strength_points = {"high": 12, "medium": 8, "low": 4, "unknown": 0}.get(strength, 0)
    trend_points = {"rising": 8, "stable": 5, "declining": 2, "unknown": 0}.get(trend, 0)
    total = strength_points + trend_points
    return total, f"signal={strength}, trend={trend}"


def score_pain_points(pain_points: list) -> tuple[int, str]:
    n = len(pain_points or [])
    platforms = {p.get("platform") for p in (pain_points or []) if p.get("platform")}
    if n == 0:
        return 0, "no pain-point evidence found"
    base = min(n, 4) * 4  # up to 16 for 4+ quotes
    diversity_bonus = min(len(platforms) - 1, 1) * 4  # +4 if 2+ distinct platforms
    total = min(base + diversity_bonus, 20)
    return total, f"{n} quote(s) across {len(platforms)} platform(s)"


def score_competitors(competitors: list) -> tuple[int, str]:
    n = len(competitors or [])
    if n == 0:
        return 4, "0 competitors found — usually signals no market, not a hidden opportunity"
    if 1 <= n <= 5:
        return 18, f"{n} competitors — validated demand with room to differentiate"
    return 10, f"{n} competitors — crowded field, differentiation bar is high"


def score_pricing(pricing_points: list) -> tuple[int, str]:
    n = len(pricing_points or [])
    if n == 0:
        return 0, "no pricing evidence found — willingness to pay unverified"
    total = min(n * 5, 20)
    return total, f"{n} real price point(s) found"


def score_market_size(signal: str) -> tuple[int, str]:
    points = {"large": 20, "medium": 13, "niche": 12, "unknown": 4}.get(signal or "unknown", 4)
    return points, f"market_size_signal={signal or 'unknown'}"


def band_for(score: int) -> str:
    if score >= 80:
        return "Strong Go"
    if score >= 60:
        return "Promising — Validate Further"
    if score >= 40:
        return "Iterate on the Idea"
    if score >= 20:
        return "Weak Signal"
    return "No-Go"


def main():
    if len(sys.argv) != 2:
        print("Usage: score_idea.py <path-to-research.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    dims = [
        ("Demand evidence", score_demand(data.get("search_demand", {}))),
        ("Pain-point intensity", score_pain_points(data.get("pain_points", []))),
        ("Competitive opening", score_competitors(data.get("competitors", []))),
        ("Willingness to pay", score_pricing(data.get("pricing_data_points", []))),
        ("Market size signal", score_market_size(data.get("market_size_signal", "unknown"))),
    ]

    total = sum(points for _, (points, _) in dims)
    verdict = band_for(total)

    print(f"# Validation score: {total}/100 — {verdict}\n")
    print("| Dimension | Score | Why |")
    print("|---|---|---|")
    for name, (points, why) in dims:
        print(f"| {name} | {points}/20 | {why} |")
    print(f"\n**Idea:** {data.get('idea_name', '(unnamed)')}")


if __name__ == "__main__":
    main()
