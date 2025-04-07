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

# Define grid parameters
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
diameter_main = 0.059
radius_main = diameter_main
center_x_main = 0.814
center_y_main = 0.5
center_z_main = 0.207

diameter_additional = 0.029
radius_additional = diameter_additional 

# First additional semisphere
center_x1 = 0.757
center_y1 = 0.410
center_z1 = 0.233

# Second additional semisphere
center_x2 = 0.757
center_y2 = 0.590
center_z2 = 0.233

# Function to create a semisphere mask
def create_semisphere_mask(X, Y, center_x, center_y, radius, center_z):
    dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    semisphere_mask = dist_from_center <= radius
    Z_semisphere = np.zeros_like(Z)
    Z_semisphere[semisphere_mask] = np.sqrt(radius**2 - dist_from_center[semisphere_mask]**2) + center_z
    return Z_semisphere

# Calculate the semisphere Z-values
Z_semisphere_main = create_semisphere_mask(X, Y, center_x_main, center_y_main, radius_main, center_z_main)
Z_semisphere_1 = create_semisphere_mask(X, Y, center_x1, center_y1, radius_additional, center_z1)
Z_semisphere_2 = create_semisphere_mask(X, Y, center_x2, center_y2, radius_additional, center_z2)

# Combine the semispheres with the polynomial surface
Z_combined = np.maximum(Z, Z_semisphere_main)
Z_combined = np.maximum(Z_combined, Z_semisphere_1)
Z_combined = np.maximum(Z_combined, Z_semisphere_2)

# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)


# Write to GeoTIFF file
with rasterio.open('./polynomial_surface_with_three_semispheres.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)

# Find the index corresponding to x = 0.74
x_target = 0.75
x_index = np.abs(x - x_target).argmin()

# Extract the y and z values at x = 0.74
y_values = y
z_values = Z_combined[:, x_index]

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.plot(y_values, z_values, label=f'Z values at x = {x_target} m')

# Read data from CSV file
#csv_file_path = r'd:\IIT Mandi\obstacle_result\tiff_files\state_profile_at_y_0_5_experiment_1.csv'
#csv_data = read_csv(csv_file_path)
plt.show()
