# Theme Packs

Theme packs connect story genre, page design, typography, transitions, and prose rules. A launcher may support only part of this schema at first; still plan the full pack so the story and UI are coherent.

## Theme Pack Schema

```json
{
  "id": "rainy-dossier",
  "label": "Rainy Dossier",
  "genre": "investigation",
  "visual": {
    "palette": ["#111318", "#D7D0C2", "#7A8DA1", "#B85C38"],
    "background": "wet paper, station lights, file texture",
    "surface": "flat panels, thin borders, no glowing cards",
    "button": "compact, evidence-label feel",
    "transition": "page turn, camera shutter, rain flicker"
  },
  "typography": {
    "heading": "condensed or serif",
    "body": "readable serif or system sans",
    "voice": "case-file narration"
  },
  "prose": {
    "preset": "clear suspense",
    "sentenceLength": "mixed",
    "dialogue": "direct, subtext-light",
    "avoid": ["riddle-only clues", "abstract endings"]
  },
  "mechanics": ["clues", "case log", "relationship trust"],
  "launcher": {
    "layout": "reader-with-side-panel",
    "status": ["mainValue", "flags", "clues"],
    "choiceStyle": "compact-list",
    "sceneTransition": "soft-cut"
  }
}
```

Stories may embed this object as `meta.themePackData`. If `themePackData` exists, launchers should apply its palette, surface, typography, and labels before falling back to built-in presets.

## Presets

### investigation-dossier

- Visual: paper, folders, stamps, underlines, index cards.
- Prose: clear suspense; concrete clues before interpretations.
- Mechanics: clues, suspect notes, evidence gates.

### campus-summer

- Visual: bright daylight, notebooks, phones, chat bubbles, maps.
- Prose: contemporary, quick, emotionally direct.
- Mechanics: relationship meters, schedule choices, chat choices.

### palace-intrigue

- Visual: scrolls, lacquer, candlelight, thin ornamental borders.
- Prose: formal but readable; status and implication matter.
- Mechanics: favor, faction, hidden letters, audience order.

### cyber-terminal

- Visual: terminal layers, neon restraint, scanlines, network maps.
- Prose: clipped, procedural, occasionally lyrical at emotional breaks.
- Mechanics: hacking checks, data fragments, system flags.

### cozy-mystery

- Visual: warm interiors, small-town maps, soft contrast.
- Prose: friendly, witty, low brutality, clear investigation steps.
- Mechanics: clue board, conversation loops, gentle failure states.

### horror-house

- Visual: dark rooms, flashlight cones, inventory objects, harsh cuts.
- Prose: sensory but specific; fear comes from understood threats.
- Mechanics: sanity, inventory, locked rooms, timed choices.

### romance-visual-novel

- Visual: character focus, soft UI, message history, affection feedback.
- Prose: emotionally transparent; choices expose values.
- Mechanics: affection, memories, date routes, confession endings.

### wuxia-road

- Visual: ink, weather, tavern signs, road maps, martial manuals.
- Prose: clean period flavor; do not overload archaic phrasing.
- Mechanics: reputation, sect relations, duel stance, secret manual clues.

### stage-script

- Visual: rehearsal room, script pages, cue marks, spotlight pools.
- Prose: screenplay-like action with concise inner beats.
- Mechanics: scene order, actor trust, prop inventory, alternate takes.

### fairy-tale-dark

- Visual: illustrated margins, deep forest contrast, chapter ornaments.
- Prose: concrete fable language; symbolic objects repeat with consequence.
- Mechanics: vows, tokens, curses, path choices.

### absurd-office

- Visual: forms, stamps, fluorescent lights, deadpan dashboards.
- Prose: comic precision; absurd rules stated plainly.
- Mechanics: procedure compliance, reputation, resource forms, escalation timers.

## Style Guardrails

- Do not let theme override readability.
- Avoid one-color designs; include accent and neutral contrast.
- Match choice labels to genre but keep actions clear.
- If using heavy atmosphere, include a visible objective tracker or chapter goal.
- Avoid copying another product's distinctive layout, wording, title treatment, or visible credit line.
