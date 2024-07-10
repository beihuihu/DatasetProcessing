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
base_dir = 'F:/new_result'

start_id=6001
end_id=start_id+1000

folder='{}_{}'.format(start_id,end_id)
print(folder)
#predicted_image_dir = os.path.join(base_dir,'after_mask')
#tif2shp = os.path.join(predicted_image_dir,folder+'/tif2shp')
#tif2shp_dn1_path = os.path.join(predicted_image_dir,folder+'/tif2shp_dn1')
#tif2shp_ocean_path = os.path.join(predicted_image_dir,folder+'/ocean')
predicted_image_dir =r'D:\postprocess'
tif2shp = os.path.join(predicted_image_dir,'tif2shp')
tif2shp_dn1_path = os.path.join(predicted_image_dir,'tif2shp_dn1')
tif2shp_ocean_path=os.path.join(predicted_image_dir,'ocean')
#print(tif2shp)
if not os.path.exists(tif2shp):
    os.makedirs(tif2shp)

if not os.path.exists(tif2shp_dn1_path):
    os.makedirs(tif2shp_dn1_path)

if not os.path.exists(tif2shp_ocean_path):
    os.makedirs(tif2shp_ocean_path)
arcpy.env.workspace = predicted_image_dir
for i in range(6113,end_id):
    fn_name='pre_{}_masked.tif'.format(i)
    raster=os.path.join(predicted_image_dir,fn_name)
    outReclass = Reclassify(raster, "Value",RemapRange([[0, 0.5, 0], [0.5, 1, 1]]))
    shpfile = fn_name.split(".")[0] + '_2shp.shp'
    shp_path = os.path.join(tif2shp , shpfile)
    if not os.path.exists(shp_path):
        arcpy.RasterToPolygon_conversion(outReclass, shp_path,"NO_SIMPLIFY", "Value")
        shpfile_gridcode1 = 'pre_{}_masked_2shp_dn1.shp'.format(i)
        toshp_gridcode1_path = os.path.join(tif2shp_dn1_path,shpfile_gridcode1)
        #print(toshp_gridcode1_path)
        arcpy.Select_analysis(shp_path, toshp_gridcode1_path, '"gridcode" = 1') # select value=1

        #remove lakes intersect with oceanline
        oceanline_polygon=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\oceanline_polygon'
        arcpy.MakeFeatureLayer_management(oceanline_polygon,'oceanline_polygon')

        toshp_gridcode1_path_layer='toshp_gridcode1_path'
        arcpy.MakeFeatureLayer_management(toshp_gridcode1_path,toshp_gridcode1_path_layer)
        arcpy.SelectLayerByLocation_management(toshp_gridcode1_path_layer, 'INTERSECT', oceanline_polygon,search_distance="10 Meters")#select lake interect with oceanline polygon
        arcpy.CopyFeatures_management(toshp_gridcode1_path_layer,os.path.join(tif2shp_ocean_path,'pre_{}_masked_2shp_ocean.shp'.format(i)))
        arcpy.DeleteFeatures_management(toshp_gridcode1_path_layer)
        print('Finish:', str(i) + '/' + str(end_id-1))
        
print('Finish transforming tif to shp and extracting dn1.shp')


end = time.time()
print (end-start)
