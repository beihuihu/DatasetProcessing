# Set environment settings
import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

start = time.time()
base_dir = r'D:\postprocess'
# load input features and make layer

##id
# start_id=3001
# end_id=start_id+1000
# folder='{}_{}'.format(start_id,end_id)
# print(folder)
# predicted_image_dir = os.path.join(base_dir,'after_mask')
# tif2shp_dn1_path = os.path.join(predicted_image_dir,folder+'/tif2shp_dn1')

##region
region_dir=r'D:\lakemapping\8_postprocess\region'
region_name='africa_2_822'
region=os.path.join(region_dir,region_name)
tif2shp_dn1_path = os.path.join(base_dir,'tif2shp_dn1/{}'.format(region_name))
masked_shp_dn1_merge_path = base_dir + '/shp_dn1_merge.gdb'
if not os.path.exists(masked_shp_dn1_merge_path):
    arcpy.CreateFileGDB_management(base_dir, "shp_dn1_merge.gdb")

arcpy.env.workspace = tif2shp_dn1_path

lak_shp = masked_shp_dn1_merge_path + '/lakes_' +region_name #version
if not os.path.exists(lak_shp):
    mergeshp = arcpy.ListFeatureClasses()
    print('mergeshp:', len(mergeshp))
    arcpy.Merge_management(mergeshp, lak_shp) 

    print('finish merge')
    end = time.time()
    print (end-start)

lak_copy_shp=lak_shp+'_copy'#lakes_copy
print('copy data')
arcpy.CopyFeatures_management(lak_shp ,lak_copy_shp)#lake_shp
lak_copy_lyr = 'lak_copy_lyr'
arcpy.MakeFeatureLayer_management(lak_copy_shp, lak_copy_lyr)

lak_dissolved = lak_shp+'_dissolved'#dissolve geometry shp:copy_sldissolve.shp
print('start Dissolve')
dissolveFields = ["gridcode"]
arcpy.Dissolve_management(lak_copy_lyr, lak_dissolved, dissolveFields, "", "SINGLE_PART", "DISSOLVE_LINES")#dissolve copylake

lak_dissolved_Layer='lak_dissolved_lyr'
arcpy.MakeFeatureLayer_management(lak_dissolved, lak_dissolved_Layer)

arcpy.AddField_management(lak_dissolved_Layer, 'area', "Double")########################
arcpy.CalculateField_management(lak_dissolved_Layer, "area",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
print('finish dissolve')

arcpy.Delete_management(lak_copy_shp)
end = time.time()
print('All processes done: {}s'.format(end-start))
