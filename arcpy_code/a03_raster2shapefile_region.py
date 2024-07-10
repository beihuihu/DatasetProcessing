# Set environment settings
import arcpy
import os
import time
from arcpy import env
from arcpy.sa import *
arcpy.env.overwriteOutput = True

start = time.time()

arcpy.CheckOutExtension("3D") # Obtain a license for the ArcGIS 3D Analyst extension
arcpy.env.overwriteOutput = True
base_dir = r'J:\lakemapping\result0318'
region_name='as_4'
#region_name='africa_3'
print(region_name)
predicted_image_dir = os.path.join(base_dir,region_name)
tif2shp = os.path.join(predicted_image_dir,'tif2shp')
tif2shp_dn1_path = os.path.join(predicted_image_dir,'tif2shp_dn1')
#print(tif2shp)
if not os.path.exists(tif2shp):
    os.makedirs(tif2shp)
if not os.path.exists(tif2shp_dn1_path):
    os.makedirs(tif2shp_dn1_path)
arcpy.env.workspace = predicted_image_dir
tif_list = arcpy.ListRasters()
# conversion
start = time.time()
for i,tif in enumerate(tif_list):
    print(i, tif)
    shpfile = tif.split(".")[0] + '_2shp.shp'
    shp_path = os.path.join(tif2shp , shpfile)
    if not os.path.exists(shp_path):
        arcpy.RasterToPolygon_conversion(tif, shp_path,"NO_SIMPLIFY", "Value")
        shpfile_gridcode1 = tif.split(".")[0]+'2shp_dn1.shp'
        toshp_gridcode1_path = os.path.join(tif2shp_dn1_path,shpfile_gridcode1)
        #print(toshp_gridcode1_path)
        arcpy.Select_analysis(shp_path, toshp_gridcode1_path, '"gridcode" = 1') # select value=1
end=time.time()
print("Finish:{}".format(end-start))
        
