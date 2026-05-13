# Story JSON Format

Use this compact schema for branching story games. Add fields only when the launcher supports them or when documenting future theme behavior.

```json
{
  "schemaVersion": 1,
  "meta": {
    "title": "Story Title",
    "author": "Author",
    "version": "1.0.0",
    "description": "One-sentence premise.",
    "theme": "investigation",
    "themePack": "rainy-dossier",
    "themePackData": {},
    "prosePreset": "clear-suspense",
    "mode": "standard",
    "playerRole": "Night station dispatcher",
    "objective": "Find why the final train vanished before the station closes.",
    "stakes": "If the player files the wrong report, the missing passengers are erased from the record.",
    "mechanics": ["clues", "caseLog"],
    "decisionPacing": { "windowSize": 10, "maxDecisionPages": 5, "maxConsecutiveDecisionPages": 2 },
    "variableName": "Resolve",
    "initialVariable": 50
  },
  "startNodeId": "start",
  "variables": {},
  "achievements": {},
  "codex": {
    "flags": {
      "opened_dispatch": {
        "label": "已打开调度单",
        "description": "路线状态：你已经查看过封存的调度记录。"
      }
    },
    "clues": {
      "dispatch_stamp": {
        "label": "调度章",
        "description": "线索：调度单上的印章时间和系统日志不一致。"
      }
    },
    "items": {
      "rusted_key": {
        "label": "锈钥匙",
        "description": "物品：可以打开旧库房门。"
      }
    }
  },
  "nodes": {}
}
```

## Meta Fields

Required for finished stories:

- `title`
- `description`
- `mode`: `prototype`, `standard`, or `longform`
- `playerRole`: who the player is
- `objective`: what the player is trying to accomplish
- `stakes`: what gets worse if they fail
- `themePack`: preset id or custom id
- `prosePreset`: preset id from `writing-presets.md`
- `mechanics`: array of enabled mechanics
- `decisionPacing`: optional pacing hint for launchers. Default is no more than 5 decision pages in a rolling 10-page window, and no more than 2 decision pages back to back.
- `variableName`
- `initialVariable`

Use `themePackData` for custom colors, typography, background, transitions, and UI labels. A launcher should prefer `themePackData` over built-in presets when both exist.

## Node

```json
{
  "chapterTitle": "Chapter One: The Missing Train",
  "title": "Signal Room",
  "scene": {
    "id": "signal_room",
    "name": "Signal Room",
    "type": "major",
    "description": "Stable environmental description.",
    "arrival": "What happens when the player arrives."
  },
  "progress": 12,
  "segments": [
    { "text": "Narration." },
    { "speaker": "Mei", "text": "Dialogue." }
  ],
  "choices": [
    {
      "text": "Open the sealed dispatch",
      "next": "dispatch_opened",
      "condition": "val >= 30",
      "changes": {
        "val": 5,
        "set": { "dispatchOpened": true },
        "addFlag": "opened_dispatch",
        "addItem": "rusted_key",
        "addClue": "dispatch_stamp",
        "relationship": { "mei": 1 }
      }
    }
  ],
  "routes": [
    { "condition": "hasFlag 'opened_dispatch'", "next": "truth_route" },
    { "condition": "default", "next": "fallback_route" }
  ]
}
```

## Ending

```json
{
  "isEnding": true,
  "title": "Ending: Dawn Record",
  "type": "TRUE ENDING",
  "progress": 100,
  "achievement": "true_dawn",
  "description": "What happened because of the player's route.",
  "closing": "Final emotional or thematic line."
}
```

## Conditions

Support simple string conditions:

- `val >= 60`
- `val < 30`
- `trust >= 2`
- `route == 'archive'`
- `hasFlag 'opened_dispatch'`
- `!hasFlag 'opened_dispatch'`
- `default`

Support object conditions:

```json
{ "all": [{ "var": "val", "op": ">=", "value": 60 }, { "flag": "opened_dispatch" }] }
{ "any": [{ "flag": "saved_mei" }, { "var": "trust", "op": ">=", "value": 3 }] }
{ "not": { "flag": "betrayed_mei" } }
```

## Common Mechanics Fields

These fields are optional but recommended when using the matching mechanic:

- `changes.addItem`: add one inventory item id
- `changes.removeItem`: remove one inventory item id
- `changes.addClue`: add one clue id
- `changes.importantFlag`: visible route-status mark, e.g. `{ "flag": "saved_mei", "label": "你救下了梅" }`
- `changes.relationship`: map of character id to numeric delta
- `changes.time`: numeric time-slot delta
- `input`: `{ "type": "password", "answer": "0427", "success": "node_id", "failure": "node_id" }`
- `codex`: top-level object defining localized clue, item, and visible route-status descriptions for UI panels

Use `addFlags` for internal conditions. Use `importantFlag` or `importantFlags` for route-status marks the player should see in the UI.

## Required Design Discipline

- Use stable node IDs with lowercase letters, digits, and underscores.
- Give every route list a `default`.
- Every non-ending node must have choices, routes, or a next node.
- Every ending should have an achievement unless the story deliberately uses hidden or silent endings.
- Define all achievements referenced by choices or endings.
- Keep progress roughly increasing along each route.
- Avoid repeated ending descriptions with only title changes.
- Avoid branch points where every route rejoins in one node without changed state or new information.
