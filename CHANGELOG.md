# Algorithm changelog

Changes to X's For You ranking parameters, newest first, found by running `scripts/param_history.py` against [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm). Dates are commit dates in the public repo; the production change may have happened earlier.

## 2026-10-17 · commit 862a123 — new experiments, all off by default
- New filter `ZeroFavCodivertFilter` ([zero_fav_codivert_filter.rs](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/filters/zero_fav_codivert_filter.rs)). One retrieval source finds posts that have **zero likes** (`ForYouPhoenixRetrievalZeroFav`). For viewers in the experiment, posts that came *only* from that source are removed unless the author is in the treatment group. All three switches default to `false`. Meaning for posters: X is testing how much distribution zero-like posts should get; nothing changes today. The first like still matters through the early-like lottery (see 2026-09-30).
- New `EnablePostEngagers` (default `false`): would send up to 32 recent positive and 8 negative engagers of a post, with timestamps, into the ranking model. If turned on, *who* engaged with a post, not only how many, becomes a model input (inference).
- Video carousel: author dedupe `false → true`, embedding dedupe `false → true`, semantic-ID dedupe levels `0 → 3`. The carousel module itself (`EnableVideoCarousel`) is still `false`, so no visible effect yet. If it turns on, one author or near-duplicate videos get at most one slot in it (inference).
- Large rewrite of `abuse-enforcement-service` action control (levels, confidence, rollback). No rule in `RULES.md` changes; the low-quality AI label rule still reads the same.

## 2026-10-16 · commit bc3948b
- Video carousel embedding dedupe added (off) with similarity threshold 0.72. Plumbing only.

## 2026-10-15 · commit 92f0918
- Video carousel scoring parameters added: video-open weight 1.0, immersive "valid view" weight 0, long-dwell aggregation. Carousel still off.
- Ads brand-safety fallback on author `false → true`. Affects ads, not organic posts.

## 2026-10-14 · commit 17c96bf
- Like weight 0.6 → **0.66**
- "Not interested" weight -47.52 → **-52.272** (second increase in two weeks)

## 2026-10-13 · commit e1a0375
- Like weight 0.5 → **0.6**
- Video open weight 0.07 → **0.02**
- Dwell-time weight 0.004 → 0.006

## 2026-10-07 · commit 78460ca
- "Unexplored post" weight 0.02 → 0.015

## 2026-09-30 · commit 77d431a — the small-account boost changed
- Post age limit for the boost **48 hours → 2 hours**
- Impression cap for the boost **1,000 → 200**
- Follower cap for the boost **1,000 → 50,000**
- Thompson-sampling lottery on early like rate **off → on**
- No public explanation from X.

## 2026-09-29 · commit a707cc2
- "Time spent after clicking" weight **0 → 0.4** (new)
- Click weight 0.4 → 0.3
- "Not interested" weight -43.2 → **-47.52**

## 2026-09-17 · commit 42266f3
- Post age limit for the boost 24 hours → 48 hours

## 2026-08-25 · commit 0d3cdd8
- Dwell weight 0 → 0.05
- Video "valid view" weight 0.05 → **0**
- Video open weight 0.05 → 0.07

## 2026-08-13 / 14
- X publishes weights, parameters and visibility rules for the first time. Cold-start lottery parameters added (off by default).

## Earlier
- 2026-07-13: extra reply weight when viewer and author follow each other ships at +20; on 2026-07-24 it is set to +15, on top of the base reply weight of 5 — [docs/BIDIRECTIONAL_BOOST_CHANGE.md](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/docs/BIDIRECTIONAL_BOOST_CHANGE.md)
- 2026-01-20: first release of the new Grok-era algorithm.
