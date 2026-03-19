# Mesa 3.0+ Architecture Deep-Dive 🏗️

This guide documents the internals of the Mesa agent-based modeling framework as studied during my GSoC preparation. All examples reference code from my learning space models.

---

## 1. The Four Pillars of Mesa

### 1.1 Model (`mesa.Model`)
The **Model** is the top-level container for the entire simulation. It owns:
- The **grid/space** where agents live.
- The **agent registry** (`self.agents` — an `AgentSet`).
- The **data collector** for recording metrics.
- The **random number generator** (`self.random`) for reproducibility.
- A **`step()`** method that advances the simulation by one tick.

```python
from mesa import Model

class MyModel(Model):
    def __init__(self, seed=None):
        super().__init__(seed=seed)   # seed ensures reproducibility
        self.grid = ...               # create a space
        # create agents, data collector, etc.

    def step(self):
        self.agents.shuffle_do("step")  # activate all agents randomly
```

**Key Insight**: When you call `super().__init__(seed=seed)`, Mesa automatically creates:
- `self.agents` → an `AgentSet` that tracks all agents created for this model
- `self.random` → a seeded random number generator
- `self.running = True` → a flag to control simulation termination

---

### 1.2 Agent (`mesa.Agent` / `mesa.discrete_space.CellAgent`)

Agents are the individuals in the simulation. Mesa provides two main types:

| Agent Type | Use Case | How Placement Works |
|---|---|---|
| `mesa.Agent` | General-purpose (no grid needed) | No spatial position |
| `CellAgent` | Grid-based models | `self.cell = some_cell` places the agent |

```python
from mesa.discrete_space import CellAgent

class MyAgent(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)   # registers with model.agents automatically
        self.cell = cell          # places agent on the grid

    def step(self):
        # Agent behavior goes here
        pass
```

**Key Insight**: When you write `super().__init__(model)`, the agent is **automatically registered** in `model.agents`. You never need to manually add it.

---

### 1.3 Space / Grid (`mesa.discrete_space`)

Mesa provides several grid types. The modern API lives in `mesa.discrete_space`:

| Grid Type | Neighbors | Description |
|---|---|---|
| `OrthogonalMooreGrid` | 8 (including diagonals) | Most common; used in Schelling & SIR |
| `OrthogonalVonNeumannGrid` | 4 (N, S, E, W only) | For models where diagonal contact doesn't make sense |
| `HexGrid` | 6 | Hexagonal tiling |

```python
from mesa.discrete_space import OrthogonalMooreGrid

grid = OrthogonalMooreGrid(
    (width, height),        # dimensions
    random=self.random,     # for random cell selection
    capacity=1,             # max agents per cell (1 = one agent per cell)
    torus=True,             # edges wrap around (like a donut)
)
```

**Key Properties**:
- `grid.all_cells` → iterate over every cell (used during initialization)
- `grid.select_random_empty_cell()` → find a random unoccupied cell
- `cell.get_neighborhood(radius=1)` → get surrounding cells
- `cell.agents` → list of agents currently on that cell

---

### 1.4 AgentSet (The Modern Scheduler)

In Mesa 3.0+, the old `mesa.time.RandomActivation` scheduler is **deprecated**. Instead, `model.agents` is an `AgentSet` with powerful batch operations:

| Method | What It Does |
|---|---|
| `agents.shuffle_do("step")` | Randomly reorder agents, then call `step()` on each |
| `agents.do("step")` | Call `step()` on each agent in registration order |
| `agents.select(condition)` | Filter agents by a lambda/function |
| `agents.shuffle()` | Randomize the order without calling a method |

```python
# In model.step():
self.agents.shuffle_do("step")          # Random activation (most common)

# Or for two-pass logic (like Schelling):
self.agents.do("evaluate_happiness")    # First: everyone evaluates
self.agents.shuffle_do("step")          # Then: unhappy agents move
```

**Why This Matters**: `shuffle_do` prevents **order bias** — if agents always act in the same order, the first agent gets an unfair advantage. Randomization is essential for fair simulations.

---

## 2. Data Collection (`mesa.datacollection.DataCollector`)

The `DataCollector` automatically records metrics at each step without boilerplate:

```python
from mesa.datacollection import DataCollector

self.datacollector = DataCollector(
    model_reporters={
        "happy": "happy",                              # direct attribute
        "pct_happy": lambda m: (m.happy / len(m.agents)) * 100,  # computed
        "population": lambda m: len(m.agents),
    },
    agent_reporters={
        "agent_type": "type",     # per-agent attribute
        "is_happy": "happy",
    },
)
```

**Usage**:
- Call `self.datacollector.collect(self)` at the end of each `step()`.
- Retrieve data: `model.datacollector.get_model_dataframe()` → a Pandas DataFrame.

---

## 3. Visualization (`SolaraViz`)

Mesa 3.0+ uses **Solara** (a reactive Python web framework) for interactive dashboards:

```python
from mesa.visualization import SolaraViz, Slider, make_plot_component

# 1. Define how agents look
def agent_portrayal(agent):
    return AgentPortrayalStyle(
        x=agent.cell.coordinate[0],
        y=agent.cell.coordinate[1],
        color="blue" if agent.type == 0 else "orange",
        marker="s",   # square
        size=50,
    )

# 2. Define interactive parameters
model_params = {
    "density": Slider("Density", 0.8, 0.1, 1.0, 0.1),
}

# 3. Assemble the dashboard
page = SolaraViz(model, components=[...], model_params=model_params)
```

**Run with**: `solara run app.py` → opens a browser with live sliders and charts.

---

## 4. The Simulation Loop (How It All Connects)

```
Model.__init__()
│
├── Create Grid (OrthogonalMooreGrid)
├── Create Agents (CellAgent) → auto-registered in model.agents
├── Create DataCollector
└── Initial data collection
        │
        ▼
Model.step()  [called repeatedly]
│
├── Reset counters
├── agents.shuffle_do("step")  →  each agent acts
├── agents.do("evaluate")      →  each agent re-evaluates
├── datacollector.collect()    →  record metrics
└── Check termination condition (self.running = False to stop)
```

---

## 5. Key Differences: Mesa 3.0+ vs Legacy Mesa

| Feature | Legacy Mesa (< 3.0) | Modern Mesa (3.0+) |
|---|---|---|
| Scheduler | `mesa.time.RandomActivation(model)` | `model.agents.shuffle_do("step")` |
| Grid | `mesa.space.SingleGrid` | `mesa.discrete_space.OrthogonalMooreGrid` |
| Agent base class | `mesa.Agent` | `mesa.discrete_space.CellAgent` |
| Visualization | `mesa.visualization.ModularServer` (Tornado) | `SolaraViz` (Solara/browser) |
| Agent placement | `grid.place_agent(agent, pos)` | `agent.cell = cell` |
| Neighbor query | `grid.get_neighbors(pos, moore=True)` | `cell.get_neighborhood(radius=1).agents` |

---

## References
- [Mesa Documentation](https://mesa.readthedocs.io/)
- [Mesa GitHub](https://github.com/projectmesa/mesa)
- [Mesa 3.0 Migration Guide](https://mesa.readthedocs.io/stable/migration_guide.html)
