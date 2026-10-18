# Rules in effect

What X's open-source For You algorithm does today, in plain English, with the exact source for each rule.

- **Code version:** [xai-org/x-algorithm @ 862a123](https://github.com/xai-org/x-algorithm/tree/862a1235ca4d743cc48211309ebbbcc1a5a540a3) (October 17, 2026). The parameter file says it was last synced with production on October 16, 2026.
- **How to read the weights:** each weight multiplies the model's *predicted probability* that this viewer takes the action. It does not multiply raw counts. One report does not cancel 234 likes ([README, August 14 update](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/README.md#notable-updates)).
- **Confidence:** "Code" means read in the source. "X staff" means a public post by X staff. "Inference" means our reading of what the code implies, not proven.

## 1. Only the first post of a thread reaches strangers (Code)

- For You drops replies and reposts from accounts the viewer doesn't follow. A switch to let some through exists and is off. Every post after the first in a thread is a reply to yourself. ([oon_retweet_reply_filter.rs](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/filters/oon_retweet_reply_filter.rs), [param.rs L74](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/params/param.rs#L74))
- The retrieval index used to find posts for strangers skips self-replies. ([phoenixRankAllCandidateProcessor.strato L477-495](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/phoenix-rankall-strato/columns/phoenix_rank_all/phoenixRankAllCandidateProcessor.strato#L477-L495))
- Even for followers, one refresh keeps one post per conversation. ([dedup_conversation_filter.rs](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/filters/dedup_conversation_filter.rs))

## 2. The small-account boost lasts 2 hours (Code)

`AuthorColdStart` lifts at most one post per feed refresh to about position 16. A post qualifies only if it is an original (not a reply or repost), the author has at most 50,000 followers, it is under 2 hours old, and it has fewer than 200 home-timeline views. Among qualifying posts, a Thompson-sampling lottery on early like rate picks the winner: every view without a like lowers its odds. ([author_cold_start.rs](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/scorers/author_cold_start.rs#L188-L334), [param.rs L507-580](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/params/param.rs#L507-L580))

## 3. The weights (Code)

| Action | Weight |
|---|---|
| Copy link to share | 20 |
| Reply from someone who follows you back (original posts only) | 20 |
| Reply | 5 |
| Quote | 5 |
| Share via DM | 5 |
| Follow the author | 4 |
| Share | 2 |
| Repost | 1 |
| Like | 0.66 |
| Time spent after clicking | 0.4 × predicted duration (unit not documented) |
| Open a link | 0.2 |
| Click into the profile | 0 |
| Not interested | -52.272 |
| Mute author | -58.8 |
| Block author | -31.2 |
| Report | -234 |

Source: [param.rs L309-456](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/params/param.rs#L309-L456), mutual-follow boost in [weights.rs L84-91](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/xai-value-model/weights.rs#L84-L91) and [inputs.rs L20-22](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/xai-value-model/inputs.rs#L20-L22). The 2023 "author engages with your reply = 75" weight no longer exists.

## 4. Video only counts if it's your own upload (Code + X staff)

A post enters the video index only if the post itself carries the video; quoted videos don't count ([eventProcessing.strato L393](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/phoenix-rankall-strato/lib/eventProcessing.strato#L393)). Videos under 10 seconds don't count as a valid view ([param.rs MinVideoDurationMs](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/params/param.rs#L605)). X says duplicate detection got 3x better in July 2026 and pays the original creator for copies ([Nikita Bier](https://x.com/nikitabier/status/2077774853650944028)).

## 5. Posts older than 48 hours leave For You (Code)

[config.rs L40](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/home-mixer/params/config.rs#L40).

## 6. Low-quality AI content gets a 30-day label (Code)

An account classified as low-quality AI content gets a "SpamHighRecall" label for 30 days, which removes its posts from recommendations to non-followers. Accounts above a follower threshold skip this check; the public threshold is a placeholder ("a mock value to reduce gaming"). ([enforcement_user.yaml L58-69](https://github.com/xai-org/x-algorithm/blob/862a1235ca4d743cc48211309ebbbcc1a5a540a3/abuse-enforcement-service/service-lib/rules/enforcement_user.yaml#L58-L69))

## 7. Links: no hard-coded penalty (Code + X staff + Inference)

No rule penalizes links in the ranking code; opening a link is weighted 0.2. X staff explain that link posts get fewer likes and replies because the browser covers the post ([Nikita Bier](https://x.com/nikitabier/status/1979994223224209709)). The model learns from that behavior, so link posts still tend to rank lower (inference).

## 8. Asking for engagement is penalized (X staff)

Soliciting engagement ("I'll follow everyone who replies") 3 or more times removes an account from creator payouts; Grok detects it ([Nikita Bier](https://x.com/nikitabier/status/2077774853650944028)).

## 9. Check your own labels

[x.com/i/jf/under_the_hood](https://x.com/i/jf/under_the_hood) shows visibility labels on your account and posts.

## Known unknowns

- How replies are ranked under a post is not in the repo.
- The unit of the "time spent after clicking" weight is not documented.
- `home-mixer/params/param.rs` (synced) has likes at 0.66; `vm-ranker/params.rs` still has 0.5.
- Some thresholds are deliberate placeholders in the public code.
- X has not explained the September 30, 2026 cold-start change.
