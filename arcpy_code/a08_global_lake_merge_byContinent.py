import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

# load input features and make layer
version='v13_241021'
stastic_v=''#f'{version}_v2'
output_dir = os.path.join(r'J:\lakemapping\postprocess',version)

auxiliary_dataset_gdb=r'D:\postprocess\v240220\auxiliary_dataset.gdb'
after_mask_gdb=os.path.join(output_dir,'3_polygon_after_rivermask.gdb')
stastics_gdb=os.path.join(output_dir,'0_summary_stastics.gdb')
polygon_iwR_gdb=os.path.join(output_dir,'2_polygon_iw_River.gdb')
mwBL_gdb=os.path.join(output_dir,'4_polygon_afm_mergeWith_BigLake.gdb')
mwBG_gdb=os.path.join(output_dir,'5_polygon_afm_mwBL_BigGLAKES.gdb')
mwPLD_gdb=os.path.join(output_dir,'5_polygon_afm_mwBL_BigPLD.gdb')
excel_dir=os.path.join(output_dir,'stastics_excel')

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)

lakes_iwBR=os.path.join(polygon_iwR_gdb,'total_iwBR_arm_SJ')
total_lakes_arm=os.path.join(polygon_iwR_gdb,'total_lakes_arm')
lakes_iwBR_afterMask=os.path.join(after_mask_gdb,'lakes_iwBR_afterMask')
lakes_iwBR_lyr='lakes_iwBR'
total_lakes_arm_lyr='lakes_arm'
lakes_iwBR_afm_lyr='lakes_iwBR_afm'

a_iwBL_merge_with_BL_raw=os.path.join(after_mask_gdb,'a_total_lakes_afm_iwBL_merge_with_BigLakes_raw')
a_iwBL_merge_with_BL=os.path.join(after_mask_gdb,'a_total_lakes_afm_iwBL_merge_with_BigLakes')
a_iwBL_merge_with_BL_raw_lyr='a_lakes_afm_iwBL_mw_BL_raw'
a_iwBL_merge_with_BL_lyr='a_lakes_afm_iwBL_mw_BL'

b_iwBG=os.path.join(mwBL_gdb,'b_total_lakes_afm_mwBL_iwBG')
b_iwBG_point=os.path.join(mwBL_gdb,'b_total_lakes_afm_mwBL_iwBG_point')
b_iwBG_lyr='b_lakes_afm_mwBL_iwBG'
b_iwBG_point_lyr='b_lakes_afm_mwBL_iwBG_point'


b_iwBG_merge_with_BG_raw=os.path.join(mwBL_gdb,'b_total_lakes_afm_mwBL_iwBG_merge_with_BG_raw')
b_iwBG_merge_with_BG=os.path.join(mwBL_gdb,'b_total_lakes_afm_mwBL_iwBG_merge_with_BG')
b_iwBG_merge_with_BG_raw_lyr='b_lakes_afm_mwBL_iwBG_mw_BG_raw'
b_iwBG_merge_with_BG_lyr='b_lakes_afm_mwBL_iwBG_mw_BG'

b_iwBG_merge_with_BG_SJ=os.path.join(mwBL_gdb,'b_iwBG_merge_with_BG_SJ')
b_iwBG_merge_with_BG_SJ_SJ=os.path.join(mwBL_gdb,'b_iwBG_merge_with_BG_SJ_SJ')
b_iwBG_merge_with_BG_SJ_dissolve=os.path.join(mwBL_gdb,'b_iwBG_merge_with_BG_SJ_dissolve')
b_iwBG_merge_with_BG_SJ_GLAKES_SJ=os.path.join(mwBL_gdb,'b_iwBG_merge_with_BG_SJ_GLAKES_SJ')
b_iwBG_merge_with_BG_final=os.path.join(mwBL_gdb,'b_iwBG_merge_with_BG_final')
b_iwBG_merge_with_BG_SJ_lyr='b_lakes_afm_mwBL_iwBG_mw_BG_SJ'
b_iwBG_merge_with_BG_SJ_dissolve_lyr='b_iwBG_merge_with_BG_SJ_dissolve'
b_iwBG_merge_with_BG_SJ_GLAKES_SJ_lyr='b_iwBG_merge_with_BG_SJ_GLAKES_SJ'
b_iwBG_merge_with_BG_final_lyr='b_iwBG_merge_with_BG_final'

big_lakes=os.path.join(after_mask_gdb,f'total_big_lakes')
big_lakes_lyr=f'big_lakes'
GLAKES_gte1_Rser=os.path.join(mwBL_gdb,'GLAKES_gte1_Rser')
GLAKES_gte1_Rser_singlepart=os.path.join(mwBL_gdb,'GLAKES_gte1_Rser_singlepart')
GLAKES_gte1_Rser_point=os.path.join(mwBL_gdb,'GLAKES_gte1_Rser_point')
GLAKES_gte1_Rser_lyr='GLAKES_gte1_Rser'
GLAKES_gte1_Rser_point_lyr='GLAKES_gte1_Rser_point'

osm_reservoir=os.path.join(auxiliary_dataset_gdb,'osm_natural_water_reservoir')
arcpy.MakeFeatureLayer_management(osm_reservoir,'osm_reservoir')

