# Interaction Patterns

Use mechanics only when they support the story. Do not add systems that create bookkeeping without payoff.

## Plain Branching

Best for literary or emotional stories.

- State: one main value, a few flags.
- Choices: attitude, trust, reveal, leave, confront.
- Risk: routes can feel cosmetic unless later scenes remember choices.

## Investigation

Best for mystery, thriller, case-file stories.

- State: clue flags, suspect trust, evidence count.
- UI idea: case log, evidence board, discovered clue list.
- Branch payoff: different accusation options, missing evidence endings, true solution.

## Relationship Routes

Best for romance, ensemble drama, campus, court intrigue.

- State: per-character trust/favor, faction flags.
- UI idea: relationship panel, memory list.
- Branch payoff: route scenes, ally availability, betrayal or support endings.

## Inventory And Locks

Best for horror, adventure, escape-room, fantasy quests.

- State: items, locked locations, used items.
- UI idea: inventory drawer with item descriptions.
- Branch payoff: optional rooms, alternate solutions, rescue/failure variants.

## Map And Time

Best for investigations, road stories, survival, school schedules.

- State: current location, time slot, visited places.
- UI idea: map menu, time-of-day indicator.
- Branch payoff: events expire, people move, clues become unavailable.

## Dialogue Tree

Best when conversation is the main gameplay.

- State: asked topics, pressure, rapport.
- UI idea: topic list, remembered answers.
- Branch payoff: contradictions, confessions, withheld information.

## Password Or Input Gate

Best for investigation, escape-room, ARG, sci-fi terminal, sealed-letter plots.

- State: discovered codes, wrong attempts, hint flags.
- UI idea: short text input with visible clue recall.
- Branch payoff: correct answer opens shortcut or truth; wrong answer costs time, trust, or access.

## Investigation Points

Best for rooms, crime scenes, maps, object-heavy horror.

- State: examined hotspots, clue dependencies, location completeness.
- UI idea: location screen with 3-6 inspectable points.
- Branch payoff: optional evidence, hidden choices, alternate accusation route.

## Timed Pressure

Best for chase, rescue, school schedule, court deadline, disaster.

- State: time slots, countdown, missed windows.
- UI idea: visible clock or chapter deadline.
- Branch payoff: scenes open/close, NPCs move, rescue/arrival changes.

## Random Or Procedural Events

Use sparingly. Randomness should change texture, not break story logic.

- Good: a different rumor appears after the same clue.
- Bad: a random ending ignores the player's accumulated route.

## Mechanic Selection Rule

For a standard story, choose:

- 1 primary mechanic
- 1 secondary mechanic
- 1 main state value
- 3-8 named variables or flags that matter to endings

More systems are allowed in longform, but each must affect scenes or endings.

## Effect Fields

Use these optional fields in `changes` when the launcher supports them:

- `addClue`
- `addItem`
- `removeItem`
- `relationship`
- `time`
- `addLocation`
- `unlockTopic`

The validator treats these as meaningful consequences.
