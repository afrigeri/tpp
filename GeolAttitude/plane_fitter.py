# -*- coding: utf-8 -*-
"""Plane fitting utilities for GeolAttitude.

Coordinates are assumed to be x=east, y=north, z=up, with compatible
linear units. The default method fits a plane in the form:

    z = a*x + b*y + c

and returns geological attitude parameters derived from the fitted plane.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Iterable, Mapping, Sequence

import numpy as np


class PlaneFitter:
    """Fit a geological plane from 3D points.

    Public API
    ----------
    PlaneFitter.fit(points, method="least_squares")

    Parameters
    ----------
    points : iterable
        Each point can be either a mapping with keys ``x``, ``y``, ``z``
        or a sequence ``(x, y, z)``.
    method : str
        Currently supported: ``least_squares`` / ``ols``.

    Returns
    -------
    dict
        Plane coefficients, geological attitude, residual statistics and
        metadata. Dip direction is the azimuth of steepest descent measured
        clockwise from north.
    """

    @classmethod
    def fit(cls, points: Iterable, method: str = "least_squares") -> dict:
        """Fit a plane to points and return geological attitude results."""
        method_key = method.lower().strip().replace("-", "_")
        if method_key in ("least_squares", "ols", "ordinary_least_squares"):
            return cls._fit_least_squares(points, method_name="least_squares")
        raise ValueError(f"Unsupported plane fitting method: {method}")

    @staticmethod
    def _as_array(points: Iterable) -> np.ndarray:
        """Convert supported point formats to a finite Nx3 numpy array."""
        rows = []
        for point in points:
            if isinstance(point, Mapping):
                rows.append([point["x"], point["y"], point["z"]])
            else:
                if not isinstance(point, Sequence) or len(point) < 3:
                    raise ValueError(
                        "Each point must be a mapping with x/y/z keys or a sequence (x, y, z)."
                    )
                rows.append([point[0], point[1], point[2]])

        arr = np.asarray(rows, dtype=float)
        if arr.ndim != 2 or arr.shape[1] != 3:
            raise ValueError("Points must define an Nx3 array.")
        if arr.shape[0] < 3:
            raise ValueError("At least three points are required.")
        if not np.all(np.isfinite(arr)):
            raise ValueError("All point coordinates must be finite numeric values.")
        return arr

    @classmethod
    def _fit_least_squares(cls, points: Iterable, method_name: str) -> dict:
        """Fit z = ax + by + c using vertical least squares."""
        arr = cls._as_array(points)
        x = arr[:, 0]
        y = arr[:, 1]
        z = arr[:, 2]

        matrix = np.column_stack([x, y, np.ones_like(x)])
        coeff, _residuals, rank, singular_values = np.linalg.lstsq(
            matrix, z, rcond=None
        )
        if rank < 3:
            raise ValueError(
                "The selected points are nearly collinear or numerically degenerate."
            )

        a, b, c = coeff
        z_fit = matrix @ coeff
        residual_vec = z - z_fit

        slope = math.hypot(a, b)
        dip = math.degrees(math.atan(slope))
        dip_direction = (math.degrees(math.atan2(-a, -b)) + 360.0) % 360.0
        strike_rhr = (dip_direction - 90.0) % 360.0

        normal = np.array([-a, -b, 1.0], dtype=float)
        normal /= np.linalg.norm(normal)

        rmse = math.sqrt(float(np.mean(residual_vec**2)))
        max_abs_resid = float(np.max(np.abs(residual_vec)))

        return {
            "method": method_name,
            "a": float(a),
            "b": float(b),
            "c": float(c),
            "dip": float(dip),
            "dip_direction": float(dip_direction),
            "strike_rhr": float(strike_rhr),
            "rmse": float(rmse),
            "max_abs_resid": max_abs_resid,
            "normal": normal,
            "rank": int(rank),
            "singular_values": singular_values,
            "residuals": residual_vec,
            "z_fit": z_fit,
            "n": int(arr.shape[0]),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
