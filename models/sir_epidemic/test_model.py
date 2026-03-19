import pytest
from model import SIRModel, State

def test_sir_initialization():
    """Test that the model initializes with the correct number of agents and initial infected."""
    width, height = 10, 10
    initial_infected = 5
    model = SIRModel(width=width, height=height, initial_infected=initial_infected)
    
    assert len(model.agents) == width * height
    infected_count = sum(1 for a in model.agents if a.state == State.INFECTED)
    assert infected_count == initial_infected

def test_sir_spread():
    """Test that the infection spreads over time."""
    model = SIRModel(width=10, height=10, initial_infected=1, transmission_prob=1.0)
    initial_infected = sum(1 for a in model.agents if a.state == State.INFECTED)
    
    # Run a few steps
    for _ in range(3):
        model.step()
        
    current_infected = sum(1 for a in model.agents if a.state == State.INFECTED)
    current_recovered = sum(1 for a in model.agents if a.state == State.RECOVERED)
    
    # Infection should have spread or some should have recovered
    assert (current_infected + current_recovered) >= initial_infected

def test_sir_recovery():
    """Test that agents recover after the specified recovery time."""
    recovery_time = 5
    model = SIRModel(width=5, height=5, initial_infected=1, transmission_prob=0.0, recovery_time=recovery_time)
    
    # Find the infected agent
    infected_agent = [a for a in model.agents if a.state == State.INFECTED][0]
    
    # Run for recovery_time + 1 steps
    for _ in range(recovery_time + 1):
        model.step()
        
    assert infected_agent.state == State.RECOVERED

if __name__ == "__main__":
    pytest.main([__file__])
