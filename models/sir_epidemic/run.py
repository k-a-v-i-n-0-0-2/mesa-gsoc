"""
SIR Epidemic Model - Headless Runner
=====================================
Runs the simulation and plots the S, I, R curves.
"""

import matplotlib.pyplot as plt
import pandas as pd
from model import SIRModel

def run_simulation():
    # Initialize model
    model = SIRModel(
        width=30, 
        height=30, 
        initial_infected=2, 
        transmission_prob=0.15, 
        recovery_time=15
    )
    
    # Run until termination
    print("Starting simulation...")
    while model.running:
        model.step()
    
    # Get results
    df = model.datacollector.get_model_dataframe()
    
    # Plotting
    ax = df.plot(figsize=(10, 6), color={"Susceptible": "blue", "Infected": "red", "Recovered": "green"})
    ax.set_title("SIR Epidemic Progression")
    ax.set_xlabel("Step")
    ax.set_ylabel("Number of Agents")
    plt.grid(True, alpha=0.3)
    plt.savefig("sir_results.png")
    print("Simulation complete. Results saved to 'sir_results.png'.")
    plt.show()

if __name__ == "__main__":
    run_simulation()
