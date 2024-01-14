# %%
import time
from typing import Callable, Optional, Tuple, Union

import numpy as np
from scipy.interpolate import LinearNDInterpolator, griddata
from scipy.stats import binned_statistic_2d


def bin_center_to_bin_edge(bin_center: np.ndarray) -> np.ndarray:
    diffs = np.diff(bin_center) / 2
    return np.concatenate(
        ([bin_center[0] - diffs[0]], bin_center[:-1] + diffs, [bin_center[-1] + diffs[-1]])
    )


def create_2d_grid(xi: np.ndarray, yi: np.ndarray):
    return np.meshgrid(xi, yi)


def bin_grid_2d(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    xi: np.ndarray,
    yi: np.ndarray,
    fun: Union[Callable, str],
    is_bin_center: bool = True,
):
    """
    Bin the values in z into the bins defined by xg and yg.
    fun is a function that takes a 1d array and returns a scalar.
    """
    if is_bin_center:
        xi = bin_center_to_bin_edge(xi)
        yi = bin_center_to_bin_edge(yi)

    return binned_statistic_2d(y, x, z, statistic=fun, bins=[yi, xi]).statistic


def idw_interp_grid_2d(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    xi: np.ndarray,
    yi: np.ndarray,
    p: float = 2,
    eps: float = 1e-10,
    max_vals: Optional[int] = 12,
    max_range: Optional[float] = None,
) -> np.ndarray:
    # Create the output grid
    xg, yg = np.meshgrid(xi, yi)

    # Initialize the result array
    zg = np.zeros_like(xg) * np.nan

    # Loop over all grid points - vectorization for this operation is complex and memory-intensive
    for i in range(xg.shape[0]):
        for j in range(xg.shape[1]):
            # Calculate the distance from each grid point to each data point
            dist = np.sqrt((x - xg[i, j]) ** 2 + (y - yg[i, j]) ** 2)

            # Apply max_range limit if specified
            if max_range is not None:
                mask = dist < max_range
                if not np.any(mask):
                    continue
                dist = dist[mask]
                z_vals = z[mask]
            else:
                z_vals = z

            # Avoid division by zero
            dist = np.maximum(dist, eps)

            # Calculate weights
            weights = 1 / dist**p

            # Apply max_vals limit if specified
            if max_vals is not None and len(weights) > max_vals:
                idx = np.argpartition(weights, -max_vals)[-max_vals:]
                weights = weights[idx]
                z_vals = z_vals[idx]

            # Calculate interpolated value
            zg[i, j] = np.sum(weights * z_vals) / np.sum(weights)

    return zg


def linear_interp_grid_2d(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    xi: np.ndarray,
    yi: np.ndarray,
):
    """
    Perform linear interpolation on a 2D grid.

    Parameters:
    x: np.ndarray - array of x-coordinates of data points.
    y: np.ndarray - array of y-coordinates of data points.
    z: np.ndarray - array of z-values (function values) at data points.
    xi: np.ndarray - array of x-coordinates for interpolation points.
    yi: np.ndarray - array of y-coordinates for interpolation points.

    Returns:
    zg: np.ndarray - interpolated z-values on the 2D grid.
    """
    # create grid
    xg, yg = create_2d_grid(xi, yi)

    # interpolate using linear method
    zg = griddata((x, y), z, (xg, yg), method="linear")

    return zg


def linear_extrapolate_2d(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, xi: np.ndarray, yi: np.ndarray
):
    """
    Perform linear interpolation with extrapolation on a 2D grid.

    Parameters:
    x, y, z: Arrays of data points.
    xi, yi: Arrays of points for interpolation and extrapolation.

    Returns:
    zg: Interpolated and extrapolated values on the 2D grid.
    """
    # Create the interpolator
    interpolator = LinearNDInterpolator(list(zip(x, y)), z)

    # Create grid
    xg, yg = create_2d_grid(xi, yi)

    # Interpolate and extrapolate
    zg = interpolator(xg, yg)

    return zg


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    num_pts = 200
    x = np.random.uniform(0, 1, num_pts)
    y = np.random.uniform(0, 1, num_pts)
    z = np.cos(x * np.pi)
    xi = np.linspace(0, 1, 100)
    yi = np.linspace(0, 1, 100)
    xg, yg = create_2d_grid(xi, yi)

    start_time = time.perf_counter()
    zg_bin = bin_grid_2d(x, y, z, xi, yi, "mean")
    print(f"bin_grid_2d took {time.perf_counter() - start_time} seconds")

    start_time = time.perf_counter()
    zg_idw = idw_interp_grid_2d(x, y, z, xi, yi, p=2, max_vals=12)
    print(f"idw_interp_grid_2d took {time.perf_counter() - start_time} seconds")

    start_time = time.perf_counter()
    zg_lin = linear_interp_grid_2d(x, y, z, xi, yi)
    print(f"linear_interp_grid_2d took {time.perf_counter() - start_time} seconds")

    start_time = time.perf_counter()
    zg_lin_extrap = linear_extrapolate_2d(x, y, z, xi, yi)
    print(f"linear_extrapolate_2d took {time.perf_counter() - start_time} seconds")

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for ax, zg, title_str in zip(
        axs.flatten(),
        [zg_bin, zg_idw, zg_lin, zg_lin_extrap],
        ["bin", "idw", "linear", "linear_extrap"],
    ):
        ax.set_title(title_str)
        ax.pcolormesh(xi, yi, zg)
        ax.plot(x, y, "m.")
