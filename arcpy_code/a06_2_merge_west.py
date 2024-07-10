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
WH_region_list=['greenland','sa_1','sa_2']    
for i in range(1,7):
    WH_region_list.append(f'na_{i}')
print(WH_region_list)

version='v240706'
merge_dataset=f'4_polygon_after_merge_{version}.gdb'
merge_dir=os.path.join(output_dir,merge_dataset)
if not os.path.exists(merge_dir):
    arcpy.CreateFileGDB_management(output_dir,merge_dataset)

region='WH'#western_hemisphere
region_list=WH_region_list

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)

a1_lakes_afm=os.path.join(merge_dir,f'a1_{region}_lakes_after_mask')
a2_big_lakes=os.path.join(merge_dir,f'a2_{region}_big_lakes')
a3_GLAKES_gte1=os.path.join(merge_dir,'a3_GLAKES_gte1')
a4_GLAKES_lt1=os.path.join(merge_dir,'a4_GLAKES_lt1')
a1_lakes_afm_lyr=f'a1_{region}_lakes_afm'
a2_big_lakes_lyr=f'a2_{region}_big_lakes'
a3_GLAKES_gte1_lyr='a3_GLAKES_gte1'
a4_GLAKES_lt1_lyr='a4_GLAKES_gte1'

a1p1=os.path.join(merge_dir,f'a1p1_{region}_lakes_after_mask_iw_a2')
a1p2=os.path.join(merge_dir,f'a1p2_{region}_lakes_after_mask_niw_a2')
a1p1_merge_with_a2_raw=os.path.join(merge_dir,f'a1p1_{region}_merge_with_a2_raw')
a1p1_merge_with_a2=os.path.join(merge_dir,f'a1p1_{region}_merge_with_a2')
b1_lakes_afm_mergewith_a2=os.path.join(merge_dir,f'b1_{region}_lakes_afm_mergewith_BL')

a1p1_lyr=f'a1p1_{region}'
a1p2_lyr=f'a1p2_{region}'
a1p1_merge_with_a2_raw_lyr=f'a1p1_{region}_merge_with_a2_raw'
a1p1_merge_with_a2_lyr=f'a1p1_{region}_merge_with_a2'
b1_lakes_afm_mergewith_a2_lyr=f'b1_{region}_lakes_afm_mergewith_a2'

b1p1=os.path.join(merge_dir,f'b1p1_{region}_lakes_afm_mergewith_BL_iw_BG')
b1p2=os.path.join(merge_dir,f'b1p2_{region}_lakes_afm_mergewith_BL_niw_BG')

b1p1_lyr=f'b1p1_{region}'
b1p2_lyr=f'b1p2_{region}'

# polygon_afm_list=[]
# big_lake_list=[]
# print('start import region lakes')
# start=time.time()
# for region in region_list:
#     polygon_afm=os.path.join(after_mask_gdb,'lakes_'+region+'_afterMask')
#     arcpy.MakeFeatureLayer_management(polygon_afm,'lakes_'+region+'_afm')
#     polygon_afm_list.append('lakes_'+region+'_afm')
    
# for region in region_list:
#     polygon_big_lake=os.path.join(after_mask_gdb,'big_lakes_'+region)
#     arcpy.MakeFeatureLayer_management(polygon_big_lake,'big_lakes_'+region)
#     big_lake_list.append('big_lakes_'+region)
    
# end=time.time()
# print(f'time:{end-start}s')
# start=time.time()
# print('start merge')
# #把polygon merge到一起
# arcpy.Merge_management(polygon_afm_list,a1_lakes_afm)
# #把与GLAKES要合并的文件相交的polygon merge到一起
# arcpy.Merge_management(big_lake_list,a2_big_lakes)
# end=time.time()
# print(f'time:{end-start}s')

# print('start select and export lakes intersect with big lakes')
# arcpy.MakeFeatureLayer_management(a1_lakes_afm,a1_lakes_afm_lyr)
# arcpy.MakeFeatureLayer_management(a2_big_lakes,a2_big_lakes_lyr)

