"""
Schelling Segregation Model - Model Definition
===============================================
This module defines the Schelling model, which manages the grid,
agents, data collection, and simulation stepping logic.

The Schelling Segregation Model demonstrates how individual preferences
for same-type neighbors can lead to large-scale spatial segregation,
even when each agent's preference is relatively mild.
"""

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid

from agents import SchellingAgent


class Schelling(Model):
    """The Schelling Segregation Model.

    This model places agents of two types on a grid. Each agent has a
    "homophily" threshold — the minimum fraction of same-type neighbors
    it needs to be happy. Unhappy agents relocate to a random empty cell.
    The simulation runs until all agents are happy or a maximum number
    of steps is reached.

    Key Mesa concepts demonstrated:
        - mesa.Model:       The top-level simulation manager
        - CellAgent:        Agents that live on grid cells
        - OrthogonalMooreGrid: A 2D grid with 8-neighbor connectivity
        - DataCollector:    Automatic data recording each step
        - AgentSet:         Managing and activating groups of agents

    Attributes:
        grid: The spatial grid where agents live.
        happy (int): Count of happy agents in the current step.
        datacollector: Records model-level and agent-level metrics.
    """

    def __init__(
        self,
        width: int = 20,
        height: int = 20,
        density: float = 0.8,
        minority_pc: float = 0.3,
        homophily: float = 0.4,
        radius: int = 1,
        seed: int | None = None,
    ):
        """Initialize the Schelling model.

        Args:
            width: Number of columns in the grid.
            height: Number of rows in the grid.
            density: Probability that a cell starts with an agent (0.0–1.0).
                     Higher values mean a more crowded grid.
            minority_pc: Probability that an agent is type 1 (minority).
                         0.5 means equal split; lower values mean fewer
                         minority agents.
            homophily: The minimum fraction of same-type neighbors an agent
                       needs to be happy (0.0–1.0).
            radius: How many cells away agents look for neighbors.
            seed: Random seed for reproducibility (None for random).
        """
        super().__init__(seed=seed)

        # Store parameters for reference / data collection
        self.density = density
        self.minority_pc = minority_pc

        # ──────────────────────────────────────────────────────────
        # 1. CREATE THE GRID (Space)
        # ──────────────────────────────────────────────────────────
        # OrthogonalMooreGrid: a 2D rectangular grid where each cell
        # connects to up to 8 neighbors (N, NE, E, SE, S, SW, W, NW).
        # - capacity=1 means each cell can hold at most one agent.
        # - torus=True wraps the grid so edges connect (like a donut).
        self.grid = OrthogonalMooreGrid(
            (width, height),
            random=self.random,
            capacity=1,
            torus=True,
        )

        # Counter for happy agents — reset each step
        self.happy = 0

        # ──────────────────────────────────────────────────────────
        # 2. SET UP DATA COLLECTION
        # ──────────────────────────────────────────────────────────
        # DataCollector automatically records metrics at each step.
        # - model_reporters:  model-level metrics (e.g., % happy)
        # - agent_reporters:  per-agent metrics (e.g., agent type)
        self.datacollector = DataCollector(
            model_reporters={
                "happy": "happy",
                "pct_happy": lambda m: (
                    (m.happy / len(m.agents)) * 100
                    if len(m.agents) > 0
                    else 0
                ),
                "population": lambda m: len(m.agents),
            },
            agent_reporters={
                "agent_type": "type",
                "is_happy": "happy",
            },
        )

        # ──────────────────────────────────────────────────────────
        # 3. CREATE AND PLACE THE AGENTS
        # ──────────────────────────────────────────────────────────
        # Iterate over every cell in the grid. For each cell, randomly
        # decide whether to place an agent there based on `density`.
        for cell in self.grid.all_cells:
            if self.random.random() < self.density:
                # Randomly assign the agent's type
                agent_type = 1 if self.random.random() < self.minority_pc else 0

                # Create the agent and place it on the cell
                SchellingAgent(
                    self,
                    cell,
                    agent_type,
                    homophily=homophily,
                    radius=radius,
                )

        # ──────────────────────────────────────────────────────────
        # 4. INITIAL STATE EVALUATION & DATA COLLECTION
        # ──────────────────────────────────────────────────────────
        # Evaluate happiness before the first step so we have a baseline.
        self.agents.do("evaluate_happiness")
        self.datacollector.collect(self)

    def step(self):
        """Advance the model by one step.

        Each step does the following:
        1. Reset the happy counter.
        2. Activate all agents in random order — unhappy agents move.
        3. Re-evaluate every agent's happiness.
        4. Collect data for this step.
        5. Check if the simulation should stop (all agents happy).
        """
        # Reset the happiness counter for this step
        self.happy = 0

        # Randomly shuffle agents and let each one act (move if unhappy)
        self.agents.shuffle_do("step")

        # After everyone has moved, re-evaluate happiness
        self.agents.do("evaluate_happiness")

        # Record the data for this step
        self.datacollector.collect(self)

        # Stop the simulation when everyone is happy
        if len(self.agents) > 0:
            self.running = self.happy < len(self.agents)
