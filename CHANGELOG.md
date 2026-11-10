# Algorithm changelog

Changes to X's For You ranking parameters, newest first, found by running `scripts/param_history.py` against [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm). Dates are commit dates in the public repo; the production change may have happened earlier.

## 2026-11-05 to 11-10 · commits 021afa4 … 660cd74 — weights retuned, new signals still at 0

- **November 5, `021afa4`: the first weight change since October 14.** Like 0.66 → **0.708**, share 2.0 → **2.118**, "not interested" -52.272 → **-53.07** (third increase since late September), time spent after clicking 0.4 → 0.385, click 0.3 → 0.274, dwell time 0.006 → 0.0075, video open 0.02 → **0** ([param.rs](https://github.com/xai-org/x-algorithm/blob/660cd7407c5726ec8d3aef27c32e1377b1c7e480/home-mixer/params/param.rs#L400-L540)). Copy-link share (20), reply (5), quote (5), DM share (5), follow (4), repost (1) and the negative weights other than "not interested" did not move. Posting implication: the balance keeps tilting toward likes and shares and further against posts people mark "not interested"; merely getting someone to open a video now earns nothing.
- Same commit: `EnableHomeExcursionScores` false → **true** and the model aggregation becomes `DENSE_WITH_LONG_DWELL_HOME_EXCURSION`. The model now also predicts how many seconds a viewer keeps watching a video after opening it, and how long they stay on your profile after clicking it ([phoenix_scorer.rs](https://github.com/xai-org/x-algorithm/blob/660cd7407c5726ec8d3aef27c32e1377b1c7e480/home-mixer/scorers/phoenix_scorer.rs#L131-L185)). In the home-mixer scorer both weights are hard-coded to 0 ([value_model.rs](https://github.com/xai-org/x-algorithm/blob/660cd7407c5726ec8d3aef27c32e1377b1c7e480/home-mixer/scorers/value_model.rs#L39-L41)), so they do not change scores yet. What the new aggregation type changes inside the model is not documented (unclear).
- **November 10, `660cd74`: new-viewer quality filter tuned, still off.** `NewUserMinEngagementFilter` ([code](https://github.com/xai-org/x-algorithm/blob/660cd7407c5726ec8d3aef27c32e1377b1c7e480/home-mixer/filters/new_user_min_engagement_filter.rs)) applies only to viewers whose account is under 30 minutes old or who came back to X in the last 30 minutes. For them it would drop posts from accounts they don't follow whose likes divided by views are below **0.4%**. The ratio mode and 0.004 threshold were switched on, but the filter itself (`EnableNewUserMinEngagementFilter`) is still `false`. Posting implication if it turns on: posts with fewer than about 4 likes per 1,000 views stop reaching brand-new users.
- New model heads, weighted 0: `GrokAnalyzeWeight` (Nov 4, the viewer asking Grok about the post) and `PostVideoWeight` (Oct 30, replaces `ReactWithVideoWeight`). They are plumbing until a weight appears.
- Off by default: `PageDecodeRerank` (Oct 28; from its parameters it appears to pick a whole page of posts as a set rather than one by one, with an exploration mode), `ShuffledHistoryRetrieval` and an in-feed "Under the hood" frame (Nov 10). The video carousel gained a click-through model, a seen filter and high-risk filters, but `EnableVideoCarousel` is still `false`.
- `NewUserSoftNsfwFilterMaxAccountAgeSecs` 1 day → 7 days (Oct 28); the filter itself is still off. Ads blender switched three times (`multi_risk` ↔ `slot_spread`); ads only.
- Large rewrite of visibility filtering (verdict gate, treatment code) and of abuse-enforcement action control. The low-quality AI label rule in `enforcement_user.yaml` did not change. The cold-start boost, the 48-hour age limit and the stranger-reply filter did not change.
- The README's Notable Updates gained three dated entries after October 27: October 8 (better time-spent prediction), October 13 (retrieval trained on read-through) and October 26 (Brazil election filter removed).
- The parameter file at `660cd74` records its most recent production-default sync as November 9, 2026, 16:00:34 UTC.

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
