# %%
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
from matplotlib.colors import ListedColormap
from scipy.interpolate import interp1d

from pytars.transforms.transform1d import scale_array
from pytars.utils.bin_edges import bin_center_to_bin_edge


def get_fixed_cmap(bin_centers, cmap_name, num_visual_bins: int = 256):
    cmap = colormaps[cmap_name]
    # normalize bin centers
    bin_edges = bin_center_to_bin_edge(bin_centers)
    bin_edges_norm = scale_array(bin_edges, (0, 1), (bin_edges[0], bin_edges[-1]))
    bin_centers_norm = scale_array(bin_centers, (0, 1), (bin_edges[0], bin_edges[-1]))
    # find ind fo rnearest color
    xi = np.linspace(0, 1, num_visual_bins)

    f = interp1d(
        bin_centers_norm,
        np.arange(len(bin_centers)),
        kind="nearest",
        bounds_error=False,
        fill_value="extrapolate",
    )
    color_ind = f(xi).astype(int)

    # get colors
    fixed_colors = cmap(bin_edges_norm)
    all_colors = fixed_colors[color_ind]

    final_cmap = ListedColormap(all_colors)
    norm = colors.Normalize(vmin=bin_edges[0], vmax=bin_edges[-1])
    return final_cmap, norm


if __name__ == "__main__":
    # Sample data
    bin_centers = np.linspace(1, 10, 10)
    cmap_name = "jet"
    visual_bins = 256

    cmap, norm = get_fixed_cmap(bin_centers, cmap_name, visual_bins)

    xi = np.linspace(-5, 5, 100)

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    for bin_center in bin_centers:
        yi = np.cos(xi) + bin_center
        ax.plot(xi, yi, color=cmap(norm(bin_center)), label=bin_center, linewidth=2)

    cbar = fig.colorbar(None, ax=ax, cmap=cmap, norm=norm)
    cbar.set_ticks(bin_centers)
