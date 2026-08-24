# ScrapingDog MCP tool reference

The ScrapingDog MCP server (`npx -y scrapingdog-mcp`, authenticated via the `SCRAPINGDOG_API_KEY`
env var on the server side — you never see or send the key) ships in more than one build. Check
your actual tool list first (Step 0); don't assume both sets exist. This doc documents the full
30-tool build. If you only see the small (~9 tool) build, use the fallback notes inline below.

## Universal-search engines

| Tool | What it does | Typical args |
|---|---|---|
| `google_search` | Google SERP: organic results, sometimes "people also ask" | `query`, optional `country`/`language`/`page` |
| `bing_search` | Bing SERP — cross-check, or when Google results look thin | `query` |
| `baidu_search` | Baidu SERP — only relevant for China-market ideas | `query` |
| `universal_search` | One call, unified organic results across engines | `query` — good for a fast first pass before drilling in with the engine-specific tools |
| `web_scrape` | Fetches a URL's rendered content; JS rendering, markdown mode, AI-extraction rules | `url`, optional `dynamic`, `markdown`, `ai_query` |
| `screenshot` | Visual PNG/JPG/WEBP capture of a URL | `url`, optional `fullPage` |

## AI-answer-engine visibility (the tools a plain search skill doesn't have)

| Tool | What it does | Why it matters for validation |
|---|---|---|
| `chatgpt` | Sends a prompt to ChatGPT, returns its structured answer | Ask it directly: `"what's the best tool for <problem>"`. Whatever it names is today's AI-assistant incumbent — and if it says "I don't know of one," that's a real competitive opening most search-only research never surfaces. |
| `google_ai_mode` | Google's AI Mode conversational answer for a query | Same idea, Google's assistant instead of ChatGPT's — compare the two for consensus vs. disagreement on who "owns" the category. |
| `google_ai_overview` | Fetches the AI Overview block from a prior `google_search` response (URL expires ~2min) | Use right after a `google_search` call on the same query if an AI Overview link came back in the results. |

## Demand, trend, and news signal

| Tool | What it does | Typical args |
|---|---|---|
| `google_trends` | Interest-over-time and regional data | `query`, `date` (e.g. `today 12-m`) — **read the full series**, not just the latest week; a spike-then-drop pattern usually means a news event, not declining demand |
| `google_news` | Recent news coverage of a topic/company | `query` — funding rounds, launches, category-defining articles |
| `google_jobs` | Job listings aggregated from across the web | `query` (role or skill tied to the problem) — hiring volume for a role is a budget-line-item signal; also useful later for buyer-persona research (what titles/skills postings ask for) |

## Competitors, pricing, and company signals

| Tool | What it does | Typical args |
|---|---|---|
| `linkedin_profile` | Public LinkedIn person or company profile | `type: "company"` for a competitor's headcount/description, `type: "profile"` for a founder |
| `google_finance` | Live stock quotes/market data | Only useful if a competitor or close comp is publicly traded — a market-size proxy |
| `google_patents` | Patent search by query/assignee/inventor/date | Filing volume and recency around a technical approach — deep-tech/IP-landscape signal |
| `google_scholar` | Academic papers, authors, citation counts | For research-backed or novel-technical ideas — is there prior art / academic validation |

## Physical products & marketplaces (idea type: physical product / e-commerce)

| Tool | What it does | Typical args |
|---|---|---|
| `amazon_search` | Amazon search-result listings | `query`, `domain`, `country` |
| `amazon_product` | Single product page by ASIN (price, specs, ratings) | `asin` |
| `amazon_reviews` | Customer reviews for a product by ASIN | `asin`, `page` — a direct source of verbatim pain-point/satisfaction quotes for physical products |
| `amazon_offers` | All sellers/offers for a product by ASIN | `asin` — price-competition signal |
| `google_shopping` | Product listings and prices across retailers | `query` |
| `google_immersive_product` | Detailed product popup via a page token from a Shopping/Search response | `page_token` |
| `ebay_search` | eBay search listings from a full eBay search URL | `url` |
| `walmart_search` | Walmart search listings from a full Walmart search URL | `url` |
| `google_lens` | Reverse image search for visual matches/products | `url` of an image — useful for "does a product like this already exist" when you have a reference photo |

