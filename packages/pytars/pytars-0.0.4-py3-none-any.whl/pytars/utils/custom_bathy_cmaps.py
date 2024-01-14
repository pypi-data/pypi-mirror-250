# %%
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


@dataclass
class InWaterBathymetricFalloff:
    """Class for propagating light attenuation through water."""

    rgb_attenuation: Tuple[float, float, float] = (0.59, 0.96, 0.98)
    max_depth: float = 20

    def calc_color(
        self,
        depth_meters: Union[float, np.ndarray],
        seafloor_rgb: Tuple[float, float, float] = (0.91, 0.88, 0.87),
        atmosphere_rgb: Tuple[float, float, float] = (1, 1, 1),
    ) -> np.ndarray:
        """Calculate the color of the water at a given depth.

        Args:
            depth_meters (Union[float, np.ndarray]): depth in meters
            seafloor_rgb (Tuple[float, float, float], optional): rgb color of the seafloor
            atmosphere_rgb (Tuple[float, float, float], optional): light from the atmosphere
        Returns:
            np.ndarray: rgb color of the water
        """
        rgb_light_to_seafloor = (
            np.array(atmosphere_rgb)[:, None]
            * np.array(self.rgb_attenuation)[:, None] ** depth_meters
        )
        rgb = (
            np.array(seafloor_rgb)[:, None]
            * rgb_light_to_seafloor
            * np.array(self.rgb_attenuation)[:, None] ** depth_meters
        )
        return rgb.T


class AttenuationTypes(Enum):
    """Constants for Jerlov attenuation types + some custom ones."""

    RS = InWaterBathymetricFalloff(rgb_attenuation=(0.65, 0.93, 0.98), max_depth=10)
    J_I = InWaterBathymetricFalloff(rgb_attenuation=(0.59, 0.96, 0.98), max_depth=20)
    J_IA = InWaterBathymetricFalloff(rgb_attenuation=(0.59, 0.95, 0.98), max_depth=20)
    J_IB = InWaterBathymetricFalloff(rgb_attenuation=(0.58, 0.95, 0.97), max_depth=15)
    J_II = InWaterBathymetricFalloff(rgb_attenuation=(0.56, 0.92, 0.94), max_depth=9.7)
    J_III = InWaterBathymetricFalloff(rgb_attenuation=(0.54, 0.88, 0.89), max_depth=5.2)
    J_1 = InWaterBathymetricFalloff(rgb_attenuation=(0.54, 0.88, 0.87), max_depth=4.7)
    J_3 = InWaterBathymetricFalloff(rgb_attenuation=(0.51, 0.82, 0.79), max_depth=3)
    J_5 = InWaterBathymetricFalloff(rgb_attenuation=(0.45, 0.73, 0.65), max_depth=1.9)
    J_7 = InWaterBathymetricFalloff(rgb_attenuation=(0.40, 0.61, 0.48), max_depth=1.2)
    J_9 = InWaterBathymetricFalloff(rgb_attenuation=(0.33, 0.47, 0.27), max_depth=0.8)


class ElevationTypes(Enum):
    """RGB constants for elevation color maps."""

    RS = np.array(
        [
            [0.8387, 0.9419, 0.6806],
            [0.8066, 0.9032, 0.6060],
            [0.7805, 0.8645, 0.5354],
            [0.7596, 0.8258, 0.4688],
            [0.7431, 0.7871, 0.4062],
            [0.7301, 0.7484, 0.3476],
            [0.7097, 0.6996, 0.2930],
            [0.6710, 0.6306, 0.2424],
            [0.6323, 0.5607, 0.1958],
            [0.5935, 0.4906, 0.1532],
            [0.5548, 0.4211, 0.1145],
            [0.5161, 0.3531, 0.0799],
            [0.4774, 0.2875, 0.0493],
            [0.4387, 0.2251, 0.0226],
            [0.4000, 0.1667, 0],
        ]
    )


