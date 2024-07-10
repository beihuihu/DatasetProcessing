# Set environment settings
import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

start = time.time()
# load input features and make layer
base_dir = 'E:/new_result'
version = '4001_6000'
print(version)

masked_shp_dn1_merge_path = base_dir + '/shp_dn1_merge.gdb'
print('select the lake intersected with bound ')
lak_dissolved = os.path.join(masked_shp_dn1_merge_path,'lakes_{}_dissolved' .format('4001_5138'))#version dissolve geometry shp:copy_sldissolve.shp

oceanline_polygon=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\oceanline_polygon'
arcpy.MakeFeatureLayer_management(oceanline_polygon,'oceanline_polygon')

GRWL_river=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\GRWL_DNRiver'
arcpy.MakeFeatureLayer_management(GRWL_river,'GRWL_river')

#delete lake polygon interect with ocean and river
lak_dissolved_copy=lak_dissolved+'_copy'#lakes_copy
print('copy dissolved data')
arcpy.CopyFeatures_management(lak_dissolved , lak_dissolved_copy)#lake_shp
lak_dissolved_copy_layer='lak_dissolved_copy'
arcpy.MakeFeatureLayer_management(lak_dissolved_copy, lak_dissolved_copy_layer)

arcpy.SelectLayerByLocation_management(lak_dissolved_copy_layer, 'INTERSECT', oceanline_polygon,search_distance="10 Meters")#select lake interect with oceanline polygon
arcpy.DeleteFeatures_management(lak_dissolved_copy_layer)

arcpy.SelectLayerByLocation_management(lak_dissolved_copy_layer, 'INTERSECT', GRWL_river)#select lake interect with grwl
arcpy.DeleteFeatures_management(lak_dissolved_copy_layer)

lak_final_shp = lak_dissolved + '_bt001_1_remove_ocean_river'
arcpy.Select_analysis(lak_dissolved_copy_layer, lak_final_shp, '"area" >= 0.005 and "area"<1')  #   #########################area>=0.005
# delete intermediate features
print('start delete intermediate features')
arcpy.Delete_management(lak_dissolved_copy)
end = time.time()
print('All processes done: {}s'.format(end-start))
