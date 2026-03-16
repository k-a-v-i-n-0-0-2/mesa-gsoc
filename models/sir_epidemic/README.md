# SIR Epidemic Model 🦠

## What the Model Does

The **SIR model** is a classic mathematical tool in epidemiology to understand how diseases spread through a population. It divides people into three categories:
- **S (Susceptible)**: Healthy individuals who can catch the disease.
- **I (Infected)**: Individuals who have the disease and can spread it to others.
- **R (Recovered)**: Individuals who have recovered and gain permanent immunity.

In this agent-based version, we simulate individuals on a 2D grid where infection spreads through contact (proximity).

---

## How it Works

### 1. The Agents (`InfectiousAgent`)
- Each agent has a state (S, I, or R).
- **Susceptible agents** check their immediate neighbors (8 surrounding cells). If any neighbors are infected, the susceptible agent has a probability (`transmission_prob`) of becoming infected.
- **Infected agents** stay sick for a fixed number of steps (`recovery_time`). After this time, they automatically transition to the Recovered state.
- **Recovered agents** do nothing—they are effectively removed from the transmission chain.

### 2. The Model (`SIRModel`)
- Manages a grid of agents.
- Initializes the simulation with a small number of "Patient Zeros" (`initial_infected`).
- Tracks the population counts over time using Mesa's `DataCollector`.
- The simulation ends when there are no more infected individuals left.

---

## What I Learned

- **Stochastic Processes**: Unlike the Schelling model, which is often deterministic in its movement, the SIR model relies heavily on probabilities. I learned how to use `self.random.random()` within Mesa to handle infection chances.
- **Data Visualization**: Implementing multiple line charts in `SolaraViz` to track the classic SIR curve (where 'I' peaks and then falls).
- **States and Enums**: Using Python's `enum.IntEnum` to manage agent states cleanly.

---

## How to Run

### Headless (Static Plot)
```bash
python run.py
```

### Interactive Dashboard
```bash
solara run app.py
```

---

## Key Files
- `agents.py`: Individual infectious logic.
- `model.py`: Environment and population management.
- `run.py`: Script to generate the epidemiology curve.
- `app.py`: Interactive dashboard for parameter tweaking.
