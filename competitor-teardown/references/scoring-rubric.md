# Momentum scoring rubric

This score answers a different question than `startup-idea-validator`'s: not "is there a market" but
"which of these named competitors is actually moving, and which has gone quiet." It's a **relative**
comparison across the competitors you researched, not an absolute judgment of product quality — a
mediocre product backed by aggressive hiring and a recent funding round can still score high
momentum. Say that plainly in the report; don't let the score imply "best."

## Input schema (`competitors.json`)

```json
{
  "competitors": [
    {
      "name": "string",
      "url": "string",
      "open_roles": 0,
      "last_funding_or_news_days_ago": null,
      "review_count": 0,
      "review_rating": null,
      "social_followers": 0,
      "employee_count_signal": "unknown | 1-10 | 11-50 | 51-200 | 201-1000 | 1000+"
    }
  ]
}
```

Every numeric field can be `0`/`null`/`"unknown"` — that's a legitimate finding ("no open roles
found," "no headcount public") and scores low on that dimension accordingly. Don't estimate a number
you didn't actually find; use the null/unknown value.

## The five dimensions (0-20 each, sum to 0-100)

1. **Hiring velocity (0-20)** — from `open_roles`. 0 roles scores near 0 (could mean dormant, or just
   fully staffed — note which if you can tell from context); 1-3 is modest; 4-10 is a real push;
   11+ scores near max. Role mix (noted in the report, not the score) tells you *what* they're
   investing in.
2. **News/funding recency (0-20)** — from `last_funding_or_news_days_ago`. Within 30 days scores near
   max; within 90 days is still strong; within a year is moderate; older than a year or unknown scores
   low — silence is itself a signal for a company that used to be press-active.
3. **Review volume & rating (0-20)** — from `review_count` and `review_rating` together. High volume
   at a high rating scores near max; high volume at a low rating is a real finding (bring the
   competitor's specific complaint pattern into the report — that's an opening); low volume scores
   low regardless of rating because the signal isn't confident yet; no reviews found scores near 0.
4. **Social reach (0-20)** — from `social_followers`, log-scaled (the gap between 500 and 5,000
   matters more than the gap between 50,000 and 55,000). Treat as a rough proxy, not precision.
5. **Team-scale signal (0-20)** — from `employee_count_signal`. Larger buckets score higher as a
   resource/staying-power proxy; `unknown` scores near 0 because it's unverified, not because small
   is bad — a lean, unlisted team can still be dangerous, the score just can't see it.

## Momentum bands

| Score | Band | What it means |
|---|---|---|
| 80-100 | Aggressive Growth | Hiring, in the news, well-reviewed, real reach — actively pulling ahead. |
| 55-79 | Steady | Real signal on most dimensions, nothing alarming, nothing explosive. |
| 25-54 | Stalling | Multiple dimensions thin or aging — worth watching for an opening. |
| 0-24 | Dormant | Little to no recent activity signal found — verify it's not just under-researched before treating this as "safe to ignore." |
