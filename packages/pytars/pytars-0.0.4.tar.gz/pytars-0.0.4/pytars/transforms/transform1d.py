# %%
from typing import Optional, Tuple

import numpy as np


def scale_array(
    data: np.ndarray,
    new_range: Tuple[float, float],
    data_range: Optional[Tuple[float, float]] = None,
):
    """Scales an array to a new range."""
    if data_range is None:
        data_range = (data.min(), data.max())

    # check that datarange is not 0
    if data_range[0] == data_range[1]:
        raise ValueError("Data range cannot be 0.")

    # scale to 0-1
    data = (data - data_range[0]) / (data_range[1] - data_range[0])

    # scale to new range
    return data * (new_range[1] - new_range[0]) + new_range[0]
