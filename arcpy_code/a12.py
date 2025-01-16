import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True
# load input features and make layer

version='v16_250104'
sub_v=''
stastic_v=f'{version}{sub_v}'
output_dir = os.path.join(r'J:\lakemapping\postprocess',version)

auxiliary_dataset_gdb=r'J:\lakemapping\auxiliary_dataset.gdb'
stastics_gdb=os.path.join(output_dir,f'0_summary_stastics{sub_v}.gdb')
river_mask_gdb=os.path.join(output_dir,'2_polygon_iw_River.gdb')
after_mask_gdb=os.path.join(output_dir,f'3_polygon_after_rivermask.gdb')
mwBL_gdb=os.path.join(output_dir,f'4_polygon_afm_mergeWith_BigLake.gdb')
merge_data_gdb=os.path.join(output_dir,f'4_merge_process.gdb')
merge_gdb=os.path.join(output_dir,f'5_polygon_afm_mergeWith_GLAKES_PLD.gdb')
point_gdb=os.path.join(output_dir,f'6_point{sub_v}.gdb')
excel_dir=os.path.join(output_dir,f'stastics_excel{sub_v}')
os.makedirs(excel_dir, exist_ok=True)
new_PLD_gdb=r'J:\lakemapping\PLD\PLD.gdb'
temp_gdb=os.path.join(output_dir,f'7_correct_temp_file{sub_v}.gdb')

lakes_iwBR_SJ=os.path.join(river_mask_gdb,'total_iwBR_arm_SJ')
total_lakes_arm=os.path.join(river_mask_gdb,'total_lakes_arm_singlepart')
lakes_iwBR_afterMask=os.path.join(after_mask_gdb,'lakes_iwBR_afterMask')
total_lakes_arm_lyr='lakes_arm'
lakes_iwBR_SJ_lyr='lakes_iwBR_arm_SJ'
lakes_iwBR_afm_lyr='lakes_iwBR_afm'

a_iwBL_merge_with_BL_raw=os.path.join(after_mask_gdb,'a_total_lakes_afm_iwBL_merge_with_BigLakes_raw')
a_iwBL_merge_with_BL=os.path.join(after_mask_gdb,'a_total_lakes_afm_iwBL_merge_with_BigLakes')
a_iwBL_merge_with_BL_raw_lyr='a_lakes_afm_iwBL_mw_BL_raw'
a_iwBL_merge_with_BL_lyr='a_lakes_afm_iwBL_mw_BL'

big_lakes=os.path.join(after_mask_gdb,f'total_big_lakes')
big_lakes_lyr=f'big_lakes'

three_dataset_dissolve_SJ=os.path.join(merge_data_gdb,'three_dataset_dissolve_SJ')
three_dataset_dissolve_SJ_lyr=f'three_dataset_dissolve_SJ'
three_dataset_dissolve_SJ_SJ=os.path.join(merge_data_gdb,'three_dataset_dissolve_SJ_SJ')
three_dataset_dissolve_SJ_SJ_lyr='three_dataset_dissolve_SJ_SJ'

PLD_Arid=os.path.join(merge_data_gdb,'PLD_Arid')
PLD_Arid_point=os.path.join(merge_data_gdb,'PLD_Arid_point')

Arid_region=r'D:\lakemapping\0_auxiliary_data\AI\Global-AI_ET0_annual_v3\Global-AI_ET0_v3_annual\Global_AI_Reclassify_Clip_simple.shp'
Arid_region_lyr='Global_AI_Reclassify_Clip_simple'

three_dataset_merge=os.path.join(merge_data_gdb,'three_dataset_merge')
three_dataset_merge_lyr=f'three_dataset_merge'
three_dataset_dissolve=os.path.join(merge_data_gdb,'three_dataset_dissolve')
three_dataset_dissolve_lyr=f'three_dataset_dissolve'

b_merge_file=os.path.join(merge_data_gdb,'b_for_merge')
b_merge_file_point=os.path.join(merge_data_gdb,'b_for_merge_point')

