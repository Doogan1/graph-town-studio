"""Beat -> scene dispatcher.

Maps each beat's ``scene_name`` (parsed from its ``scene_spec``) to the
corresponding scene class in the scene library, resolves any named
:class:`~graph_town.beatsheet.parser.Ref` arguments against a caller-supplied
registry of graphs, and triggers a render.
"""

from __future__ import annotations

from graph_town.beatsheet.parser import Beat, Ref
from graph_town.scenes.recap import RecapScene
from graph_town.scenes.two_switch import TwoSwitchScene
from graph_town.scenes.vertex_deletion import VertexDeletionScene

SCENE_REGISTRY = {
    "vertex_deletion": VertexDeletionScene,
    "two_switch": TwoSwitchScene,
    "recap": RecapScene,
}


def resolve_args(scene_args: dict, graphs: dict) -> dict:
    """Substitute any :class:`Ref` values with the named graph from ``graphs``."""
    resolved = {}
    for key, value in scene_args.items():
        if isinstance(value, Ref):
            if value.name not in graphs:
                raise KeyError(
                    f"Unknown graph reference '{value.name}' — register it in "
                    "the `graphs` dict passed to the dispatcher"
                )
            resolved[key] = graphs[value.name]
        else:
            resolved[key] = value
    return resolved


def dispatch_beat(beat: Beat, graphs: dict | None = None, **render_kwargs):
    """Instantiate and render the scene for a single beat.

    Static beats (``visual_type == "static"``) have no scene to render and
    are skipped, returning ``None``.
    """
    if beat.visual_type != "animation":
        return None

    scene_cls = SCENE_REGISTRY.get(beat.scene_name)
    if scene_cls is None:
        raise KeyError(f"No scene registered for '{beat.scene_name}' (beat {beat.beat_id})")

    args = resolve_args(beat.scene_args, graphs or {})
    scene_subclass = type(f"{scene_cls.__name__}_{beat.beat_id}", (scene_cls,), args)

    scene = scene_subclass(**render_kwargs)
    scene.render()
    return scene


def dispatch_beatsheet(beats: list[Beat], graphs: dict | None = None, **render_kwargs) -> list:
    """Dispatch every beat in order, returning the rendered scene instances."""
    return [dispatch_beat(beat, graphs=graphs, **render_kwargs) for beat in beats]
