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

# Diamond-shaped cuboid parameters
cuboid_height = 0.06        # Height of each cuboid
half_width_x = 0.0167        # Half width along the x-axis (before rotation)
half_width_y = 0.0167        # Half width along the y-axis (before rotation)
angle = np.radians(45)      # 45-degree rotation for diamond shape
cos_angle, sin_angle = np.cos(angle), np.sin(angle)

# Centers for the staggered pattern (adjust Z as needed for each obstacle)
centers_row1 = [(0.714, 0.2474, 0.2378), (0.714, 0.3316, 0.2378), (0.714, 0.4158, 0.2378), (0.714, 0.5, 0.2378), (0.714, 0.5842, 0.2378), (0.714, 0.6684, 0.2378), (0.714, 0.7526, 0.2378)]
# Second row: 8 cuboids, staggered
centers_row2 = [(0.7682, 0.2053, 0.207), (0.7682, 0.2895, 0.207), (0.7682, 0.3737, 0.207), (0.7682, 0.4579, 0.207), (0.7682, 0.5421, 0.207), (0.7682, 0.6263, 0.207), (0.7682, 0.7105, 0.207), (0.7682, 0.7947, 0.207)]
# Third row: 9 cuboids, staggered
centers_row3 = [(0.8224, 0.1632, 0.2045), (0.8224, 0.2474, 0.2045), (0.8224, 0.3316, 0.2045), (0.8224, 0.4158, 0.2045), (0.8224, 0.5, 0.2045), (0.8224, 0.5842, 0.2045), (0.8224, 0.6684, 0.2045), (0.8224, 0.7526, 0.2045), (0.8224, 0.8368, 0.2045)]

# Function to add a diamond-shaped cuboid
def add_diamond_cuboid(Z, center_x, center_y, base_z, height, half_width_x, half_width_y):
    # Rotate coordinates for diamond shape
    X_rotated = (X - center_x) * cos_angle + (Y - center_y) * sin_angle
    Y_rotated = -(X - center_x) * sin_angle + (Y - center_y) * cos_angle
    
    # Create mask for the diamond shape
    cuboid_mask = (np.abs(X_rotated) <= half_width_x) & (np.abs(Y_rotated) <= half_width_y)
    Z_cuboid = np.zeros_like(Z)
    Z_cuboid[cuboid_mask] = base_z + height
    return np.maximum(Z, Z_cuboid)

# Add all diamond obstacles in the staggered pattern
Z_combined = Z.copy()
for center_x, center_y, base_z in centers_row1 + centers_row2 + centers_row3:
    Z_combined = add_diamond_cuboid(Z_combined, center_x, center_y, base_z, cuboid_height, half_width_x, half_width_y)

# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)

# Write to GeoTIFF file
with rasterio.open('./array_diamond_cuboid_obstacles.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)

