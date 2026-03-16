"""
Schelling Segregation Model - Headless Runner
==============================================
This script runs the Schelling model without visualization,
collects data, and produces summary statistics and plots.

Usage:
    python run.py

This is useful for:
    - Understanding the model behavior through data
    - Running experiments and parameter sweeps
    - Generating plots for your README / learning space
"""

import matplotlib.pyplot as plt
import pandas as pd

from model import Schelling


def run_single_simulation(
    width: int = 20,
    height: int = 20,
    density: float = 0.8,
    minority_pc: float = 0.3,
    homophily: float = 0.4,
    max_steps: int = 100,
    seed: int = 42,
) -> tuple[Schelling, pd.DataFrame]:
    """Run the Schelling model once and return the model + collected data.

    Args:
        width: Grid width.
        height: Grid height.
        density: Fraction of cells initially occupied.
        minority_pc: Fraction of agents that are type 1 (minority).
        homophily: Similarity threshold for agent happiness.
        max_steps: Maximum number of steps to run.
        seed: Random seed for reproducibility.

    Returns:
        A tuple of (model_instance, model_level_dataframe).
    """
    print(f"Running Schelling model: {width}x{height} grid, "
          f"density={density}, minority={minority_pc}, homophily={homophily}")
    print("-" * 60)

    # Create the model
    model = Schelling(
        width=width,
        height=height,
        density=density,
        minority_pc=minority_pc,
        homophily=homophily,
        seed=seed,
    )

    # Run the model step by step
    for step_num in range(max_steps):
        model.step()

        # Print progress every 10 steps
        if (step_num + 1) % 10 == 0:
            print(f"  Step {step_num + 1:3d}: "
                  f"{model.happy}/{len(model.agents)} agents happy "
                  f"({model.happy / len(model.agents) * 100:.1f}%)")

        # Stop if everyone is happy
        if not model.running:
            print(f"\n  ✓ All agents happy after {step_num + 1} steps!")
            break
    else:
        print(f"\n  ⚠ Reached max steps ({max_steps}) — "
              f"not all agents are happy yet.")

    # Get the collected data as a DataFrame
    model_data = model.datacollector.get_model_dataframe()
    return model, model_data


def plot_results(model_data: pd.DataFrame, save_path: str = "results.png"):
    """Create a plot showing how happiness evolves over time.

    Args:
        model_data: DataFrame from DataCollector.get_model_dataframe().
        save_path: Where to save the plot image.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Number of happy agents over time
    axes[0].plot(model_data.index, model_data["happy"],
                 color="#2ecc71", linewidth=2, label="Happy agents")
    axes[0].axhline(y=model_data["population"].iloc[0],
                    color="#e74c3c", linestyle="--",
                    linewidth=1, label="Total agents")
    axes[0].set_xlabel("Step")
    axes[0].set_ylabel("Number of Agents")
    axes[0].set_title("Happy Agents Over Time")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Percentage happy over time
    axes[1].plot(model_data.index, model_data["pct_happy"],
                 color="#3498db", linewidth=2)
    axes[1].axhline(y=100, color="#e74c3c", linestyle="--",
                    linewidth=1, alpha=0.5)
    axes[1].set_xlabel("Step")
    axes[1].set_ylabel("% Happy")
    axes[1].set_title("Percentage of Happy Agents Over Time")
    axes[1].set_ylim(0, 105)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"\n  📊 Plot saved to: {save_path}")


def run_parameter_sweep():
    """Run the model with different homophily values to see the effect.

    This demonstrates how even small changes in homophily preference
    can dramatically affect segregation outcomes.
    """
    print("\n" + "=" * 60)
    print("PARAMETER SWEEP: Varying Homophily")
    print("=" * 60)

    homophily_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    results = []

    for h in homophily_values:
        model = Schelling(
            width=20, height=20, density=0.8,
            minority_pc=0.3, homophily=h, seed=42,
        )

        # Run for up to 200 steps
        steps_taken = 0
        for step_num in range(200):
            model.step()
            steps_taken = step_num + 1
            if not model.running:
                break

        pct_happy = (model.happy / len(model.agents)) * 100
        results.append({
            "homophily": h,
            "steps_to_converge": steps_taken,
            "pct_happy": pct_happy,
            "converged": not model.running or model.happy == len(model.agents),
        })
        print(f"  Homophily={h:.1f} → "
              f"Steps={steps_taken:3d}, "
              f"Happy={pct_happy:.1f}%, "
              f"Converged={'Yes' if results[-1]['converged'] else 'No'}")

    # Plot the sweep results
    df = pd.DataFrame(results)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["homophily"], df["steps_to_converge"],
           color="#9b59b6", alpha=0.8, width=0.08)
    ax.set_xlabel("Homophily Threshold")
    ax.set_ylabel("Steps to Converge")
    ax.set_title("Effect of Homophily on Convergence Speed")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig("parameter_sweep.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("\n  📊 Parameter sweep plot saved to: parameter_sweep.png")


# ──────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("SCHELLING SEGREGATION MODEL")
    print("=" * 60)
    print()

    # Run a single simulation with default parameters
    model, data = run_single_simulation()
    print()
    print("Model Data (last 5 steps):")
    print(data.tail())
    plot_results(data)

    # Run a parameter sweep
    run_parameter_sweep()

    print("\n" + "=" * 60)
    print("Done! Check the generated plots.")
    print("=" * 60)
