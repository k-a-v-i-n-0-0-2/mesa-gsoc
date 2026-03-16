"""
SIR Epidemic Model - Agent Definition
=======================================
This module defines the InfectiousAgent, representing an individual
in a population that can be Susceptible, Infected, or Recovered.
"""

from mesa.discrete_space import CellAgent
import enum

class State(enum.IntEnum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2

class InfectiousAgent(CellAgent):
    """An agent in the SIR model.
    
    Attributes:
        state (State): The current health state (S, I, or R).
        infection_duration (int): How long the agent has been infected.
    """

    def __init__(self, model, cell, initial_state=State.SUSCEPTIBLE):
        super().__init__(model)
        self.cell = cell
        self.state = initial_state
        self.infection_duration = 0

    def step(self):
        """Execute one step of agent logic."""
        if self.state == State.INFECTED:
            self.update_infection()
        elif self.state == State.SUSCEPTIBLE:
            self.check_infection()

    def check_infection(self):
        """Check if susceptible agent becomes infected by neighbors."""
        # Get neighbors
        neighbors = self.cell.get_neighborhood(radius=1).agents
        
        # Count infected neighbors
        infected_neighbors = sum(1 for n in neighbors if n.state == State.INFECTED)
        
        if infected_neighbors > 0:
            # Chance of infection based on number of infected neighbors
            # P = 1 - (1 - p)^n where p is transmission probability
            p = self.model.transmission_prob
            infection_chance = 1 - (1 - p)**infected_neighbors
            
            if self.model.random.random() < infection_chance:
                self.state = State.INFECTED
                self.infection_duration = 0

    def update_infection(self):
        """Update the state of an infected agent."""
        self.infection_duration += 1
        
        # Check for recovery
        if self.infection_duration >= self.model.recovery_time:
            self.state = State.RECOVERED
