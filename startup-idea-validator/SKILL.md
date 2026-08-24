---
name: startup-idea-validator
description: Validates a startup, SaaS, app, physical-product, local-business, or research-heavy idea using live web data pulled through the ScrapingDog MCP server's full 30-tool surface (Google/Bing/Baidu search, Google Trends/News/Jobs/Patents/Scholar, Amazon/eBay/Walmart/Shopping, LinkedIn, X, YouTube, Maps, screenshots, and a direct ChatGPT-query tool) — finds real competitors, demand and trend signals, hiring-side demand, pricing benchmarks, AI-answer-engine visibility, and verbatim audience pain points, then scores the idea 0-100 and delivers a go/no-go verdict as a polished, shareable report. First stage of a three-skill pipeline: this validates the idea, `competitor-teardown` goes deep on the rivals this surfaces, and `gtm-launch-planner` turns a Go verdict into an actual launch plan. Use this whenever the user wants to validate, vet, sanity-check, or "market research" a specific idea — phrases like "is this a good idea", "should I build this", "will people pay for X", "does this have a market", "validate my startup idea", "check if anyone needs this", or "who's already doing this" all mean pull in this skill, even if the user never says ScrapingDog or MCP. Also trigger for narrower asks that are really a slice of this workflow: "find competitors for X", "how much does X cost people already", "what are people complaining about in [niche]", or "check demand for [product]".
---

# Startup Idea Validator

Turns a one-line idea into an evidence-backed validation report by scraping the live web through
the ScrapingDog MCP server, instead of relying on training-data guesses about a market. The whole
point is that every claim in the final report traces back to a URL someone can click — and that the
research draws on more than a search engine, because a search engine can't tell you who's hiring for
this problem right now, what ChatGPT already recommends when someone asks it, or what a competitor's
actual customers say in their reviews.

## Why this works the way it does

Idea validation fails most often for one of two reasons: the founder never leaves their own head
(no real user pain points, no competitor check), or they drown in unstructured research and never
turn it into a decision. This skill forces both: it goes and finds primary sources across whichever
data surface actually has the answer for this kind of idea (search, but also jobs postings, patent
filings, marketplace reviews, hiring velocity, social presence, and what AI assistants already say),
and it always converges on a scored verdict so the output is a decision aid, not a pile of links.

This is stage one of a pipeline. If the verdict is Go/Promising, the natural next moves are
`competitor-teardown` (deep intelligence on the specific rivals this surfaces — hiring velocity,
funding recency, review sentiment, social reach) and `gtm-launch-planner` (turn the validated idea
into a channel plan, positioning statement, and first-customers strategy). Mention these as the next
step when you hand back a Go/Promising verdict — don't run them automatically unless asked.

## Step 0 — Confirm the MCP server and discover its actual tools

Different builds of the ScrapingDog MCP server expose different tool sets. A small build ships ~9
tools (`scrape`/`web_scrape`, `google_search`, `bing_search`, `x_profile`, `screenshot`, ...); the
full build ships 30+, adding structured engines for Trends, News, Jobs, Patents, Scholar, Maps,
Shopping, Images, Lens, Hotels, three e-commerce marketplaces (Amazon/eBay/Walmart), LinkedIn,
YouTube (search/video/channel/comments/transcripts), and a tool that sends a prompt straight to
ChatGPT and returns its answer. Don't assume — check what's actually connected first:

1. Look at your available tools for anything namespaced like `mcp__scrapingdog*`.
2. If nothing shows up, the server isn't configured yet. Tell the user to add it:
   ```json
   {
     "mcpServers": {
       "scrapingdog": {
         "command": "npx",
         "args": ["-y", "scrapingdog-mcp"],
         "env": { "SCRAPINGDOG_API_KEY": "<their key from scrapingdog.com>" }
       }
     }
   }
   ```
   Then stop and wait for them to restart Claude Code with it configured — don't fall back to
   ungrounded web knowledge and call it validation.
3. Once tools are visible, read `references/scrapingdog-tools.md` — it maps the full tool catalog to
   every research question in this workflow, including which tools only apply to certain idea types,
   so you don't waste calls guessing or reach for the small-build workaround when the real tool
   exists.

