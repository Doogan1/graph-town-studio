import networkx as nx

from graph_town.scenes.two_switch import TwoSwitchScene

g = nx.petersen_graph()


class DemoTwoSwitch(TwoSwitchScene):
    nx_graph = g
    edge1 = (1, 2)
    edge2 = (3, 4)
    label_kind = "name"  # or "degree"
