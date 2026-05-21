# events-stats

Single-page unified analytics dashboard for the four city pages of [fengelh2/events](https://github.com/fengelh2/events) — Hong Kong, Los Angeles, NRW, and Singapore.

**Live:** https://fengelh2.github.io/events-stats/

## One-time setup

1. Sign up at https://www.goatcounter.com/signup (free, no credit card).
2. The default site uses your username as the subdomain (currently `fengelh.goatcounter.com`).
3. Go to **Settings → Site → Access → "Allow access to all"** (so the public stats endpoints work without an API token).

That's it. All four city pages (`/events/hk/`, `/events/la/`, `/events/nrw/`, `/events/singa/`) post to the same GoatCounter site; the dashboard splits per-city by URL path prefix.

## What it shows

Per site, for any of: today / 7d / 30d / 90d / 12 months:
- Unique visitors
- Pageviews
- Event clicks (which event rows users opened)
- Mobile vs desktop split (derived from screen sizes)
- Top pages
- Top **event clicks** (which specific events got clicked — most useful signal)
- Where visitors came from (referrers — WhatsApp, Google, direct, etc.)
- Top countries
- Top browsers

Plus a side-by-side comparison bar of unique visitors across the four sites.

## Privacy

GoatCounter is cookie-free and GDPR-friendly by default — no banner needed.
