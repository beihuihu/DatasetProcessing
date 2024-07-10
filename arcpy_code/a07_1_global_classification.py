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
merge_dataset=f'5_polygon_after_merge_{version}.gdb'
classification_dataset=f'5_polygon_after_classification_{version}.gdb'
merge_gdb=os.path.join(output_dir,merge_dataset)
classification_gdb=os.path.join(output_dir,merge_dataset)
if not os.path.exists(classification_dataset):
    arcpy.CreateFileGDB_management(output_dir,classification_dataset)


def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)
b1_EH_lakes_afm_mergewith_a2=os.path.join(merge_gdb,f'b1_EH_lakes_afm_mergewith_BL')
b1_WH_lakes_afm_mergewith_a2=os.path.join(merge_gdb,f'b1_wH_lakes_afm_mergewith_BL')
b1_global_lakes_afm_mergewith_a2=os.path.join(classification_dataset,'b1_global_lakes_afm_mergewith_BL')
c1_global_lakes_afM_mergewith_a2_a3=os.path.join(merge_gdb,'c1_global_lakes_afm_mergewith_BL_BG')
b1_EH_lakes_afm_mergewith_a2_lyr='b1_EH_lakes_afm_mergewith_a2_lyr'
b1_EH_lakes_afm_mergewith_a2_lyr='b1_EH_lakes_afm_mergewith_a2_lyr'
b1_global_lakes_afm_mergewith_a2_lyr='b1_global_lakes_afm_mergewith_a2'
c1_global_lakes_after_mask_mergewith_a2_a3_lyr='c1_global_lakes_afm_mergewith_BL_BG'

start=time.time()

arcpy.Merge_management([b1_EH_lakes_afm_mergewith_a2_lyr,b1_EH_lakes_afm_mergewith_a2_lyr],b1_global_lakes_afm_mergewith_a2)
arcpy.MakeFeatureLayer_management(b1_global_lakes_afm_mergewith_a2, b1_global_lakes_afm_mergewith_a2_lyr)#global_lakes_afm_merged_with_GBL