# arcpy.AddField_management(a1_lakes_afm_lyr, 'iwBL', "Short")
# selectByLocation(a1_lakes_afm_lyr,'INTERSECT',a2_big_lakes_lyr)
# calculateField(a1_lakes_afm_lyr,'iwBL',1)
# selectByAttribute(a1_lakes_afm_lyr,'NEW_SELECTION','"iwBL"=1')
# arcpy.conversion.ExportFeatures(a1_lakes_afm_lyr,a1p1)
# selectByAttribute(a1_lakes_afm_lyr,'SWITCH_SELECTION', '')
# calculateField(a1_lakes_afm_lyr,'iwBL',0)
# arcpy.conversion.ExportFeatures(a1_lakes_afm_lyr,a1p2)
# selectByAttribute(a1_lakes_afm_lyr,'NEW_SELECTION', '')
# out_table_1=os.path.join(stastics_gdb,f'{region}_lakes_afm_stastics' )
# arcpy.analysis.Statistics(a1_lakes_afm_lyr, out_table_1, [['area',"sum"]], ['iwBL']) 

# arcpy.MakeFeatureLayer_management(a1p1,a1p1_lyr)
arcpy.MakeFeatureLayer_management(a1p2,a1p2_lyr)

# print('start merge')
# # 把merge后的文件与big lake文件合并，并融合.为了加快处理速度分了两个部分
# start=time.time()
# arcpy.Merge_management([a1p1_lyr,a2_big_lakes_lyr],a1p1_merge_with_a2_raw)
# arcpy.MakeFeatureLayer_management(a1p1_merge_with_a2_raw, a1p1_merge_with_a2_raw_lyr)#global_lakes_afm_merged_with_GBL
# end=time.time()
# print(f'time:{end-start}s')
# print('start Dissolve')
# arcpy.Dissolve_management(a1p1_merge_with_a2_raw_lyr, a1p1_merge_with_a2,"", "", "SINGLE_PART")#dissolve copylake
arcpy.MakeFeatureLayer_management(a1p1_merge_with_a2, a1p1_merge_with_a2_lyr)
# arcpy.AddField_management(a1p1_merge_with_a2_lyr,"area","Double")
# arcpy.CalculateField_management(a1p1_merge_with_a2_lyr, "area",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
# end2=time.time()
# print(f'time:{end2-end}s')
print('start Merge')
arcpy.MakeFeatureLayer_management(a1p1_merge_with_a2, a1p1_merge_with_a2_lyr)
arcpy.Merge_management([a1p1_merge_with_a2_lyr,a1p2_lyr],b1_lakes_afm_mergewith_a2)
print('start select and export lakes intersect with big GLAKES')
arcpy.MakeFeatureLayer_management(b1_lakes_afm_mergewith_a2, b1_lakes_afm_mergewith_a2_lyr)
arcpy.AddField_management(b1_lakes_afm_mergewith_a2_lyr, 'iwBG', "Short")
arcpy.MakeFeatureLayer_management(a3_GLAKES_gte1,a3_GLAKES_gte1_lyr)
selectByLocation(b1_lakes_afm_mergewith_a2_lyr,'INTERSECT',a3_GLAKES_gte1_lyr)
calculateField(b1_lakes_afm_mergewith_a2_lyr,'iwBG',1)
# selectByAttribute(b1_lakes_afm_mergewith_a2_lyr,'NEW_SELECTION','"iwBG"=1')
arcpy.conversion.ExportFeatures(b1_lakes_afm_mergewith_a2_lyr,b1p1)
selectByAttribute(b1_lakes_afm_mergewith_a2_lyr,'SWITCH_SELECTION', '')
calculateField(b1_lakes_afm_mergewith_a2_lyr,'iwBG',0)
arcpy.conversion.ExportFeatures(b1_lakes_afm_mergewith_a2_lyr,b1p2)
selectByAttribute(b1_lakes_afm_mergewith_a2_lyr,'NEW_SELECTION', '')
out_table_2=os.path.join(stastics_gdb,f'{region}_lakes_afm_mergewith_BL_stastics' )
arcpy.analysis.Statistics(b1_lakes_afm_mergewith_a2_lyr, out_table_2, [['area',"sum"]], ['iwBG']) 