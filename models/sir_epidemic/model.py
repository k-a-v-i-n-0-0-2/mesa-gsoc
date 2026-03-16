"""
SIR Epidemic Model - Model Definition
======================================
This module defines the SIRModel, managing the simulation environment,
agent placement, and data collection for an epidemic outbreak.
"""

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from agents import InfectiousAgent, State

class SIRModel(Model):
    """A simple SIR epidemic model on a grid."""

    def __init__(
        self,
        width=20,
        height=20,
        initial_infected=5,
        transmission_prob=0.1,
        recovery_time=10,
        seed=None
    ):
        super().__init__(seed=seed)
        self.transmission_prob = transmission_prob
        self.recovery_time = recovery_time
        
        # 1. Create the grid (capacity=1 means one agent per cell)
        self.grid = OrthogonalMooreGrid((width, height), capacity=1)
        
        # 2. Place agents in every cell
        for cell in self.grid.all_cells:
            # All start as Susceptible
            InfectiousAgent(self, cell, State.SUSCEPTIBLE)
            
        # 3. Randomly infect initial agents
        all_agents = list(self.agents)
        initial_cases = self.random.sample(all_agents, initial_infected)
        for agent in initial_cases:
            agent.state = State.INFECTED

        # 4. Data Collection
        self.datacollector = DataCollector(
            model_reporters={
                "Susceptible": lambda m: self.count_state(m, State.SUSCEPTIBLE),
                "Infected": lambda m: self.count_state(m, State.INFECTED),
                "Recovered": lambda m: self.count_state(m, State.RECOVERED),
            }
        )

    @staticmethod
    def count_state(model, state):
        """Helper to count agents in a specific state."""
        return sum(1 for a in model.agents if a.state == state)

    def step(self):
        """Advance the model by one step."""
        # Record data
        self.datacollector.collect(self)
        
        # Advance agents
        self.agents.shuffle_do("step")
        
        # Stopping condition: no more infected agents
        if self.count_state(self, State.INFECTED) == 0:
            self.running = False
