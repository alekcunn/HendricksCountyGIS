from tasks import match_streets

'''
    this script is the main script for processing the dataset
    it loads the dataset, parses the addresses, and matches the streets

    will eventually be able to run qgis tasks as well
'''

if __name__ == "__main__":
    match_streets.match_streets(osm_path='export-04082025.osm',)