three_dataset_dissolve_for_merge=os.path.join(merge_data_gdb,'three_dataset_dissolve_for_merge')
b_merge_layer='three_dataset_dissolve_for_merge'

GLAKES_gte1_Rser=os.path.join(merge_data_gdb,'GLAKES_gte1_Rser_eraser')
GLAKES_gte1_Rser_lyr='GLAKES_gte1_Rser'

GLAKES_merge_file=os.path.join(merge_data_gdb,'GLAKES_for_merge')
GLAKES_merge_file_point=os.path.join(merge_data_gdb,'GLAKES_for_merge_point')

pond_region=r'D:\lakemapping\10_paper_writting\figure\8_visualize.gdb\Region_1_pond_for_GLAKES_merge'
GLAKES_merge_file_lyr='GLAKES_for_merge'
GLAKES_merge_file_point_lyr='GLAKES_for_merge_point'


GLAKES_Res=os.path.join(auxiliary_dataset_gdb,'GLAKES_Res')
arcpy.MakeFeatureLayer_management(GLAKES_Res,'GLAKES_Res')

osm_reservoir=os.path.join(auxiliary_dataset_gdb,'osm_natural_water_reservoir')
arcpy.MakeFeatureLayer_management(osm_reservoir,'osm_reservoir')

GeoDAR=r'D:\lakemapping\0_auxiliary_data\GeoDAR\GeoDAR_v10_v11\GeoDAR_v11_reservoirs.shp'
arcpy.MakeFeatureLayer_management(GeoDAR,'GeoDAR')

continent=r'D:\lakemapping\0_auxiliary_data\World_Continents\World_Continents.shp'
continent_lyr='continent'
arcpy.MakeFeatureLayer_management(continent,continent_lyr)

ar=os.path.join(auxiliary_dataset_gdb,'ar')
arcpy.MakeFeatureLayer_management(ar,'ar')

ar=os.path.join(auxiliary_dataset_gdb,'si')
arcpy.MakeFeatureLayer_management(ar,'si')

seven_continents=['Asia','Africa','Europe','Oceania_Anta','North_America','South_America']
eight_continents=['Asia','Siberia','Africa','Europe','Oceania_Anta','North_America','Arctic','South_America']

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)


def add_Res_flag(inputFeature):
    selectByAttribute(inputFeature,'NEW_SELECTION', 'flag IS NULL OR "flag" <= 1 ')
    selectByLocation(inputFeature,'INTERSECT',GeoDAR,'SUBSET_SELECTION')
    arcpy.CalculateField_management(inputFeature, 'flag',  4)

    selectByAttribute(inputFeature,'NEW_SELECTION', 'flag IS NULL OR "flag" <= 1 ')
    selectByLocation(inputFeature,'INTERSECT',osm_reservoir,'SUBSET_SELECTION')
    arcpy.CalculateField_management(inputFeature, 'flag',  3)


def cal_continent(lyr):
    arcpy.AddField_management(lyr, 'Continent', "Text")
    for i in range(0,6):
        continent=seven_continents[i]
        selectByAttribute(continent_lyr,'NEW_SELECTION',f"Continent = '{continent}'")
        selectByAttribute(lyr,'NEW_SELECTION',"Continent IS NULL")
        selectByLocation(lyr,'HAVE_THEIR_CENTER_IN',continent_lyr,'SUBSET_SELECTION')
        calculateField(lyr,'Continent',f"'{continent}'")
    selectByAttribute(lyr,'NEW_SELECTION',"Continent = 'Asia'")
    selectByLocation(lyr,'HAVE_THEIR_CENTER_IN','si','SUBSET_SELECTION')
    arcpy.CalculateField_management(lyr, "continent","'Siberia'")
    selectByLocation(lyr,'HAVE_THEIR_CENTER_IN','ar','NEW_SELECTION')
    arcpy.CalculateField_management(lyr, "Continent","'Arctic'")

def cal_lake_type(lyr,area_column):
    lake_list=[0,0.01,0.03,0.1,1,100,1000000]
    arcpy.AddField_management(lyr,'lake_type','Short')
    for i in range(6):
        selectByAttribute(lyr,'NEW_SELECTION',f"{area_column}>={lake_list[i]} AND {area_column}<{lake_list[i+1]}")
        arcpy.CalculateField_management(lyr,'lake_type',i)

