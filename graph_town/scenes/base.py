"""Shared base Scene class for Graph Town videos.

Builds on Manim's networkx-backed ``Graph`` mobject so scenes generalize
across arbitrary input graphs rather than hand-placed shapes.
"""

from __future__ import annotations

from typing import Callable, Literal

import networkx as nx
import numpy as np
from manim import Graph, Scene, Text

from graph_town import style

LabelKind = Literal["degree", "name"]
LabelTextFn = Callable[[object, nx.Graph], str]


class GraphScene(Scene):
    """Base scene with helpers for building house-style graphs and vertex labels."""

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

    def make_label(self, text: str) -> Text:
        """A house-styled Text mobject for a vertex annotation."""
        return Text(str(text), font_size=style.LABEL_FONT_SIZE, color=style.NAVY)

    def degree_label(self, degree: int) -> Text:
        """A house-styled Text mobject for a vertex degree annotation."""
        return self.make_label(str(degree))

    def label_text_for(self, vertex, nx_graph: nx.Graph, kind: LabelKind) -> str:
        """Resolve the string shown next to ``vertex`` for the given label kind."""
        if kind == "degree":
            return str(nx_graph.degree[vertex])
        if kind == "name":
            return str(vertex)
        raise ValueError(f"Unknown label kind {kind!r}; expected 'degree' or 'name'")

    def build_vertex_labels(
        self,
        graph: Graph,
        nx_graph: nx.Graph,
        kind: LabelKind = "degree",
        text_for: LabelTextFn | None = None,
    ) -> dict:
        """Create labels for every vertex, positioned just outside each node.

        Parameters
        ----------
        kind:
            ``"degree"`` (default) or ``"name"`` (the NetworkX node key).
        text_for:
            Optional ``(vertex, nx_graph) -> str`` override. When set, ``kind``
            is ignored — use this for one-off custom labeling.
        """
        labels = {}
        center = graph.get_center()
        for v in nx_graph.nodes:
            vertex_mob = graph[v]
            text = text_for(v, nx_graph) if text_for is not None else self.label_text_for(v, nx_graph, kind)
            label = self.make_label(text)
            outward = vertex_mob.get_center() - center
            if np.linalg.norm(outward) < 1e-6:
                outward = np.array([0.6, 0.6, 0.0])
            label.next_to(vertex_mob, direction=outward, buff=0.15)
            labels[v] = label
        return labels

    def build_degree_labels(self, graph: Graph, nx_graph: nx.Graph) -> dict:
        """Create degree labels for every vertex (shortcut for ``kind="degree"``)."""
        return self.build_vertex_labels(graph, nx_graph, kind="degree")
