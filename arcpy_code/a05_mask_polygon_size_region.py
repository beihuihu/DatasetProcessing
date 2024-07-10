# Set environment settings
import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

start = time.time()
# load input features and make layer
base_dir = 'D:\postprocess'
version = 'europe_2'
print(version)

masked_shp_dn1_merge_path = base_dir + '/postprocess.gdb'
lake_dissolved = os.path.join(masked_shp_dn1_merge_path,'lakes_{}_dissolved' .format(version))#version dissolve geometry shp:copy_sldissolve.shp

lake_dissolved_layer='lake_dissolved_lyr'
arcpy.MakeFeatureLayer_management(lake_dissolved, lake_dissolved_layer)

GLAKES_gte1=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\GLAKES_gte1'
arcpy.MakeFeatureLayer_management(GLAKES_gte1,'GLAKES_gte1')

print('select polygons intersect with GLAKES great than 1 km2')
print('calculate area')
arcpy.AddField_management(lake_dissolved_layer, 'area', "Double")########################
arcpy.CalculateField_management(lake_dissolved_layer, "area",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")

oceanline_polygon=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\oceanline_polygon'
arcpy.MakeFeatureLayer_management(oceanline_polygon,'oceanline_polygon')

GRWL_river=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\GRWL_DNRiver'
arcpy.MakeFeatureLayer_management(GRWL_river,'GRWL_river')

osm_river=r'D:\lakemapping\0_auxiliary_data\auxiliary_dataset.gdb\global_osm_rivers'
arcpy.MakeFeatureLayer_management(osm_river,'osm_river')
#delete lake polygon interect with ocean and river


print('start mask')
arcpy.SelectLayerByLocation_management(lake_dissolved_layer, 'INTERSECT', oceanline_polygon)#select lake interect with oceanline polygon
arcpy.CopyFeatures_management(lake_dissolved_layer,os.path.join(masked_shp_dn1_merge_path,lake_dissolved +'_intersect_ocean'))
arcpy.DeleteFeatures_management(lake_dissolved_layer)

arcpy.SelectLayerByLocation_management(lake_dissolved_layer, 'INTERSECT', GRWL_river)#select lake interect with grwl
arcpy.SelectLayerByLocation_management(lake_dissolved_layer, 'INTERSECT', osm_river,selection_type='ADD_TO_SELECTION')
arcpy.CopyFeatures_management(lake_dissolved_layer,os.path.join(masked_shp_dn1_merge_path,lake_dissolved +'_intersect_grwl_osm'))
arcpy.DeleteFeatures_management(lake_dissolved_layer)

lak_bt0005_1_shp = lake_dissolved + '_aftermask_bt0005_1'
arcpy.Select_analysis(lake_dissolved_layer, lak_bt0005_1_shp, '"area" >= 0.005 and "area"<1')
#arcpy.DeleteFeatures_management(lake_dissolved_layer)
lake_lge_1_shp = lake_dissolved + '_aftermask_lge1'
arcpy.Select_analysis(lake_dissolved_layer, lake_lge_1_shp, '"area" >= 1')
#arcpy.DeleteFeatures_management(lake_dissolved_layer)
end = time.time()
#os.rename(lake_dissolved,lake_dissolved+'aftermask_lt0005')
print('All processes done: {}s'.format(end-start))
