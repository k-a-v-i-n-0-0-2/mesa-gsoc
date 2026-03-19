# Contributing Examples to Mesa 🏘️

To maintain high quality across the library, every modernized example in this repository should follow the **"Gold Template"** standard.

---

## 🏗️ The "Gold Template" Structure

Every model directory MUST follow this structure:

```
model_name/
├── agents.py       # Agent classes with logic (e.g., step(), move(), etc.)
├── model.py        # Main Model class (inheriting from mesa.Model)
├── run.py          # Script for headless model execution (python run.py)
├── app.py          # Solara-based interactive dashboard (solara run app.py)
├── test_model.py   # Unit tests using Pytest for core logic
└── README.md       # Educational documentation (Science & Usage)
```

---

## ✅ Contribution Checklist

Before submitting a PR to modernize an existing model or add a new one, ensure:

1. **No Deprecation Warnings**: The model should not use `mesa.time.RandomActivation` or `mesa.space.SingleGrid`. Use `AgentSet.shuffle_do()` and `mesa.discrete_space`.
2. **Interactive Visualization**: The `app.py` must include parameter sliders (e.g., `Density`, `Transmission Prob`) using `SolaraViz`.
3. **Automated Tests**: At least three `pytest` functions in `test_model.py` that verify:
   - Initialization parameters.
   - At least one step of model logic.
   - A core behavioral expectation (e.g., "infection spreads," "unhappy agents move").
4. **Educational README**: The documentation must explain:
   - The **Scientific Basis** (reference original papers!).
   - A **Parameter Table** with default ranges.
   - **What to Learn**: What emergent phenomena does this model explain?
5. **CI/CD Compliance**: All local `pytest` tests MUST pass.

---

## 🧪 Running Tests Locally

To verify your example before pushing, run:

```bash
cd models/your_model
pytest test_model.py
```

---

## 🛠️ Porting from Legacy (Mesa < 3.0)

### 1. Scheduler
**Legacy**: `self.schedule = RandomActivation(model); self.schedule.step()`  
**Modern**: Use `self.agents.shuffle_do("step")` directly in `model.step()`.

### 2. Grid
**Legacy**: `self.grid = SingleGrid(w, h, torus=True); grid.place_agent(a, pos)`  
**Modern**: Use `OrthogonalMooreGrid` with `capacity=1`. Place agents by setting `agent.cell = cell`.

### 3. Visualization
**Legacy**: `ModularServer(Model, [grid], "Name").launch()`  
**Modern**: Use `SolaraViz(model, components=[...], model_params={...})` in `app.py`.
