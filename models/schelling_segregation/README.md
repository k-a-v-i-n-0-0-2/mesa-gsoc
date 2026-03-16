# Schelling Segregation Model 🏘️

## What the Model Does

The **Schelling Segregation Model** is one of the most famous agent-based models in social science. Created by economist Thomas Schelling in 1971, it shows a counterintuitive result: **even when individuals have only a mild preference for living near people like themselves, the population can end up highly segregated.**

### The Setup
- A 2D grid is populated with agents of **two types** (think of them as two colors, or two groups).
- Each agent checks its **neighboring cells** (the 8 surrounding squares).
- Each agent has a **homophily threshold** — the minimum fraction of same-type neighbors needed to feel "happy."
- **Unhappy agents** move to a random empty cell.
- The simulation runs until all agents are happy or a maximum number of steps is reached.

### The Surprising Result
Even with a homophily threshold of just 30–40% (meaning agents are perfectly fine being a minority in their neighborhood), the grid evolves into **highly segregated clusters**. This emergent behavior arises from simple individual rules — a hallmark of agent-based modeling.

---

## How It Works

### Architecture

```
agents.py  →  SchellingAgent (CellAgent)
                ├── evaluate_happiness()  — check neighbors, set happy/unhappy
                └── step()               — move if unhappy

model.py   →  Schelling (Model)
                ├── __init__()           — create grid, agents, data collector
                └── step()              — shuffle agents, evaluate, collect data

run.py     →  Headless runner
                ├── run_single_simulation()  — run one experiment
                ├── plot_results()           — matplotlib charts
                └── run_parameter_sweep()    — vary homophily

app.py     →  Interactive SolaraViz dashboard (browser-based)
```

### Mesa Features Used

| Mesa Component | What It Does | Where Used |
|---|---|---|
| `mesa.Model` | Manages the overall simulation | `model.py` |
| `CellAgent` | Agent that lives on a grid cell | `agents.py` |
| `OrthogonalMooreGrid` | 2D grid with 8-neighbor connectivity | `model.py` |
| `DataCollector` | Automatically records metrics each step | `model.py` |
| `AgentSet` (`shuffle_do`, `do`) | Activates agents in bulk | `model.py` |
| `SolaraViz` | Interactive browser dashboard | `app.py` |
| `SpaceRenderer` | Renders agents on the grid | `app.py` |
| `make_plot_component` | Creates live line charts | `app.py` |

### Step-by-Step Flow

1. **Initialization**: Grid created → agents randomly placed → initial happiness evaluated
2. **Each Step**:
   - Reset happy counter
   - Shuffle all agents randomly
   - Each unhappy agent moves to a random empty cell
   - Re-evaluate every agent's happiness
   - Collect data (happy count, % happy, population)
3. **Termination**: Stop when all agents are happy

---

## How to Run

### Prerequisites
```bash
pip install mesa matplotlib pandas
# For interactive visualization:
pip install "mesa[rec]"
```

### Run the headless simulation
```bash
cd models/schelling_segregation
python run.py
```
This runs a single simulation + parameter sweep and generates plots.

### Run the interactive dashboard
```bash
cd models/schelling_segregation
solara run app.py
```
This opens a browser with sliders for density, minority fraction, and homophily.

---

## What I Learned

### Mesa's Architecture
- **Model/Agent separation**: Mesa cleanly separates the "manager" (Model) from the "individuals" (Agent). The Model creates agents, manages the grid, and orchestrates each step. Agents contain their own behavior logic.
- **Grid systems**: `OrthogonalMooreGrid` provides 8-directional neighborhood queries out of the box. The `CellAgent` class makes placement as simple as `self.cell = cell`.
- **Data collection**: `DataCollector` eliminates boilerplate — you declare what to track, and Mesa records it automatically each step.
- **AgentSet operations**: `shuffle_do("step")` activates agents in random order with one line. This is cleaner than manually iterating and shuffling.

### Agent-Based Modeling Concepts
- **Emergence**: Simple individual rules (move if < 40% similar neighbors) produce complex macro patterns (full segregation). You can't predict the outcome just by reading the rules.
- **Activation order matters**: Random shuffling (`shuffle_do`) vs. sequential (`do`) can produce different results. Mesa makes it easy to experiment with different activation schemes.
- **Parameter sensitivity**: The parameter sweep shows that homophily has a nonlinear effect on convergence speed. Small changes in threshold can dramatically change outcomes.

### What Was Hard
- Understanding the difference between `CellAgent` and `mesa.Agent` — the discrete space system is the modern way, but older tutorials still reference the legacy `mesa.space` module.
- Getting the visualization right with `AgentPortrayalStyle` — the API has changed significantly in Mesa 3.x compared to older versions.
- Separating "evaluate" from "step" to avoid order-dependent bugs (if agents both evaluate and move in the same pass, early movers affect late evaluators).

### What Surprised Me
- How few lines of code are needed for a meaningful simulation — the entire model is ~50 lines of actual logic.
- How Mesa's `DataCollector` with lambda reporters makes it trivial to track derived metrics (like percentage happy).
- The Schelling result itself: 30% homophily preference → near-complete segregation. The model makes this tangible.

---

## Files

| File | Description |
|---|---|
| `agents.py` | `SchellingAgent` class — agent behavior (evaluate + move) |
| `model.py` | `Schelling` model class — grid, agents, data collection, stepping |
| `run.py` | Headless runner with plotting and parameter sweep |
| `app.py` | Interactive Solara-based browser visualization |
| `README.md` | This file — documentation of what I built and learned |

---

## Further Reading

- **Schelling's original paper**: [Dynamic Models of Segregation (1971)](https://www.stat.berkeley.edu/~aldous/157/Papers/Schelling_Seg_Models.pdf)
- **Interactive explanation**: [Parable of the Polygons](http://ncase.me/polygons/) by Vi Hart & Nicky Case
- **Mesa documentation**: [mesa.readthedocs.io](https://mesa.readthedocs.io/)
- **Mesa tutorials**: [Getting Started](https://mesa.readthedocs.io/stable/getting_started.html)