## 2.1 获得river mask后结果
# print('start river mask')
# arcpy.MakeFeatureLayer_management(lakes_iwBR_SJ,lakes_iwBR_SJ_lyr)
# arcpy.MakeFeatureLayer_management(total_lakes_arm,total_lakes_arm_lyr)

# out_table=os.path.join(stastics_gdb,'0_iwBR_stastics')
# selectByAttribute(lakes_iwBR_SJ_lyr,'NEW_SELECTION',"")
# arcpy.analysis.Statistics(lakes_iwBR_SJ_lyr, out_table, [['area',"sum"]], ['Continent','operate']) 
# file_name='0_iwBR_stastics.xls'
# Output_Excel_File=os.path.join(excel_dir,file_name)
# arcpy.conversion.TableToExcel(out_table, Output_Excel_File)

# selectByAttribute(lakes_iwBR_SJ_lyr,'NEW_SELECTION','"operate" = 0.5')
# selectByLocation(total_lakes_arm_lyr, 'WITHIN', lakes_iwBR_SJ_lyr,'NEW_SELECTION')
# selectByAttribute(total_lakes_arm_lyr,'SUBSET_SELECTION','"operate" IS NULL')
# selectByAttribute(total_lakes_arm_lyr,'ADD_TO_SELECTION','"operate" = 1')
# selectByAttribute(lakes_iwBR_SJ_lyr,'NEW_SELECTION','"operate">= 1')
# fieldmappings = arcpy.FieldMappings()
# fieldmappings_all = arcpy.FieldMappings()
# fieldmappings_all.addTable(lakes_iwBR_SJ_lyr)#未mask
# fieldmappings_all.addTable(total_lakes_arm_lyr)
# field_list = ['area','flag','Continent','iwBL']
# for field_i in field_list:
#         field_idx = fieldmappings_all.findFieldMapIndex(field_i)
#         fieldmappings.addFieldMap(fieldmappings_all.getFieldMap(field_idx))
# arcpy.Merge_management([lakes_iwBR_SJ_lyr,total_lakes_arm_lyr],lakes_iwBR_afterMask,fieldmappings)

# arcpy.MakeFeatureLayer_management(lakes_iwBR_afterMask,lakes_iwBR_afm_lyr)
# selectByAttribute(lakes_iwBR_afm_lyr,'NEW_SELECTION','area IS NULL')
# arcpy.CalculateField_management(lakes_iwBR_afm_lyr, "area",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")

# arcpy.MakeFeatureLayer_management(big_lakes,big_lakes_lyr)
# selectByLocation(lakes_iwBR_afm_lyr, 'INTERSECT', big_lakes_lyr,'NEW_SELECTION')
# # arcpy.AddField_management(lakes_iwBR_afm_lyr, 'iwBL', "short")
# calculateField(lakes_iwBR_afm_lyr, 'iwBL',1)
# selectByAttribute(lakes_iwBR_afm_lyr,'SWITCH_SELECTION',"")
# calculateField(lakes_iwBR_afm_lyr, 'iwBL',0)
# out_table=os.path.join(stastics_gdb,'1_a_iwBR_afm_column_flag_stastics')
# selectByAttribute(lakes_iwBR_afm_lyr,'NEW_SELECTION',"")
# arcpy.analysis.Statistics(lakes_iwBR_afm_lyr, out_table, [['area',"sum"]], ['Continent','flag']) 
# file_name='1_a_iwBR_afm_stastics.xls'
# Output_Excel_File=os.path.join(excel_dir,file_name)
# arcpy.conversion.TableToExcel(out_table, Output_Excel_File)

