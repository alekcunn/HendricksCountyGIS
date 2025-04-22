import geopandas as gpd
import numpy as np
from shapely.geometry import box

def split_geodataframe_into_grid(gdf, grid_size_x, grid_size_y, output_path_template):
    """
    Split a GeoDataFrame into a grid and save each cell as a separate file.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        The GeoDataFrame to split
    grid_size_x, grid_size_y : int
        Number of grid cells in x and y direction
    output_path_template : str
        Template for output files (e.g., "grid_{x}_{y}.geojson")
    """
    # Get the bounds of the entire dataset
    minx, miny, maxx, maxy = gdf.total_bounds
    
    # Calculate cell dimensions
    cell_width = (maxx - minx) / grid_size_x
    cell_height = (maxy - miny) / grid_size_y
    
    # Create grid cells and process each one
    for i in range(grid_size_x):
        for j in range(grid_size_y):
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

# Example usage
gdf = gpd.read_file("./IndianaMapDS-current.geojson")
split_geodataframe_into_grid(gdf, 10, 10, "output/grid_{x}_{y}.geojson")