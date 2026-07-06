"""Ordinary least-squares plane fitting for GeolAttitude."""

import math

import numpy as np

from .common import (
    points_to_array,
    base_result,
    point_plane_residuals,
    add_point_usage_fields,
    compute_plane_statistics,
)


def fit_least_squares(points):
    """Fit z = ax + by + c using ordinary least squares."""
    arr = points_to_array(points)
    x = arr[:, 0]
    y = arr[:, 1]
    z = arr[:, 2]

    matrix = np.column_stack([x, y, np.ones_like(x)])
    coeff, residuals, rank, singular_values = np.linalg.lstsq(matrix, z, rcond=None)

    if rank < 3:
        raise ValueError("The selected points are nearly collinear or numerically degenerate.")

    a, b, c = coeff
    normal = np.array([-a, -b, 1.0], dtype=float)
    centroid = arr.mean(axis=0)

    #residuals = point_plane_residuals(points, normal, centroid)
    #rmse = float(np.sqrt(np.mean(residuals ** 2)))
    #max_abs_resid = float(np.max(np.abs(residuals)))
    
    result = base_result("least_squares", normal, centroid, len(points))
    
    #result["rmse"] = rmse
    #result["max_abs_resid"] = max_abs_resid
    #result["max_abs_vertical_residual"] = max_abs_resid
    
    result.update(
        {
            "a": float(a),
            "b": float(b),
            "c": float(c),
     #      "rmse": rmse,
     #      "max_abs_resid": max_abs_resid,
            "rank": int(rank),
            "singular_values": singular_values,
     #      "residuals": residual_vec,
        }
    )
    
    result.update(
        compute_plane_statistics(points, normal, centroid)
    )

    #return result
    return add_point_usage_fields(result, points)
