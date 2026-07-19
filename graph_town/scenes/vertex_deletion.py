"""Vertex deletion animation.

Given a graph and a vertex, fade out the vertex and its incident edges while
each former neighbor's degree label decrements by 1 in place.
"""

from __future__ import annotations

import networkx as nx
from manim import Create, FadeIn, FadeOut, Transform

from graph_town import style
from graph_town.scenes.base import GraphScene


def animate_vertex_deletion(
    scene: GraphScene,
    graph,
    nx_graph: nx.Graph,
    vertex,
    labels: dict,
    run_time: float = style.DEFAULT_RUN_TIME,
    *,
    update_degree_labels: bool = True,
) -> None:
    """Play the vertex-deletion animation and mutate ``nx_graph``/``labels`` in place.

    Reusable inside larger composite scenes (not just the standalone
    :class:`VertexDeletionScene`) — pass in whatever graph mobject, networkx graph,
    and label dict are already on screen.

    When ``update_degree_labels`` is True (default), neighbor labels are
    transformed to the new degrees. Set False when labels are vertex names.
    """
    neighbors = list(nx_graph.neighbors(vertex))
    vertex_mob = graph[vertex]
    incident_edge_mobs = [graph.edges[e] for e in list(graph.edges) if vertex in e]

    fade_outs = [FadeOut(vertex_mob), *[FadeOut(edge_mob) for edge_mob in incident_edge_mobs]]
    if vertex in labels:
        fade_outs.append(FadeOut(labels[vertex]))

    scene.play(*fade_outs, run_time=run_time)

    if update_degree_labels:
        new_labels = {}
        for neighbor in neighbors:
            new_degree = nx_graph.degree[neighbor] - 1
            new_label = scene.degree_label(new_degree)
            new_label.move_to(labels[neighbor])
            new_labels[neighbor] = new_label

        scene.play(
            *[Transform(labels[neighbor], new_labels[neighbor]) for neighbor in neighbors],
            run_time=run_time,
        )

    nx_graph.remove_node(vertex)
    labels.pop(vertex, None)


class VertexDeletionScene(GraphScene):
    """Standalone scene: build a graph, then delete one vertex.

    Set ``nx_graph`` and ``vertex`` (e.g. via subclassing or before ``render()``)
    to parameterize; not written against a specific example graph.

    Set ``label_kind`` to ``"degree"`` (default) or ``"name"``.
    """

    nx_graph: nx.Graph | None = None
    vertex = None
    label_kind: str = "degree"

    def construct(self) -> None:
        if self.nx_graph is None or self.vertex is None:
            raise ValueError("VertexDeletionScene requires nx_graph and vertex to be set")

        graph = self.build_graph(self.nx_graph)
        labels = self.build_vertex_labels(graph, self.nx_graph, kind=self.label_kind)

        self.play(Create(graph))
        self.play(*[FadeIn(label) for label in labels.values()])
        self.wait(0.5)

        animate_vertex_deletion(
            self,
            graph,
            self.nx_graph,
            self.vertex,
            labels,
            update_degree_labels=self.label_kind == "degree",
        )

        self.wait(0.5)
