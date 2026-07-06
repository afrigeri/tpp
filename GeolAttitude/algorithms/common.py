"""Shared helpers for GeolAttitude plane-fitting algorithms."""

import math
from datetime import datetime

import numpy as np


def points_to_array(points):
    """Convert a list of point dictionaries to an Nx3 NumPy array."""
    if len(points) < 3:
        raise ValueError("At least three points are required.")

    arr = np.array([[p["x"], p["y"], p["z"]] for p in points], dtype=float)

    if arr.ndim != 2 or arr.shape[1] != 3:
        raise ValueError("Points must define x, y, z coordinates.")

    if not np.all(np.isfinite(arr)):
        raise ValueError("Point coordinates must be finite numeric values.")

    return arr


def normalize_vector(vector):
    """Return a normalized vector."""
    vector = np.asarray(vector, dtype=float)
    norm = np.linalg.norm(vector)

    if norm == 0.0 or not np.isfinite(norm):
        raise ValueError("Cannot normalize a zero or invalid vector.")

    return vector / norm

def orientation_from_normal(normal):
    """
    Compute geological orientation from an upward-pointing normal.

    Coordinates are assumed to be x=east, y=north, z=up.
    Dip direction is the azimuth of steepest descent, clockwise from north.
    Strike is returned using the right-hand rule.
    
    Parameters
    ----------
    normal : array-like
        Unit normal vector with nz > 0.

    Returns
    -------
    dip : float
    dip_direction : float
    strike_rhr : float
    """
    
    nx, ny, nz = normal

    # Ensure upward-pointing normal
    if nz < 0:
        nx, ny, nz = -nx, -ny, -nz

    dip = math.degrees(math.atan2(math.hypot(nx, ny), nz))

    dip_direction = (
        math.degrees(math.atan2(nx, ny))
        + 360.0
    ) % 360.0

    strike_rhr = (dip_direction - 90.0) % 360.0

    return normal, dip, dip_direction, strike_rhr
    
    
def orientation_from_normal_old(normal):
    """Compute geological orientation from an upward-pointing plane normal.

    Coordinates are assumed to be x=east, y=north, z=up.
    Dip direction is the azimuth of steepest descent, clockwise from north.
    Strike is returned using the right-hand rule.
    """
    normal = normalize_vector(normal)

    if normal[2] < 0.0:
        normal = -normal

    nx, ny, nz = normal

    dip = math.degrees(math.atan2(math.hypot(nx, ny), abs(nz)))
    #dip_direction = (math.degrees(math.atan2(-nx, -ny)) + 360.0) % 360.0
    dip_direction = (math.degrees(math.atan2(nx, ny)) + 360.0) % 360.0
    strike_rhr = (dip_direction - 90.0) % 360.0

    return normal, float(dip), float(dip_direction), float(strike_rhr)


def plane_coefficients_from_normal(normal, centroid):
    """Return z = ax + by + c coefficients from a plane normal and centroid.

    Vertical planes cannot be represented as z = ax + by + c, so the
    coefficients are returned as NaN in that case.
    """
    normal = normalize_vector(normal)
    centroid = np.asarray(centroid, dtype=float)

    nx, ny, nz = normal

    if abs(nz) < 1.0e-12:
        return float("nan"), float("nan"), float("nan")

    a = -nx / nz
    b = -ny / nz
    c = (nx * centroid[0] + ny * centroid[1] + nz * centroid[2]) / nz

    return float(a), float(b), float(c)


def base_result(method, normal, centroid, n):
    """Create the common part of a plane-fit result dictionary."""
    normal, dip, dip_direction, strike_rhr = orientation_from_normal(normal)
    a, b, c = plane_coefficients_from_normal(normal, centroid)

    return {
        "method": method,
        "n": int(n),
        "normal": normal,
        "centroid": centroid,
        "a": a,
        "b": b,
        "c": c,
        "dip": dip,
        "dip_direction": dip_direction,
        "strike_rhr": strike_rhr,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "n_selected": int(n),
        "n_used": int(n),
        "n_inliers": int(n),
        "inlier_indices": list(range(int(n))),
        "outlier_indices": [],
    }

def point_plane_residuals(points, normal, centroid):
    """Return signed orthogonal point-to-plane residuals."""
    arr = points_to_array(points)
    normal = normalize_vector(normal)
    centroid = np.asarray(centroid, dtype=float)

    return (arr - centroid) @ normal


def add_point_usage_fields(result, points, inlier_indices=None):
    """Add common selected/used/inlier/outlier fields to a fit result."""
    n_selected = len(points)

    if inlier_indices is None:
        inlier_indices = list(range(n_selected))
    else:
        inlier_indices = sorted(int(i) for i in inlier_indices)

    inlier_set = set(inlier_indices)
    outlier_indices = [
        i for i in range(n_selected)
        if i not in inlier_set
    ]

    result["n"] = n_selected
    result["n_selected"] = n_selected
    result["n_used"] = len(inlier_indices)
    result["n_inliers"] = len(inlier_indices)
    result["inlier_indices"] = inlier_indices
    result["outlier_indices"] = outlier_indices

    return result