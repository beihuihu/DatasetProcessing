import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

# load input features and make layer
output_dir = r'J:\lakemapping\postprocess\v9_240622'
auxiliary_dataset_gdb=r'D:\postprocess\v240220\auxiliary_dataset.gdb'
river_mask_gdb=os.path.join(output_dir,'2_polygon_iw_River.gdb')
after_mask_gdb=os.path.join(output_dir,'3_polygon_after_rivermask.gdb')
stastics_gdb=os.path.join(output_dir,f'0_summary_stastics.gdb')

version='v240706'
merge_dataset=f'4_polygon_after_merge_{version}.gdb'
merge_gdb=os.path.join(output_dir,merge_dataset)
if not os.path.exists(merge_gdb):
    arcpy.CreateFileGDB_management(output_dir,merge_dataset)
final_result_dataset=f'5_final_result_{version}.gdb'
final_result_gdb=os.path.join(output_dir,final_result_dataset)
if not os.path.exists(final_result_gdb):
    arcpy.CreateFileGDB_management(output_dir,final_result_dataset)

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)

a3_GLAKES_gte1=os.path.join(merge_gdb,'a3_GLAKES_gte1')
b1p1_east=os.path.join(merge_gdb,f'b1p1_EH_lakes_afm_mergewith_BL_iw_BG')
b1p2_east=os.path.join(merge_gdb,f'b1p2_EH_lakes_afm_mergewith_BL_niw_BG')
b1p1_west=os.path.join(merge_gdb,f'b1p1_WH_lakes_afm_mergewith_BL_iw_BG') 
b1p2_west=os.path.join(merge_gdb,f'b1p2_WH_lakes_afm_mergewith_BL_niw_BG') 
b1p1_merge_with_a3_raw=os.path.join(merge_gdb,'b1p1_merge_with_a3_raw')
b1p1_merge_with_a3=os.path.join(merge_gdb,'b1p1_merge_with_a3')
c1_global_lakes_after_mask_mergewith_a2_a3=os.path.join(final_result_gdb,'c1_global_lakes_afm_mergewith_BL_BG')

a3_GLAKES_gte1_lyr='a3_GLAKES_gte1'
b1p1_east_lyr=f'b1p1_EH'
b1p2_east_lyr=f'b1p2_EH'
b1p1_west_lyr=f'b1p1_WH' 
b1p2_west_lyr=f'b1p2_WH'
b1p1_merge_with_a3_raw_lyr=f'b1p1_merge_with_a3_raw'
b1p1_merge_with_a3_lyr=f'b1p1_merge_with_a3'
c1_global_lakes_after_mask_mergewith_a2_a3_lyr='c1_global_lakes_afm_mergewith_BL_BG'

start=time.time()
arcpy.MakeFeatureLayer_management(b1p1_west,b1p1_west_lyr)
arcpy.MakeFeatureLayer_management(b1p1_east,b1p1_east_lyr)  
arcpy.MakeFeatureLayer_management(b1p2_west,b1p2_west_lyr)
arcpy.MakeFeatureLayer_management(b1p2_east,b1p2_east_lyr)    
arcpy.MakeFeatureLayer_management(a3_GLAKES_gte1,a3_GLAKES_gte1_lyr)

arcpy.Merge_management([b1p1_west_lyr,b1p1_east_lyr,a3_GLAKES_gte1_lyr],b1p1_merge_with_a3_raw)
arcpy.MakeFeatureLayer_management(b1p1_merge_with_a3_raw, b1p1_merge_with_a3_raw_lyr)#global_lakes_afm_merged_with_GBL
end=time.time()
print(f'time:{end-start}s')
print('start Dissolve')
arcpy.Dissolve_management(b1p1_merge_with_a3_raw_lyr, b1p1_merge_with_a3,"", "", "SINGLE_PART")#dissolve copylake
arcpy.MakeFeatureLayer_management(b1p1_merge_with_a3, b1p1_merge_with_a3_lyr)
arcpy.AddField_management(b1p1_merge_with_a3_lyr,"area","Double")
arcpy.CalculateField_management(b1p1_merge_with_a3_lyr, "area",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
end2=time.time()
print(f'time:{end2-end}s')
print('start Merge')
arcpy.Merge_management([b1p1_merge_with_a3_lyr,b1p2_east_lyr,b1p2_west_lyr],c1_global_lakes_after_mask_mergewith_a2_a3)
arcpy.MakeFeatureLayer_management(c1_global_lakes_after_mask_mergewith_a2_a3, c1_global_lakes_after_mask_mergewith_a2_a3_lyr)
out_table_2=os.path.join(stastics_gdb,f'global_lakes_afm_mergewith_BL_BG_stastics' )
arcpy.analysis.Statistics(c1_global_lakes_after_mask_mergewith_a2_a3_lyr, out_table_2, [['area',"sum"]]) 