# x-algorithm-playbook

**X's algorithm changes almost every weekday. This repo tells you what changed, what's in effect today, and how your posts stack up against it.**

X open-sourced its For You ranking code at [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) and keeps updating it, usually without an announcement. One example: on September 30, 2026, the boost for small accounts quietly went from 48 hours to 2 hours. If you were still timing posts for a two-day window, you were optimizing for a rule that no longer existed.

This repo reads that code for you, in plain English, with a link to the exact line behind every claim.

> Last synced to X's code on **November 10, 2026** (commit `660cd74`). See [How current is this?](#how-current-is-this)

---

## Start here: what do you want to do?

| I want to… | Go to |
|---|---|
| Know the rules in effect right now | [Path 1](#path-1-read-the-rules) |
| Check a post or thread before I publish it | [Path 2](#path-2-check-a-post-before-posting) |
| Review how my posts and replies did last week or last month | [Path 3](#path-3-review-your-last-week-or-month) |
| See every algorithm change myself, straight from the code | [Path 4](#path-4-track-changes-yourself) |

Paths 1 to 3 need no install: any chatbot works (Claude, ChatGPT, Grok). Claude Code users get a fuller version through the skills.

---

### Path 1: Read the rules

1. Skim the [7-point checklist](#the-7-point-checklist) below.
2. For the reasoning and sources, open [`RULES.md`](RULES.md). Each rule is labeled **Code** (read in X's source), **X staff** (a public post by X staff) or **Inference** (our reading, not proven).
3. To see what changed recently, open [`CHANGELOG.md`](CHANGELOG.md), newest first.

### Path 2: Check a post before posting

**In any chatbot**

1. Open [`prompts/audit-prompt.md`](prompts/audit-prompt.md) and copy the prompt.
2. Paste it into your chatbot, then add your draft (and, optionally, your last 3 posts so it can catch repeated openings).
3. You get seven checks, each marked pass or fail with a reason, plus a rewrite that keeps your voice.

**In Claude Code**

```bash
git clone https://github.com/leohuanfang-hub/x-algorithm-playbook
mkdir -p ~/.claude/skills && cp -r x-algorithm-playbook/skills/* ~/.claude/skills/
```

Then say *"Check this thread before I post it"* and paste the draft. The skill version also tells you when to post.

### Path 3: Review your last week or month

1. **Get your numbers.** Go to [X Analytics](https://x.com/i/account_analytics), open the Content tab, pick the period and export. No export? A pasted table or screenshots also work. The more of these you include, the better: post text, date and time, impressions, likes, replies, profile visits, new follows.
2. **Run the review.**
   - Any chatbot that can open links: copy [`prompts/review-prompt.md`](prompts/review-prompt.md), then paste your numbers. The prompt points the chatbot at this repo's current rules, so it stays up to date without you changing anything.
   - Claude Code (skills installed as in Path 2): say *"Review my X posts and replies from last week"* and attach the export.
3. **What you get back:** your posts split by type (originals, later thread posts, replies, own video, links), which type actually brings you followers and which only brings reach, the rules you broke, your top and bottom 3 posts, and **at most 5 concrete actions** for the next period. Every claim is labeled as coming from your data, from the rules, or as a guess.
4. **Next period, run it again** and check whether those actions moved the numbers.

Replies get their own groups on purpose. For a small account, replies under bigger accounts can carry most of the reach while bringing few followers, and mixing them with original posts hides that. The Claude Code skill goes further: it splits replies by the size of the account you replied to and by how fast you replied, and warns you when one or two lucky posts produced most of your follows.

### Path 4: Track changes yourself

Needs Python 3 and git, nothing else.

```bash
git clone https://github.com/leohuanfang-hub/x-algorithm-playbook && cd x-algorithm-playbook
python3 scripts/param_history.py --since 2026-09-01
```

The first run clones X's repo into `.x-algorithm/`. The output lists every ranking parameter that changed, with date, commit, and old and new value:

```
2026-09-30  77d431a  ColdStartMaxPostAgeSecs: 172800 -> 7200
2026-10-14  17c96bf  NotInterestedWeight: -47.52 -> -52.272
2026-11-05  021afa4  FavoriteWeight: 0.66 -> 0.708
2026-11-10  660cd74  NewUserMinEngagementThreshold: 0.0 -> 0.004
...
```

Useful flags: `--grep ColdStart` to follow one family of parameters, `--markdown` for a table you can paste.

In Claude Code, the `x-algo-watch` skill runs this and explains each change in plain English: *"Did the X algorithm change since October 1?"*

---

## The 7-point checklist

1. **Put your best idea in the first post.** Strangers only see post 1 of a thread; every later post is a reply to yourself.
2. **Upload your own video, over 10 seconds.** Quoted videos don't enter the video index.
3. **Stay online for the first 2 hours.** The small-account boost only considers posts under 2 hours old.
4. **Write something people copy the link of.** Copy link is weighted 20, a like 0.708.
5. **Build mutuals in your niche.** A reply between mutual follows weighs 20 instead of 5.
6. **Never post from a template.** "Not interested" is weighted -53, and a low-quality AI label hides you from strangers for 7 days.
7. **Put links in a reply.** There's no hard-coded link penalty, but link posts collect less engagement.

Sources for each point: [`RULES.md`](RULES.md).

---

## What's inside

| File | What it is |
|---|---|
| [`RULES.md`](RULES.md) | The rules in effect, in plain English, each linked to the source line |
| [`CHANGELOG.md`](CHANGELOG.md) | Every ranking change since August 2026, newest first |
| [`scripts/param_history.py`](scripts/param_history.py) | Diffs X's ranking parameters across every commit |
| [`skills/x-post-check`](skills/x-post-check/SKILL.md) | Claude Code skill: check a draft, then rewrite it |
| [`skills/x-post-review`](skills/x-post-review/SKILL.md) | Claude Code skill: weekly or monthly review ending in an action list |
| [`skills/x-algo-watch`](skills/x-algo-watch/SKILL.md) | Claude Code skill: explain what changed and update the changelog |
| [`prompts/audit-prompt.md`](prompts/audit-prompt.md) | The pre-post check as a copy-paste prompt |
| [`prompts/review-prompt.md`](prompts/review-prompt.md) | The review as a copy-paste prompt |

**Shortcut for any AI that can open links:** give it this link along with your question.

```
https://raw.githubusercontent.com/leohuanfang-hub/x-algorithm-playbook/main/RULES.md
```

---

## How current is this?

`RULES.md` is pinned to a specific commit of X's code, shown at its top, and is updated after each meaningful change. X can change things in between, so before relying on a number, run:

```bash
python3 scripts/param_history.py --since <the date at the top of RULES.md>
```

No output means no parameter has changed since. (New filters or rules files can still appear without a parameter change; the `x-algo-watch` skill checks for those too.)

## FAQ

**Is this official?** No. It's an independent reading of public code, not affiliated with X.

**Does a weight of 0.708 mean one like is worth 0.708 points?** No. Each weight multiplies the model's *predicted probability* that a given viewer takes that action, not raw counts. So you can't add up likes and reports on your post to get a score.

**Does the public code match what runs in production?** Not guaranteed. The parameter file records when it was last synced with production, and `RULES.md` quotes that date, but X doesn't promise the two are identical.

**What can't the code tell us?** Some things, such as how replies are ordered under a post. They're listed under "Known unknowns" at the end of [`RULES.md`](RULES.md).

## Contributing

- **Spotted a change before it's here?** Open an issue with the commit link.
- **Have data the code doesn't show**, such as a test you ran on your own account? Open an issue. Evidence that confirms or contradicts a rule is the most useful thing you can add.
- **Improved a skill or prompt?** Pull requests welcome. Keep it general: it should work for any account.

If this saved you time, a ⭐ helps other people find it.

---

MIT License · by [@leohuanfang](https://x.com/leohuanfang)
