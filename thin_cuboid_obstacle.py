# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 15:10:29 2024

@author: visha
"""

import rasterio
import numpy as np
from rasterio.transform import Affine
import matplotlib.pyplot as plt
import csv

# Define grid parameters with fixed cell sizes
cell_size_x = 0.0028
cell_size_y = 0.0028
x = np.linspace(-0.098, 1.75, 660)
y = np.linspace(-0.06, 1.06, 400)
X, Y = np.meshgrid(x, y)

# Polynomial equation for the base surface
def polynomial_z(x):
    return 0.1086 * (x**4) - 0.5179 * (x**3) + 1.3434 * (x**2) - 1.6513 * x + 0.8923

# Calculate Z-values using the polynomial equation
Z = polynomial_z(X)

# Cuboid parameters
cuboid_height = 0.05  # Height of the cuboid
cuboid_base_z = 0.207  # Base elevation of the cuboid
cuboid_min_x, cuboid_max_x = 0.814, 0.864  # X-range of the cuboid
cuboid_min_y, cuboid_max_y = 0.45, 0.5  # Y-range of the cuboid

# Create mask for the cuboid
cuboid_mask = (X >= cuboid_min_x) & (X <= cuboid_max_x) & (Y >= cuboid_min_y) & (Y <= cuboid_max_y)
Z_cuboid = np.zeros_like(Z)
Z_cuboid[cuboid_mask] = cuboid_base_z + cuboid_height

# Combine the cylinder and cuboid with the polynomial surface
#Z_combined = np.maximum(Z, Z_cylinder1)
Z_combined = np.maximum(Z, Z_cuboid)

# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)

# Write to GeoTIFF file
with rasterio.open('./cuboid_obstacle.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)

