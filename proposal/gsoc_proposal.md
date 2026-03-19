# Google Summer of Code 2026 — Proposal 🚀

## Revitalizing the Mesa Example Library: Porting Classic ABM Simulations to Modern Solara-Based Architectures

**Organization**: Mesa — Agent-Based Modeling in Python  
**Project Size**: Medium (~175 hours)  
**Contributor**: Kavin M  
**GitHub**: [k-a-v-i-n-0-0-2](https://github.com/k-a-v-i-n-0-0-2)  
**Email**: kavinm.cse2023@dscet.ac.in  
**Timezone**: Indian Standard Time (IST / GMT +5:30)

---

## 1. About Me

### 1.1 Goals and Objectives
My interest in programming started during school and has deepened through college as I explore simulation, data science, and complex systems. I discovered Mesa — Python's leading agent-based modeling library — and was drawn to its Python-native architecture and active community.

**What I hope to learn during GSoC:**
- **Mesa 3.0+ internals**: Mastering the `AgentSet` API, `discrete_space`, and `SolaraViz` reactive dashboards.
- **Modernization patterns**: Systematically auditing and porting legacy codebases without breaking behavioral consistency.
- **CI/CD for Open Source**: Implementing robust automated testing (GitHub Actions) to prevent "example rot."
- **ABM fundamentals**: Deepening my understanding of emergence, activation order effects, and stochastic transitions.

### 1.2 Prior Experience
- **Mesa Learning Space**: Built two complete Mesa 3.0+ models (Schelling and SIR) demonstrating spatial agent logic and stochastic state machines.
- **Data Engineering**: Built multiple data-driven Python applications; comfortable with class hierarchies and modular software design.
- **Open Source**: Familiar with PR-based workflows, code review, and contribution norms.

---

## 2. The Problem

### 2.1 The "Front Door" Problem
The `mesa-examples` repository is the primary entry point for new users. If a researcher runs an example and finds deprecated syntax (`RandomActivation`, `SingleGrid`) or a broken visualizer (`ModularServer`), it erodes trust in the framework.

### 2.2 Core User Needs
1. **Modern API Consistency**: All examples should use the latest Mesa 3.0+ standards.
2. **Interactive Visualization**: Every model needs a Solara-based dashboard for real-time parameter exploration.
3. **Automated Verification**: A CI/CD pipeline is required to catch breaks introduced by future Mesa releases.
4. **Educational Value**: Examples need consistent documentation (READMEs) explaining both the code and the underlying science.

---

## 3. Proposed Solution

### 3.1 The "Gold Template" Standard
Every modernized model will follow a strict structural standard:
- `agents.py`: Clean agent classes with clear state logic.
- `model.py`: Model definition using `discrete_space` and `DataCollector`.
- `run.py`: Headless runner for automated execution/parameter sweeps.
- `app.py`: Reactive SolaraViz dashboard.
- `test_model.py`: **Pytest-based unit tests** (Demonstrated in this repo).
- `README.md`: Comprehensive documentation.

### 3.2 Automated CI/CD
I will implement a GitHub Actions pipeline (`run_examples.yml`) that:
1. Installs the latest Mesa and dependencies.
2. Executes headless smoke tests for every model.
3. Runs `pytest` on all model test suites.
4. Ensures zero deprecation warnings are present.

---

## 4. Deliverables & Timeline

### Milestone 1: Foundation & Core Models (May 26 – July 14)
- **Example Audit**: Catalog 25+ existing models and classify status.
- **CI/CD Pipeline**: Live automated testing for the examples repository.
- **Phase 1 Models**: Wolf-Sheep Predation, Forest Fire, Boltzmann Wealth, Conway's Game of Life.
- **Contribution Guide**: A `CONTRIBUTING_EXAMPLES.md` defining the Gold Template.

### Milestone 2: Advanced Models & Gallery (July 15 – Sept 15)
- **Phase 2 Models**: Sugarscape, Epstein Civil Violence, Flockers (Boids).
- **Phase 3 Models**: Bank Reserves, Virus on Network, PD Grid.
- **Example Gallery**: A browsable Solara multi-page app to explore all models from one interface.

---

## 5. Evidence of Technical Competence

I have already established this learning space as a **"Proof of Concept"** for the full GSoC project.

### 5.1 Schelling Segregation Model (`models/schelling_segregation/`)
- **Logic**: Separates evaluation from movement (two-pass) to prevent order-dependent bugs.
- **Features**: `OrthogonalMooreGrid`, `AgentSet.shuffle_do()`, `SolaraViz` with `SpaceRenderer`.
- **Testing**: Includes `test_model.py` for initialization and convergence checks.

### 5.2 SIR Epidemic Model (`models/sir_epidemic/`)
- **Logic**: Implements `P = 1 - (1-p)^N` infection probability and auto-termination.
- **Features**: `enum.IntEnum` states, `DataCollector` with multi-variate reporting.
- **Testing**: Includes `test_model.py` for infection spread and recovery timing.

### 5.3 CI/CD Demonstration
This repository already features a working [GitHub Actions workflow](.github/workflows/run_examples.yml) that automatically runs tests for both models on every push — exactly as proposed for the main Mesa examples repo.

---

## 6. Commitment
I can commit **~30 hours/week** während der summer break and **~20 hours/week** when the semester resumes. I aim to provide daily updates via email and participate in bi-weekly mentor syncs.

---

## References
- [Mesa 3.0 Migration Guide](https://mesa.readthedocs.io/stable/migration_guide.html)
- [Mesa Examples Repository](https://github.com/projectmesa/mesa-examples)
- Schelling, T.C. (1971). "Dynamic Models of Segregation."
- Kermack, W.O. & McKendrick, A.G. (1927). "A Contribution to the Mathematical Theory of Epidemics."
