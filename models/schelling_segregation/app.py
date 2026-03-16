"""
Schelling Segregation Model - Interactive Visualization
========================================================
This module sets up Mesa's SolaraViz interactive dashboard.

Run with:
    solara run app.py

This will open a browser window with sliders to control model
parameters and a live grid + chart visualization.

Requires:
    pip install "mesa[rec]"
"""

from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

from model import Schelling

# ──────────────────────────────────────────────────────────
# 1. AGENT PORTRAYAL FUNCTION
# ──────────────────────────────────────────────────────────
# This function tells the visualizer how to draw each agent.
# It returns an AgentPortrayalStyle with position, color,
# shape, and size information.


def agent_portrayal(agent):
    """Define how each agent should appear on the grid.

    Args:
        agent: A SchellingAgent instance.

    Returns:
        An AgentPortrayalStyle with visual properties.
    """
    style = AgentPortrayalStyle(
        x=agent.cell.coordinate[0],
        y=agent.cell.coordinate[1],
        marker="s",   # Square marker
        size=50,
    )

    # Color-code by type and happiness
    if agent.type == 0:
        # Majority type → blue shades
        if agent.happy:
            style.update(("color", "#3498db"), ("size", 50))   # Happy: bright blue
        else:
            style.update(("color", "#1a5276"), ("size", 35))   # Unhappy: dark blue
    else:
        # Minority type → orange shades
        if agent.happy:
            style.update(("color", "#e67e22"), ("size", 50))   # Happy: bright orange
        else:
            style.update(("color", "#784212"), ("size", 35))   # Unhappy: dark orange

    return style


# ──────────────────────────────────────────────────────────
# 2. MODEL PARAMETERS (Sliders)
# ──────────────────────────────────────────────────────────
# These create interactive sliders in the dashboard so you
# can tweak parameters and restart the model live.

model_params = {
    "density": Slider("Agent Density", 0.8, 0.1, 1.0, 0.1),
    "minority_pc": Slider("Fraction Minority", 0.3, 0.0, 1.0, 0.05),
    "homophily": Slider("Homophily Threshold", 0.4, 0.0, 1.0, 0.05),
    "width": 20,
    "height": 20,
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
}

# ──────────────────────────────────────────────────────────
# 3. CREATE THE VISUALIZATION
# ──────────────────────────────────────────────────────────

# Create a model instance for the visualization
model1 = Schelling()

# Set up the grid renderer with our portrayal function
renderer = SpaceRenderer(model1, backend="matplotlib").setup_agents(
    agent_portrayal
)
renderer.render()

# Create a line chart component for tracking happiness
HappyPlot = make_plot_component({"happy": "tab:green"})

# Assemble the full interactive dashboard
page = SolaraViz(
    model1,
    renderer,
    components=[HappyPlot],
    model_params=model_params,
)
page  # noqa — Solara needs this at module level
