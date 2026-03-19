# SIR Epidemic Model 🦠

## What the Model Does

The **SIR model** (Kermack & McKendrick, 1927) is a foundational model in mathematical epidemiology. It tracks how a disease spreads through a population by dividing individuals into three categories:

- **S (Susceptible)**: Healthy individuals who can catch the disease
- **I (Infected)**: Individuals who have the disease and can transmit it
- **R (Recovered)**: Individuals who have recovered and gained permanent immunity

In this agent-based version, we simulate the SIR dynamics on a 2D spatial grid where infection spreads through **proximity** (contact with infected neighbors), adding a realistic spatial dimension that the traditional ODE-based SIR model lacks.

---

## The Rules (How It Works)

### Setup
- A 30×30 grid is **fully populated** (one agent per cell = 900 agents).
- All agents start as **Susceptible** except for a small number of **"Patient Zeros"** (`initial_infected`, default: 2–5).

### Agent Behavior (Each Step)

**If Susceptible**:
1. Check all 8 neighbors (Moore neighborhood, radius=1).
2. Count how many neighbors are Infected (`N`).
3. Calculate infection probability using compound formula:  
   **`P(infection) = 1 - (1 - transmission_prob)^N`**  
   This means more infected neighbors = higher chance of catching the disease.
4. Roll a random number. If `random() < P`, the agent becomes **Infected**.

**If Infected**:
1. Increment `infection_duration` by 1.
2. If `infection_duration >= recovery_time`, transition to **Recovered**.

**If Recovered**:
- Do nothing. The agent has permanent immunity and cannot be re-infected.

### Termination
The simulation stops when the **infected count reaches zero** — the epidemic has burned out.

### The Expected Result
The model produces the classic **SIR curve**:
- **S** (blue) starts high and drops as people get infected
- **I** (red) rises to a peak, then falls as people recover
- **R** (green) steadily rises as the population gains immunity

---

## Architecture

```
agents.py  →  State (IntEnum: SUSCEPTIBLE=0, INFECTED=1, RECOVERED=2)
               InfectiousAgent (CellAgent)
                ├── check_infection()    — susceptible → check neighbors → maybe get infected
                ├── update_infection()   — infected → track duration → maybe recover
                └── step()              — dispatch based on current state

model.py   →  SIRModel (Model)
                ├── __init__()           — create grid, place agents, infect Patient Zeros
                ├── count_state()        — helper to count S, I, or R agents
                └── step()              — collect data → shuffle agents → check termination

run.py     →  Headless runner
                └── run_simulation()     — run until burnout, plot SIR curves

app.py     →  SolaraViz interactive dashboard
```

### Key Design Decision: Compound Probability
Instead of a simple flat infection chance per infected neighbor, we use:

```
P = 1 - (1 - p)^N
```

This models **independent exposure events**. If `p = 0.1` and you have 3 infected neighbors:
- `P = 1 - (1 - 0.1)^3 = 1 - 0.729 = 0.271` (27.1% chance)

This is more realistic than `P = 3 × 0.1 = 30%` (which could exceed 100% with many neighbors).

---

## Mesa Features Used

| Mesa Component | What It Does | Where Used |
|---|---|---|
| `mesa.Model` | Top-level simulation manager | `model.py` |
| `CellAgent` | Agent that lives on a grid cell | `agents.py` |
| `OrthogonalMooreGrid` | 2D grid with 8-neighbor connectivity | `model.py` |
| `DataCollector` | Records S, I, R counts each step | `model.py` |
| `AgentSet.shuffle_do()` | Random activation order | `model.py` |
| `SolaraViz` | Interactive browser dashboard | `app.py` |
| `make_plot_component` | Real-time SIR curve chart | `app.py` |
| `Slider` | Controls for transmission_prob, recovery_time | `app.py` |

---

## How to Run

### Prerequisites
```bash
pip install "mesa[rec]" matplotlib pandas
```

### Headless simulation (generates SIR curve plot)
```bash
cd models/sir_epidemic
python run.py
```
This runs the simulation until the epidemic burns out and saves `sir_results.png`.

### Interactive dashboard
```bash
cd models/sir_epidemic
solara run app.py
```
This opens a browser with sliders for initial infected count, transmission probability, and recovery time.

---

## What I Learned

### Stochastic vs Deterministic Modeling
Unlike the Schelling model (where movement is deterministic — unhappy agents always move), the SIR model is fundamentally **probabilistic**. Infection depends on `self.model.random.random()`, meaning every run can produce different outcomes even with the same parameters. This taught me:
- Why **random seeds** matter for reproducibility (`seed=42`)
- How to think about simulations statistically (run multiple times, analyze distributions)

### State Management with Enums
Using `enum.IntEnum` for agent states provides:
- **Type safety**: Can't accidentally assign `state = 3` (not a valid SIR state)
- **Readability**: `State.INFECTED` is clearer than `state == 1`
- **Performance**: IntEnums are integers under the hood, so comparisons are fast

### Termination Conditions
The Schelling model uses `self.running = self.happy < len(self.agents)` (stop when everyone is happy). The SIR model uses `self.running = False` when `count_state(INFECTED) == 0` (stop when the epidemic burns out). This taught me that **different models need different stopping logic**.

### Spatial vs Non-Spatial SIR
Traditional SIR models use **ordinary differential equations** (ODEs) that assume "well-mixed" populations. Our grid-based version adds **spatial structure**, which produces:
- **Wavefront propagation**: Infection spreads outward from Patient Zero like a wave
- **Spatial clustering**: Recovered agents form "immune barriers" that slow spread
- **Different dynamics**: The peak is lower and wider compared to ODE-based SIR

---

## Files

| File | Description |
|---|---|
| `agents.py` | `State` enum + `InfectiousAgent` — infection and recovery logic |
| `model.py` | `SIRModel` — grid, Patient Zero initialization, data collection |
| `run.py` | Headless runner that generates SIR curve plot |
| `app.py` | Interactive Solara dashboard with parameter sliders |
| `README.md` | This file |

---

## Further Reading

- **Original SIR paper**: Kermack, W.O. & McKendrick, A.G. (1927). "A Contribution to the Mathematical Theory of Epidemics." *Proceedings of the Royal Society of London*.
- **Interactive SIR explainer**: [Epidemic Calculator](https://gabgoh.github.io/COVID/index.html)
- **Mesa documentation**: [mesa.readthedocs.io](https://mesa.readthedocs.io/)
- **Spatial SIR models**: Riley, S. (2007). "Large-Scale Spatial-Transmission Models of Infectious Disease." *Science*.
