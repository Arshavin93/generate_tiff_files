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

# Cylinder parameters
radius = 0.02
height = 0.1

center_x, center_y = 0.814, 0.5
base_z = 0.207  # Z-coordinate of the base of the first cylinder


# Calculate the first cylinder Z-values
dist_from_center1 = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
cylinder_mask1 = dist_from_center1 <= radius
Z_cylinder1 = np.zeros_like(Z)
Z_cylinder1[cylinder_mask1] = base_z + height


# Combine the cylinders with the polynomial surface
Z_combined = np.maximum(Z, Z_cylinder1)

# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)

# Write to GeoTIFF file
with rasterio.open('./cylinder_obstacle.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)


