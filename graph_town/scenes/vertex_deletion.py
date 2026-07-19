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
    degree_labels: dict,
    run_time: float = style.DEFAULT_RUN_TIME,
) -> None:
    """Play the vertex-deletion animation and mutate ``nx_graph``/``degree_labels`` in place.

    Reusable inside larger composite scenes (not just the standalone
    :class:`VertexDeletionScene`) — pass in whatever graph mobject, networkx graph,
    and degree-label dict are already on screen.
    """
    neighbors = list(nx_graph.neighbors(vertex))
    vertex_mob = graph[vertex]
    incident_edge_mobs = [graph.edges[e] for e in list(graph.edges) if vertex in e]

    scene.play(
        FadeOut(vertex_mob),
        *[FadeOut(edge_mob) for edge_mob in incident_edge_mobs],
        run_time=run_time,
    )

    new_labels = {}
    for neighbor in neighbors:
        new_degree = nx_graph.degree[neighbor] - 1
        new_label = scene.degree_label(new_degree)
        new_label.move_to(degree_labels[neighbor])
        new_labels[neighbor] = new_label

    scene.play(
        *[Transform(degree_labels[neighbor], new_labels[neighbor]) for neighbor in neighbors],
        run_time=run_time,
    )

    nx_graph.remove_node(vertex)
    del degree_labels[vertex]


class VertexDeletionScene(GraphScene):
    """Standalone scene: build a graph, then delete one vertex.

    Set ``nx_graph`` and ``vertex`` (e.g. via subclassing or before ``render()``)
    to parameterize; not written against a specific example graph.
    """

    nx_graph: nx.Graph | None = None
    vertex = None

    def construct(self) -> None:
        if self.nx_graph is None or self.vertex is None:
            raise ValueError("VertexDeletionScene requires nx_graph and vertex to be set")

        graph = self.build_graph(self.nx_graph)
        labels = self.build_degree_labels(graph, self.nx_graph)

        self.play(Create(graph))
        self.play(*[FadeIn(label) for label in labels.values()])
        self.wait(0.5)

        animate_vertex_deletion(self, graph, self.nx_graph, self.vertex, labels)

        self.wait(0.5)
