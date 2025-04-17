'''
This script concatenates the street fields into a single field
I used this directly in QGIS so there arent any import statements
'''


layer = iface.activeLayer()
if not layer:
    raise Exception("No active layer found.")


# Start an edit session to modify the layer

features = [feature for feature in layer.getFeatures()] 
layer.startEditing()
layer.addAttribute(QgsField("addr:street ", QVariant.String))

layer.updateFields()

street_index = layer.fields().indexOf("addr:street")

street_fields = ["St_PreMod" , "St_PreDir", "St_PreTyp", "St_PreSep", "St_Name", "St_Pos_Typ", "St_PosDir", "St_PosMod"]

for feature in features:
    print(feature.id())

    #concatentate the street fields into a single string
    street_name = ""
    for field in street_fields:
        street_name += feature[field] + " "


    layer.changeAttributeValue(feature.id(), street_index, street_name)
            
    layer.updateFields()
    layer.commitChanges()