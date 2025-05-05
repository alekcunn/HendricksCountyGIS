import geopandas as gpd
import numpy as np
from shapely.geometry import box
import matplotlib.pyplot as plt
import json

def split_geodataframe_into_grid(gdf, grid_size_x, grid_size_y, output_path_template):
    """
    Split a GeoDataFrame into a grid and save each cell as a separate file, excluding finished cells.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        The GeoDataFrame to split
    grid_size_x, grid_size_y : int
        Number of grid cells in x and y direction
    output_path_template : str
        Template for output files (e.g., "grid_{x}_{y}.geojson")
    """
    # Load finished cells
    with open("./finished-cells.json", "r") as f:
        finished_cells = json.load(f)

    # Get the bounds of the entire dataset
    minx, miny, maxx, maxy = gdf.total_bounds
    
    # Calculate cell dimensions
    cell_width = (maxx - minx) / grid_size_x
    cell_height = (maxy - miny) / grid_size_y
    
    # Create grid cells and process each one
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            # Check if the cell is in finished cells
            cell_key = f"grid_{i}_{j}"
            if cell_key in finished_cells:
                print(f"Skipping finished cell ({i},{j})")
                continue

            # Calculate cell bounds
            cell_minx = minx + i * cell_width
            cell_maxx = minx + (i + 1) * cell_width
            cell_miny = miny + j * cell_height
            cell_maxy = miny + (j + 1) * cell_height
            
            # Create cell polygon
            cell = box(cell_minx, cell_miny, cell_maxx, cell_maxy)
            
            # Get features that intersect with this cell
            cell_gdf = gdf[gdf.intersects(cell)].copy()
            
            # If the cell contains data, save it
            if not cell_gdf.empty:
                output_path = output_path_template.format(x=i, y=j)
                print(f"Saving grid cell ({i},{j}) with {len(cell_gdf)} features to {output_path}")
                cell_gdf.to_file(output_path, driver="GeoJSON")

def visualize_grid(gdf, grid_size_x, grid_size_y, output_image_path):
    """
    Visualize the grid overlaid on the GeoDataFrame and save it as a PNG image.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        The GeoDataFrame to visualize
    grid_size_x, grid_size_y : int
        Number of grid cells in x and y direction
    output_image_path : str
        Path to save the PNG image
    """
    # Load finished cells
    with open("./finished-cells.json", "r") as f:
        finished_cells = json.load(f)

    # Get the bounds of the entire dataset
    minx, miny, maxx, maxy = gdf.total_bounds
    
    # Calculate cell dimensions
    cell_width = (maxx - minx) / grid_size_x
    cell_height = (maxy - miny) / grid_size_y
    
    # Plot the GeoDataFrame
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color='lightgrey', edgecolor='black')
    
    # Add grid cells with transparent green for completed cells
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            cell_minx = minx + i * cell_width
            cell_maxx = minx + (i + 1) * cell_width
            cell_miny = miny + j * cell_height
            cell_maxy = miny + (j + 1) * cell_height
            
            # Check if the cell is completed
            cell_key = f"grid_{i}_{j}"
            if cell_key in finished_cells:
                ax.add_patch(plt.Rectangle(
                    (cell_minx, cell_miny), cell_width, cell_height,
                    color='green', alpha=0.3, edgecolor='none'
                ))
    
    # Add grid lines and labels
    for i in range(grid_size_x + 1):
        x = minx + i * cell_width
        ax.plot([x, x], [miny, maxy], color='red', linewidth=0.5)
    for j in range(grid_size_y + 1):
        y = miny + j * cell_height
        ax.plot([minx, maxx], [y, y], color='red', linewidth=0.5)
    
    # Add labels to each cell
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            cell_center_x = minx + (i + 0.5) * cell_width
            cell_center_y = miny + (j + 0.5) * cell_height
            ax.text(cell_center_x, cell_center_y, f"{i},{j}", color='Red', 
                    fontsize=20, ha='center', va='center', weight='bold')
    
    # Save the image
    plt.title("Grid Visualization")
    plt.savefig(output_image_path, dpi=300)
    plt.close()

# Example usage
gdf = gpd.read_file("./IndianaMapDS-current.geojson")
split_geodataframe_into_grid(gdf, 10, 10, "output/grid_{x}_{y}.geojson")
visualize_grid(gdf, 10, 10, "docs/images/grid_visualization.png")