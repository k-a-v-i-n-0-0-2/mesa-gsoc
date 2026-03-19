# Schelling Segregation Model 🏘️

## What the Model Does

The **Schelling Segregation Model** (Thomas Schelling, 1971) is one of the most influential agent-based models in social science. It demonstrates a counterintuitive result: **even when individuals have only a mild preference for living near similar people, the population self-organizes into highly segregated clusters.**

This is a textbook example of **emergence** — complex macro-level patterns arising from simple micro-level rules.

---

## The Rules (How It Works)

### Setup
- A 20×20 grid is populated with agents at a configurable **density** (default: 80% of cells filled).
- Each agent belongs to one of **two types** (Type 0 = majority, Type 1 = minority).
- The fraction of minority agents is controlled by `minority_pc` (default: 30%).

### Agent Behavior (Each Step)
1. **Evaluate Happiness**: The agent counts its neighbors within `radius` cells (default: 1, meaning the 8 surrounding squares).
   - If `same_type_neighbors / total_neighbors >= homophily_threshold`, the agent is **happy**.
   - Otherwise, the agent is **unhappy**.
2. **Move if Unhappy**: Unhappy agents relocate to a **random empty cell** on the grid.

### Termination
The simulation stops when **all agents are happy** (i.e., every agent has enough same-type neighbors).

### The Surprising Result
Even with a homophily threshold of just 30–40% (agents are perfectly fine being a minority), the grid evolves into **highly segregated clusters**. Small individual preferences amplify into large-scale collective segregation.

---

## Architecture

```
agents.py  →  SchellingAgent (CellAgent)
                ├── evaluate_happiness()  — check neighbors, set happy/unhappy
                └── step()               — move to random empty cell if unhappy

model.py   →  Schelling (Model)
                ├── __init__()           — create grid, place agents, setup DataCollector
                └── step()              — reset counter → shuffle agents → evaluate → collect data

run.py     →  Headless runner
                ├── run_single_simulation()  — run one experiment, print progress
                ├── plot_results()           — matplotlib charts (happy count + % happy)
                └── run_parameter_sweep()    — vary homophily from 0.1 to 0.8

app.py     →  SolaraViz interactive dashboard (browser-based)
```

### Key Design Decision: Two-Pass Activation
We separate `evaluate_happiness()` from `step()` to prevent **order-dependent bugs**:
- **First pass**: `self.agents.do("evaluate_happiness")` — ALL agents evaluate before anyone moves.
- **Second pass**: `self.agents.shuffle_do("step")` — unhappy agents move in random order.

If we combined evaluation and movement in one pass, early movers would change the neighborhood for late evaluators, producing biased results.

---

## Mesa Features Used

| Mesa Component | What It Does | Where Used |
|---|---|---|
| `mesa.Model` | Top-level simulation manager | `model.py` |
| `CellAgent` | Agent that lives on a grid cell | `agents.py` |
| `OrthogonalMooreGrid` | 2D grid with 8-neighbor connectivity | `model.py` |
| `DataCollector` | Automatically records metrics each step | `model.py` |
| `AgentSet.shuffle_do()` | Random activation order | `model.py` |
| `AgentSet.do()` | Sequential evaluation pass | `model.py` |
| `SolaraViz` | Interactive browser dashboard | `app.py` |
| `SpaceRenderer` | Renders agents on the grid | `app.py` |
| `make_plot_component` | Creates live line charts | `app.py` |
| `Slider` | Interactive parameter controls | `app.py` |

---

## How to Run

### Prerequisites
```bash
pip install "mesa[rec]" matplotlib pandas
```

### Headless simulation (generates plots)
```bash
cd models/schelling_segregation
python run.py
```
This runs a single simulation + parameter sweep and generates `results.png` and `parameter_sweep.png`.

### Interactive dashboard
```bash
cd models/schelling_segregation
solara run app.py
```
This opens a browser with sliders for density, minority fraction, and homophily threshold.

---

## What I Learned

### Mesa's Architecture
- **Model/Agent separation**: Mesa cleanly separates the "manager" (Model) from the "individuals" (Agent). The Model creates agents, manages the grid, and orchestrates each step. Agents contain their own behavior logic.
- **Grid systems**: `OrthogonalMooreGrid` provides 8-directional neighborhood queries. The `CellAgent` class makes placement as simple as `self.cell = cell`.
- **Data collection**: `DataCollector` eliminates boilerplate — declare what to track, and Mesa records it automatically.
- **AgentSet operations**: `shuffle_do("step")` activates agents in random order with one line. This is cleaner than manually iterating and shuffling.

### Agent-Based Modeling Concepts
- **Emergence**: Simple rules (move if < 40% similar neighbors) → complex outcomes (full segregation). You cannot predict the outcome just by reading the rules.
- **Activation order matters**: Random shuffling (`shuffle_do`) vs. sequential (`do`) can produce different results.
- **Parameter sensitivity**: The parameter sweep shows that homophily has a **nonlinear** effect on convergence speed. Small threshold changes can dramatically alter outcomes.

### What Was Challenging
- Understanding `CellAgent` vs `mesa.Agent` — the discrete space system is the modern way, but older tutorials still reference `mesa.space`.
- Getting `AgentPortrayalStyle` correct — the API changed significantly in Mesa 3.x.
- Separating "evaluate" from "step" to avoid order-dependent bugs.

---

## Files

| File | Description |
|---|---|
| `agents.py` | `SchellingAgent` — agent behavior (evaluate + move) |
| `model.py` | `Schelling` — grid, agents, data collection, stepping |
| `run.py` | Headless runner with plotting and parameter sweep |
| `app.py` | Interactive Solara dashboard |
| `README.md` | This file |

---

## Further Reading

- **Schelling's original paper**: [Dynamic Models of Segregation (1971)](https://www.stat.berkeley.edu/~aldous/157/Papers/Schelling_Seg_Models.pdf)
- **Interactive explanation**: [Parable of the Polygons](http://ncase.me/polygons/) by Vi Hart & Nicky Case
- **Mesa documentation**: [mesa.readthedocs.io](https://mesa.readthedocs.io/)
