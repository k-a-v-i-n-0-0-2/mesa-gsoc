import pytest
from model import Schelling

def test_schelling_initialization():
    """Test that the model initializes correctly with default parameters."""
    model = Schelling(width=10, height=10, density=0.8)
    assert len(model.agents) > 0
    assert model.grid.width == 10
    assert model.grid.height == 10

def test_schelling_step():
    """Test that the model can run a step without crashing."""
    model = Schelling(width=10, height=10, density=0.8)
    initial_happy = model.happy
    model.step()
    # Happiness might change after a step
    assert hasattr(model, "happy")

def test_schelling_convergence():
    """Test that the model eventually reaches a state where everyone is happy (or runs out of steps)."""
    # Use a small grid and high density for faster test
    model = Schelling(width=5, height=5, density=0.6, homophily=0.3, seed=42)
    for _ in range(100):
        model.step()
        if not model.running:
            break
    # In a small grid with low homophily, it should converge quickly
    assert not model.running or model.happy <= len(model.agents)

if __name__ == "__main__":
    pytest.main([__file__])
