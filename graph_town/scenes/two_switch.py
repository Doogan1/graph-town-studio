"""2-switch (edge swap) animation.

Given two edges (v, a) and (u, b), animate them morphing into (v, u) and
(a, b) while everything else in the graph stays static — making clear
visually that no other degree changes.
"""

from __future__ import annotations

import networkx as nx
from manim import Create, FadeIn

from graph_town import style
from graph_town.scenes.base import GraphScene


def _edge_mobject(graph, u, v):
    """Look up an edge mobject regardless of the tuple order it was stored under."""
    if (u, v) in graph.edges:
        return graph.edges[(u, v)]
    return graph.edges[(v, u)]


def animate_two_switch(
    scene: GraphScene,
    graph,
    nx_graph: nx.Graph,
    edge1: tuple,
    edge2: tuple,
    run_time: float = style.DEFAULT_RUN_TIME,
) -> None:
    """Play the 2-switch animation and mutate ``nx_graph``/``graph`` in place.

    ``edge1`` and ``edge2`` are the two edges being swapped, e.g. ``(v, a)`` and
    ``(u, b)`` become ``(v, u)`` and ``(a, b)``. Reusable inside larger composite
    scenes, not just the standalone :class:`TwoSwitchScene`.
    """
    v, a = edge1
    u, b = edge2

    old_va = _edge_mobject(graph, v, a)
    old_ub = _edge_mobject(graph, u, b)
    key_va = (v, a) if (v, a) in graph.edges else (a, v)
    key_ub = (u, b) if (u, b) in graph.edges else (b, u)

    # Isolate the two edges under scrutiny in the highlight color; everything
    # else in the graph is left untouched to make clear no other degree changes.
    scene.play(
        old_va.animate.set_color(style.MAGENTA),
        old_ub.animate.set_color(style.MAGENTA),
        run_time=run_time / 2,
    )

    # Manim Graph keeps an ``update_edges`` updater that re-pins every edge to
    # its dict-key endpoints each frame. Suspend it so the morph can stick,
    # then re-key the edges before restoring the updater.
    graph.remove_updater(graph.update_edges)

    scene.play(
        old_va.animate.put_start_and_end_on(graph[v].get_center(), graph[u].get_center()),
        old_ub.animate.put_start_and_end_on(graph[a].get_center(), graph[b].get_center()),
        run_time=run_time,
    )

    del graph.edges[key_va]
    del graph.edges[key_ub]
    graph.edges[(v, u)] = old_va
    graph.edges[(a, b)] = old_ub
    graph.add_updater(graph.update_edges)

    scene.play(
        old_va.animate.set_color(style.NAVY),
        old_ub.animate.set_color(style.NAVY),
        run_time=run_time / 2,
    )

    nx_graph.remove_edge(v, a)
    nx_graph.remove_edge(u, b)
    nx_graph.add_edge(v, u)
    nx_graph.add_edge(a, b)


class TwoSwitchScene(GraphScene):
    """Standalone scene: build a graph, then perform one 2-switch.

    Set ``nx_graph``, ``edge1``, and ``edge2`` to parameterize.
    Set ``label_kind`` to ``"degree"`` or ``"name"`` (vertex ids).
    """

    nx_graph: nx.Graph | None = None
    edge1: tuple | None = None
    edge2: tuple | None = None
    label_kind: str = "name"

    def construct(self) -> None:
        if self.nx_graph is None or self.edge1 is None or self.edge2 is None:
            raise ValueError("TwoSwitchScene requires nx_graph, edge1, and edge2 to be set")

        graph = self.build_graph(self.nx_graph)
        labels = self.build_vertex_labels(graph, self.nx_graph, kind=self.label_kind)

        self.play(Create(graph))
        self.play(*[FadeIn(label) for label in labels.values()])
        self.wait(0.5)

        animate_two_switch(self, graph, self.nx_graph, self.edge1, self.edge2)

        self.wait(0.5)
