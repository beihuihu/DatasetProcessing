# Set environment settings
import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

start = time.time()
# load input features and make layer
base_dir = r'D:\lakemapping\0_auxiliary_data\GLAKES\GLAKES'
GLAKES_path = base_dir + '/GLAKES.gdb'
out_path=GLAKES_path+'GLAKES_interect_with_ocean_10m'
GLAKES = os.path.join(GLAKES_path,'GLAKES')
GLAKES_layer=('GLAKES')
arcpy.MakeFeatureLayer_management(GLAKES,GLAKES_layer)
oceanline_polygon=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\oceanline_polygon'
arcpy.MakeFeatureLayer_management(oceanline_polygon,'oceanline_polygon')

arcpy.SelectLayerByLocation_management(GLAKES_layer, 'INTERSECT', oceanline_polygon,search_distance="10 Meters")#select lake interect with oceanline polygon
arcpy.CopyFeatures_management(GLAKES_layer,out_path)
end = time.time()
print('All processes done: {}s'.format(end))
