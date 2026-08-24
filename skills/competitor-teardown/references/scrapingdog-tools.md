# ScrapingDog MCP tool reference: competitor teardown

Full tool catalog and how it maps to this skill's five research questions. See
`startup-idea-validator/references/scrapingdog-tools.md` for the complete 30-tool reference with
every tool's args. This file is the trimmed, teardown-specific lookup.

## Product & positioning

| Tool | Use |
|---|---|
| `web_scrape` | Homepage + `/pricing` page, `markdown: true` for a clean read. `ai_query` can extract a specific fact directly (e.g. "what does the free tier include") if the raw page is noisy. |
| `screenshot` | Visual capture of the homepage: `fullPage: true` when the page is short enough to matter in full; otherwise viewport is fine for a first impression. |
| `google_images` | Fast visual scan across several competitors at once before deciding which to `screenshot` in full. |

## Hiring velocity

| Tool | Use |
|---|---|
| `google_jobs` | `query: "<competitor name>"` or narrower (`"<competitor name> engineer"`). Count and categorize open roles (eng vs. GTM vs. support): the mix tells you what stage they're investing in, not just that they're growing. |
| `linkedin_profile` (`type: "company"`) | Headcount and description, when public. Cross-check against job-posting volume: a lot of open roles against a small existing headcount signals a real growth push. |

## Funding & press recency

| Tool | Use |
|---|---|
| `google_news` | `query: "<competitor name>"`. Sort by recency; the gap between "now" and the last substantive mention is the actual signal, not the mention count. |
| `google_finance` | Only if the competitor (or its parent) is publicly traded. |
| `google_patents` | `assignee: "<competitor name>"`: filing activity as a technical-investment signal, mainly relevant for deep-tech competitors. |

## Review volume & sentiment

| Tool | Use |
|---|---|
| `amazon_reviews` | Direct for a physical-product competitor, by ASIN (find it via `amazon_search` first). |
| `web_scrape` | For software: search `site:g2.com`/`site:capterra.com`/`site:trustpilot.com "<competitor>"` via `google_search`, then scrape the actual review page. Don't quote a search snippet. |
| `youtube_comments` | On a review or comparison video (find via `youtube_search`): real reactions, often more candid than star-rated reviews. |
| `youtube_transcripts` | When a reviewer's actual verdict matters more than comment reactions: pull what they said, not just what viewers replied. |

## Social reach

| Tool | Use |
|---|---|
| `x_profile` | Follower count and bio: a rough audience-size and positioning proxy. |
| `youtube_channel` | If the competitor runs a YouTube presence: subscriber count and upload cadence as a content-investment signal. |

## Query hygiene

- One competitor at a time in your head, even when calling tools in parallel. Don't let evidence
  from two competitors blend into one paragraph.
- A long scraped review or forum page can exceed the inline output limit and land in a file instead;
  read it in chunks rather than re-scraping with different parameters.
- If `google_jobs`/`google_news`/reviews genuinely return nothing after a real attempt, that's a
  valid "not found": don't substitute a plausible-sounding guess.
