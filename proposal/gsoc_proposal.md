# Google Summer of Code 2026 — Proposal

## Revitalizing the Mesa Example Library: Porting Classic ABM Simulations to Modern Solara-Based Architectures

**Organization**: Mesa — Agent-Based Modeling in Python  
**Project Size**: Medium (~175 hours)  
**Contributor**: [Your Name]  
**GitHub**: [Your GitHub URL]  
**Email**: [Your Email]  
**Timezone**: IST (UTC+5:30)

---

## 1. Abstract

Mesa is the leading open-source Python framework for agent-based modeling, used by researchers worldwide to simulate complex systems from urban segregation to pandemic spread. With the release of Mesa 3.0+, the framework has undergone a major architectural overhaul — introducing the `AgentSet` API, the `discrete_space` module, and reactive Solara-based visualization. However, the companion `mesa-examples` repository still contains models built with deprecated APIs (`mesa.time.RandomActivation`, `mesa.space.SingleGrid`, `ModularServer`), creating a confusing experience for new users.

**This project will modernize the Mesa example library** by porting 10+ classic agent-based models to the Mesa 3.0+ API, implementing interactive SolaraViz dashboards for each, and establishing automated CI/CD testing to prevent future "example rot."

---

## 2. The Problem

### 2.1 Why This Matters
The examples repository is the **front door** of Mesa. When a researcher evaluates whether to adopt Mesa, they:
1. Read the README (30 seconds)
2. Run an example (5 minutes)
3. Decide to adopt or abandon (immediate)

If the example they run uses deprecated syntax, throws warnings, or has a broken visualizer, Mesa loses that user permanently. Currently:
- Multiple examples still use `mesa.time.RandomActivation` (deprecated in favor of `AgentSet`)
- Several models reference `mesa.space.SingleGrid` (replaced by `mesa.discrete_space`)
- The old Tornado-based `ModularServer` visualization is still present in many examples
- Some examples lack interactive parameter controls

### 2.2 The Opportunity
A single, focused effort can transform the examples from a liability into Mesa's greatest asset — a gallery of polished, interactive, educational simulations that showcase the framework's full power.

---

## 3. Technical Approach

### 3.1 The Modernization Pipeline
For each model, I will follow a systematic four-step process:

**Step 1 — API Migration**
```diff
# OLD (Legacy)
- from mesa.time import RandomActivation
- self.schedule = RandomActivation(self)
- self.schedule.step()

# NEW (Mesa 3.0+)
+ # No scheduler import needed — model.agents is an AgentSet
+ self.agents.shuffle_do("step")
```

**Step 2 — Space Migration**
```diff
# OLD (Legacy)
- from mesa.space import SingleGrid
- self.grid = SingleGrid(width, height, torus=True)
- self.grid.place_agent(agent, (x, y))

# NEW (Mesa 3.0+)
+ from mesa.discrete_space import OrthogonalMooreGrid, CellAgent
+ self.grid = OrthogonalMooreGrid((width, height), capacity=1, torus=True)
+ agent.cell = cell  # placement via property assignment
```

**Step 3 — Visualization Upgrade**
```diff
# OLD (Legacy Tornado)
- from mesa.visualization.modules import CanvasGrid
- server = ModularServer(MyModel, [grid], "Model")
- server.launch()

# NEW (Solara)
+ from mesa.visualization import SolaraViz, Slider, make_plot_component
+ page = SolaraViz(model, components=[...], model_params={...})
```

**Step 4 — Testing & Documentation**
- Write a `pytest` test that verifies the model converges to known mathematical results
- Write a comprehensive README documenting the science, the code, and what users can learn

### 3.2 Code Quality Standards
Every modernized example will follow this structure:
```
model_name/
├── agents.py       # Agent classes with full docstrings
├── model.py        # Model class with commented sections
├── run.py          # Headless runner for data analysis
├── app.py          # SolaraViz interactive dashboard
├── test_model.py   # Pytest verification suite
└── README.md       # Educational documentation
```

---

## 4. Deliverables & Timeline

### Phase 1: Foundation (Weeks 1–2)
| Deliverable | Detail |
|---|---|
| Example Audit | Catalog all 25+ existing examples; classify as "working," "broken," or "deprecated" |
| Gold Template | Create a reference template that all future examples must follow |
| CI/CD Setup | GitHub Actions workflow that runs every example on each PR |

