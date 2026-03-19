# My Mesa GSoC Learning Space 🚀

Welcome to my GSoC learning space for the [Mesa](https://github.com/projectmesa/mesa) agent-based modeling framework.

## About This Repo

This repository documents my journey learning Mesa — the Python library for agent-based modeling. I'm building models, studying the framework's architecture, and preparing to contribute to Mesa through Google Summer of Code 2026.

**My GSoC Focus**: [Mesa Examples Revival](proposal/gsoc_proposal.md) — Porting classic ABM simulations to the modern Mesa 3.0+ API with interactive Solara dashboards.

---

## Repository Structure

```
├── motivation.md                          # Why I want to contribute to Mesa
├── proposal/
│   └── gsoc_proposal.md                   # My full GSoC 2026 proposal
├── notes/
│   └── mesa_architecture_guide.md         # Deep-dive into Mesa 3.0+ internals
├── models/
│   ├── schelling_segregation/             # Model 1: Social Dynamics
│   │   ├── agents.py                      # SchellingAgent (CellAgent)
│   │   ├── model.py                       # Schelling (Model)
│   │   ├── run.py                         # Headless runner + parameter sweep
│   │   ├── app.py                         # SolaraViz interactive dashboard
│   │   └── README.md                      # Full documentation
│   └── sir_epidemic/                      # Model 2: Biological Dynamics
│       ├── agents.py                      # InfectiousAgent (S/I/R states)
│       ├── model.py                       # SIRModel with DataCollector
│       ├── run.py                         # Headless runner + SIR curves
│       ├── app.py                         # SolaraViz interactive dashboard
│       └── README.md                      # Full documentation
└── README.md                              # This file
```

---

## Models Built

### 1. [Schelling Segregation Model](models/schelling_segregation/) 🏘️
**Status**: ✅ Complete

Demonstrates how **mild individual preferences** for similar neighbors lead to **extreme collective segregation**. A cornerstone of agent-based social science.

| Feature | Detail |
|---|---|
| **Scientific basis** | Schelling (1971) — Dynamic Models of Segregation |
| **Grid** | `OrthogonalMooreGrid` (20×20, 8-neighbor, torus) |
| **Agent logic** | Two-pass: evaluate happiness → move if unhappy |
| **Activation** | `AgentSet.shuffle_do()` — random order each step |
| **Data collected** | Happy count, % happy, population |
| **Visualization** | Solara dashboard with density/homophily sliders |

---

### 2. [SIR Epidemic Model](models/sir_epidemic/) 🦠
**Status**: ✅ Complete

Simulates **disease spread** through a population using the classic **Susceptible → Infected → Recovered** framework. Demonstrates stochastic modeling and multi-variate data collection.

| Feature | Detail |
|---|---|
| **Scientific basis** | Kermack & McKendrick (1927) — SIR Epidemiological Model |
| **Grid** | `OrthogonalMooreGrid` (30×30, 8-neighbor) |
| **Agent logic** | Probabilistic infection: `P = 1 - (1-p)^N` |
| **State management** | Python `enum.IntEnum` (SUSCEPTIBLE, INFECTED, RECOVERED) |
| **Data collected** | S, I, R counts per step |
| **Visualization** | Solara dashboard with transmission/recovery sliders |

---

## Mesa Features Demonstrated

| Mesa 3.0+ Component | Where Used | Purpose |
|---|---|---|
| `mesa.Model` | Both models | Top-level simulation manager |
| `CellAgent` | Both models | Grid-based agent with `self.cell` |
| `OrthogonalMooreGrid` | Both models | 2D grid with 8-neighbor connectivity |
| `DataCollector` | Both models | Automatic per-step metric recording |
| `AgentSet.shuffle_do()` | Both models | Random activation order |
| `AgentSet.do()` | Schelling | Sequential evaluation pass |
| `SolaraViz` | Both models | Interactive browser dashboard |
| `SpaceRenderer` | Schelling | Grid rendering with agent portrayal |
| `make_plot_component` | Both models | Real-time line charts |
| `Slider` | Both models | Interactive parameter controls |

---

## What I'm Learning

- **Mesa 3.0+ architecture**: The modern `discrete_space` system, `AgentSet` API, and Solara-based visualization
- **ABM fundamentals**: Emergence, activation order effects, stochastic transitions, parameter sensitivity
- **Open source workflow**: Clean git history, documentation-driven development, modular code
- **Scientific modeling**: Translating mathematical models (Schelling 1971, SIR 1927) into code

---

## Getting Started

```bash
# Install Mesa with visualization support
pip install "mesa[rec]" matplotlib pandas

# Run the Schelling model (headless)
cd models/schelling_segregation
python run.py

# Run the SIR model (headless)
cd models/sir_epidemic
python run.py

# Run any interactive dashboard
solara run app.py
```

---

## Key Documents

| Document | Purpose |
|---|---|
| [motivation.md](motivation.md) | Why I want to contribute to Mesa |
| [gsoc_proposal.md](proposal/gsoc_proposal.md) | My full GSoC 2026 proposal |
| [mesa_architecture_guide.md](notes/mesa_architecture_guide.md) | Deep-dive into Mesa 3.0+ internals |

---

## Resources

- [Mesa Documentation](https://mesa.readthedocs.io/)
- [Mesa GitHub](https://github.com/projectmesa/mesa)
- [Mesa Examples](https://github.com/projectmesa/mesa-examples)
- [GSoC Learning Space Template](https://github.com/mesa/GSoC-learning-space)
- [Mesa Contributing Guide](https://github.com/mesa/mesa/blob/main/CONTRIBUTING.md)
