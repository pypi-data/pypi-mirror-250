# %%
import numpy as np
from scipy.spatial.transform import Rotation as R


def transform_xyz(points_xyz: np.ndarray, extrinsic_4x4: np.ndarray) -> np.ndarray:
    """Transform 3D points based on 4x4 rotation matrix."""
    points_xyz_homogeneous = np.concatenate([points_xyz, np.ones((points_xyz.shape[0], 1))], axis=1)
    rotated_xyz = points_xyz_homogeneous @ extrinsic_4x4
    return rotated_xyz[:, :3]


def create_rotation_matrix_4x4(tx, ty, tz, roll, pitch, yaw, is_degrees=True):
    """Creates a 4x4 rotation matrix from the given translation and rotation."""
    r = R.from_euler("zyx", [yaw, pitch, roll], degrees=is_degrees)
    rotation_matrix = np.eye(4)
    rotation_matrix[:3, :3] = r.as_matrix()
    translation_matrix = np.eye(4)
    translation_matrix[:3, 3] = np.array([tx, ty, tz])
    return rotation_matrix @ translation_matrix


if __name__ == "__main__":
    test = create_rotation_matrix_4x4(1, 0, 0, 45, 0, 0)
    print(np.round(test, 1))