# out_table=os.path.join(stastics_gdb,'1_a_iwBR_afm_column_iwBL_stastics')
# selectByAttribute(lakes_iwBR_afm_lyr,'NEW_SELECTION',"")
# arcpy.analysis.Statistics(lakes_iwBR_afm_lyr, out_table, [['area',"sum"]], ['Continent','iwBL']) 
# file_name='1_a_iwBR_afm_column_iwBL_stastics.xls'
# Output_Excel_File=os.path.join(excel_dir,file_name)
# arcpy.conversion.TableToExcel(out_table, Output_Excel_File)

## 2.2 与Big Lakes合并
# arcpy.MakeFeatureLayer_management(big_lakes,big_lakes_lyr)
# print('start merge')
# merge_list=[lakes_iwBR_afm_lyr]
# selectByAttribute(lakes_iwBR_afm_lyr,'NEW_SELECTION',"iwBL = 1")
# for continent in eight_continents:
#     lakes_niwBR_afm_lyr='lakes_'+continent+'_niwBR_afm'
#     lakes_niwBR_afm=os.path.join(after_mask_gdb,'lakes_'+continent+'_niwBR_afterMask')
#     arcpy.MakeFeatureLayer_management(lakes_niwBR_afm,lakes_niwBR_afm_lyr)
#     merge_list.append(lakes_niwBR_afm_lyr)
#     selectByAttribute(lakes_niwBR_afm_lyr,'NEW_SELECTION',"iwBL = 1")
# #把iwBL=1的湖泊与big lake文件合并，并融合
# merge_list.append(big_lakes_lyr)
# print(merge_list)

# start=time.time()
# arcpy.Merge_management(merge_list,a_iwBL_merge_with_BL_raw)
# arcpy.MakeFeatureLayer_management(a_iwBL_merge_with_BL_raw, a_iwBL_merge_with_BL_raw_lyr)#global_lakes_afm_merged_with_GBL
# end=time.time()
# print(f'time:{end-start}s')

# start=time.time()
# print('start Dissolve')
# arcpy.Dissolve_management(a_iwBL_merge_with_BL_raw_lyr, a_iwBL_merge_with_BL,"", "", "SINGLE_PART")#dissolve copylake
# arcpy.MakeFeatureLayer_management(a_iwBL_merge_with_BL, a_iwBL_merge_with_BL_lyr)
# arcpy.AddField_management(a_iwBL_merge_with_BL_lyr,"area","Double")
# arcpy.CalculateField_management(a_iwBL_merge_with_BL_lyr, "area",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
# end=time.time()
# print(f'time:{end-start}s')

# arcpy.management.DeleteIdentical(a_iwBL_merge_with_BL_lyr,['area','Shape_Length','Shape_Area'],"5 Meters")

# arcpy.AddField_management(a_iwBL_merge_with_BL_lyr, 'iwBL', "short")
# calculateField(a_iwBL_merge_with_BL_lyr, "iwBL",1)
# cal_continent(a_iwBL_merge_with_BL_lyr)

# arcpy.management.Delete(a_iwBL_merge_with_BL_raw)
# arcpy.AddField_management(a_iwBL_merge_with_BL_lyr, 'flag', "short")
# selectByLocation(a_iwBL_merge_with_BL_lyr, 'INTERSECT', GLAKES_Res)
# calculateField(a_iwBL_merge_with_BL_lyr, "flag",2)
# add_Res_flag(a_iwBL_merge_with_BL_lyr)

# out_table=os.path.join(stastics_gdb,f'a_iwBL_merge_with_BL_stastics')
# selectByAttribute(a_iwBL_merge_with_BL_lyr,'NEW_SELECTION',"")
# arcpy.analysis.Statistics(a_iwBL_merge_with_BL_lyr, out_table, [['area',"sum"]], ['continent']) 
# file_name=f'a_iwBL_merge_with_BL_stastics.xls'
# Output_Excel_File=os.path.join(excel_dir,file_name)
# arcpy.conversion.TableToExcel(out_table, Output_Excel_File)

# arcpy.MakeFeatureLayer_management(GLAKES_merge_file,GLAKES_merge_file_lyr)
# arcpy.MakeFeatureLayer_management(PLD_Arid,'PLD_Arid')

# ## 2.2 与Big Lakes合并
# print('start generate b')

