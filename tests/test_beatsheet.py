from pathlib import Path

import networkx as nx
import pytest

from graph_town.beatsheet.dispatcher import SCENE_REGISTRY, resolve_args
from graph_town.beatsheet.parser import Ref, SceneSpecError, parse_beatsheet, parse_scene_spec

SAMPLE_CSV = Path(__file__).parent.parent / "examples" / "sample_beatsheet.csv"


def test_parse_scene_spec_vertex_deletion():
    name, args = parse_scene_spec("vertex_deletion(nx_graph=g1, vertex=3)")
    assert name == "vertex_deletion"
    assert args == {"nx_graph": Ref("g1"), "vertex": 3}


def test_parse_scene_spec_two_switch_tuples():
    name, args = parse_scene_spec("two_switch(nx_graph=g1, edge1=(1, 2), edge2=(4, 5))")
    assert name == "two_switch"
    assert args["edge1"] == (1, 2)
    assert args["edge2"] == (4, 5)


def test_parse_scene_spec_recap_list_of_strings():
    name, args = parse_scene_spec('recap(title="X", steps=["a", "b"])')
    assert name == "recap"
    assert args == {"title": "X", "steps": ["a", "b"]}


def test_parse_scene_spec_rejects_positional_args():
    with pytest.raises(SceneSpecError):
        parse_scene_spec("vertex_deletion(g1, 3)")


def test_parse_scene_spec_rejects_garbage():
    with pytest.raises(SceneSpecError):
        parse_scene_spec("not a call")


def test_parse_beatsheet_sample_csv():
    beats = parse_beatsheet(SAMPLE_CSV)
    assert [b.beat_id for b in beats] == ["b1", "b2", "b3", "b4"]

    static_beat = beats[0]
    assert static_beat.visual_type == "static"
    assert static_beat.scene_name == ""

    vertex_deletion_beat = beats[1]
    assert vertex_deletion_beat.scene_name == "vertex_deletion"
    assert vertex_deletion_beat.scene_args["vertex"] == 3

    recap_beat = beats[3]
    assert recap_beat.scene_name == "recap"
    assert recap_beat.scene_args["title"] == "Havel-Hakimi"
    assert recap_beat.scene_args["steps"] == [
        "Sort degrees",
        "Remove max vertex",
        "Repeat until done",
    ]


def test_resolve_args_substitutes_graph_ref():
    g1 = nx.path_graph(5)
    resolved = resolve_args({"nx_graph": Ref("g1"), "vertex": 3}, {"g1": g1})
    assert resolved == {"nx_graph": g1, "vertex": 3}


def test_resolve_args_raises_on_unknown_ref():
    with pytest.raises(KeyError):
        resolve_args({"nx_graph": Ref("missing")}, {})


def test_scene_registry_has_all_three_scenes():
    assert set(SCENE_REGISTRY) == {"vertex_deletion", "two_switch", "recap"}
