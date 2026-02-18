import numpy as np
import pandas as pd
import os
import time

def save_timestamps_to_csv(
    timestamps: np.ndarray,
    num_timestamps: int,
    max_timestamp: int,
    output_dir: str = "data",
) -> str:
    """Save timestamps to CSV with descriptive filename."""
    os.makedirs(output_dir, exist_ok=True)

    # Create descriptive filename
    if num_timestamps >= 1000:
        count_str = f"{num_timestamps // 1000}k"
    else:
        count_str = str(num_timestamps)

    # Format max_timestamp in scientific notation
    max_str = f"{max_timestamp:.0e}".replace("+", "")
    
    random = int(time.time() * 1000) % 10000  
    filename = f"{output_dir}/timestamps_{count_str}_max{max_str}_{random}.csv"

    # Save to CSV
    df = pd.DataFrame({"timestamp": timestamps})
    df.to_csv(filename, index=False)

    return filename


def generate_unique_timestamps(
    num_timestamps: int, max_timestamp: int = 10**12
) -> np.ndarray:
    """
    Generate unique, uniformly distributed timestamps in picoseconds.

    Args:
        num_timestamps: Number of timestamps to generate
        max_timestamp: Maximum timestamp value (exclusive)

    Returns:
        Sorted numpy array of unique integer timestamps in range [0, max_timestamp)
    """

    if num_timestamps > max_timestamp:
        raise ValueError(
            f"Cannot generate {num_timestamps} unique timestamps in range [0, {max_timestamp})"
        )

    # Mathematical insight: If points are uniformly distributed, gaps between
    # consecutive sorted points follow an exponential distribution with rate λ = n / max_value
    rate = num_timestamps / max_timestamp
    gaps = np.random.exponential(scale=1 / rate, size=num_timestamps)

    # Convert gaps to cumulative positions
    positions = np.cumsum(gaps)
    timestamps = positions.astype(np.int64)

    # Ensure we're within bounds and handle any potential duplicates from rounding
    timestamps = np.clip(timestamps, 0, max_timestamp - 1)
    timestamps = np.unique(timestamps)

    # If we lost some due to rounding, fill in the gaps
    while len(timestamps) < num_timestamps:
        additional_needed = num_timestamps - len(timestamps)
        extra = np.random.randint(0, max_timestamp, size=additional_needed * 2)
        timestamps = np.unique(np.concatenate([timestamps, extra]))[:num_timestamps]

    # Return as numpy array of integers
    return timestamps.astype(np.int64)
