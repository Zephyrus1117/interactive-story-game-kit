---
name: interactive-story-builder
description: Create, adapt, or revise readable branching narrative games with JSON story structure, theme-pack planning, interaction mechanics, and quality checks. Use when the user asks for an interactive story, branching novel, text adventure, visual-novel style experience, story-to-game conversion, playable narrative JSON, themeable story launcher content, or improvements to narrative clarity, length, writing style, choices, endings, achievements, or story UI themes.
---

# Interactive Story Builder

## Purpose

Build branching story games that are understandable, replayable, and visually themeable. Prefer clear dramatic causality over foggy atmosphere, and produce enough story mass for choices and endings to feel earned.

This skill is intentionally independent: do not preserve third-party branding, sample stories, UI copy, author credit lines, or distinctive wording from any source project unless the user explicitly provides permission and license requirements are satisfied.

For copyright and originality checks, read `references/legal-and-originality.md` before reusing any existing launcher, sample, visual style, named setting, or copied text.

## Workflow

1. Define the mode:
   - `prototype`: quick playable slice only when the user explicitly asks for a demo or test.
   - `standard`: default for finished short-to-medium interactive stories.
   - `longform`: for novel, script, or series adaptation.
2. Build a one-page design brief:
   - player role, setting, concrete objective, stakes, central conflict, genre, tone, target length, theme pack, prose preset, core mechanics.
3. Plan the story before writing JSON:
   - chapter arc, branch topology, state variables, endings, achievements, and replay incentives.
4. Draft nodes in playable order:
   - every node needs concrete action, new information, a decision, or a meaningful transition.
5. Run clarity and scale checks from `references/readability-and-scale.md`.
6. Use `references/story-format.md` for JSON structure.
7. Use `references/theme-packs.md` when selecting or creating visual/writing themes.
8. Use `references/writing-presets.md` to choose a readable prose style.
9. Use `references/interaction-patterns.md` when adding mechanics beyond plain choices.
10. Use `assets/themeable-launcher/index.html` as the clean launcher template when a self-contained page is requested.
11. Use `scripts/build_launcher.py story.json output.html` to embed a story JSON into the clean launcher.
12. Validate with `scripts/validate_story_game.py` before delivery whenever a JSON file is produced.

## Default Scale

Do not create ultra-short finished games by default. A finished interactive story should usually be:

- `standard`: 60-120 nodes, 5-8 chapters, 5-8 endings, 25-45 minutes for one complete playthrough.
- `longform`: 150-300+ nodes, 8+ chapters, 8-15 endings, designed for repeated exploration.
- `prototype`: 25-40 nodes, 3+ chapters, 3+ endings, only when explicitly requested.

If time or budget requires a smaller artifact, label it as a prototype and keep the premise unusually clear.

## Writing Rules

- In the first 3 playable nodes, establish who the player is, where they are, what they want, and what will go wrong if they fail.
- Do not use mystery as a substitute for plot. A secret may be hidden; the current situation must still be legible.
- Avoid over-compressed poetic prose. Use concrete actions, objects, dialogue, and cause-effect transitions.
- Keep each node focused: one beat, one emotional turn, or one decision.
- Pace decisions. In any rolling span of about 10 playable pages on a route, no more than 5 pages should require a meaningful multi-option decision, and avoid more than 2 decision pages back to back; use narration pages, one-button continue pages, routes, or delayed consequences between decision points.
- Every major branch must change at least one of: information, relationship, resource, route, available choice, ending eligibility, or player self-understanding.
- Avoid “all options lead to the same paragraph” unless state changes or later consequences make the choice matter.
- Make endings feel like consequences of accumulated choices, not random mood shifts.

## Generation Modes

- `quick`: only for ideation, sample mechanics, or a vertical slice. Produce an outline or prototype and label it as such.
- `standard`: default. Produce enough setup, escalation, reversal, and consequence for a complete playable story.
- `longform`: use for source-text adaptation, novel-scale plots, or route-heavy games. Split work by chapter and validate each batch.

Do not run the long planning workflow for quick mode. Do not use quick mode when the user asks for a finished experience.

## Theme System

Every story should include a theme plan, even when the current launcher only supports part of it.

Define:

- visual genre: e.g. noir, campus, wuxia, cyberpunk, cozy mystery, palace intrigue, horror, romance, comedy, post-apocalyptic.
- typography mood: literary, chat, dossier, terminal, diary, screenplay, archive.
- UI treatment: colors, background texture/image direction, transition style, button feel, status display.
- prose preset: plain, light-literary, suspense, comedic, period-drama, youth, romance, investigative.

Use `references/theme-packs.md` for reusable presets and schema.

## Mechanics

Plain choices are the base, not the ceiling. Standard stories should usually include one primary mechanic and one secondary mechanic:

- clues/case log
- inventory/locks
- relationship/favor
- map/time schedule
- password/input gate
- dialogue topics
- random texture events with deterministic endings

Use `references/interaction-patterns.md` to keep mechanics tied to story consequences.

When using flags, clues, or items, define user-facing `codex` entries with localized labels and short descriptions. Treat ordinary `addFlags` as internal route state; reserve visible route-status marks for `importantFlag` / `importantFlags`.

## Validation Expectations

Run:

```bash
python3 scripts/validate_story_game.py path/to/story.json --mode standard
```

Use `--mode prototype` only for explicitly labeled prototypes. Treat warnings about short scale, missing theme fields, repeated endings, shallow branches, weak choice labels, or brand residue as revision prompts.

## Deliverables

For JSON story work, deliver:

- playable JSON file
- clean launcher HTML when requested, preferably derived from `assets/themeable-launcher/index.html`
- validation result
- node count, ending count, achievement count
- intended playtime
- theme pack summary
- notes about any known limitations

For skill or launcher revision work, deliver:

- changed files
- what quality rule or product goal each change supports
- remaining decisions for the user
