# Algorithm changelog

Changes to X's For You ranking parameters, newest first, found by running `scripts/param_history.py` against [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm). Dates are commit dates in the public repo; the production change may have happened earlier.

## 2026-10-27 · commit 2f25214 — debias inputs sent, debias scoring still off
- `VMRankerSendDebiasInputs` changed from `false` to `true`. Home-mixer now sends the viewer's engagement sequence, surface and per-candidate content features to the value-model ranker ([payload](https://github.com/xai-org/x-algorithm/blob/2f252142b9284e692ac72851768c8072d045f0d5/home-mixer/scorers/vm_ranker_debias_payload.rs)). The new [per-user debias step](https://github.com/xai-org/x-algorithm/blob/2f252142b9284e692ac72851768c8072d045f0d5/vm-ranker/scoring/debias.rs) would recenter each viewer's predicted probabilities (like, reply, profile click, bookmark and others) against a global baseline, so viewers who engage with everything count for less. It is gated by `UserDebiasEnabled`, which defaults to `false`, with `UserDebiasAlpha` at `0.0` ([params](https://github.com/xai-org/x-algorithm/blob/2f252142b9284e692ac72851768c8072d045f0d5/vm-ranker/params.rs)). Sending inputs alone does not change scores. Posting implication: none yet; watch for `UserDebiasEnabled` turning on.
- `ShadowTrafficPhoenixClusterRates` adds `Experiment19Fou:0.3`. Shadow traffic is a copy of requests scored by an experimental cluster; it does not change what viewers see.
- The same commit restructures visibility filtering (a new verdict gate and treatment code). Rule defaults covered in RULES.md were not re-audited in this entry.
- The parameter file at `2f25214` records its most recent production-default sync as October 26, 2026, 16:00:39 UTC.

## 2026-10-24 · commit 6258a15 — source allocation and label duration
- October 22, `989fb91`: `EnableFairShareRanking` changed from `false` to `true`. The new [filter](https://github.com/xai-org/x-algorithm/blob/6258a1549ef808be88fba83d3b2d58364b587ee0/home-mixer/filters/fair_share_ranking_filter.rs) divides the candidate budget proportionally across retrieval source types, preserving each source's existing order. It only runs without cached posts, with a scoring sequence, and without the ranker kill switch. This allocates places to retrieval sources, not to authors or follower sizes. No claim that it boosts small accounts is justified.
- October 23, `07d159b`: the low-quality AI account rule (`act_add_llm_slop_label`) changed newly applied `SpamHighRecall` label duration from 30 days to **7 days** (604,800,000 milliseconds). The rule still skips an account already bearing the label; this diff does not prove existing labels expire sooner. Other spam rules retain separate durations. Posting implication: avoid low-quality repetitive AI output; the shorter duration is not permission to spam.
- October 20–23: 28-day history-topic inputs and recent search-query hydration were added but remain disabled by default. The new-account soft-NSFW filter also defaults to off. No new posting checklist follows from disabled experiments.
- October 22–24: video candidate logging and ad funnel tracing default to on; these are logging changes, not evidence of a new organic score weight. The video carousel itself stays off. Like, negative-feedback and cold-start parameter defaults did not change during this interval.
- The parameter file at `6258a15` records its most recent production-default sync as October 23, 2026, 16:00:34 UTC. The README's Notable Updates section has no new dated announcement after September 18. Public code defaults do not establish per-account production experiment assignment.

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
