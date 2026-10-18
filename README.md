# x-algorithm-playbook

**Keep up with X's algorithm, and review your posts against it.**

X open-sourced its For You algorithm ([xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)) and updates it almost every weekday, usually without an announcement. On September 30, 2026, the boost for small accounts quietly went from 48 hours to 2 hours.

This repo does two things:

1. **Tracks every algorithm change.** A script diffs X's ranking parameters across every commit. [`CHANGELOG.md`](CHANGELOG.md) lists what changed and when; [`RULES.md`](RULES.md) says what's in effect today, with the exact line of code behind each rule.
2. **Reviews everything you posted.** A weekly or monthly review of all your posts *and replies*, checked against the current rules, ending in a short action list for the next period.

Plus a pre-post check for long posts, threads and replies.

## What's inside

| | What it does |
|---|---|
| [`RULES.md`](RULES.md) | The rules in effect, in plain English, each linked to the source line |
| [`CHANGELOG.md`](CHANGELOG.md) | Every ranking change since August 2026, newest first |
| [`scripts/param_history.py`](scripts/param_history.py) | Lists every change to X's ranking parameters: date, commit, old → new |
| [`skills/x-algo-watch`](skills/x-algo-watch/SKILL.md) | Claude Code skill: "what changed in the X algorithm since…", updates the changelog |
| [`skills/x-post-review`](skills/x-post-review/SKILL.md) | Claude Code skill: weekly / monthly review of your posts and replies → action list |
| [`skills/x-post-check`](skills/x-post-check/SKILL.md) | Claude Code skill: check a long post, thread or reply before posting, then rewrite it |
| [`prompts/audit-prompt.md`](prompts/audit-prompt.md) | The same pre-post check as a copy-paste prompt for Claude, ChatGPT or Grok |

## Quick start

**See what changed recently**

```bash
git clone https://github.com/leohuanfang-hub/x-algorithm-playbook && cd x-algorithm-playbook
python3 scripts/param_history.py --since 2026-09-01
```

```
2026-09-29  a707cc2  NotInterestedWeight: -43.2 -> -47.52
2026-09-30  77d431a  ColdStartFollowerCap: 1000 -> 50000
2026-09-30  77d431a  ColdStartImpressionThreshold: 1000 -> 200
2026-09-30  77d431a  ColdStartMaxPostAgeSecs: 172800 -> 7200
...
2026-10-14  17c96bf  NotInterestedWeight: -47.52 -> -52.272
```

**Use the skills in Claude Code**

```bash
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

Then ask Claude Code: *"Review my X posts and replies from last week"* (paste or attach your numbers from X Analytics), *"Check this thread before I post it"*, or *"Did the X algorithm change since October 1?"*

**No Claude Code?** Use [`prompts/audit-prompt.md`](prompts/audit-prompt.md) in any chatbot.

## The 7-point checklist (short version)

1. Put your best idea in the first post. Strangers only see post 1 of a thread.
2. Upload your own video, over 10 seconds. Quoted videos don't count.
3. Stay online for the first 2 hours. The small-account boost only considers posts under 2 hours old.
4. Write something people copy the link of. Copy link = 20, like = 0.66.
5. Build mutuals in your niche. Replies between mutual follows weigh 20 instead of 5.
6. Never post from a template. "Not interested" = -52, and AI-slop labels last 30 days.
7. Put links in a reply.

Details and sources: [`RULES.md`](RULES.md).

## How current is this?

Rules are pinned to a specific commit, shown at the top of `RULES.md`. Before relying on a number, run `scripts/param_history.py --since <that date>` or the `x-algo-watch` skill. If you find something new, or have data on what the code doesn't show (for example how replies are ranked under a post), open an issue.

## Not affiliated with X

This is an independent reading of public code. Weights multiply the model's predicted probabilities for each viewer, not raw counts, and the public code is not guaranteed to match production exactly.

MIT License · by [@leohuanfang](https://x.com/leohuanfang)
