# Scoring rubric

The score exists so the verdict is defensible and repeatable, not a vibe. `scripts/score_idea.py`
implements this exact rubric — read this file to understand *why* a score landed where it did so
you can explain it in the report, but let the script do the arithmetic.

The five dimensions below are evidence-agnostic: it doesn't matter whether a competitor came from
`google_search` or `amazon_search`, or whether a pain-point quote came from `web_scrape` on a Reddit
thread or from `youtube_comments` — it's still one competitor, one quote. Hiring signal
(`google_jobs`) and AI-answer-engine findings (`chatgpt`/`google_ai_mode`) don't get their own
column; fold them into `search_demand` and the report's demand-signal prose rather than inventing new
JSON fields. Wider tool coverage should mean *better* evidence in these five buckets, not a wider
rubric.

## Input schema (`research.json`)

```json
{
  "idea_name": "string",
  "search_demand": {
    "signal_strength": "high | medium | low | unknown",
    "trend_direction": "rising | stable | declining | unknown"
  },
  "competitors": [
    { "name": "string", "url": "string", "pricing": "string or null", "notes": "string" }
  ],
  "pain_points": [
    { "quote": "string", "source_url": "string", "platform": "reddit | hn | x | forum | other" }
  ],
  "pricing_data_points": [
    { "source": "string", "price": "string", "url": "string" }
  ],
  "market_size_signal": "large | medium | niche | unknown"
}
```

Every list can be empty — an empty list is a legitimate finding ("no pain-point evidence found")
and scores accordingly low on that dimension. Don't pad lists to avoid a low score.

## The five dimensions (0-20 each, sum to 0-100)

1. **Demand evidence (0-20)** — from `search_demand`. High + rising signal scores near 20; unknown
   signal scores near 0. A `low` but `rising` signal can beat a `medium` but `declining` one —
   direction matters as much as level for an early-stage idea.

2. **Pain-point intensity (0-20)** — from `pain_points`. Scored on count *and* specificity: 4+
   distinct, specific, cross-platform quotes is a near-max score; 1-2 generic complaints is
   mid-range; zero real quotes is near 0 regardless of how good the idea sounds in theory. This is
   usually the dimension that most separates a real problem from a founder's assumption.

3. **Competitive opening (0-20)** — from `competitors`, scored as a curve, not linearly:
   - 0 competitors after a genuine search effort: low score (~4/20) — usually means no market, not
     a hidden opportunity.
   - 1-5 competitors: high score (~16-20/20) — proof people pay to solve this, with room to
     differentiate.
   - 6+ competitors with no obvious gap: mid score (~8-12/20) — validated demand, but a crowded
     field raises the bar on differentiation.

4. **Willingness to pay (0-20)** — from `pricing_data_points`. Multiple real prices found (even
   for adjacent/competitor products) scores high; no pricing evidence anywhere scores near 0 — it
   means nobody's proven anyone will pay for this class of solution yet.

5. **Market size signal (0-20)** — from `market_size_signal`. `large` scores high, `niche` scores
   mid (niches can be great businesses — this isn't a penalty, just a smaller ceiling), `unknown`
   scores low because it's unverified, not because niche is bad.

## Verdict bands

| Score | Band | What it means |
|---|---|---|
| 80-100 | Strong Go | Multiple dimensions have real evidence; act on it (build an MVP/landing page test). |
| 60-79 | Promising — Validate Further | Real signal, but at least one dimension is thin — say which, and what to check next. |
| 40-59 | Iterate on the Idea | Mixed evidence — likely the idea, audience, or angle needs to change before building. |
| 20-39 | Weak Signal | Little verifiable evidence found — treat as a hypothesis, not a validated idea. |
| 0-19 | No-Go | No real demand, pain-point, or willingness-to-pay evidence surfaced. |

A score is only as good as the research feeding it — if a category was skipped because the tools
came up empty, say that explicitly next to that dimension in the report rather than letting a low
sub-score speak for itself.