## Local & service businesses (idea type: local/service)

| Tool | What it does | Typical args |
|---|---|---|
| `google_maps` | Local business listings and place details | `query` (e.g. "pilates studio austin tx"), `type: "search"` for a list or `"place"` with `place_id` for detail — competitor density and rating benchmark in one call |
| `google_hotels` | Hotel/vacation-rental pricing and availability | Only relevant for travel/hospitality-adjacent ideas |

## Audience, community, and content (idea type: content/creator/community, or general pain-point mining)

| Tool | What it does | Typical args |
|---|---|---|
| `x_profile` | Public X (Twitter) profile metadata: bio, follower count | `profileId` — gauge whether a community/influencer around this problem exists and how big it is |
| `youtube_search` | YouTube search results with titles/metadata | `search_query` — what content already exists/ranks for this problem; a content gap is a channel opportunity |
| `youtube_video` | Metadata for a single video | `v` (video id) |
| `youtube_channel` | A channel's details and videos | `channel_id` |
| `youtube_comments` | Comments on a video | `v` — real, unprompted pain-point and satisfaction language, especially on "how do I..." or product-review videos |
| `youtube_transcripts` | Full transcript with timestamps | `v` — for a deeper read than comments alone, e.g. confirming what a reviewer actually said about a competitor |
| `google_images` | Image search results with sources | `query` — quick visual scan of a competitive landscape (logos, product screenshots, UI style) |
| `google_shorts` | Short-video search results | `query` — short-form content volume/gap signal, useful for consumer/creator ideas |

## Mapping research questions to tool calls (quick lookup)

**Demand & trend signal** — `google_trends` for the core keyword + 1-2 variants; `google_news` for
recent coverage; `google_jobs` for hiring-side demand. On the small tool-set build: `google_search`
for the keyword plus `"<keyword> alternative"` / `"<keyword> vs"` as a comparison-volume proxy.

**AI-answer-engine visibility** — `chatgpt` with a direct "what's the best tool for X" prompt, plus
`google_ai_mode`/`google_ai_overview` for the same question on Google. Not available on the small
build — skip this category honestly rather than faking it with a regular search result.

**Competitors** — `google_search` for `<problem/keyword> tool`, `<keyword> software`, `best <category>
for <audience>`; `web_scrape` each candidate's homepage/pricing page; `screenshot` when a visual
comparison would help the report. For physical products, `amazon_search`/`google_shopping` instead.
For local businesses, `google_maps` search mode covers competitors and their ratings in one call.

**Pricing / willingness-to-pay** — `web_scrape` the `/pricing` page of each competitor. For physical
products, `amazon_product`/`amazon_offers`/`google_shopping` give real transaction prices directly.
`google_search` for `<keyword> pricing reddit` or `<keyword> "worth it"` finds real users discussing
whether the price is justified — stronger evidence than the sticker price alone.

**Audience pain points** — `google_search`/`bing_search` with `site:reddit.com <problem keywords>`,
`site:news.ycombinator.com <keyword>`. `web_scrape` the actual thread before quoting — search
snippets are truncated and easy to misquote. `youtube_comments` on a relevant tutorial/review video
and `x_profile` for a known community/influencer add pain-point sources a search-only skill can't
reach. For physical products, `amazon_reviews` is a direct, high-volume pain-point source.

**Market size** (best-effort, treat as weak signal) — `google_search` for `<category> market size` /
TAM / industry-report titles; `google_finance` if a public comp exists; competitor count from the
step above is itself a rough proxy. `google_patents`/`google_scholar` filing/publication volume is a
weak-but-real proxy specifically for deep-tech ideas.

## Query hygiene

- Run 2-4 targeted queries per category rather than one broad one — SERPs (and marketplace/social
  APIs) reward specificity.
- If a query returns nothing useful twice, stop and record the gap rather than burning more calls
  rephrasing the same idea a fifth way.
- Large scraped pages (a long Reddit/HN thread, a big listing page) can exceed the tool's inline
  output limit and get saved to a file instead — read it in chunks with the file-reading tool rather
  than re-scraping with different params.
- Always keep the source URL for anything you plan to cite or quote in the report.
