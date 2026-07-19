"""Recap / flowchart closing-scene pattern.

Restates an algorithm or theorem as a short flowchart or structured text.
Reusable across different theorems/videos — parameterized by title and steps,
not written against one specific example.
"""

from __future__ import annotations

from manim import DOWN, UP, Arrow, FadeIn, Scene, Text, VGroup, Write

from graph_town import style


def build_flowchart(steps: list[str], font_size: int = style.LABEL_FONT_SIZE) -> VGroup:
    """Build a vertical flowchart VGroup: a Text box per step, connected by arrows."""
    boxes = [Text(step, font_size=font_size, color=style.NAVY) for step in steps]
    chart = VGroup(*boxes).arrange(DOWN, buff=0.8)

    arrows = [
        Arrow(boxes[i].get_bottom(), boxes[i + 1].get_top(), color=style.GRAY, buff=0.1)
        for i in range(len(boxes) - 1)
    ]

    return VGroup(*boxes, *arrows)


class RecapScene(Scene):
    """Standalone closing scene: a title plus a flowchart of steps.

    Set ``title`` and ``steps`` (a list of short strings, one per flowchart
    node) to parameterize for a given theorem/algorithm.
    """

    title: str = ""
    steps: list[str] = []

    def construct(self) -> None:
        if not self.steps:
            raise ValueError("RecapScene requires steps to be set")

        title_mob = Text(self.title, font_size=style.LABEL_FONT_SIZE + 12, color=style.MAGENTA)
        title_mob.to_edge(UP)

        chart = build_flowchart(self.steps)
        chart.next_to(title_mob, DOWN, buff=0.8)
        if chart.width > 10:
            chart.set_width(10)

        self.play(Write(title_mob), run_time=style.DEFAULT_RUN_TIME)
        self.play(FadeIn(chart), run_time=style.SLOW_RUN_TIME)
        self.wait(1.0)
