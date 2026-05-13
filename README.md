# Interactive Story Game Kit

一个干净、可主题化的互动叙事游戏生成与播放工具。它包含：

- Codex skill：用于把故事、大纲或设定改写成可游玩的分支剧情 JSON。
- 主题化 HTML 启动器：可直接加载 JSON，也可把 JSON 打包成独立 HTML。
- 剧情质量校验器：检查断链、死胡同、结局数量、选择密度、线索/物品说明等。
- 示例游戏：《白霜七日》，一个极寒末世恐怖互动故事。

这个项目已经移除第三方可见品牌、默认样例文案和原启动器痕迹，适合继续改造成你自己的版本。

## Features

- 全屏居中阅读体验，主体无卡片背景。
- 左侧历史页圆点导航，支持回看旧页，但旧页选项只读。
- 回看旧页时可一键回到最新页。
- 支持点击画面空白处翻页，避免在多选决策页误选。
- 支持路线状态、线索、物品资料库，并以中央弹窗按行展示。
- 支持主题包：颜色、字体、背景方向、按钮风格、转场氛围。
- 支持选择节奏控制：默认 10 页内最多 5 页需要多选决策，最多连续 2 页决策。
- 支持 JSON 校验：结构、可达性、结局、选择质量、品牌残留、资料库缺失。

## Project Structure

```text
.
├── SKILL.md
├── agents/
├── assets/
│   └── themeable-launcher/
│       └── index.html
├── references/
├── scripts/
│   ├── build_launcher.py
│   └── validate_story_game.py
└── examples/
    └── frostfall-seven-days/
        ├── build_story.py
        ├── index.html
        └── story.json
```

## Quick Start

Validate the example story:

```bash
python3 scripts/validate_story_game.py examples/frostfall-seven-days/story.json --mode standard
```

Build a standalone playable HTML file:

```bash
python3 scripts/build_launcher.py examples/frostfall-seven-days/story.json examples/frostfall-seven-days/index.html
```

Open the example locally:

```bash
python3 -m http.server 8765
```

Then visit:

```text
http://127.0.0.1:8765/examples/frostfall-seven-days/
```

## Use As A Codex Skill

Place this folder under your Codex skills directory, for example:

```bash
cp -R . ~/.codex/skills/interactive-story-builder
```

Then ask Codex to use `interactive-story-builder` for interactive fiction, branching story JSON, visual-novel style demos, theme packs, or story quality checks.

## Story JSON

A story JSON includes:

- `meta`: title, theme, player role, objective, stakes, decision pacing.
- `nodes`: playable pages, choices, routes, endings.
- `codex`: localized descriptions for route status, clues, and items.
- `achievements`: unlockable ending or route achievements.

See [references/story-format.md](references/story-format.md) for the schema.

## Example

The bundled example is:

```text
examples/frostfall-seven-days/
```

It contains an original Chinese horror story, `story.json`, and a generated playable `index.html`.

## GitHub Upload

Recommended commands after creating an empty GitHub repository:

```bash
cd /Users/kanyun/Documents/New\ project/interactive-story-game-kit
git init
git add .
git commit -m "Initial release"
git branch -M main
git remote add origin https://github.com/Zephyrus1117/interactive-story-game-kit.git
git push -u origin main
```

If you use GitHub CLI:

```bash
cd /Users/kanyun/Documents/New\ project/interactive-story-game-kit
gh repo create interactive-story-game-kit --public --source=. --remote=origin --push
```

Use `--private` instead of `--public` if you do not want it public yet.

## GitHub Pages

After pushing, you can enable GitHub Pages:

1. Open the repository on GitHub.
2. Go to `Settings` -> `Pages`.
3. Choose `Deploy from a branch`.
4. Select branch `main` and folder `/root`.
5. The example will be available at:

```text
https://Zephyrus1117.github.io/interactive-story-game-kit/examples/frostfall-seven-days/
```

## License

This project is released under the MIT License.
