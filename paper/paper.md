---
title: "GeolAttitude: A QGIS plugin for estimating geological attitude from Digital Elevation Models"
tags:
  - QGIS
  - geology
  - structural geology
  - geomorphology
  - digital elevation models
  - GIS
  - planetary science
  - remote sensing
authors:
  - name: Alessandro Frigeri
    affiliation: 1
    corresponding: true
    orcid: YOUR-ORCID-HERE

affiliations:
  - name: INAF – Istituto di Astrofisica e Planetologia Spaziali (IAPS), Rome, Italy
    index: 1

date: 2026
bibliography: paper.bib
---

# Summary

Geological attitude—the three-dimensional orientation of planar and linear geological features—is one of the most fundamental observations in structural geology. Traditionally, strike and dip are measured directly in the field using a geological compass. Increasingly, however, geological investigations rely on Digital Elevation Models (DEMs) acquired from airborne LiDAR, terrestrial laser scanning, UAV photogrammetry, satellite stereoscopy, and planetary missions, where direct field measurements are either impractical or impossible.

GeolAttitude is an open-source QGIS plugin that estimates the orientation of geological planes from three-dimensional point selections on raster DEMs. The plugin computes dip and dip direction using several numerical approaches, including least-squares regression, principal component analysis (PCA), singular value decomposition (SVD), and robust RANSAC fitting. In addition, GeolAttitude provides quantitative uncertainty metrics through residual analysis and bootstrap resampling.

Because the software operates entirely on raster topography, it can be applied equally to terrestrial datasets and planetary Digital Elevation Models derived from missions to the Moon and Mars. This makes GeolAttitude suitable for structural mapping in locations where field measurements cannot be obtained directly.

# Statement of need

The orientation of geological planes is a key parameter in structural geology, engineering geology, geomorphology, hydrogeology, mining, and planetary science. Measurements of dip and dip direction are routinely used to characterize bedding, faults, fractures, dikes, lava flows, and other geological structures.

Although GIS software provides powerful visualization and analysis capabilities, there are few open-source tools that allow users to estimate geological attitude directly from DEMs inside QGIS. Existing solutions are frequently proprietary, limited to simple three-point constructions, or lack uncertainty estimation and robust fitting algorithms.

GeolAttitude addresses these limitations by providing a complete and reproducible workflow within QGIS that includes:

- interactive point selection from raster DEMs;
- multiple numerical plane-fitting algorithms;
- robust outlier rejection;
- bootstrap uncertainty estimation;
- residual analysis;
- automatic generation of geological attitude parameters.

The plugin enables reproducible structural measurements from any raster topography and is particularly valuable where traditional compass measurements are unavailable.

# State of the field

Estimating the orientation of geological planes from three-dimensional data has become increasingly common with the widespread availability of LiDAR, photogrammetry, terrestrial laser scanning, and planetary stereo imagery.

Commercial geological modelling packages such as Leapfrog Geo, MOVE, and GOCAD include structural analysis capabilities, while cloud-processing software such as CloudCompare can estimate local surface normals from dense point clouds. However, these packages are not designed for interactive geological attitude estimation directly from raster DEMs within an open-source GIS environment.

Several QGIS plugins support terrain visualization, slope calculation, profile extraction, and geological mapping, but none provide a dedicated workflow for estimating geological attitude from user-selected three-dimensional points using multiple fitting algorithms and uncertainty estimation.

GeolAttitude fills this gap by combining:

- interactive GIS workflows,
- robust numerical methods,
- uncertainty quantification,
- planetary compatibility,

within a single open-source plugin.

Potential applications include:

- structural geology;
- engineering geology;
- mining;
- geomorphology;
- landslide analysis;
- volcanic geology;
- planetary geology;
- geological mapping.

# Software design

GeolAttitude follows a modular architecture that separates the graphical user interface from the numerical computation engine.

The computational core implements several independent plane-fitting algorithms:

- Least Squares regression;
- Principal Component Analysis (PCA);
- Singular Value Decomposition (SVD);
- Random Sample Consensus (RANSAC).

Each algorithm estimates the best-fitting geological plane from an arbitrary number of selected points and returns:

- unit normal vector;
- plane centroid;
- dip;
- dip direction;
- plane equation.

