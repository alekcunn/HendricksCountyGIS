This is my proof of work and attempt at making it easy to collaborate

The steps I have taken so far are:
1. Removed unnecessary fields in qgis (TODO: make it automated)
2. I have added a field that will be used to filter unmatched streets, it will be removed before upload
3. I created a TODO file


4. Continuing. I have created a script that will split the dataset into a 10x10 grid. honoring that my uploads won't be larger than 4mb. The largest chunk of the grid is 8_3 which is 1,202KB .
5. I have completed the first official upload grid_0_0 : https://www.openstreetmap.org/changeset/165176881



In order to assist in progress run the run_tasks.py script. The script will parse the data 

The run task will generate 


I created a visual to see the grid

![Grid of the data](/docs/images/grid_visualization.png)
