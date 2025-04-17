'''
I use this for working on data that shouldn't exist in normal runs
'''

from match_streets import load_geojson, save_geojson

geo = load_geojson('IndianaMapDS-matched.geojson')

for feature in geo['features']:
    if 'properties' in feature and 'GEOCITY2' in feature['properties']:
        feature['properties'].pop('GEOCITY2')

save_geojson(geo, 'IndianaMapDS-matched.geojson')