GeoDAR=r'D:\lakemapping\0_auxiliary_data\GeoDAR\GeoDAR_v10_v11\GeoDAR_v11_reservoirs.shp'
arcpy.MakeFeatureLayer_management(GeoDAR,'GeoDAR')

GLAKES_Res=os.path.join(auxiliary_dataset_gdb,'GLAKES_Res')
arcpy.MakeFeatureLayer_management(GLAKES_Res,'GLAKES_Res')

GLAKES_natural_lake=os.path.join(auxiliary_dataset_gdb,'GLAKES_gte1_natural_lake')
arcpy.MakeFeatureLayer_management(GLAKES_natural_lake,'GLAKES_natural_lake')

arcpy.MakeFeatureLayer_management(GLAKES_gte1_Rser,GLAKES_gte1_Rser_lyr)

eight_continents=['Asia','Siberia','Africa','Europe','Oceania_Anta','North_America','Arctic','South_America']

# for i in range(0,8):
#     continent=eight_continents[i]
#     print(continent)
#     lakes_niwBR=os.path.join(polygon_iwR_gdb,'lakes_'+continent+'_niwBR')
#     lakes_niwBR_lyr='lakes_'+continent+'_niwBR'
#     lakes_niwBR_afm_lyr='lakes_'+continent+'_niwBR_afm'
#     lakes_niwBR_afm=os.path.join(after_mask_gdb,'lakes_'+continent+'_niwBR_afterMask')
#     arcpy.MakeFeatureLayer_management(lakes_niwBR,lakes_niwBR_lyr)
#     selectByAttribute(lakes_niwBR_lyr,'NEW_SELECTION','"operate"<> 0 or operate IS NULL')
#     arcpy.conversion.ExportFeatures(lakes_niwBR_lyr,lakes_niwBR_afm)
#     arcpy.MakeFeatureLayer_management(lakes_niwBR_afm,lakes_niwBR_afm_lyr)
#     out_table=os.path.join(stastics_gdb,f'{stastic_v}_{continent}_niwBR_afm_stastics')
#     arcpy.analysis.Statistics(lakes_niwBR_afm_lyr, out_table, [['area',"sum"]], ['iwBL']) 

arcpy.MakeFeatureLayer_management(a_iwBL_merge_with_BL, a_iwBL_merge_with_BL_lyr)
arcpy.MakeFeatureLayer_management(lakes_iwBR_afterMask,lakes_iwBR_afm_lyr)

for i in range(6,7):
    continent=eight_continents[i]
    print(continent)
    selectByAttribute(a_iwBL_merge_with_BL_lyr,'NEW_SELECTION',f"Continent = '{continent}'")
    
    selectByAttribute(lakes_iwBR_afm_lyr,'NEW_SELECTION',f"iwBL = 0 AND Continent = '{continent}'")
    lakes_niwBR_afm=os.path.join(after_mask_gdb,'lakes_'+continent+'_niwBR_afterMask')
    lakes_niwBR_afm_lyr='lakes_'+continent+'_niwBR_afm'
    arcpy.MakeFeatureLayer_management(lakes_niwBR_afm,lakes_niwBR_afm_lyr)
    
    selectByAttribute(lakes_niwBR_afm_lyr,'NEW_SELECTION',f"iwBL = 0")
    b_lake_afm_merge_with_BL=os.path.join(mwBL_gdb,f'b{i+1}_{continent}_polygon_afm_mwBL')
    b_lake_afm_merge_with_BL_lyr=f'b{i+1}_{continent}_lake_afm_merge_with_BL'
    
    field_list=['area','operate','iwBL','flag']
    fieldmappings = arcpy.FieldMappings()
    fieldmappings_all = arcpy.FieldMappings()
    fieldmappings_all.addTable(lakes_niwBR_afm_lyr)
    for field_i in field_list:
        field_idx = fieldmappings_all.findFieldMapIndex(field_i)
        fieldmappings.addFieldMap(fieldmappings_all.getFieldMap(field_idx))
        
    arcpy.Merge_management([lakes_niwBR_afm_lyr,a_iwBL_merge_with_BL_lyr,lakes_iwBR_afm_lyr],b_lake_afm_merge_with_BL,field_mappings=fieldmappings)
    arcpy.MakeFeatureLayer_management(b_lake_afm_merge_with_BL, b_lake_afm_merge_with_BL_lyr)
#     选出和big glakes合并的湖泊及原先flag=3、4的湖泊，赋值2.5
    selectByAttribute(b_lake_afm_merge_with_BL_lyr,'NEW_SELECTION','flag > 2 OR flag = 0 OR flag IS NULL')
    selectByLocation(b_lake_afm_merge_with_BL_lyr, 'INTERSECT', GLAKES_gte1_Rser_lyr,'SUBSET_SELECTION')
    calculateField(b_lake_afm_merge_with_BL_lyr, "flag",2.5)
    # selectByAttribute(b_lake_afm_merge_with_BL_lyr,'NEW_SELECTION','')
    # out_table=os.path.join(stastics_gdb,f'{stastic_v}_{continent}_lakes_merge_with_BL_stastics')
    # arcpy.analysis.Statistics(b_lake_afm_merge_with_BL_lyr, out_table, [['area',"sum"]], ['flag']) 