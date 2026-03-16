"""
SIR Epidemic Model - Interactive Visualization
===============================================
Solara-based dashboard for the SIR model.
"""

from mesa.visualization import SolaraViz, make_plot_component, Slider
from mesa.visualization.components import AgentPortrayalStyle
from model import SIRModel, State

def agent_portrayal(agent):
    """Define how each agent looks on the grid."""
    style = AgentPortrayalStyle(
        x=agent.cell.coordinate[0],
        y=agent.cell.coordinate[1],
        marker="o",
        size=40,
    )
    
    # Colors based on state
    if agent.state == State.SUSCEPTIBLE:
        style.update({"color": "blue"})
    elif agent.state == State.INFECTED:
        style.update({"color": "red"})
    elif agent.state == State.RECOVERED:
        style.update({"color": "green"})
        
    return style

# Parameters for the dashboard
model_params = {
    "initial_infected": Slider("Initial Infected", 5, 1, 20, 1),
    "transmission_prob": Slider("Transmission Probability", 0.1, 0.01, 1.0, 0.05),
    "recovery_time": Slider("Recovery Time", 10, 1, 50, 1),
    "width": 20,
    "height": 20,
}

# Visualization components
SIR_Plot = make_plot_component({
    "Susceptible": "blue",
    "Infected": "red",
    "Recovered": "green"
})

# Assemble the app
page = SolaraViz(
    SIRModel(),
    components=[SIR_Plot],
    model_params=model_params,
    agent_portrayal=agent_portrayal
)
page
