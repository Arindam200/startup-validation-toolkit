# ScrapingDog MCP tool reference: go-to-market planning

Full tool catalog and args live in `startup-idea-validator/references/scrapingdog-tools.md`. This is
the trimmed, GTM-specific lookup: which tools answer which planning question.

## Buyer persona, evidence-based

| Tool | Use |
|---|---|
| `google_jobs` | `query: "<role tied to the problem>"`. Pull actual job titles and the skills/tools listed as requirements across several postings: a real, evidence-based persona instead of an assumed one. |
| `linkedin_profile` (`type: "company"`) | For B2B ideas, look up 2-3 target-customer-shaped companies for size/industry context on the buyer persona. |

## Where the audience already is

| Tool | Use |
|---|---|
| `youtube_search` | What content already ranks for this problem: a crowded, recent results list means the audience is there watching; a thin/stale one is a content gap. |
| `youtube_comments` | On the top-ranking video(s) from the search above: real audience language and unmet requests. |
| `youtube_transcripts` | When what a creator actually said matters more than what viewers replied. |
| `x_profile` | Any known community/influencer account in the space: audience size and positioning proxy. |
| `google_maps` | For local/service ideas: where the physical audience already goes and who currently serves them. |
| `google_trends` | Seasonality: whether interest in this problem clusters around a time of year worth timing a launch to. |

## AI-answer-engine visibility (this skill's core differentiator)

| Tool | Use |
|---|---|
| `chatgpt` | Direct prompts: `"what's the best tool for <problem>"`, `"how do people usually solve <problem>"`. Record exactly who's recommended and in what order. |
| `google_ai_mode` | Same questions through Google's AI Mode: compare against ChatGPT's answer for consensus vs. disagreement. |
| `google_ai_overview` | The AI Overview block from a `google_search` call on the same query (URL expires ~2min: fetch right after the search). |

## Positioning inputs

| Tool | Use |
|---|---|
| `google_search` / `bing_search` | `site:reddit.com`/`site:news.ycombinator.com` pain-point search if `competitor-teardown` wasn't already run. |
| `web_scrape` | Read the actual thread before quoting; also used for competitor `/pricing` pages for the pricing benchmark. |

## Content/SEO seed list

| Tool | Use |
|---|---|
| `google_search` | The "people also ask" block in results is a direct source of real questions to write content around. |
| `youtube_search` | Video titles/descriptions on adjacent, well-performing content reveal phrasing and angles that already work. |

## Query hygiene

- Ask the `chatgpt`/AI-overview questions in more than one phrasing (as a beginner would ask, as an
  experienced buyer would ask): the recommended answer can shift with phrasing, and that shift is
  itself useful information about which angle to own.
- Don't recommend a channel a tool call didn't actually support: an empty or thin result for
  `youtube_search` is evidence against that channel, not a reason to skip mentioning it.
