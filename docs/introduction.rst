Scientific Background
=====================

The algorithms implemented in **GeolAttitude** are based on established methods from numerical linear algebra,
statistical estimation, and structural geology. This chapter summarizes the mathematical foundations of the
implemented methods and provides references to the original literature and standard textbooks.

The objective of the plugin is to estimate the orientation of planar geological features from a set of sampled
three-dimensional points. The implemented algorithms aim to provide robust estimates of strike, dip, dip
direction, residual statistics, and uncertainty measures.

.. contents::
   :local:
   :depth: 2


Introduction
------------

Estimating the orientation of a geological plane from a set of sampled points is a classical problem in
structural geology. Modern solutions combine techniques from

* least-squares estimation,
* Principal Component Analysis (PCA),
* Singular Value Decomposition (SVD),
* robust estimation methods,
* statistical analysis.

Although these methods originate from mathematics and computer science, they have become standard tools for
quantitative structural geology :cite:`Allmendinger2012,PollardFletcher2005`.


Plane Representation
--------------------

A plane in Cartesian coordinates is represented by

.. math::

   ax + by + cz + d = 0

where

* :math:`(a,b,c)` is the unit normal vector,
* :math:`d` is the signed distance from the origin.

The geological attitude is obtained from the normal vector by computing

* dip,
* dip direction,
* strike.

GeolAttitude follows the right-hand-rule convention commonly adopted in geological mapping.


Least-Squares Plane Fitting
---------------------------

The most fundamental plane-fitting method minimizes the sum of squared orthogonal distances between the sampled
points and the estimated plane.

Unlike ordinary regression, the orthogonal formulation does not assume that one coordinate is dependent upon the
others, making it appropriate for geological measurements.

The theoretical foundations of orthogonal least-squares fitting were introduced by Pearson
:cite:`Pearson1901`.

Modern numerical implementations typically solve the problem using Singular Value Decomposition (SVD)
:cite:`GolubReinsch1970,GolubVanLoan2013`.

GeolAttitude computes

* centroid of the observations,
* covariance matrix,
* plane normal,
* orthogonal residuals,
* RMS residual.


Principal Component Analysis
----------------------------

Principal Component Analysis (PCA) interprets the point cloud as a multivariate dataset.

The covariance matrix

.. math::

   C = \frac{1}{n-1}\sum_i
   (\mathbf{x}_i-\bar{\mathbf{x}})
   (\mathbf{x}_i-\bar{\mathbf{x}})^T

is decomposed into eigenvalues and eigenvectors.

The eigenvector corresponding to the smallest eigenvalue represents the direction of minimum variance and
therefore the normal vector of the best-fitting plane.

This interpretation originates from the pioneering work of Pearson :cite:`Pearson1901` and has become standard
through the work of Jolliffe :cite:`Jolliffe2002`.

The magnitude of the eigenvalues also provides information about the spatial distribution of the measurements.


Singular Value Decomposition
----------------------------

Singular Value Decomposition provides one of the most stable numerical methods for solving least-squares
problems.

Given the centered observation matrix

.. math::

   X = U \Sigma V^T

the right singular vector corresponding to the smallest singular value defines the normal vector of the fitted
plane.

SVD offers excellent numerical stability even for nearly coplanar datasets and is considered the reference
method in numerical linear algebra :cite:`GolubReinsch1970,GolubVanLoan2013`.


Residual Analysis
-----------------

For every observation GeolAttitude computes the orthogonal distance to the estimated plane.

Residual analysis provides quantitative information regarding

* measurement precision,
* geological scatter,
* data quality,
* possible outliers.

Typical statistics include

* RMS residual,
* maximum residual,
* mean residual,
* standard deviation.

These quantities follow the standard methodology of experimental uncertainty analysis
:cite:`Taylor1997`.


Robust Estimation using RANSAC
------------------------------

Field measurements may contain erroneous observations due to

* GPS inaccuracies,
* digitizing errors,
* mixed geological surfaces,
* operator mistakes.

To reduce the influence of outliers, GeolAttitude implements the Random Sample Consensus (RANSAC) algorithm.

RANSAC repeatedly estimates candidate planes from randomly selected subsets and retains the model that maximizes
the number of inliers.

The original algorithm was introduced by Fischler and Bolles
:cite:`FischlerBolles1981`.

Compared with classical least squares, RANSAC is considerably more robust when a significant fraction of the
measurements are contaminated by outliers.


Geological Orientation
----------------------

The normal vector of the fitted plane is converted into

* dip,
* dip direction,
* strike.

These quantities follow conventional structural geology definitions.

Because geological orientations are angular variables, their statistical treatment differs from ordinary linear
statistics.

Circular and directional statistics provide the appropriate theoretical framework
:cite:`Fisher1993,MardiaJupp2000`.

These methods become particularly important when analyzing large collections of structural measurements.


Structural Geology Context
--------------------------

Plane fitting is one component of quantitative structural geology.

The estimated orientations may represent

* bedding,
* foliations,
* fractures,
* faults,
* joints,
* unconformities.

Computational methods based on vectors and tensors have become standard tools in structural analysis
:cite:`Allmendinger2012`.

The geological interpretation of the resulting orientations should always consider

* field observations,
* lithological context,
* measurement uncertainty,
* structural relationships.

General principles of structural interpretation are discussed in
:cite:`PollardFletcher2005`.

Future Developments
-------------------

The modular architecture of GeolAttitude facilitates the implementation of additional estimation techniques,
including

* weighted least squares,
* nonlinear optimization,
* Bayesian estimation,
* bootstrap uncertainty analysis,
* confidence ellipsoids,
* robust M-estimators.

Many of these methods are based on modern numerical optimization techniques
:cite:`NocedalWright2006`.

References
----------

.. bibliography::
   :style: unsrt
