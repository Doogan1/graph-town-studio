# Graph Town Studio

A reusable Python toolkit for producing [ManimCE](https://www.manim.community/)-based
math education videos for the **Graph Town** YouTube channel (graph theory / discrete
math content).

This is not a fork of Manim — it's a package that depends on ManimCE as a library and
extends it via subclassing (custom `Scene` / `Mobject` classes), the same way most
Manim content creators build their own tooling.

This repo holds the **shared toolkit only**. Individual videos (the first is a
Havel–Hakimi theorem video) live in their own scripts/repos that import from this one —
nothing video-specific is hardcoded here.

## Install

```bash
pip install -e ".[dev]"
```

## Structure

```
graph_town/
  style.py                # house style constants (colors, timing)
  scenes/
    base.py                # shared base Scene class
    vertex_deletion.py      # vertex + incident edges fade out, neighbor degrees decrement
    two_switch.py            # 2-switch / edge-swap animation
    recap.py                  # closing recap/flowchart scene
  beatsheet/
    parser.py               # CSV -> structured Beat objects
    dispatcher.py            # Beat -> scene call
examples/
  sample_beatsheet.csv
tests/
```

## House style

Colors are sourced by pixel-sampling the channel's profile image (a Clebsch graph
rendering), so branding and video visuals share one palette by design. See
`graph_town/style.py`.

## Beat sheets

Videos are scripted as a CSV "beat sheet" with columns:

```
beat_id, t_start, t_end, narration, visual_type, scene_spec, notes
```

- `visual_type`: `static` or `animation`
- `scene_spec`: a small DSL string identifying which scene builder to call and with
  what arguments, e.g. `vertex_deletion(graph=g1, vertex=3)`. See
  `graph_town/beatsheet/parser.py` for the exact grammar and
  `examples/sample_beatsheet.csv` for a worked example.

The dispatcher (`graph_town/beatsheet/dispatcher.py`) maps each beat's `scene_spec` to
the corresponding function in the scene library and triggers a render.
