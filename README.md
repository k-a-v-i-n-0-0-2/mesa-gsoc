# My Mesa GSoC Learning Space 🚀

Welcome to my GSoC learning space for the [Mesa](https://github.com/projectmesa/mesa) agent-based modeling framework.

## About This Repo

This repository documents my journey learning Mesa — the Python library for agent-based modeling. I'm building models, studying the framework's architecture, and preparing to contribute to Mesa through Google Summer of Code.

## Repository Structure

```
├── motivation.md                       # Why I want to contribute to Mesa
├── models/
│   ├── schelling_segregation/          # ← My first model
│   │   ├── agents.py                   # Agent class (SchellingAgent)
│   │   ├── model.py                    # Model class (Schelling)
│   │   ├── run.py                      # Headless runner + plots
│   │   ├── app.py                      # Interactive visualization
│   │   └── README.md                   # What I built and learned
│   └── [future models...]
├── reviews/                            # Notes from reviewing others' work
├── notes/                              # Reading notes, design explorations
└── README.md                           # This file
```

## Models Built

### 1. [Schelling Segregation Model](models/schelling_segregation/)
**Status**: ✅ Complete

A classic agent-based model showing how mild individual homophily preferences lead to large-scale segregation. Demonstrates Mesa's core architecture: `Model`, `CellAgent`, `OrthogonalMooreGrid`, `DataCollector`, `AgentSet`, and `SolaraViz`.

**Mesa features used**: Model, CellAgent, OrthogonalMooreGrid, DataCollector, AgentSet (shuffle_do), SolaraViz, SpaceRenderer, Slider

### 2. [SIR Epidemic Model](models/sir_epidemic/)
**Status**: ✅ Complete

A simulation of disease spread through a population on a grid. Demonstrates probabilistic transitions, state management with Enums, and multi-line time-series plotting.

**Mesa features used**: Model, CellAgent, OrthogonalMooreGrid, DataCollector, AgentSet, Enum State Management, SolaraViz

---

## What I'm Learning

- **Mesa 3.x architecture**: The modern discrete_space system, AgentSet API, and Solara-based visualization
- **ABM fundamentals**: Emergence, activation order effects, parameter sensitivity
- **Open source workflow**: Clean git history, documentation-driven development, modular code

## Getting Started

```bash
# Install Mesa
pip install "mesa[rec]" matplotlib pandas

# Run the Schelling model
cd models/schelling_segregation
python run.py

# Or run the interactive dashboard
solara run app.py
```

## Resources

- [Mesa Documentation](https://mesa.readthedocs.io/)
- [Mesa GitHub](https://github.com/projectmesa/mesa)
- [GSoC Learning Space Template](https://github.com/mesa/GSoC-learning-space)
- [Mesa Contributing Guide](https://github.com/mesa/mesa/blob/main/CONTRIBUTING.md)
