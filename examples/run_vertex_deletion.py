import networkx as nx

from graph_town.scenes.vertex_deletion import VertexDeletionScene

g = nx.petersen_graph()


class DemoVertexDeletion(VertexDeletionScene):
    nx_graph = g
    vertex = 2
    label_kind = "degree"