# for i in range(0,8):
#     continent=eight_continents[i]
#     print(continent)
#     selectByAttribute(a_iwBL_merge_with_BL_lyr,'NEW_SELECTION',f"Continent = '{continent}'")

#     selectByAttribute(lakes_iwBR_afm_lyr,'NEW_SELECTION',f"iwBL = 0 AND Continent = '{continent}'")
#     lakes_niwBR_afm=os.path.join(after_mask_gdb,'lakes_'+continent+'_niwBR_afterMask')
#     lakes_niwBR_afm_lyr='lakes_'+continent+'_niwBR_afm'
#     arcpy.MakeFeatureLayer_management(lakes_niwBR_afm,lakes_niwBR_afm_lyr)
    
#     selectByAttribute(lakes_niwBR_afm_lyr,'NEW_SELECTION',f"iwBL = 0")
#     b_lake_afm_merge_with_BL=os.path.join(mwBL_gdb,f'b{i+1}_{continent}_polygon_afm_mwBL')
#     b_lake_afm_merge_with_BL_lyr=f'b{i+1}_{continent}_lake_afm_merge_with_BL'
    
#     field_list=['area','iwBL','flag']
#     fieldmappings = arcpy.FieldMappings()
#     fieldmappings_all = arcpy.FieldMappings()
#     fieldmappings_all.addTable(lakes_niwBR_afm_lyr)
#     for field_i in field_list:
#         field_idx = fieldmappings_all.findFieldMapIndex(field_i)
#         fieldmappings.addFieldMap(fieldmappings_all.getFieldMap(field_idx))
        
#     arcpy.Merge_management([lakes_niwBR_afm_lyr,a_iwBL_merge_with_BL_lyr,lakes_iwBR_afm_lyr],b_lake_afm_merge_with_BL,field_mappings=fieldmappings)
#     arcpy.MakeFeatureLayer_management(b_lake_afm_merge_with_BL, b_lake_afm_merge_with_BL_lyr)

#     arcpy.AddField_management(b_lake_afm_merge_with_BL_lyr, 'lake_area', "DOUBLE")
#     arcpy.CalculateField_management(b_lake_afm_merge_with_BL_lyr, 'lake_area','!area!')
#     cal_lake_type(b_lake_afm_merge_with_BL_lyr,'lake_area')

#     arcpy.AddField_management(b_lake_afm_merge_with_BL_lyr,'mwGLAKES_PLD','Short')
#     selectByLocation(b_lake_afm_merge_with_BL_lyr, 'INTERSECT',GLAKES_merge_file_lyr,'NEW_SELECTION')
#     arcpy.CalculateField_management(b_lake_afm_merge_with_BL_lyr,'mwGLAKES_PLD',1)
#     selectByAttribute(b_lake_afm_merge_with_BL_lyr,'SWITCH_SELECTION',"")
#     selectByLocation(b_lake_afm_merge_with_BL_lyr, 'INTERSECT', 'PLD_Arid','SUBSET_SELECTION')
#     arcpy.CalculateField_management(b_lake_afm_merge_with_BL_lyr,'mwGLAKES_PLD',2)


    # selectByAttribute(b_lake_afm_merge_with_BL_lyr,'NEW_SELECTION','')
    # out_table=os.path.join(stastics_gdb,f'{stastic_v}_b{i+1}_{continent}_lakes_merge_with_BL_stastics')
    # arcpy.analysis.Statistics(b_lake_afm_merge_with_BL_lyr, out_table, [['area',"sum"]], ['flag']) 

# merge_list=[]
# for i in range(0,8):
#     continent=eight_continents[i]
#     b_lake_afm_merge_with_BL=os.path.join(mwBL_gdb,f'b{i+1}_{continent}_polygon_afm_mwBL')
#     b_lake_afm_merge_with_BL_lyr=f'b{i+1}_{continent}_lake_afm_merge_with_BL'
#     selectByAttribute(b_lake_afm_merge_with_BL_lyr,'NEW_SELECTION','mwGLAKES_PLD>0')
#     merge_list.append(b_lake_afm_merge_with_BL_lyr)
# arcpy.Merge_management(merge_list,b_merge_file)
# arcpy.management.FeatureToPoint(b_merge_file,b_merge_file_point,'INSIDE')