Additional statistical outputs include:

- orthogonal residuals;
- vertical residuals;
- root mean square error (RMSE);
- maximum absolute residual;
- inlier and outlier identification (RANSAC);
- bootstrap confidence intervals for dip and dip direction.

The numerical implementation is independent of the QGIS interface, allowing algorithms to be tested separately and facilitating future extensions.

The graphical interface uses the QGIS raster API to retrieve elevation values directly from Digital Elevation Models while users interactively select points on the map canvas.

# Mathematical formulation

Given a set of three-dimensional observations

$$
P_i=(x_i,y_i,z_i)
$$

GeolAttitude estimates the best-fitting plane

$$
Ax+By+Cz+D=0
$$

using one of several numerical algorithms.

The plane normal vector

$$
\mathbf{n}=(A,B,C)
$$

is obtained either by least-squares regression or by computing the eigenvector associated with the smallest eigenvalue of the covariance matrix (PCA/SVD).

Dip is computed as

$$
\delta=\arctan\left(
\frac{\sqrt{n_x^2+n_y^2}}
{|n_z|}
\right)
$$

while dip direction is derived from the horizontal projection of the upward-pointing normal vector using the geological convention

$$
\theta=
\operatorname{atan2}(n_x,n_y).
$$

Bootstrap resampling provides empirical confidence intervals for the estimated orientation parameters.

# Example applications

GeolAttitude can be applied to a broad range of Digital Elevation Models, including:

- airborne LiDAR;
- UAV photogrammetry;
- terrestrial laser scanning;
- structure-from-motion reconstructions;
- satellite stereo DEMs;
- planetary DEMs.

Typical geological applications include measuring:

- bedding orientation;
- lava-flow attitudes;
- fault planes;
- fracture sets;
- dikes;
- sills;
- landslide scarps;
- crater-wall stratigraphy.

Planetary applications include structural measurements from:

- HiRISE stereo DEMs (Mars);
- HRSC DEMs (Mars);
- CTX stereo models;
- LROC NAC stereo DEMs (Moon);
- LOLA topography;
- future rover-derived Digital Elevation Models.

These datasets enable structural analyses in environments where direct field measurements are impossible.

# Research impact statement

The increasing availability of high-resolution Digital Elevation Models has transformed geological mapping on both Earth and planetary bodies. GeolAttitude provides an open-source and reproducible workflow for estimating geological attitude directly from raster topography.

The software is particularly useful for:

- inaccessible terrestrial outcrops;
- hazardous environments;
- historical datasets;
- planetary exploration.

Potential scientific applications include:

- tectonic reconstruction;
- structural mapping;
- volcanic stratigraphy;
- impact crater analysis;
- wrinkle-ridge fault geometry;
- lava-flow characterization;
- rover traverse planning;
- planetary geological mapping.

Because modern lunar and Martian missions routinely generate metre-scale DEMs, GeolAttitude extends traditional structural geology methods to planetary surfaces where direct field observations are unavailable.

# Availability

GeolAttitude is released under the GNU General Public License version 3 (GPLv3).

The source code, documentation, issue tracker, and release history are publicly available through GitHub.

The plugin is distributed through the official QGIS Plugin Repository and supports recent QGIS 3 and QGIS 4 releases.

# Future developments

Future developments will focus on extending GeolAttitude to support:

- lineation (trend and plunge) measurements;
- cylindrical and conical surface fitting;
- uncertainty propagation from DEM vertical accuracy;
- stereonet visualization;
- batch processing of mapped surfaces;
- direct integration with geological mapping workflows in QGIS.

These additions will further expand the applicability of the software to both terrestrial and planetary structural geology.

# AI usage disclosure

Generative AI was used to assist editing the language of the manuscript. The article contents, software design, implementation, algorithms, validation, and scientific content were developed and verified by the author.

# Acknowledgements

The author gratefully acknowledges the QGIS development community and the developers of NumPy, SciPy, and the broader open-source scientific Python ecosystem.

GeolAttitude has been developed within the planetary geology activities of the Istituto Nazionale di Astrofisica (INAF), Istituto di Astrofisica e Planetologia Spaziali (IAPS), where it supports research on terrestrial and planetary geological mapping.

# References

(Automatically generated from `paper.bib`.)