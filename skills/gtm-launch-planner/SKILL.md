---
name: gtm-launch-planner
description: "Turns a validated idea into an actual go-to-market plan using the ScrapingDog MCP server — maps buyer-persona titles from live job postings, finds where the audience already gathers (YouTube content gaps, X communities, local listings), checks what ChatGPT and Google AI answers already recommend for this problem, benchmarks pricing against real competitor data, and turns competitor weaknesses into a positioning statement. Third and final stage of a three-skill pipeline, after startup-idea-validator and competitor-teardown. Use when the user has a validated idea and asks how to launch, market, position, price, or find first customers — 'how do I sell this', 'who is my audience and where do I find them', 'how should I position this against [competitor]', 'what channels should I use', 'help me plan my launch', or 'write me a go-to-market plan'. For the initial 'is this a good idea' question, use startup-idea-validator instead."
---

# GTM Launch Planner

Validation tells you an idea *can* work. This skill is about the much harder question: given this
idea, these competitors, and this audience, what's the actual sequence of moves that gets the first
100 customers: which channel, what to say to them, and how to price it. It leans hard on the two
tools a plain web-search skill doesn't have: a direct ChatGPT-query tool and Google's AI Overview/AI
Mode, because "what does an AI assistant already recommend when someone asks this question" is
rapidly becoming a real discovery channel, and almost nobody's research process checks it.

## Why this isn't just "marketing advice"

Generic go-to-market advice ("post on Twitter, do content marketing") is worthless because it isn't
grounded in anything specific to this idea. This skill instead pulls real inputs: the actual job
titles companies use when hiring for the problem this idea solves (from live job postings, so the
buyer persona is evidence-based, not guessed), the actual content that already exists and ranks for
the problem (so a content gap is identified, not assumed), and the actual answer an AI assistant
gives right now when asked "what's the best tool for this" (so positioning targets a real, current
gap instead of a hypothetical one).

## Step 0: Confirm the MCP server and tools

Same check as the rest of the pipeline: confirm `mcp__scrapingdog*` tools are available before
starting (see `startup-idea-validator/SKILL.md` for the config block if not). Read
`references/scrapingdog-tools.md` for this skill's tool-to-question mapping.

## Step 1: Gather what's already known

Get the idea (what it is, who it's for, the problem it solves) and, if available, reuse the outputs
of a prior `startup-idea-validator` run (score, competitors, pain points) and/or a
`competitor-teardown` run (momentum, gaps and openings) instead of re-deriving them. If neither exists
yet, do a fast version of the competitor + pain-point research inline: this skill still needs to
know who else is in the space and what people complain about before it can plan positioning, but it
doesn't need the full scoring pipeline to do it.

## Step 2: Research

Use `references/scrapingdog-tools.md` for exact tool/query mapping.

1. **Buyer persona, evidence-based**: `google_jobs` for roles tied to the problem this idea solves.
   Pull the actual job titles and the skills/tools listed as requirements across several postings:
   that's a real buyer/user persona, not an assumed one. For a B2B idea, `linkedin_profile`
   (`type: "company"`) on 2-3 target-customer-shaped companies adds company-size/industry context.
2. **Where the audience already is**: `youtube_search` for existing content on this problem: what
   ranks, how recent, how good. A crowded, current results list means the audience is already there
   watching content: go find that channel's comments (`youtube_comments`) for language and unmet
   requests. A thin or stale results list is itself a content-gap opportunity. `x_profile` for any
   known community/influencer accounts in the space. For local/service ideas, `google_maps` shows
   where the physical audience already is and how they're currently served.
3. **AI-answer-engine visibility (the differentiated part)**: use the `chatgpt` tool directly:
   `"what's the best tool for <problem>"`, `"how do people usually solve <problem>"`, `"what should I
   use for <problem> as a <target user>"`. Also pull `google_ai_overview`/`google_ai_mode` for the
   same questions on Google. Record exactly who gets recommended, in what order, and with what
   caveats. This tells you two things directly usable in the plan: (a) whether "ask an AI assistant"
   is already how people discover solutions here: if so, that's a channel to optimize for, not
   just social/content; (b) precisely who currently owns that answer, which is the competitor to
   position against first.
4. **Positioning inputs**: pull whatever gaps/openings `competitor-teardown` already found; if that
   wasn't run, do a fast pain-point pass (`google_search site:reddit.com`/`site:news.ycombinator.com`,
   `web_scrape` the threads) specifically looking for what people say is missing or wrong with
   existing options.
