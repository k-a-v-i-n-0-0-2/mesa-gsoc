"""
Schelling Segregation Model - Agent Definition
================================================
This module defines the SchellingAgent, which represents an individual
resident in the Schelling Segregation simulation.

Each agent has a "type" (representing their group/color) and a preference
for living near similar neighbors (homophily threshold). If the fraction
of similar neighbors falls below this threshold, the agent becomes
"unhappy" and will relocate to a random empty cell.
"""

from mesa.discrete_space import CellAgent


class SchellingAgent(CellAgent):
    """An agent in the Schelling segregation model.

    Each agent belongs to one of two groups (type 0 or type 1).
    Agents evaluate their neighborhood and move if the fraction
    of same-type neighbors is below their homophily threshold.

    Attributes:
        type (int): The agent's group (0 = majority, 1 = minority).
        homophily (float): Minimum fraction of similar neighbors
                           needed for the agent to be "happy" (0.0 to 1.0).
        radius (int): How far the agent looks when checking neighbors.
        happy (bool): Whether the agent is currently satisfied with
                      its neighborhood.
    """

    def __init__(
        self,
        model,
        cell,
        agent_type: int,
        homophily: float = 0.4,
        radius: int = 1,
    ) -> None:
        """Create a new Schelling agent.

        Args:
            model: The Model instance this agent belongs to.
            cell: The grid cell where the agent is initially placed.
            agent_type: The agent's group identifier (0 or 1).
            homophily: Fraction of similar neighbors required for happiness.
            radius: How many cells away to look for neighbors.
        """
        super().__init__(model)
        self.cell = cell           # Place the agent on the grid
        self.type = agent_type     # Group membership (0 or 1)
        self.homophily = homophily # Similarity threshold
        self.radius = radius       # Neighborhood search radius
        self.happy = False         # Start as unhappy

    def evaluate_happiness(self) -> None:
        """Check the neighborhood and determine if the agent is happy.

        The agent looks at all neighbors within `self.radius` cells.
        If the fraction of same-type neighbors is >= `self.homophily`,
        the agent is happy; otherwise it is unhappy.

        This is separated from `step()` so that all agents evaluate
        their state before any of them move.
        """
        # Get all agents in the surrounding neighborhood
        neighbors = list(self.cell.get_neighborhood(radius=self.radius).agents)

        if len(neighbors) == 0:
            # No neighbors → agent is considered unhappy
            self.happy = False
            return

        # Count how many neighbors share the same type
        similar_count = sum(1 for n in neighbors if n.type == self.type)

        # Calculate the fraction of similar neighbors
        similarity_fraction = similar_count / len(neighbors)

        # Compare against the homophily threshold
        if similarity_fraction >= self.homophily:
            self.happy = True
            self.model.happy += 1  # Update the model's happy counter
        else:
            self.happy = False

    def step(self) -> None:
        """Execute one step for this agent.

        If the agent is unhappy, it moves to a random empty cell
        on the grid. Happy agents stay where they are.
        """
        if not self.happy:
            self.cell = self.model.grid.select_random_empty_cell()
