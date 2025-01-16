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
# base_dir = 'J:\lakemapping\postprocess\补充'
base_dir=r'D:\lakemapping\4_prediction\model0130\sampleV8\test_buffer_0_02degree'
# predicted_image_dir =r'J:\lakemapping\postprocess\补充\tif'
# tif2shp = r'J:\lakemapping\postprocess\补充\tif2shp'
# tif2shp_dn1_path = r'J:\lakemapping\postprocess\补充\tif2shp_dn1'

predicted_image_dir =base_dir+r'\result\iew25'
tif2shp =predicted_image_dir+r'\tif2shp'
tif2shp_dn1_path = predicted_image_dir+r'\tif2shp_dn1'
if not os.path.exists(tif2shp):
    os.makedirs(tif2shp)

if not os.path.exists(tif2shp_dn1_path):
    os.makedirs(tif2shp_dn1_path)

arcpy.env.workspace = predicted_image_dir
tif_list = arcpy.ListRasters()
print(tif_list)
# conversion
# start = time.time()
for i,tif in enumerate(tif_list):
    raster=os.path.join(predicted_image_dir,tif)
    outReclass = Reclassify(raster, "Value",RemapRange([[0, 0.5, 0], [0.5, 1, 1]]))
    shpfile = tif.split(".")[0] + '_2shp.shp'
    shp_path = os.path.join(tif2shp , shpfile)
    if not os.path.exists(shp_path):
        arcpy.RasterToPolygon_conversion(outReclass, shp_path,"NO_SIMPLIFY", "Value")
        shpfile_gridcode1 = tif.split(".")[0] + '_2shp_dn1.shp'
        toshp_gridcode1_path = os.path.join(tif2shp_dn1_path,shpfile_gridcode1)
        #print(toshp_gridcode1_path)
        arcpy.Select_analysis(shp_path, toshp_gridcode1_path, '"gridcode" = 1') # select value=1
        
print('Finish transforming tif to shp and extracting dn1.shp')


end = time.time()
print (end-start)
