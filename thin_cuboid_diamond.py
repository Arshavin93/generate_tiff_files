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
cuboid_height = 0.05        # Height of the cuboid
cuboid_base_z = 0.207       # Base elevation of the cuboid
center_x, center_y = 0.814, 0.5  # Center of the rotated cuboid
half_width_x = 0.025        # Half width along the x-axis (before rotation)
half_width_y = 0.025        # Half width along the y-axis (before rotation)

# Rotate coordinates by 45 degrees to create a diamond shape
angle = np.radians(45)
cos_angle, sin_angle = np.cos(angle), np.sin(angle)

# Apply rotation to the grid coordinates
X_rotated = (X - center_x) * cos_angle + (Y - center_y) * sin_angle
Y_rotated = -(X - center_x) * sin_angle + (Y - center_y) * cos_angle

# Create a mask for the diamond-shaped cuboid
cuboid_mask = (np.abs(X_rotated) <= half_width_x) & (np.abs(Y_rotated) <= half_width_y)
Z_cuboid = np.zeros_like(Z)
Z_cuboid[cuboid_mask] = cuboid_base_z + cuboid_height

# Combine the cuboid with the polynomial surface
Z_combined = np.maximum(Z, Z_cuboid)

# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)

# Write to GeoTIFF file
with rasterio.open('./diamond_cuboid_obstacle.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)

