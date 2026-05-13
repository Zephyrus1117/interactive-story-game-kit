#!/usr/bin/env python3
"""Validate a branching story JSON file for structure, reachability, and scale."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any


SCALE_GATES = {
    "prototype": {"nodes": 25, "chapters": 3, "endings": 3},
    "standard": {"nodes": 60, "chapters": 5, "endings": 5},
    "longform": {"nodes": 150, "chapters": 8, "endings": 8},
}

NODE_ID = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
BRAND_RESIDUE = [
    "Powered By",
    "Powered by",
    "@山音",
    "山音",
    "Story-to-game",
    "Story-to-Game",
    "Shanyin",
    "li-yinqian",
]
MEANINGFUL_CHANGE_KEYS = {
    "val",
    "valSet",
    "set",
    "addFlag",
    "addFlags",
    "importantFlag",
    "importantFlags",
    "removeFlag",
    "unlockAchievement",
    "unlockAchievements",
    "addItem",
    "removeItem",
    "addClue",
    "relationship",
    "time",
    "addLocation",
    "unlockTopic",
}
WEAK_CHOICE_WORDS = [
    "trust the silence",
    "follow the feeling",
    "wait",
    "沉默",
    "感觉",
    "顺其自然",
    "继续相信",
    "听从直觉",
]


def target_refs(node: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    if isinstance(node.get("next"), str):
        refs.append(node["next"])
    for choice in node.get("choices", []) or []:
        if isinstance(choice, dict) and isinstance(choice.get("next"), str):
            refs.append(choice["next"])
    for route in node.get("routes", []) or []:
        if isinstance(route, dict) and isinstance(route.get("next"), str):
            refs.append(route["next"])
    return refs


def first_target(node: dict[str, Any]) -> str | None:
    refs = target_refs(node)
    return refs[0] if len(refs) == 1 else None


def achievement_refs(node: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    if node.get("isEnding") and isinstance(node.get("achievement"), str):
        refs.append(node["achievement"])
    for choice in node.get("choices", []) or []:
        if not isinstance(choice, dict):
            continue
        changes = choice.get("changes") or {}
        if isinstance(changes.get("unlockAchievement"), str):
            refs.append(changes["unlockAchievement"])
        if isinstance(changes.get("unlockAchievements"), list):
            refs.extend(x for x in changes["unlockAchievements"] if isinstance(x, str))
    return refs


def reachable_nodes(nodes: dict[str, Any], start: str) -> set[str]:
    seen: set[str] = set()
    queue: deque[str] = deque([start] if start in nodes else [])
    while queue:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        node = nodes.get(current) or {}
        for ref in target_refs(node):
            if ref in nodes and ref not in seen:
                queue.append(ref)
    return seen


def shortest_to_ending(nodes: dict[str, Any], start: str, max_depth: int = 12) -> int | None:
    queue: deque[tuple[str, int]] = deque([(start, 0)])
    seen: set[str] = set()
    while queue:
        current, depth = queue.popleft()
        if current in seen or depth > max_depth:
            continue
        seen.add(current)
        node = nodes.get(current) or {}
        if node.get("isEnding"):
            return depth
        for ref in target_refs(node):
            if ref in nodes:
                queue.append((ref, depth + 1))
    return None


def text_of_node(node: dict[str, Any]) -> str:
    parts: list[str] = []
    for seg in node.get("segments", []) or []:
        if isinstance(seg, dict):
            parts.append(str(seg.get("text") or ""))
        elif isinstance(seg, str):
            parts.append(seg)
    for choice in node.get("choices", []) or []:
        if isinstance(choice, dict):
            parts.append(str(choice.get("text") or ""))
    return " ".join(parts).strip()


def walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for item in value.values():
            out.extend(walk_strings(item))
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(walk_strings(item))
        return out
    return []


def normalized_text(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def char_shingles(text: str, size: int = 6) -> set[str]:
    text = normalized_text(text)
    if len(text) <= size:
        return {text} if text else set()
    return {text[i : i + size] for i in range(len(text) - size + 1)}


def similarity(left: str, right: str) -> float:
    a = char_shingles(left)
    b = char_shingles(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def has_meaningful_changes(choice: dict[str, Any]) -> bool:
    changes = choice.get("changes")
    if not isinstance(changes, dict):
        return False
    return any(key in changes for key in MEANINGFUL_CHANGE_KEYS)


def choice_text_is_weak(text: str) -> bool:
    stripped = text.strip().lower()
    if len(stripped) < 3:
        return True
    return any(word in stripped for word in WEAK_CHOICE_WORDS)


def is_decision_node(node: dict[str, Any]) -> bool:
    if node.get("input"):
        return True
    choices = node.get("choices") or []
    return isinstance(choices, list) and len(choices) > 1


def change_id(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return str(value.get("flag") or value.get("id") or value.get("name") or "")
    return ""


def codex_has(codex: dict[str, Any], kind: str, item_id: str) -> bool:
    singular = kind[:-1] if kind.endswith("s") else kind
    plural_entries = codex.get(kind)
    singular_entries = codex.get(singular)
    return bool(
        (isinstance(plural_entries, dict) and item_id in plural_entries)
        or (isinstance(singular_entries, dict) and item_id in singular_entries)
    )


def validate(path: Path, mode: str) -> tuple[list[str], list[str], dict[str, int]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["root must be a JSON object"], [], {}

    nodes = data.get("nodes")
    meta = data.get("meta")
    start = data.get("startNodeId")
    achievements = data.get("achievements") or {}
    codex = data.get("codex") or {}

    if not isinstance(meta, dict):
        errors.append("missing or invalid meta")
        meta = {}
    if not isinstance(start, str):
        errors.append("missing or invalid startNodeId")
    if not isinstance(nodes, dict):
        errors.append("missing or invalid nodes")
        return errors, warnings, {}
    if not isinstance(achievements, dict):
        errors.append("achievements must be an object")
        achievements = {}
    if not isinstance(codex, dict):
        warnings.append("codex should be an object when using visible clues/items")
        codex = {}

    if isinstance(start, str) and start not in nodes:
        errors.append(f"startNodeId '{start}' does not exist")

    for required in ("playerRole", "objective", "stakes", "themePack", "prosePreset", "mechanics"):
        if not meta.get(required):
            warnings.append(f"meta.{required} is recommended for readable, themeable stories")
    if meta.get("mode") and meta.get("mode") != mode:
        warnings.append(f"meta.mode is '{meta.get('mode')}' but validator mode is '{mode}'")
    if meta.get("mechanics") and not isinstance(meta.get("mechanics"), list):
        errors.append("meta.mechanics must be an array when present")
    if not meta.get("themePackData") and not meta.get("themePack"):
        warnings.append("story has no theme pack; visual adaptation may be generic")
    pacing = meta.get("decisionPacing")
    if pacing is not None:
        if not isinstance(pacing, dict):
            warnings.append("meta.decisionPacing should be an object")
        else:
            window_size = pacing.get("windowSize", 10)
            max_decisions = pacing.get("maxDecisionPages", 5)
            max_consecutive = pacing.get("maxConsecutiveDecisionPages", 2)
            valid_window = isinstance(window_size, int) and window_size >= 4
            if not valid_window:
                warnings.append("meta.decisionPacing.windowSize should be an integer >= 4")
            if not isinstance(max_decisions, int) or max_decisions < 1 or (valid_window and max_decisions > window_size):
                warnings.append("meta.decisionPacing.maxDecisionPages should be between 1 and windowSize")
            if not isinstance(max_consecutive, int) or max_consecutive < 1 or max_consecutive > 4:
                warnings.append("meta.decisionPacing.maxConsecutiveDecisionPages should be an integer from 1 to 4")

    all_text = "\n".join(walk_strings(data))
    for marker in BRAND_RESIDUE:
        if marker in all_text:
            warnings.append(f"possible third-party brand residue found: {marker}")

    endings: list[str] = []
    ending_texts: dict[str, str] = {}
    chapter_count = 0
    clue_ids: set[str] = set()
    item_ids: set[str] = set()
    important_flags_missing_label: list[str] = []

    for node_id, node in nodes.items():
        if not NODE_ID.match(node_id):
            errors.append(f"node id '{node_id}' must use letters, digits, and underscores")
        if not isinstance(node, dict):
            errors.append(f"node '{node_id}' must be an object")
            continue
        if node.get("chapterTitle"):
            chapter_count += 1
        if node.get("isEnding"):
            endings.append(node_id)
            ending_texts[node_id] = f"{node.get('title', '')} {node.get('description', '')} {node.get('closing', '')}"
            if not node.get("description"):
                warnings.append(f"ending '{node_id}' lacks description")
            if not node.get("closing"):
                warnings.append(f"ending '{node_id}' lacks closing")
        else:
            has_flow = bool(node.get("choices") or node.get("next") or node.get("routes"))
            if not has_flow:
                errors.append(f"node '{node_id}' is not an ending and has no outgoing flow")
        for ref in target_refs(node):
            if ref not in nodes:
                errors.append(f"node '{node_id}' references missing node '{ref}'")
        for ref in achievement_refs(node):
            if ref not in achievements:
                errors.append(f"node '{node_id}' references missing achievement '{ref}'")
        routes = node.get("routes") or []
        if routes and not any(isinstance(r, dict) and r.get("condition") == "default" for r in routes):
            errors.append(f"node '{node_id}' routes need a default fallback")
        choices = node.get("choices") or []
        for choice in choices:
            if not isinstance(choice, dict):
                continue
            changes = choice.get("changes") or {}
            if not isinstance(changes, dict):
                continue
            clue_id = change_id(changes.get("addClue"))
            item_id = change_id(changes.get("addItem"))
            if clue_id:
                clue_ids.add(clue_id)
            if item_id:
                item_ids.add(item_id)
            important = changes.get("importantFlag")
            if important:
                flag_id = change_id(important)
                has_label = isinstance(important, dict) and bool(important.get("label") or important.get("title") or important.get("name"))
                if flag_id and not has_label and not codex_has(codex, "flags", flag_id):
                    important_flags_missing_label.append(flag_id)
            for important_item in changes.get("importantFlags") or []:
                flag_id = change_id(important_item)
                has_label = isinstance(important_item, dict) and bool(
                    important_item.get("label") or important_item.get("title") or important_item.get("name")
                )
                if flag_id and not has_label and not codex_has(codex, "flags", flag_id):
                    important_flags_missing_label.append(flag_id)
        if len(choices) >= 2:
            targets = {c.get("next") for c in choices if isinstance(c, dict)}
            has_consequence = any(
                isinstance(c, dict) and (has_meaningful_changes(c) or c.get("effect") or c.get("effects"))
                for c in choices
            )
            if len(targets) == 1 and not has_consequence:
                errors.append(f"node '{node_id}' choices share one target with no state/effect consequence")
            target_nodes = [nodes.get(t) for t in targets if t in nodes]
            immediate = [first_target(tn) for tn in target_nodes if isinstance(tn, dict)]
            if len(targets) >= 2 and len(immediate) >= 2 and len(set(immediate)) == 1 and not has_consequence:
                warnings.append(f"node '{node_id}' branches rejoin immediately without state changes")
            for choice in choices:
                if isinstance(choice, dict) and choice_text_is_weak(str(choice.get("text") or "")):
                    warnings.append(f"node '{node_id}' has a weak or vague choice label: {choice.get('text')!r}")
                if isinstance(choice, dict) and choice.get("next") in nodes:
                    distance = shortest_to_ending(nodes, choice["next"])
                    if mode != "prototype" and distance is not None and distance <= 1:
                        target = nodes[choice["next"]]
                        etype = str(target.get("type", ""))
                        if target.get("isEnding") and "RASH" not in etype and "BAD" not in etype:
                            warnings.append(f"node '{node_id}' choice jumps directly to a non-rash ending '{choice['next']}'")

    if not isinstance(meta.get("decisionPacing"), dict):
        ordered_nodes = sorted(
            ((node_id, node) for node_id, node in nodes.items() if isinstance(node, dict) and not node.get("isEnding")),
            key=lambda item: (item[1].get("progress", 0), item[0]),
        )
        window_size = 10
        max_decisions = 5
        max_consecutive = 2
        for index in range(max(0, len(ordered_nodes) - window_size + 1)):
            window = ordered_nodes[index : index + window_size]
            count = sum(1 for _, node in window if is_decision_node(node))
            if count > max_decisions:
                first_id = window[0][0]
                last_id = window[-1][0]
                warnings.append(
                    f"decision pacing is dense: nodes '{first_id}'..'{last_id}' include {count}/{window_size} decision pages"
                )
                break
        streak: list[str] = []
        for node_id, node in ordered_nodes:
            if is_decision_node(node):
                streak.append(node_id)
                if len(streak) > max_consecutive:
                    warnings.append(f"decision pacing has more than {max_consecutive} decision pages in a row near node '{node_id}'")
                    break
            else:
                streak = []

    for clue_id in sorted(clue_ids):
        if not codex_has(codex, "clues", clue_id):
            warnings.append(f"clue '{clue_id}' has no codex label/description")
    for item_id in sorted(item_ids):
        if not codex_has(codex, "items", item_id):
            warnings.append(f"item '{item_id}' has no codex label/description")
    for flag_id in sorted(set(important_flags_missing_label)):
        warnings.append(f"important flag '{flag_id}' should have a localized label or codex entry")

    seen = reachable_nodes(nodes, start if isinstance(start, str) else "")
    for node_id in sorted(set(nodes) - seen):
        warnings.append(f"node '{node_id}' is unreachable from startNodeId")
    if endings and not any(node_id in seen for node_id in endings):
        errors.append("no ending is reachable")

    ending_ids = list(ending_texts)
    for index, left_id in enumerate(ending_ids):
        for right_id in ending_ids[index + 1 :]:
            score = similarity(ending_texts[left_id], ending_texts[right_id])
            if score >= 0.72:
                warnings.append(f"endings '{left_id}' and '{right_id}' read very similarly ({score:.0%})")

    gate = SCALE_GATES[mode]
    if len(nodes) < gate["nodes"]:
        warnings.append(f"{mode} mode expects at least {gate['nodes']} nodes; found {len(nodes)}")
    if chapter_count < gate["chapters"]:
        warnings.append(f"{mode} mode expects at least {gate['chapters']} chapter starts; found {chapter_count}")
    if len(endings) < gate["endings"]:
        warnings.append(f"{mode} mode expects at least {gate['endings']} endings; found {len(endings)}")

    first_text = ""
    if isinstance(start, str) and start in nodes:
        walk = [start]
        first = nodes[start]
        for ref in target_refs(first)[:2]:
            if ref in nodes:
                walk.append(ref)
        first_text = " ".join(text_of_node(nodes[x]) for x in walk)
    if len(first_text) < 220:
        warnings.append("opening may be too thin; first playable nodes should establish player, place, goal, and pressure")
    if len(first_text) >= 220:
        objective = str(meta.get("objective") or "")
        stakes = str(meta.get("stakes") or "")
        if objective and objective not in first_text and mode != "prototype":
            warnings.append("opening may not state the concrete objective clearly")
        if stakes and stakes not in first_text and mode != "prototype":
            warnings.append("opening may not state the stakes clearly")

    stats = {
        "nodes": len(nodes),
        "chapters": chapter_count,
        "endings": len(endings),
        "achievements": len(achievements),
        "reachable": len(seen),
    }
    return errors, warnings, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--mode", choices=sorted(SCALE_GATES), default="standard")
    args = parser.parse_args()

    try:
        errors, warnings, stats = validate(args.json_path, args.mode)
    except Exception as exc:  # noqa: BLE001
        print(f"fatal: {exc}", file=sys.stderr)
        return 2

    print(f"Story validation: {args.json_path}")
    for key, value in stats.items():
        print(f"{key}: {value}")
    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("\nOK: no errors or warnings")
    elif not errors:
        print("\nOK with warnings")
    else:
        print("\nFailed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
