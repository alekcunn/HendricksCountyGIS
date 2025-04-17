import json
from get_streets_osm import getStreetNames

# Load GeoJSON data
def load_geojson(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Save GeoJSON data
def save_geojson(data, path):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

# Match streets
def match_streets(DatasetMap = '../IndianaMapDs.geojson', osm_path = '../export.osm', matched_dataset_path = '../IndianaMapDs.geojson', missing_streets_path = './missing_streets.json'):
    '''
        This function matches streets from a GeoJSON file with street names from an OSM file.
        it saves addresses to a new GeoJSON file and adds a "matched" property to each feature.
        If a street name from the GeoJSON file is not found in the OSM data, it is left in place
        and the name is saved to a separate file for further review.

        :param DatasetMap: Path to the GeoJSON file containing street data.
        :param osm_path: Path to the OSM file containing street names.
        :param matched_dataset_path: Path to save the updated GeoJSON file with matched status.
        :param missing_streets_path: Path to save the unmatched streets.

        :return: None
    '''
    geojson_data = load_geojson(DatasetMap)
    print(f"GeoJSON data loaded: {len(geojson_data['features'])} features")

    # Use getStreetNames to get all street names from the OSM data
    with open(osm_path, 'r', encoding='utf-8') as file:
        osm_data = file.read()
        osm_street_names = set(getStreetNames(osm_data))

    print(f"OSM street names loaded: {len(osm_street_names)}")

    matched_streets = set()
    unmatched_streets = set()

    # Extract addr:street values from GeoJSON
    for feature in geojson_data['features']:
        if 'properties' in feature and 'addr:street' in feature['properties']:
            street_name = feature['properties']['addr:street']

            # Check if the street name exists in the OSM street names set
            if street_name in osm_street_names:
                matched_streets.add(street_name)
                feature['properties']['matched'] = True
                # Optionally, remove the matched street from the OSM set
                osm_street_names.remove(street_name)
            else:
                unmatched_streets.add(street_name)
                feature['properties']['matched'] = False

    # Save unmatched streets
    with open(missing_streets_path, 'w', encoding='utf-8') as file:
        json.dump(list(unmatched_streets), file, indent=2)

    # Save updated GeoJSON with matched status
    save_geojson(geojson_data, matched_dataset_path)

    print(f"Matched streets: {len(matched_streets)}")
    print(f"Unmatched streets saved to {missing_streets_path}")
    print(f"Updated GeoJSON with matched status saved to {matched_dataset_path}")


if __name__ == "__main__":
    match_streets()