## Step 1 — Pin down the idea and classify its type

Get (or infer, then confirm in one line) three things before spending API credits:
- **What it is**: the product/service in one sentence.
- **Who it's for**: the specific user, not "everyone" — "freelance video editors" not "creators."
- **What problem it solves**: the pain point, in the user's own words if they gave one.

If the user's pitch is vague ("an app for productivity"), ask one sharpening question rather than
researching a fog. A vague idea produces a useless report no matter how good the scraping is.

Also classify the idea's **type**, since this decides which extra tools earn their keep in Step 2.
Pick the closest match (an idea can match more than one — use all that apply):

| Type | Signal | Extra tools worth pulling in |
|---|---|---|
| Physical product / e-commerce | Sells a physical good | `amazon_search`, `amazon_product`, `amazon_reviews`, `amazon_offers`, `google_shopping`, `ebay_search`, `walmart_search` |
| Local or service business | Tied to a place (studio, clinic, restaurant, local service) | `google_maps` (search + place) for competitor density and rating benchmarks |
| Deep-tech / research-heavy | Novel technical approach, possible IP | `google_patents`, `google_scholar` |
| Content / creator / community-driven | Audience-first, media, community product | `youtube_search`, `youtube_comments`, `youtube_transcripts`, `x_profile` |
| B2B / enterprise software | Sold to companies, not individuals | `linkedin_profile` (company mode), `google_jobs` for buyer-persona titles |
| Everything else (default SaaS/app/consumer) | — | The universal set below covers it |

## Step 2 — Research (run these in parallel where the tools allow it)

Work through each of these using `references/scrapingdog-tools.md` for exact tool/query mapping.
Pull 2-4 real, cite-able data points per category — depth beats breadth here.

**Run these seven for every idea, regardless of type:**

1. **Demand & trend signal** — `google_trends` for the core keyword (read the whole time range, not
   just the latest point — a mid-range spike followed by a drop to baseline is a news event, not
   declining demand; say so explicitly rather than letting the raw number mislead), plus
   `google_search`/`google_news` for comparison searches and recent coverage.
2. **Competitive landscape** — 3-6 real competitors or close substitutes via `google_search`, each
   confirmed with `web_scrape` (and optionally `screenshot`) on their homepage/pricing page — don't
   trust a search snippet alone. Include indie/small players, not just incumbents.
3. **Pricing & willingness-to-pay** — actual prices from `web_scrape` on competitor `/pricing` pages,
   cross-checked with `google_search` for `"<keyword> pricing reddit"` style discussion.
4. **Audience pain points** — verbatim quotes from real people describing the problem unprompted.
   `google_search`/`bing_search` with `site:reddit.com` / `site:news.ycombinator.com` style queries,
   then `web_scrape` the actual thread — a search snippet is not a source, it's truncated and easy to
   misattribute. Add `x_profile` or `youtube_comments` (on a relevant tutorial/review video) when the
   audience is known to be vocal there.
5. **Market size signal** (best-effort) — `google_search` for `<category> market size` / TAM industry
   reports; the number of distinct competitors found above is itself a rough proxy.
6. **Hiring/demand-side signal** — `google_jobs` for roles tied to this problem (e.g. "changelog" for
   a changelog tool, "code reviewer" for a review tool). Companies actively hiring or building
   internal tooling around a problem is a budget-line-item signal that search volume alone can't
   show — note the roughly-how-many and how recent, not just whether any exist.
7. **AI-answer-engine visibility** — this is the one a plain web search can't do at all. Use the
   `chatgpt` tool to literally ask it: `"what's the best tool for <problem>"` or `"how do people
   usually solve <problem>"`, and pull `google_ai_overview`/`google_ai_mode` for the same query on
   Google. Record who (if anyone) gets recommended. Two things this proves: whether people are
   already routing this exact question through an AI assistant (a live, growing discovery channel),
   and who currently owns that answer — which is direct competitive-opening evidence for later.