# arcpy.Merge_management([b_merge_file,GLAKES_merge_file,PLD_Arid],three_dataset_merge)
# arcpy.MakeFeatureLayer_management(three_dataset_merge,three_dataset_merge_lyr)
# arcpy.Dissolve_management(three_dataset_merge_lyr, three_dataset_dissolve,"", "", "SINGLE_PART")

# arcpy.MakeFeatureLayer_management(three_dataset_dissolve,three_dataset_dissolve_lyr)
# arcpy.AddField_management(three_dataset_dissolve_lyr,"lake_area","Double")
# arcpy.CalculateField_management(three_dataset_dissolve_lyr, "lake_area",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")


# arcpy.MakeFeatureLayer_management(three_dataset_dissolve_SJ_SJ,three_dataset_dissolve_SJ_SJ_lyr)
# selectByAttribute(three_dataset_dissolve_SJ_SJ_lyr,'NEW_SELECTION','operate IS NULL OR operate>0')
# fieldmappings = arcpy.FieldMappings()
# fieldmappings_all = arcpy.FieldMappings()
# fieldmappings_all.addTable(three_dataset_dissolve_SJ_SJ_lyr)
# field_list=['lake_area','sources','Continent']#,'Arid_flag'
# for field_i in field_list:
#     field_idx = fieldmappings_all.findFieldMapIndex(field_i)
#     field_fieldmap = fieldmappings_all.getFieldMap(field_idx)
#     fieldmappings.addFieldMap(field_fieldmap)
# arcpy.conversion.ExportFeatures(three_dataset_dissolve_SJ_SJ_lyr,three_dataset_dissolve_for_merge,field_mapping=fieldmappings)


arcpy.MakeFeatureLayer_management(three_dataset_dissolve_for_merge,b_merge_layer)
arcpy.MakeFeatureLayer_management(b_merge_file_point,'b_for_merge_point')
# cal_lake_type(b_merge_layer,'lake_area')
# selectByAttribute(b_merge_layer,'NEW_SELECTION','')

arcpy.SelectLayerByLocation_management('b_for_merge_point', 'WITHIN',b_merge_layer,selection_type='NEW_SELECTION',invert_spatial_relationship=True)
for i in range(0,8):
    continent=eight_continents[i]
    print(continent)
    b_lake_afm_merge_with_BL=os.path.join(mwBL_gdb,f'b{i+1}_{continent}_polygon_afm_mwBL')
    b_lake_afm_merge_with_BL_lyr=f'b{i+1}_{continent}_lake_afm_merge_with_BL'
    arcpy.MakeFeatureLayer_management(b_lake_afm_merge_with_BL, b_lake_afm_merge_with_BL_lyr)
    c_lake_afm_mw_GP=os.path.join(merge_gdb,f'c{i+1}_{continent}_lakes')
    c_lake_afm_mw_GP_lyr=f'c{i+1}_{continent}_lakes'

    selectByAttribute(b_lake_afm_merge_with_BL_lyr,'NEW_SELECTION',"mwGLAKES_PLD IS NULL")
    selectByLocation(b_lake_afm_merge_with_BL_lyr, 'CONTAINS', 'b_for_merge_point','ADD_TO_SELECTION')
    selectByAttribute(b_merge_layer,'NEW_SELECTION',f"Continent = '{continent}'")
    field_list=['lake_area','lake_type''sources']#,'Arid_flag'
    fieldmappings = arcpy.FieldMappings()
    fieldmappings_all = arcpy.FieldMappings()
    fieldmappings_all.addTable(b_merge_layer)
    for field_i in field_list:
        field_idx = fieldmappings_all.findFieldMapIndex(field_i)
        fieldmappings.addFieldMap(fieldmappings_all.getFieldMap(field_idx))

    arcpy.Merge_management([b_lake_afm_merge_with_BL_lyr,b_merge_layer],c_lake_afm_mw_GP,field_mappings=fieldmappings)