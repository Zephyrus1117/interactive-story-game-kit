# 白霜七日

《白霜七日》是一个极寒末世恐怖互动故事示例，用来展示 `interactive-story-builder` 的 JSON 格式、主题启动器和校验流程。

## Files

- `story.json`: 可编辑的剧情 JSON。
- `index.html`: 已嵌入剧情数据的独立可玩 HTML。
- `build_story.py`: 生成 `story.json` 的脚本。

## Rebuild

From the repository root:

```bash
python3 examples/frostfall-seven-days/build_story.py
python3 scripts/validate_story_game.py examples/frostfall-seven-days/story.json --mode standard
python3 scripts/build_launcher.py examples/frostfall-seven-days/story.json examples/frostfall-seven-days/index.html
```

## Play Locally

From the repository root:

```bash
python3 -m http.server 8765
```

Then visit:

```text
http://127.0.0.1:8765/examples/frostfall-seven-days/
```

