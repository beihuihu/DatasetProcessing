# Set environment settings
import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

start = time.time()
# load input features and make layer
base_dir = 'D:\postprocess'
#target_region = 'southern_america_2'
#origin_region_list=['southern_america_1']
target_region = 'northern_america_1'
origin_region_list=['northern_america_2','southern_america_1']
#target_region = 'northern_america_4'
#origin_region_list=['northern_america_5','northern_america_2']
#target_region = 'asia_3'
#origin_region_list=['asia_5','asia_7']
#target_region = 'asia_4'
#origin_region_list=['asia_2','asia_3','asia_5']
#target_region = 'asia_1'
#origin_region_list=['middle_east','asia_2','asia_4','asia_3']
#target_region = 'europe_2'
#origin_region_list=['europe_1','middle_east','asia_2']
#target_region = 'middle_east'
#origin_region_list=['europe_1']
#target_region = 'northern_america_3'
#origin_region_list=['northern_america_5','northern_america_4','northern_america_2','northern_america_1']
#target_region='africa_1'
#origin_region_list=['africa_2','middle_east','europe_1']
#target_region='africa_3'
#origin_region_list=['africa_2']
intersect_polygon_list=[]
print(target_region)

masked_shp_dn1_merge_path = base_dir + '/shp_dn1_merge.gdb'
arcpy.env.workspace = masked_shp_dn1_merge_path

target_region_file ='lakes_{}_raw_dissolved' .format(target_region)# os.path.join(masked_shp_dn1_merge_path,'lakes_{}_raw_merged_dissolved' .format(target_region))#version dissolve geometry shp:copy_sldissolve.shp
target_region_layer='target_region_layer'
arcpy.MakeFeatureLayer_management(target_region_file, target_region_layer)


for origin_region in origin_region_list:
    print('select polygons in region:'+ origin_region)
    origin_region_file='lakes_{}_raw_dissolved' .format(origin_region)#os.path.join(masked_shp_dn1_merge_path,'lakes_{}_raw_merged_dissolved' .format(origin_region))
    origin_region_layer='origin_region_layer'
    arcpy.MakeFeatureLayer_management(origin_region_file,origin_region_layer)

    arcpy.SelectLayerByLocation_management(origin_region_layer, 'INTERSECT',target_region_layer )#select lake interect with origin polygon
    output_file='lakes_{}_interect_with_{}' .format(origin_region,target_region)
    arcpy.CopyFeatures_management(origin_region_layer,output_file)
    intersect_polygon_list.append(output_file)
    arcpy.DeleteFeatures_management(origin_region_layer)