**Then layer in whichever type-specific tools matched in Step 1** (Amazon/Shopping/eBay/Walmart for
physical products, Maps for local business, Patents/Scholar for deep-tech, YouTube/X for
content-driven ideas, LinkedIn/Jobs-as-persona-research for B2B).

If a category comes up empty after a couple of honest attempts, say so in the report instead of
padding it — "no verifiable pain-point evidence found" is a real and useful finding.

## Step 3 — Score it

Don't eyeball a number. Write the gathered evidence into a JSON file matching the schema in
`references/scoring-rubric.md`, then run:

```bash
python3 scripts/score_idea.py <path-to-research.json>
```

This gives a deterministic 0-100 score across five weighted dimensions (demand evidence, pain-point
intensity, competitive opening, willingness to pay, market size) plus a verdict band. The scoring
math doesn't change based on idea type or which tools you used — hiring signal, AI-visibility
findings, and marketplace review data all feed into the same five dimensions as extra evidence, they
don't add new categories. Read `references/scoring-rubric.md` once so you can explain *why* the score
landed where it did in the report — the rubric, not vibes, is what makes the verdict defensible.

## Step 4 — Deliver the report

Default to publishing it as a shareable Artifact (an HTML page), since a link people can open beats
a wall of markdown in the terminal — this is the part that makes the output worth sending to a
co-founder or posting for feedback. Before writing the HTML, load the `artifact-design` skill as
usual — do not skip that step just because a starting point exists. `assets/report-template.html`
is a theme-aware (light/dark) starting layout you can adapt; treat it as a base, not a mold — change
it where the content calls for it. Its `{{VERDICT_BAND_CLASS}}` placeholder should resolve to `go`
for Strong Go/Promising, `mid` for Iterate/Weak Signal, or `no` for No-Go, so the badge color
matches the verdict.

If the user is scripting this or explicitly wants markdown/plain text instead, that's fine — just
keep the same structure.

### Report structure

ALWAYS include these sections, in this order:

1. **Idea snapshot** — the one-sentence idea, target user, and problem, restated back cleanly.
2. **Validation score** — the number, its band (see below), and a one-line summary of why.
3. **Demand & trend signal** — what the data shows, with sources. Note hiring-side and
   AI-answer-engine findings here too rather than burying them.
4. **Competitive landscape** — a table: competitor, what they do, target user, pricing, one-line
   differentiation angle for this idea.
5. **Audience pain points** — direct quotes with links to where they came from, not paraphrases.
6. **Pricing & willingness-to-pay** — the price points found and what they imply.
7. **Risks & open questions** — the honest gaps: what wasn't found, what would kill the idea,
   what to test next (e.g., a landing page, 10 customer interviews).
8. **Verdict** — one of: Strong Go / Promising, Validate Further / Iterate on the Idea / Weak
   Signal / No-Go — matching the score band — with the 2-3 sentence reasoning a founder would
   actually act on.
9. **Sources** — every URL actually scraped or searched, so the whole report is auditable.

If the verdict lands Go or Promising, close with one line pointing at the next stage: naming the top
1-2 competitors worth a `competitor-teardown` pass, and noting that `gtm-launch-planner` is the move
once they're ready to plan the actual launch. Skip this for Iterate/Weak Signal/No-Go verdicts — it's
premature.

Score bands (from `scripts/score_idea.py`):

| Score | Band |
|---|---|
| 80-100 | Strong Go |
| 60-79 | Promising — Validate Further |
| 40-59 | Iterate on the Idea |
| 20-39 | Weak Signal |
| 0-19 | No-Go |

## Guardrails

- Never invent a competitor, quote, price, hiring number, or AI-assistant answer. If you can't find
  it, the report says so — a fabricated data point is worse than a gap, because it gets acted on.
- Don't let the score become the whole report. The evidence underneath it is what makes this
  useful; the number is just the summary.
- Keep pain-point quotes short and attributed (platform + link), not screenshots of entire threads.
- Don't reach for every tool on every idea just because it exists. The type-classification table in
  Step 1 exists so a B2C mobile app doesn't get a pointless `google_patents` call and a physical
  product doesn't get skipped on `amazon_reviews`. Breadth should track the idea, not the toolbox.
