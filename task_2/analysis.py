import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def load_timestamps(csv_path: str) -> np.ndarray:
    """
    Load timestamps from a CSV file.

    Args:
        csv_path: Path to the CSV file

    Returns:
        Numpy array of timestamps
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File '{csv_path}' not found")

    df = pd.read_csv(csv_path)
    return df["timestamp"].values


def plot_histogram(
    timestamps, output_dir: str = "plots", output_filename: str = "histogram.png"
) -> str:
    """
    Create histogram plot showing distribution uniformity.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Main histogram
    ax.hist(timestamps, bins=100, edgecolor="black", alpha=0.7, color="steelblue")
    ax.set_xlabel("Timestamp (picoseconds)", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_title("Histogram of Timestamps\n(Uniform distribution check)", fontsize=12)
    ax.grid(True, alpha=0.3)

    # Add expected uniform line
    expected_height = len(timestamps) / 100  # 100 bins
    ax.axhline(
        y=expected_height,
        color="red",
        linestyle="--",
        alpha=0.7,
        label=f"Expected uniform (mean={expected_height:.0f})",
    )
    ax.legend()

    output_path = os.path.join(output_dir, output_filename)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    return output_path


def plot_qq(
    timestamps, output_dir: str = "plots", output_filename: str = "qq_plot.png"
) -> str:
    """
    Create Q-Q (Quantile-Quantile) plot to test for uniform distribution.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5))

    # Generate theoretical quantiles from uniform distribution [0, 1e12)
    n = len(timestamps)
    theoretical_quantiles = np.linspace(0, 1e12, n)

    # Create Q-Q plot
    ax.scatter(
        theoretical_quantiles,
        timestamps,
        alpha=0.5,
        s=1,
        color="darkblue",
        label="Empirical quantiles",
    )

    # Add diagonal reference line (perfect uniform distribution)
    ax.plot(
        [0, 1e12],
        [0, 1e12],
        color="red",
        linestyle="--",
        linewidth=2,
        label="Theoretical uniform",
    )

    ax.set_xlabel("Theoretical Uniform Quantiles (picoseconds)", fontsize=11)
    ax.set_ylabel("Empirical Quantiles (picoseconds)", fontsize=11)
    ax.set_title("Q-Q Plot: Uniform Distribution Test", fontsize=12)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)

    output_path = os.path.join(output_dir, output_filename)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    return output_path


def plot_cdf(
    timestamps, output_dir: str = "plots", output_filename: str = "cdf.png"
) -> str:
    """
    Create CDF (Cumulative Distribution Function) plot.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    cumulative = np.arange(1, len(timestamps) + 1) / len(timestamps)

    ax.plot(
        timestamps,
        cumulative,
        linewidth=2,
        color="darkblue",
    )

    ax.set_xlabel("Timestamp (picoseconds)", fontsize=11)
    ax.set_ylabel("Cumulative Probability", fontsize=11)
    ax.set_title("CDF of Timestamps\n(Monotonic increasing check)", fontsize=12)
    ax.grid(True, alpha=0.3)

    output_path = os.path.join(output_dir, output_filename)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    return output_path


def plot_gap_distribution(
    timestamps, output_dir: str = "plots", output_filename: str = "gap_distribution.png"
) -> str:
    """
    Create gap distribution plot showing spacing between consecutive timestamps.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    gaps = np.diff(timestamps)
    ax.hist(gaps, bins=100, edgecolor="black", alpha=0.7, color="orange")
    ax.set_xlabel("Gap Size (picoseconds)", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_title("Histogram of Gaps\n(Exponential decay check)", fontsize=12)
    ax.grid(True, alpha=0.3)

    output_path = os.path.join(output_dir, output_filename)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    return output_path
