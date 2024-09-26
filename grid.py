import matplotlib.pyplot as plt
import numpy as np

# Function to create the grid
def make_grid(size):
    outer_dict = dict()
    for i in range(size):
        inner_dict = dict()
        outer_dict[i] = inner_dict
        for j in range(size):
            outer_dict[i][j] = (j, 0)  # Modify as needed to represent each element
    return outer_dict

# Function to convert grid dictionary into a NumPy array
def grid_to_array(grid):
    size = len(grid)
    array = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            array[i][j] = grid[i][j][0]  # Use the value you want to display/color
    return array

# Generate a grid of size 10x10 (or any size)
size = 10
grid = make_grid(size)

# Convert the dictionary to a NumPy array for visualization
grid_array = grid_to_array(grid)

# Visualize the grid using matplotlib
plt.figure(figsize=(6, 6))

# Use imshow to create a grid visualization
plt.imshow(grid_array, cmap='viridis', origin='upper')

# Add color bar for reference
plt.colorbar(label='Value')

# Show the plot
plt.grid(False)  # Turn off the matplotlib grid
plt.show()