5. **Pricing benchmark**: reuse competitor pricing already gathered by the earlier skills, or pull it
   fresh with `web_scrape` on competitor `/pricing` pages if starting cold.

If a category comes up thin, say so plainly in the plan rather than filling it with generic advice:
"no clear existing content on this exact problem" is itself a real, usable finding.

## Step 3: Build the plan

There's no scoring script here: a go-to-market plan is a set of ranked, justified recommendations,
not a single number. Structure it as:

1. **Positioning statement**: one or two sentences: for [buyer persona, from Step 2's job-posting
   evidence], [idea] is the [category] that [specific differentiator, from the gaps/openings and
   AI-visibility findings], unlike [the competitor currently owning the AI-answer-engine
   recommendation and/or the top pain-point complaint].
2. **Primary channel recommendation**: ranked, with the evidence for each: content (if a gap exists),
   community (if an active one was found), AI-answer-engine optimization (if "ask AI" is clearly how
   people already search this category), local/outbound (for local-business or B2B ideas with a
   findable persona). Justify the ranking with what Step 2 actually found. Don't default to "do
   everything."
3. **First-customers plan**: concrete: which specific community/thread/channel to show up in first,
   what to say (tied to the positioning statement), and what a reasonable first-30-days target looks
   like given the audience size signals found.
4. **Pricing recommendation**: a specific number or range, benchmarked against the real competitor
   prices gathered, with the reasoning (undercut, match, or premium-position, and why).
5. **Content/SEO seed list**: 5-10 concrete topics or questions pulled from "people also ask" data,
   YouTube content gaps, or recurring pain-point language: things to actually write next, not a
   generic content-calendar template.
6. **AI-visibility play**: the specific, concrete move: e.g. "get listed/mentioned where ChatGPT's
   current answer sources from" or "the current AI Overview cites [X]: publish the kind of content
   that page has, since that's evidently what the answer engine is pulling from."

Before moving to Step 4, confirm:

- [ ] Every job title, channel claim, and pricing figure traces to a specific finding from Step 2,
      not memory.
- [ ] Any category that came up thin says so plainly instead of being papered over with generic
      advice.
- [ ] The channel ranking and positioning statement are justified by what Step 2 actually found, not
      a default "do everything" list.
- [ ] The AI-visibility findings are surfaced prominently, not buried as an aside.

## Step 4: Deliver the plan

Publish as a shareable Artifact by default: load the `artifact-design` skill before writing the HTML,
same as the rest of the pipeline. `assets/gtm-template.html` is a theme-aware starting layout; adapt
it to the specific idea rather than filling placeholders verbatim. This is a plan someone will
actually try to execute from, so favor clear, scannable structure (numbered actions, a channel
ranking) over prose density.

## Guardrails

- **Trace every recommendation**: every recommendation should trace to a specific finding from
  Step 2. A channel or persona claim with no cited evidence is exactly the generic advice this skill
  exists to avoid. The tell: a recommendation you can't point back to a specific Step 2 finding.
- **Absence is evidence**: don't recommend a channel just because a tool exists for it. If
  `youtube_search` turns up nothing relevant, that's evidence *against* YouTube as a channel here,
  not a reason to skip reporting it.
- **AI-visibility findings are the differentiator**: don't bury them as a minor aside. If nobody
  currently owns the AI-assistant answer for this problem, that's headline material.
- **Never invent**: a job-posting count, competitor price, or AI-assistant answer. Say "not found"
  plainly.
