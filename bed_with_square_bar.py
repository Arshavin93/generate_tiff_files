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
cell_size_x = 0.0028
cell_size_y = 0.0028

x = np.linspace(-0.098, 1.75, 660)
y = np.linspace(-0.06, 1.06, 400)
X, Y = np.meshgrid(x, y)

# Polynomial equation
def polynomial_z(x):
    return 0.1086 * (x**4) - 0.5179 * (x**3) + 1.3434 * (x**2) - 1.6513 * x + 0.8923

# Calculate Z-values using the polynomial equation
Z = polynomial_z(X)

# Define square bar parameters
square_side_length = 0.027
bar_start_x = 0.629
bar_end_x = bar_start_x + square_side_length
bar_z = 0.285

# Identify the indices in the grid where the square bar will be placed
x_indices = np.where((x >= bar_start_x) & (x <= bar_end_x))[0]
y_indices = np.arange(len(y))  # Since the bar extends fully in the y-direction

# Create the square bar in the Z_combined matrix
for xi in x_indices:
    for yi in y_indices:
        Z[yi, xi] = polynomial_z(x[xi]) + square_side_length

# Combine the bar with the polynomial surface
Z_combined = Z

# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)

# Write to GeoTIFF file
with rasterio.open('./polynomial_surface_with_bar_modi.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)

# Find the index corresponding to y = 0.5
y_index = np.argmin(np.abs(y - 0.5))

# Extract z values along the line where y = 0.5
z_values_at_y_0_5 = Z_combined[y_index, :]

plt.plot(x, z_values_at_y_0_5, label='z vs x at y=0.5')

# Read data from CSV file
csv_file_path = r'd:\IIT Mandi\obstacle_result\tiff_files\state_profile_at_y_0_5_experiment_3.csv'
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
plt.plot(csv_time_array, csv_pile_height_values, label = 'State profile at y = 0.5')
plt.legend()
plt.show()
