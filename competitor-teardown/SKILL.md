---
name: competitor-teardown
description: Produces a deep, evidence-backed intelligence report on one or more named competitors using the ScrapingDog MCP server — product and pricing (scraped, not guessed), hiring velocity from live job postings, funding/press recency, review volume and sentiment from marketplaces or forums, and social reach — then computes a deterministic 0-100 "momentum" score per competitor so a founder can see who's actually growing versus who's stalling, not just who has the nicest homepage. Second stage of a three-skill pipeline that starts with `startup-idea-validator` (which surfaces the competitor names) and ends with `gtm-launch-planner` (which turns the gaps found here into a launch plan). Use this when the user names specific competitors and wants to understand them deeply — "tell me about CodeRabbit and Greptile", "who's winning between X and Y", "is [competitor] actually growing", "what's [competitor]'s pricing/positioning/weakness", or right after a startup-idea-validator run when the user wants to go deeper on the top rivals it found. Don't use this for a first-pass "who are the competitors" scan — that's still `startup-idea-validator`'s job; this is for once you already have names and want the full picture on them.
---

# Competitor Teardown

A homepage and a pricing page tell you what a competitor *says*. This skill is about what a
competitor is *doing*: who they're hiring right now, how recently they were in the news, how their
actual customers rate them, and how big their audience really is — all pulled live, all cited, and
run through a deterministic momentum score so "who's actually winning" isn't a guess.

## Why this isn't just "look at their website"

Anyone can open a competitor's pricing page. What a plain look can't tell you: whether they're
hiring aggressively (growing) or have gone quiet (stalling or dead), whether their last press mention
was a funding round last month or a blog post two years ago, whether their five-star homepage
testimonials match what verified buyers actually say in reviews, and how big their real audience is
versus their marketing copy's implication. This skill exists to pull exactly those signals, per
competitor, and put them on the same scorecard so they're comparable.

## Step 0 — Confirm the MCP server and tools

Same check as the other skills in this pipeline: look for `mcp__scrapingdog*` tools in your available
tools. If missing, tell the user to configure the server (see `startup-idea-validator`'s SKILL.md for
the exact config block) and stop — don't substitute ungrounded knowledge for a teardown. Once
confirmed, read `references/scrapingdog-tools.md` for the tool-to-question mapping this skill uses.

## Step 1 — Get the competitor list and what's already known

Get the competitor name(s) and, if available, their site URL. If the user is coming straight from a
`startup-idea-validator` run, reuse whatever that report already found (pricing, positioning) instead
of re-deriving it — this skill's job is to go *past* that, not repeat it. Cap it at the 2-4
competitors that actually matter for the decision at hand; a 10-competitor teardown dilutes into
noise and burns credits nobody asked to spend.

## Step 2 — Research, per competitor

Run these for each competitor. Use `references/scrapingdog-tools.md` for exact tool/query mapping.

1. **Product & positioning** — `web_scrape` the homepage and pricing page (markdown mode reads
   cleaner than raw HTML for this). `screenshot` the homepage if a visual comparison will help the
   report — a founder registers "what does this look like" faster from an image than a paragraph.
2. **Hiring velocity** — `google_jobs` for `"<competitor name>"` or `site:<their careers page>`.
   Count open roles and note the mix (if it's mostly sales/CS, they're scaling GTM; mostly
   engineering, they're still building core product). No roles found after a real search effort is
   itself a signal — note it, don't skip it.
3. **Funding & press recency** — `google_news` for the competitor name. Record the most recent
   substantive mention (funding, launch, major feature, executive hire) and how long ago it was.
   `linkedin_profile` (`type: "company"`) for headcount if it's listed.
4. **Review volume & sentiment** — for a physical product, `amazon_reviews` on the ASIN directly. For
   software, `google_search` for `"<competitor> reviews"` site:g2.com / site:capterra.com /
   site:trustpilot.com, then `web_scrape` the review page. `youtube_comments` on a review/tutorial
   video is a good supplementary source when it exists. Note both volume (confidence) and sentiment
   direction, and pull 1-2 verbatim quotes — a specific complaint is worth more than a star rating.
5. **Social reach** — `x_profile` for follower count and bio positioning. Note it as a rough audience
   proxy, not a precision metric.
6. **IP/technical moat** (only for deep-tech competitors) — `google_patents` filtered by
   `assignee: "<competitor name>"` to see if they've actually filed anything or are relying on
   execution speed alone.

If a category comes up empty after a genuine attempt, record that explicitly — an unknown headcount
or zero findable reviews is real information, not a research failure to paper over.

## Step 3 — Score momentum

Write the gathered evidence into a JSON file matching the schema in
`references/scoring-rubric.md`, then run:

```bash
python3 scripts/momentum_score.py <path-to-competitors.json>
```

This gives each competitor a deterministic 0-100 momentum score across five dimensions (hiring
velocity, news/funding recency, review volume & rating, social reach, team-scale signal) and a band
from Dormant to Aggressive Growth, sorted highest-momentum first. This is a **relative** signal for
comparing the named competitors against each other, not a market-validation score — don't confuse it
with `startup-idea-validator`'s 0-100, which measures something different (whether the idea itself
has a market). Read `references/scoring-rubric.md` to explain the "why" behind each score in the
report.

## Step 4 — Deliver the report

Publish as a shareable Artifact by default — load the `artifact-design` skill before writing the
HTML, same as the other skills in this pipeline. `assets/teardown-template.html` is a theme-aware
starting layout; adapt it, don't just fill placeholders verbatim.

### Report structure

1. **Competitors covered** — names, sites, one-line description each.
2. **Momentum scorecard** — the table from Step 3: score, band, and the per-dimension breakdown, so
   the reader can see *why* one competitor outranks another, not just that it does.
3. **Per-competitor deep dive** (one subsection each) — product/positioning summary, pricing, hiring
   signal, funding/press recency, review sentiment with 1-2 quoted examples, social reach.
4. **Gaps and openings** — synthesized across all competitors: what none of them do well, where
   reviews consistently complain about the same thing, whether any have gone quiet (hiring/press).
   This section is what makes the teardown actionable rather than encyclopedic — it's the input
   `gtm-launch-planner` needs for positioning.
5. **Sources** — every URL scraped or searched.

Close with a one-line pointer to `gtm-launch-planner` if the user seems ready to act on the gaps
found — don't run it automatically.

## Guardrails

- Never invent a headcount, review quote, funding date, or job-posting count. A competitor with
  genuinely no findable signal in a category gets "not found," not a plausible-sounding guess.
- The momentum score describes trajectory signals (hiring, news, reviews, reach), not product
  quality — a well-funded competitor with a mediocre product can still score high momentum. Say so in
  the report rather than implying the score means "best."
- Cap scope at the competitors that matter. This skill rewards depth per competitor, not a long list
  of shallow entries.
