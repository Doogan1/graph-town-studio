"""House style constants for Graph Town videos.

Colors are sourced by pixel-sampling the channel's profile image (a Clebsch
graph rendering), so branding and video visuals share one palette by design.
"""

# Colors
NAVY = "#283891"  # default node/edge color
MAGENTA = "#9E1F63"  # highlight color - "whatever the narration is currently pointing at"
GRAY = "#939598"  # secondary edges / de-emphasized elements
BACKGROUND = "#FFFFFF"

# Animation timing
DEFAULT_RUN_TIME = 1.0  # standard transitions (fades, morphs)
EMPHASIS_RUN_TIME = 0.5  # quick highlight pulses
SLOW_RUN_TIME = 2.0  # deliberate, narration-paced transitions

# Layout / mobject defaults
VERTEX_RADIUS = 0.3
EDGE_STROKE_WIDTH = 4
LABEL_FONT_SIZE = 24
