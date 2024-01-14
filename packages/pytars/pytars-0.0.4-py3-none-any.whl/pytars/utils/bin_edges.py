#
import numpy as np


def bin_center_to_bin_edge(bin_center: np.ndarray) -> np.ndarray:
    diffs = np.diff(bin_center) / 2
    return np.concatenate(
        ([bin_center[0] - diffs[0]], bin_center[:-1] + diffs, [bin_center[-1] + diffs[-1]])
    )
