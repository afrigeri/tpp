import numpy as np

def point_plane_residuals(points, normal, centroid):
    """
    Signed orthogonal distance of each point from the plane.

    Parameters
    ----------
    points : (N,3) ndarray
    normal : (3,) ndarray
        Plane normal (does not need to be normalized).
    centroid : (3,) ndarray
        A point on the plane.

    Returns
    -------
    residuals : (N,) ndarray
    """
    normal = np.asarray(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    points = np.asarray(points, dtype=float)
    centroid = np.asarray(centroid, dtype=float)

    return (points - centroid) @ normal
