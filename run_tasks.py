from tasks import match_streets
from tasks.make_smaller_files import split_geodataframe_into_grid

import os

import json
import geopandas as gpd

'''
    this script is the main script for processing the dataset
    it loads the dataset, parses the addresses, and matches the streets

    will eventually be able to run qgis tasks as well
'''

if __name__ == "__main__":
    match_streets.match_streets(osm_path='export-04082025.osm')

    gdf = gpd.read_file("./IndianaMapDS-current.geojson")
    split_geodataframe_into_grid(gdf, grid_size_x=10, grid_size_y=10, output_path_template="output/grid_{x}_{y}.geojson")

    finished_grid = json.load(open("finished_grid.json", "r"))
    finished = finished_grid.keys()
    for i in finished_grid:
        #delete the file if its in the finished grid

        try:
            os.remove(f"output/{i}.geojson")
        except:
            pass
