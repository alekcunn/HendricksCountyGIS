import re
import sys

streets = []

def getStreetNames(fileContent):
    '''
        This is a function that uses regex to find all ways with the highway key
        and all addr:street tags in the fileContent. It then adds the name to the list
        if it is not already in the list. The function also prints the list of streets.

        NOTE: this function only prints the list of streets. I used out-file on powershell

        :param fileContent: The content of the file to search through.
        :return: A list of all the street names found in the fileContent.
    '''
    regex = r"<tag k='addr:street' v='(.*?)' />"
    matches = re.findall(regex, fileContent)

    for match in matches:
        if match not in streets:
            streets.append(match)

    regex = r"<way\s+[^>]*>[\s\S]*?<tag\s+k='highway'[^>]*>[\s\S]*?</way>"

    highway_matches = re.findall(regex, fileContent)
    for highway in highway_matches:
        regex = r"<tag k='name' v='(.*?)' />"
        matches = re.findall(regex, highway)
        for match in matches:
            if match not in streets:
                streets.append(match)
    print(streets)

    return streets


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
    else:
        filePath = '../export.osm'

    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            fileContent = file.read()
        getStreetNames(fileContent)
        
    except FileNotFoundError:
        print(f"Error: File not found at {filePath}")
        sys.exit(1)