def get_elevation_color(
    elevation_meters: Union[float, np.ndarray],
    max_terrain_elevation: float,
    elevation_rgb: np.ndarray = ElevationTypes.RS.value,
    bathy_falloff: InWaterBathymetricFalloff = AttenuationTypes.J_I.value,
    bathy_seafloor_rgb: Tuple[float, float, float] = (0.91, 0.88, 0.87),
    atmosphere_rgb: Tuple[float, float, float] = (1, 1, 1),
    depth_color_scalar: float = 1,
):
    """
    Calculates the color representation of elevation values.

    Args:
        elevation_meters (Union[float, np.ndarray]): The elevation values in meters.
        max_terrain_elevation (float): The maximum elevation value for the terrain.
        elevation_rgb (np.ndarray, optional): The RGB color values for elevation levels
        bathy_falloff (InWaterBathymetricFalloff, optional): The bathymetric falloff type
        bathy_seafloor_rgb (Tuple[float, float, float], optional): RGB color values for the seafloor
        atmosphere_rgb (Tuple[float, float, float], optional): RGB color values for the atmosphere
        depth_color_scalar (float, optional): A scalar to adjust the color of the water.
    Returns:
        np.ndarray: The color representation of the elevation values.
    """
    num_evaluate_colors = (
        elevation_meters.shape[0] if isinstance(elevation_meters, np.ndarray) else 1
    )
    # calculate bathy colors
    bathy_color = bathy_falloff.calc_color(
        depth_meters=-1 * elevation_meters * depth_color_scalar,
        seafloor_rgb=bathy_seafloor_rgb,
        atmosphere_rgb=atmosphere_rgb,
    )

    # calculate elevation colors
    num_elevation_colors = elevation_rgb.shape[0]
    rgb_elevation_levels = np.linspace(
        0,
        max_terrain_elevation,
        num_elevation_colors,
    )
    elevation_color = np.zeros((num_evaluate_colors, 3))
    for i in range(3):
        elevation_color[:, i] = np.interp(
            elevation_meters,
            rgb_elevation_levels,
            elevation_rgb[:, i],
            left=elevation_rgb[0, i],
            right=elevation_rgb[-1, i],
        )

    return np.where(np.tile(elevation_meters, (3, 1)).T < 0, bathy_color, elevation_color)


def create_topobathy_cmap(
    elevation_range: Tuple[float, float],
    num_levels: int,
    elevation_rgb: np.ndarray = ElevationTypes.RS.value,
    bathy_falloff_name: str = "J_I",
    bathy_seafloor_rgb: Tuple[float, float, float] = (0.91, 0.88, 0.87),
    atmosphere_rgb: Tuple[float, float, float] = (1, 1, 1),
    depth_color_scalar: float = 1,
):
    """
    Create a custom elevation colormap.

    Args:
        elevation_range (Tuple[float, float]): The range of elevation values.
        num_levels (int): The number of levels in the colormap.
        elevation_rgb (np.ndarray, optional): The RGB values for the elevation colors.
        bathy_falloff (InWaterBathymetricFalloff, optional): The type of bathymetric falloff.
        bathy_seafloor_rgb (Tuple[float, float, float], optional): RGB values for the seafloor color
        atmosphere_rgb (Tuple[float, float, float], optional):  RGB values for the atmosphere color
        depth_color_scalar (float, optional): A scalar to adjust the color of the water.
    Returns:
        ListedColormap: The custom elevation colormap.
    """
    if bathy_falloff_name not in AttenuationTypes.__members__:
        raise ValueError(f"{bathy_falloff_name} is not a valid attenuation type.")

    bathy_falloff = AttenuationTypes[bathy_falloff_name].value

    elevation_colors = get_elevation_color(
        elevation_meters=np.linspace(elevation_range[0], elevation_range[1], num_levels),
        max_terrain_elevation=elevation_range[1],
        elevation_rgb=elevation_rgb,
        bathy_falloff=bathy_falloff,
        bathy_seafloor_rgb=bathy_seafloor_rgb,
        atmosphere_rgb=atmosphere_rgb,
        depth_color_scalar=depth_color_scalar,
    )
    norm = colors.Normalize(vmin=elevation_range[0], vmax=elevation_range[1])
    return ListedColormap(elevation_colors), norm


if __name__ == "__main__":
    CMAP_RANGE = (-10, 15)
    cmap, norm = create_topobathy_cmap(elevation_range=CMAP_RANGE, num_levels=256)
    # create a norm so that the vmin = -10 and vmax = 15
    xg, yg = np.meshgrid(np.linspace(-10, 10, 1000), np.linspace(-10, 10, 1000))
    zg = np.sin(np.sqrt(xg**2 + yg**2)) * 10

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    im = ax.pcolormesh(zg, cmap=cmap, norm=norm)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.colorbar(im, ax=ax)

    # %
    fig, axs = plt.subplots(1, 11, figsize=(16, 10))
    for ax, attenutation_type in zip(axs, AttenuationTypes):
        rgb_test = attenutation_type.value.calc_color(depth_meters=np.linspace(0, 10, 1000))

        # tile to 1000 x 100 x 3
        rgb_image = np.tile(rgb_test[:, None, :], (1, 300, 1))

        ax.imshow(rgb_image)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(attenutation_type.name, fontsize=36)
    plt.tight_layout()
