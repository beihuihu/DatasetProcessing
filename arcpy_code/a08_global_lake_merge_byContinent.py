import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

# load input features and make layer
output_dir = r'J:\lakemapping\postprocess\v10_240710'
after_mask_gdb=os.path.join(output_dir,'3_polygon_after_rivermask.gdb')
stastics_gdb=os.path.join(output_dir,'0_summary_stastics.gdb')
Agdb=os.path.join(output_dir,'a_polygon_after_mask_Continent.gdb')
Bgdb=os.path.join(output_dir,'b_polygon_afm_mergeWith_BigLake_Continent.gdb')
Cgdb=os.path.join(output_dir,'c_polygon_afm_mergeWith_BL_BigGLAKES_Continent.gdb')
if not os.path.exists(Agdb):
    arcpy.CreateFileGDB_management(output_dir,'a_polygon_after_mask_Continent.gdb')
if not os.path.exists(Bgdb):
    arcpy.CreateFileGDB_management(output_dir,'b_polygon_afm_mergeWith_BigLake_Continent.gdb')
if not os.path.exists(Cgdb):
    arcpy.CreateFileGDB_management(output_dir,'c_polygon_afm_mergeWith_BL_BigGLAKES_Continent.gdb')
if not os.path.exists(stastics_gdb):
    arcpy.CreateFileGDB_management(output_dir,'0_summary_stastics.gdb')

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)
region_list=['eu','af','oc','island','greenland','sa_1','sa_2']
for i in range(1,10):
    region_list.append(f'as_{i}')
    
for i in range(1,7):
    region_list.append(f'na_{i}')

big_lakes=os.path.join(Agdb,f'big_lakes')
big_lakes_lyr=f'big_lakes'
GLAKES_gte1=os.path.join(Bgdb,'GLAKES_gte1')
GLAKES_lt1=os.path.join(Bgdb,'GLAKES_lt1')
GLAKES_gte1_lyr='GLAKES_gte1'
GLAKES_lt1_lyr='GLAKES_gte1'

continent=r'D:\lakemapping\0_auxiliary_data\World_Continents\World_Continents.shp'
continent_lyr='continent'
arcpy.MakeFeatureLayer_management(continent,continent_lyr)

GLAKES=r'D:\lakemapping\0_auxiliary_data\GLAKES\GLAKES\GLAKES.gdb\GLAKES'
arcpy.MakeFeatureLayer_management(GLAKES,'GLAKES')

# big_lake_list=[]
# for region in region_list:
#     polygon_big_lake=os.path.join(after_mask_gdb,'big_lakes_'+region)
#     arcpy.MakeFeatureLayer_management(polygon_big_lake,'big_lakes_'+region)
#     big_lake_list.append('big_lakes_'+region)
# arcpy.Merge_management(big_lake_list,big_lakes)

arcpy.MakeFeatureLayer_management(big_lakes,big_lakes_lyr)

seven_continents=['Asia','Africa','Europe','Oceania_Anta','North_America','South_America']
start=time.time()
input_table_afm_list=[]
for region in region_list[17:]:
    lakes_afm=os.path.join(after_mask_gdb,'lakes_'+region+'_afterMask')
    lakes_afm_lyr='lakes_'+region+'_afm'
    arcpy.MakeFeatureLayer_management(lakes_afm,lakes_afm_lyr)
    arcpy.AddField_management(lakes_afm_lyr, 'Continent', "Text")
    arcpy.AddField_management(lakes_afm_lyr, 'iwBL', "Short")
    selectByLocation(lakes_afm_lyr,'INTERSECT',big_lakes_lyr)
    calculateField(lakes_afm_lyr,'iwBL',1)
    for i in range(0,6):
        continent=seven_continents[i]
        selectByAttribute(continent_lyr,'NEW_SELECTION',f"Continent = '{continent}'")
        selectByAttribute(lakes_afm_lyr,'NEW_SELECTION',"Continent IS NULL")
        selectByLocation(lakes_afm_lyr,'HAVE_THEIR_CENTER_IN',continent_lyr,'SUBSET_SELECTION')
        calculateField(lakes_afm_lyr,'Continent',f"'{continent}'")
    selectByAttribute(lakes_afm_lyr,'NEW_SELECTION','')
    out_table=os.path.join(stastics_gdb,f'{region}_afm_by_Continent_stastics')
    input_table_afm_list.append(out_table)
    selectByAttribute(lakes_afm_lyr,'NEW_SELECTION','iwBL IS NULL')
    calculateField(lakes_afm_lyr,'iwBL',0)
    arcpy.analysis.Statistics(lakes_afm_lyr, out_table, [['area',"sum"]], ['Continent']) 
end=time.time()
print(f'time:{end-start}s')