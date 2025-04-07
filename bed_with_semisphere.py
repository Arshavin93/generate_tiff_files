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

# Function to read data from CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if present
        for row in csv_reader:
            data.append(row)
    return data

# Define grid parameters with fixed cell sizes
cell_size_x = 0.0025
cell_size_y = 0.0025
x = np.linspace(0.0, 1.65, 660)
y = np.linspace(0.0, 1.0, 400)
X, Y = np.meshgrid(x, y)

# Polynomial equation
def polynomial_z(x):
    return 0.1086 * (x**4) - 0.5179 * (x**3) + 1.3434 * (x**2) - 1.6513 * x + 0.8923

# Calculate Z-values using the polynomial equation
Z = polynomial_z(X)

# Semisphere parameters
diameter = 0.059
radius = diameter
center_x = 0.814
center_y = 0.5
center_z = 0.207

# Calculate the semisphere Z-values
dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
semisphere_mask = dist_from_center <= radius
Z_semisphere = np.zeros_like(Z)
Z_semisphere[semisphere_mask] = np.sqrt(radius**2 - dist_from_center[semisphere_mask]**2) + center_z

# Combine the semisphere with the polynomial surface
Z_combined = np.maximum(Z, Z_semisphere)

# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)

# Write to GeoTIFF file
with rasterio.open('./polynomial_surface_with_semisphere.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)

# Find the index corresponding to y = 0.5
y_index = np.argmin(np.abs(y - 0.5))

# Extract z values along the line where y = 0.5
z_values_at_y_0_5 = Z_combined[y_index, :]

plt.plot(x, z_values_at_y_0_5, label='z vs x at y=0.5')

# Read data from CSV file
csv_file_path = r'd:\IIT Mandi\obstacle_result\tiff_files\state_profile_at_y_0_5_experiment_1.csv'
csv_data = read_csv(csv_file_path)

# Extract relevant columns from CSV data
csv_time_array = []
csv_pile_height_values = []
for row in csv_data:
    time_value = float(row[0])  # Assuming time is in the first column
    pile_height_value = float(row[1])  # Assuming pile height is in the second column
    csv_time_array.append(time_value)
    csv_pile_height_values.append(pile_height_value)

# Plot CSV data
plt.plot(csv_time_array, csv_pile_height_values, label='State profile at y=0.5')
plt.legend()
plt.show()

