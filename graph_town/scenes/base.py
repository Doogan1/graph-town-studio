"""Shared base Scene class for Graph Town videos.

Builds on Manim's networkx-backed ``Graph`` mobject so scenes generalize
across arbitrary input graphs rather than hand-placed shapes.
"""

from __future__ import annotations

import networkx as nx
from manim import Graph, Scene, Text

from graph_town import style


class GraphScene(Scene):
    """Base scene with helpers for building house-style graphs and degree labels."""

    def build_graph(
        self,
        nx_graph: nx.Graph,
        layout: str = "spring",
        layout_scale: float = 2.5,
        vertex_color: str = style.NAVY,
        edge_color: str = style.NAVY,
    ) -> Graph:
        """Create a Manim ``Graph`` mobject from a networkx graph, house-styled."""
        return Graph(
            list(nx_graph.nodes),
            list(nx_graph.edges),
            layout=layout,
            layout_scale=layout_scale,
            vertex_config={"fill_color": vertex_color, "radius": style.VERTEX_RADIUS},
            edge_config={"stroke_color": edge_color, "stroke_width": style.EDGE_STROKE_WIDTH},
        )

    def degree_label(self, degree: int) -> Text:
        """A house-styled Text mobject for a vertex degree annotation."""
        return Text(str(degree), font_size=style.LABEL_FONT_SIZE, color=style.NAVY)

    def build_degree_labels(self, graph: Graph, nx_graph: nx.Graph) -> dict:
        """Create degree labels for every vertex, positioned just outside each node."""
        labels = {}
        for v in nx_graph.nodes:
            vertex_mob = graph[v]
            label = self.degree_label(nx_graph.degree[v])
            label.next_to(vertex_mob, direction=[0.6, 0.6, 0], buff=0.1)
            labels[v] = label
        return labels
