from manim import *
from graph_town import style

class DemoTextWrite(Scene):
    def construct(self):
        title = Text("Graph Town", font_size=72, color=style.NAVY)
        sub = Text("vertex deletion", font_size=36, color=style.GRAY)
        sub.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=style.SLOW_RUN_TIME)
        self.play(FadeIn(sub), run_time=style.DEFAULT_RUN_TIME)
        self.wait(0.5)
        self.play(
            title.animate.set_color(style.MAGENTA),
            sub.animate.shift(RIGHT),
            run_time=style.EMPHASIS_RUN_TIME,
        )
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(sub), run_time=style.DEFAULT_RUN_TIME)