### Phase 2: Core Models (Weeks 3–6)
| Week | Model | Key Mesa Feature Demonstrated |
|---|---|---|
| 3 | Wolf-Sheep Predation | Multi-agent types, agent removal/creation during simulation |
| 4 | Forest Fire | Cellular automata, grid-wide state changes |
| 5 | Boltzmann Wealth | Economic ABM, wealth distribution histograms |
| 6 | Conway's Game of Life | Pure cellular automata, PropertyLayer usage |

### Phase 3: Advanced Models (Weeks 7–9)
| Week | Model | Key Mesa Feature Demonstrated |
|---|---|---|
| 7 | Sugarscape | Environmental resources, agent metabolism, multi-layer grids |
| 8 | Epstein Civil Violence | Social dynamics, rule-based agent behavior |
| 9 | Flockers (Boids) | Continuous space, velocity-based movement |

### Phase 4: Gallery & Documentation (Weeks 10–12)
| Deliverable | Detail |
|---|---|
| Example Gallery | A browsable Solara multi-page app showcasing all models |
| Contribution Guide | A "How to Add a New Example" guide for future contributors |
| Final Review | Code review with mentors, documentation polish, final PR |

---

## 5. Evidence of Technical Competence

During the pre-application period, I built a dedicated Mesa Learning Space with two fully functional, modern simulations:

### 5.1 Schelling Segregation Model
- **What it proves**: I can implement spatial agent logic using `OrthogonalMooreGrid`, `CellAgent`, and the two-pass activation pattern (`evaluate_happiness` → `step`).
- **Mesa features used**: `Model`, `CellAgent`, `OrthogonalMooreGrid`, `DataCollector` (with lambda reporters), `AgentSet.shuffle_do()`, `SolaraViz`, `SpaceRenderer`, `Slider`.
- **Key design decision**: Separating evaluation from movement prevents order-dependent bugs — a subtlety that shows I understand ABM best practices.

### 5.2 SIR Epidemic Model
- **What it proves**: I can implement stochastic transitions, state management (via `enum.IntEnum`), and multi-variate data collection.
- **Infection logic**: `P(infection) = 1 - (1 - p)^N` where `p` is transmission probability and `N` is number of infected neighbors. This is the standard compound probability formula.
- **Key design decision**: The model uses a "burnout condition" (`self.running = False` when `infected_count == 0`) to automatically terminate.

### 5.3 Repository
All code is available at: **[Your GitHub Fork URL]**

---

## 6. About Me

### 6.1 Background
I am a [year] computer science student at [university]. My coursework includes [relevant courses], and I have experience with [relevant technologies].

### 6.2 Why This Project
The quality of a framework's examples directly determines its adoption rate. I have personally experienced the frustration of running a "tutorial" example that uses deprecated syntax — it erodes trust in the entire framework. I want to ensure that every new Mesa user has a world-class onboarding experience.

### 6.3 Why Mesa
- Python-native: Leverages the full scientific Python ecosystem (NumPy, Pandas, Matplotlib)
- Modern architecture: The Mesa 3.0+ API (`AgentSet`, `discrete_space`, `SolaraViz`) is elegant and powerful
- Real impact: Mesa is used by researchers studying urban planning, pandemic response, and financial markets

### 6.4 Post-GSoC Commitment
I plan to remain an active Mesa contributor after GSoC, focusing on:
- Reviewing community-submitted examples
- Maintaining the CI/CD pipeline for the examples repository
- Expanding the gallery with new model categories (network models, GIS-based models)

---

## 7. Communication Plan

| Channel | Frequency |
|---|---|
| GitHub PRs | Weekly — one PR per completed model |
| Mentor Check-in | Bi-weekly — 30-minute video call |
| Mesa Discord | Daily — available for async discussions |
| Blog Posts | Monthly — documenting progress and lessons learned |

---

## 8. Availability

- **Available hours per week**: 20–25 hours
- **Potential conflicts**: [List any exams, vacations, or other commitments]
- **Start date flexibility**: Available from the official GSoC start date

---

## References

- [Mesa Documentation](https://mesa.readthedocs.io/)
- [Mesa GitHub](https://github.com/projectmesa/mesa)
- [Mesa Examples Repository](https://github.com/projectmesa/mesa-examples)
- [GSoC Learning Space Template](https://github.com/mesa/GSoC-learning-space)
- Schelling, T.C. (1971). "Dynamic Models of Segregation." *Journal of Mathematical Sociology*.
- Kermack, W.O. & McKendrick, A.G. (1927). "A Contribution to the Mathematical Theory of Epidemics." *Proceedings of the Royal Society*.
