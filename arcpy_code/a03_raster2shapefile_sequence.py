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
# base_dir = r'F:\result_0303\after_land_mask'
# for i in range(0,1):
# base_dir = r'H:\result_0303\after_river_mask'
# for i in range(7,10):
#     file_name='{}_{}'.format(i*1000+1,(i+1)*1000)
#     print(file_name)
#     predicted_image_dir = os.path.join(base_dir,file_name)
#     tif2shp = os.path.join(predicted_image_dir,'tif2shp')
#     tif2shp_dn1_path = os.path.join(predicted_image_dir.replace('F','J'),file_name)
#     #print(tif2shp)
#     if not os.path.exists(tif2shp):
#         os.makedirs(tif2shp)
#     if not os.path.exists(tif2shp_dn1_path):
#         os.makedirs(tif2shp_dn1_path)
#     arcpy.env.workspace = predicted_image_dir
#     tif_list = arcpy.ListRasters()
#     # conversion
#     start = time.time()
#     for i,tif in enumerate(tif_list):
#         print(i, tif)
#         shpfile = tif.split(".")[0] + '_2shp.shp'
#         shp_path = os.path.join(tif2shp , shpfile)
#         shpfile_gridcode1 = tif.split(".")[0]+'2shp_dn1.shp'
#         toshp_gridcode1_path = os.path.join(tif2shp_dn1_path,shpfile_gridcode1)
#         print(toshp_gridcode1_path)
#         if not os.path.exists(shp_path):
#             arcpy.RasterToPolygon_conversion(tif, shp_path,"NO_SIMPLIFY", "Value")      
#             print(toshp_gridcode1_path)
#             arcpy.Select_analysis(shp_path, toshp_gridcode1_path, '"gridcode" = 1') # select value=1
# end=time.time()
# print("Finish:{}".format(end-start))
        

base_dir=r'F:\result_0303\after_land_mask\1_1000\tif2shp'
for id in range(1,583):
    if os.path.exists(os.path.join(base_dir,f'pre_{id}_alm_2shp.shp')):
        shp=os.path.join(base_dir,f'pre_{id}_alm_2shp.shp')
        print(shp)
        dn1shp=os.path.join(r'J:\result_0303\after_land_mask\sequence',f'1_1000/pre_{id}_alm2shp_dn1.shp')
        arcpy.Select_analysis(shp, dn1shp, '"gridcode" = 1')
end=time.time()
print("Finish:{}".format(end-start))