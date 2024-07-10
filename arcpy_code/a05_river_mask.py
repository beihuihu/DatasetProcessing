import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True
output_dir = r'J:\lakemapping\postprocess\v9_240622'
auxiliary_dataset_gdb=r'D:\postprocess\v240220\auxiliary_dataset.gdb'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    arcpy.CreateFileGDB_management(output_dir, "1_temp_files.gdb")
    arcpy.CreateFileGDB_management(output_dir, "2_polygon_iw_River.gdb")
    arcpy.CreateFileGDB_management(output_dir, "3_polygon_after_rivermask.gdb")
temp_file_gdb=os.path.join(output_dir,f'1_temp_files.gdb')
river_mask_gdb=os.path.join(output_dir,f'2_polygon_iw_River.gdb')
after_mask_gdb=os.path.join(output_dir,f'3_polygon_after_rivermask.gdb')
region="na_3"
raw_prediction_fn='lakes_'+region
prefix=region

GLAKES_Res=os.path.join(auxiliary_dataset_gdb,'GLAKES_Res')
arcpy.MakeFeatureLayer_management(GLAKES_Res,'GLAKES_Res')

GLAKES_natural_lake=os.path.join(auxiliary_dataset_gdb,'GLAKES_gte1_natural_lake')
arcpy.MakeFeatureLayer_management(GLAKES_natural_lake,'GLAKES_natural_lake')

GLAKES=os.path.join(auxiliary_dataset_gdb,r'D:\lakemapping\0_auxiliary_data\GLAKES\GLAKES\GLAKES.gdb\GLAKES')
arcpy.MakeFeatureLayer_management(GLAKES,'GLAKES')

GRWL_river=os.path.join(auxiliary_dataset_gdb,'GRWL_DNRiver')
arcpy.MakeFeatureLayer_management(GRWL_river,'GRWL_river')

osm_river=os.path.join(auxiliary_dataset_gdb,'osm_natural_water_river')
arcpy.MakeFeatureLayer_management(osm_river,'osm_river')

osm_waterway=os.path.join(auxiliary_dataset_gdb,'osm_waterway_river')
arcpy.MakeFeatureLayer_management(osm_waterway,'osm_waterway')

osm_reservoir=os.path.join(auxiliary_dataset_gdb,'osm_natural_water_reservoir')
arcpy.MakeFeatureLayer_management(osm_reservoir,'osm_reservoir')

GeoDAR=r'D:\lakemapping\0_auxiliary_data\GeoDAR\GeoDAR_v10_v11\GeoDAR_v11_reservoirs.shp'
arcpy.MakeFeatureLayer_management(GeoDAR,'GeoDAR')

lake_iwG=os.path.join(temp_file_gdb,raw_prediction_fn+'_iwG')
lake_niwG=os.path.join(temp_file_gdb,raw_prediction_fn+'_niwG')
lake_waterway_iwG=os.path.join(temp_file_gdb,raw_prediction_fn+'_waterway_iwG')
lake_waterway_niwG=os.path.join(river_mask_gdb,raw_prediction_fn+'_waterway_niwG')
lake_niwR=os.path.join(river_mask_gdb,raw_prediction_fn+'_niwR')

lake_arm_point=os.path.join(temp_file_gdb,raw_prediction_fn+'_arm_point')
lake_arm=os.path.join(river_mask_gdb,raw_prediction_fn+'_arm')
lake_aGm=os.path.join(temp_file_gdb,raw_prediction_fn+'_aGm')
lake_aGm_singlepart=os.path.join(temp_file_gdb,raw_prediction_fn+'_aGm_singlepart')
lake_aGm_point=os.path.join(temp_file_gdb,raw_prediction_fn+'_aGm_point')
lake_waterway_aGm=os.path.join(temp_file_gdb,raw_prediction_fn+'_waterway_aGm')
lake_waterway_aGm_singlepart=os.path.join(temp_file_gdb,raw_prediction_fn+'_waterway_aGm_singlepart')
lake_waterway_aGm_point=os.path.join(temp_file_gdb,raw_prediction_fn+'_waterway_aGm_point')
lake_arm_raw=os.path.join(r'D:\postprocess\v240306\0_raw_prediction.gdb',f'{raw_prediction_fn}_arm')#after River Mask
lake_arm_raw_point=os.path.join(r'D:\postprocess\v240306\0_raw_prediction.gdb',f'{raw_prediction_fn}_arm_point')

lake_iwG_aGm_SJ=lake_iwG+'_temp_SJ'
lake_iwG_arm_SJ=os.path.join(river_mask_gdb,raw_prediction_fn+'_iwG_arm_SJ')
lake_niwG_arm_SJ=os.path.join(river_mask_gdb,raw_prediction_fn+'_niwG_arm_SJ')
lake_waterway_iwG_SJ=os.path.join(river_mask_gdb,raw_prediction_fn+'_waterway_iwG_SJ')

lake_rmO_lyr='lake_rmO' 

lake_iwG_lyr='lake_iwG'
lake_aGm_lyr='lake_aGm'
lake_aGm_singlepart_lyr='lake_aGm_singlepart_lyr'
lake_iwG_arm_SJ_lyr=prefix+'_lake_iwG_arm_SJ'

lake_niwG_lyr='lake_niwG'
lake_niwG_arm_SJ_lyr=prefix+'_lake_niwG_arm_SJ'

lake_arm_raw_lyr='lake_arm_raw'
lake_arm_raw_point_lyr='lake_arm_raw_point_lyr'
lake_arm_point_lyr='lake_arm_point'
lake_arm_lyr=prefix+'_lake_arm'

lake_waterway_iwG_lyr='lake_waterway_iwG'
lake_waterway_iwG_lyr='lake_waterway_iwG'
lake_waterway_aGm_lyr='lake_waterway_aGm'
lake_aGm_point_lyr='lake_aGm_point'
lake_waterway_aGm_singlepart_lyr='lake_waterway_aGm_singlepart'
lake_waterway_aGm_point_lyr='lake_waterway_aGm_point'
lake_waterway_iwG_SJ_lyr=prefix+'_lake_waterway_iwG_SJ'
lake_waterway_niwG_lyr=prefix+'_lake_waterway_niwG'

lake_niwR_lyr='lake_niwR'

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)
    
def GLAKES_join(inputFeature,featureAfterGLAKESMask,outputFeauture,outLayer):
    print('Prepare the fieldmap for GLAKES mask spatial join')
    fieldmappings = arcpy.FieldMappings()
    fieldmappings_all = arcpy.FieldMappings()
    fieldmappings_all.addTable(inputFeature)#未mask
    fieldmappings_all.addTable(featureAfterGLAKESMask)
    field_list = ['area', 'area_aGm','iwG','iwR','flag']
    for field_i in field_list:
        field_idx = fieldmappings_all.findFieldMapIndex(field_i)
        fieldmappings.addFieldMap(fieldmappings_all.getFieldMap(field_idx))

    flag_idx = fieldmappings.findFieldMapIndex("flag")
    flag_fieldmap = fieldmappings.getFieldMap(flag_idx)
    flag_fieldmap.mergeRule = "max"
    fieldmappings.replaceFieldMap(flag_idx, flag_fieldmap)

    area_aGm_idx = fieldmappings.findFieldMapIndex("area_aGm")
    area_aGm_fieldmap = fieldmappings.getFieldMap(area_aGm_idx)
    area_aGm_fieldmap.mergeRule = "sum"
    fieldmappings.replaceFieldMap(area_aGm_idx, area_aGm_fieldmap)

    print('Conduct spatial join')
    arcpy.SpatialJoin_analysis(inputFeature, featureAfterGLAKESMask, outputFeauture, "JOIN_ONE_TO_ONE",
                               "KEEP_ALL", fieldmappings, "CONTAINS")
    lyr=outLayer
    arcpy.MakeFeatureLayer_management(outputFeauture, lyr)
    #计算比例
    arcpy.AddField_management(lyr, 'area_ratio_G', "DOUBLE")#新建字段为面积比例
    arcpy.CalculateField_management(lyr, 'area_ratio_G', '!area_aGm!/!area!', "PYTHON3")

def RiverMaskJoin(inputFeature,featureAfterRiverMask,outputFeauture,field_list,outLayer):
    print('Prepare the fieldmap for river mask spatial join')
    fieldmappings = arcpy.FieldMappings()
    fieldmappings_all = arcpy.FieldMappings()
    fieldmappings_all.addTable(inputFeature)#未mask
    fieldmappings_all.addTable(featureAfterRiverMask)
    for field_i in field_list:
        field_idx = fieldmappings_all.findFieldMapIndex(field_i)
        fieldmappings.addFieldMap(fieldmappings_all.getFieldMap(field_idx))
    area_idx = fieldmappings.findFieldMapIndex("area_arm")
    area_fieldmap = fieldmappings.getFieldMap(area_idx)
    area_fieldmap.mergeRule = "sum"
    fieldmappings.replaceFieldMap(area_idx, area_fieldmap)

    print('Conduct spatial join')
    arcpy.SpatialJoin_analysis(inputFeature, featureAfterRiverMask, outputFeauture, "JOIN_ONE_TO_ONE",
                               "KEEP_ALL", fieldmappings, "CONTAINS")
    lyr=outLayer
    arcpy.MakeFeatureLayer_management(outputFeauture, lyr)
    #选择掩膜后没有残留的湖泊赋值为0
    arcpy.management.SelectLayerByAttribute(lyr,'NEW_SELECTION', 'area_arm IS NULL')
    arcpy.CalculateField_management(lyr, 'area_arm', 0 , "PYTHON3")
    arcpy.management.SelectLayerByAttribute(lyr,'NEW_SELECTION', '')
    #计算比例
    arcpy.AddField_management(lyr, 'area_ratio_R', "DOUBLE")#新建字段为面积比例
    arcpy.CalculateField_management(lyr, 'area_ratio_R', '!area_arm!/!area!', "PYTHON3")
    
def normal_join(inputFeature,joinFeature,outputFeauture,field_list,outLayer):
    print('Prepare the fieldmap for river mask spatial join')
    fieldmappings = arcpy.FieldMappings()
    fieldmappings_all = arcpy.FieldMappings()
    fieldmappings_all.addTable(inputFeature)#未mask
    fieldmappings_all.addTable(featureAfterRiverMask)
    for field_i in field_list:
        field_idx = fieldmappings_all.findFieldMapIndex(field_i)
        fieldmappings.addFieldMap(fieldmappings_all.getFieldMap(field_idx))
    print('Conduct spatial join')
    arcpy.SpatialJoin_analysis(inputFeature, joinFeature, outputFeauture, "JOIN_ONE_TO_ONE",
                               "KEEP_COMMON", fieldmappings, "CONTAINS")
    
def add_Res_flag(inputFeature):
    selectByAttribute(inputFeature,'NEW_SELECTION', 'flag IS NULL OR "flag" < 2')
    selectByAttribute(inputFeature,'NEW_SELECTION', '"flag" =1 ')
    selectByLocation(inputFeature,'INTERSECT',osm_reservoir,'SUBSET_SELECTION')
    arcpy.CalculateField_management(inputFeature, 'flag',  3)

    selectByAttribute(inputFeature,'NEW_SELECTION', 'flag IS NULL OR "flag" < 2')
    selectByLocation(inputFeature,'INTERSECT',GeoDAR,'SUBSET_SELECTION')
    arcpy.CalculateField_management(inputFeature, 'flag',  4)

def calculateOperateByAttribute(inputFeature,code,operate):
    selectByAttribute(inputFeature,'NEW_SELECTION',code)
    arcpy.CalculateField_management(inputFeature, 'operate',  operate)
    
def calculateOperateByLocation(inputFeature,selectionFeature,operate,selectionType='NEW_SELECTION'):
    selectByLocation(inputFeature,selectionType,selectionFeature)
    arcpy.CalculateField_management(inputFeature, 'operate',operate)

def calculateBound(inputFeature,outputFeature,lyr):
    arcpy.management.MinimumBoundingGeometry(inputFeature,outputFeature,'RECTANGLE_BY_AREA',mbg_fields_option='MBG_FIELDS')
    arcpy.MakeFeatureLayer_management(outputFeature,lyr)

    arcpy.AddField_management(lyr,'w_l',"Double")
    calculateField(lyr, 'w_l',  '!MBG_Width!/!MBG_Length!')
    selectByAttribute(lyr,'NEW_SELECTION','"w_l" > 0.3')
    arcpy.DeleteFeatures_management(lyr)
    arcpy.AddField_management(lyr,'area_bound',"Double")
    arcpy.CalculateField_management(lyr, "area_bound",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
    arcpy.AddField_management(lyr,'area_ratio',"Double")
    calculateField(lyr, 'area_ratio',  '!area!/!area_bound!')

# start=time.time()
# print(f"start classifying predictions according to GRWL, osm river and GLAKES")
# lake_rmO=os.path.join(r'D:\postprocess\v240306\1_other_polygons.gdb',f'{raw_prediction_fn}_rmO' ) 
# arcpy.MakeFeatureLayer_management(lake_rmO, lake_rmO_lyr)
# arcpy.DeleteField_management(lake_rmO_lyr, 'iwR')
# arcpy.AddField_management(lake_rmO_lyr, 'iwR', "Short")
# selectByLocation(lake_rmO_lyr, 'INTERSECT', GRWL_river)
# calculateField(lake_rmO_lyr, 'iwR',1)
# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION',"iwR IS NULL")
# selectByLocation(lake_rmO_lyr, 'INTERSECT', osm_river,'SUBSET_SELECTION')
# calculateField(lake_rmO_lyr, 'iwR',2)
# # selectByAttribute(lake_rmO_lyr,'NEW_SELECTION','"iwR"=0')
# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION',"iwR IS NULL")
# selectByLocation(lake_rmO_lyr, 'INTERSECT', osm_waterway,'SUBSET_SELECTION')
# calculateField(lake_rmO_lyr, 'iwR',3)
# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION',"iwR IS NULL")
# calculateField(lake_rmO_lyr, 'iwR',0)

# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION','"iwG" = 1 and "iwR" > 0 and "iwR" < 3')
# arcpy.conversion.ExportFeatures(lake_rmO_lyr,lake_iwG)

# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION','"iwG" = 0 and "iwR" > 0 and "iwR" < 3')
# arcpy.conversion.ExportFeatures(lake_rmO_lyr,lake_niwG)

# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION','"iwG" = 1 and "iwR" = 3')
# arcpy.conversion.ExportFeatures(lake_rmO_lyr,lake_waterway_iwG)

# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION','"iwG" = 0 and "iwR" = 3')
# arcpy.conversion.ExportFeatures(lake_rmO_lyr,lake_waterway_niwG)

# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION','"iwR" = 0')
# arcpy.conversion.ExportFeatures(lake_rmO_lyr,lake_niwR)
# selectByAttribute(lake_rmO_lyr,'NEW_SELECTION','')
# end=time.time()
# print(f"finish:{end-start}")

arcpy.MakeFeatureLayer_management(lake_iwG,lake_iwG_lyr)
# arcpy.MakeFeatureLayer_management(lake_niwG,lake_niwG_lyr)

print(f"start generating center points of predictions after river mask and GLAKES mask")
# start=time.time()
# arcpy.MakeFeatureLayer_management(lake_arm_raw,lake_arm_raw_lyr)
# arcpy.AddField_management(lake_arm_raw_lyr , 'area_arm', "Double")
# arcpy.CalculateField_management(lake_arm_raw_lyr, "area_arm",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
# arcpy.management.FeatureToPoint(lake_arm_raw_lyr,lake_arm_raw_point,'INSIDE')
# arcpy.MakeFeatureLayer_management(lake_arm_raw_point,lake_arm_raw_point_lyr)
# selectByLocation(lake_arm_raw_point_lyr, 'WITHIN', lake_iwG_lyr)
# selectByLocation(lake_arm_raw_point_lyr, 'WITHIN', lake_niwG_lyr,'ADD_TO_SELECTION')
# arcpy.conversion.ExportFeatures(lake_arm_raw_point_lyr,lake_arm_point)
# arcpy.MakeFeatureLayer_management(lake_arm_point,lake_arm_point_lyr)
# selectByLocation(lake_arm_raw_lyr,'CONTAINS',lake_arm_point_lyr,'NEW_SELECTION')
# arcpy.conversion.ExportFeatures(lake_arm_raw_lyr,lake_arm)
arcpy.MakeFeatureLayer_management(lake_arm_point,lake_arm_point_lyr)

# arcpy.analysis.Clip(lake_rmO_lyr,GLAKES,lake_aGm)
# arcpy.MakeFeatureLayer_management(lake_aGm,lake_aGm_lyr)
# arcpy.management.MultipartToSinglepart(lake_aGm_lyr, lake_aGm_singlepart)
# arcpy.MakeFeatureLayer_management(lake_aGm_singlepart,lake_aGm_singlepart_lyr)
# arcpy.AddField_management(lake_aGm_singlepart_lyr, 'area_aGm', "Double")
# arcpy.CalculateField_management(lake_aGm_singlepart_lyr, "area_aGm",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
# arcpy.management.FeatureToPoint(lake_aGm_singlepart_lyr,lake_aGm_point,'INSIDE')
arcpy.MakeFeatureLayer_management(lake_aGm_point,lake_aGm_point_lyr)
arcpy.MakeFeatureLayer_management(lake_arm,lake_arm_lyr)
# end=time.time()
# print(f"finish:{end-start}")

# print(f"start adding Rser flag:")
# start=time.time()
# arcpy.AddField_management(lake_aGm_point_lyr, 'flag', "Double")
# selectByLocation(lake_aGm_point_lyr, 'WITHIN', GLAKES_natural_lake)
# calculateField(lake_aGm_point_lyr, "flag",1)
# selectByLocation(lake_aGm_point_lyr, 'WITHIN', GLAKES_Res)
# calculateField(lake_aGm_point_lyr, "flag",2)
# selectByAttribute(lake_aGm_point_lyr,'NEW_SELECTION','flag IS NULL' )#lakes less than 1km2
# calculateField(lake_aGm_point_lyr, "flag",0)
# selectByAttribute(lake_aGm_point_lyr,'NEW_SELECTION', '')

GLAKES_join(lake_iwG_lyr,lake_aGm_point_lyr,lake_iwG_aGm_SJ,"lake_iwG_aGm_SJ")
# arcpy.MakeFeatureLayer_management(lake_iwG_aGm_SJ,"lake_iwG_aGm_SJ")
RiverMaskJoin('lake_iwG_aGm_SJ',lake_arm_point_lyr,lake_iwG_arm_SJ, ['area', 'area_ratio_G','flag','iwG','iwR','area_arm'],lake_iwG_arm_SJ_lyr)
add_Res_flag(lake_iwG_arm_SJ_lyr)
arcpy.AddField_management(lake_iwG_arm_SJ_lyr, 'operate', "Double")

RiverMaskJoin(lake_niwG_lyr,lake_arm_point_lyr,lake_niwG_arm_SJ,['area','area_arm','iwG','iwR'],lake_niwG_arm_SJ_lyr)
arcpy.AddField_management(lake_niwG_arm_SJ_lyr, 'flag', "Short")
add_Res_flag(lake_niwG_arm_SJ_lyr)
arcpy.AddField_management(lake_niwG_arm_SJ_lyr, 'operate', "Double")


arcpy.MakeFeatureLayer_management(lake_iwG_arm_SJ,lake_iwG_arm_SJ_lyr)
arcpy.MakeFeatureLayer_management(lake_niwG_arm_SJ,lake_niwG_arm_SJ_lyr)
arcpy.AddField_management(lake_arm_lyr, 'operate', "Short")

# keep all big lake with big AR
calculateOperateByAttribute(lake_iwG_arm_SJ_lyr,'"area" >=1 AND "area_ratio_R" >= 0.9',1)
calculateOperateByAttribute(lake_iwG_arm_SJ_lyr,'"flag" = 1 AND "area_ratio_R" >= 0.8',1)

#对与GLAKES、OSM、GeoDAR水库相交的polygon
calculateOperateByAttribute(lake_iwG_arm_SJ_lyr,'"flag" = 2',2)
calculateOperateByAttribute(lake_iwG_arm_SJ_lyr,'"flag" = 3',3)
calculateOperateByAttribute(lake_iwG_arm_SJ_lyr,'"flag" = 4',4)
calculateOperateByAttribute(lake_iwG_arm_SJ_lyr,'"flag" = 0 AND "area_ratio_R" < 0.1',0)

# #对不与GLAKES相交的湖泊，删掉AR小的
# calculateOperateByAttribute(lake_niwG_arm_SJ_lyr,'"flag" IS NULL AND "area_ratio_R" < 0.8',0)
# calculateOperateByAttribute(lake_niwG_arm_SJ_lyr,' "flag" = 3',3)
# calculateOperateByAttribute(lake_niwG_arm_SJ_lyr,'"flag" = 4',4)
# calculateOperateByAttribute(lake_niwG_arm_SJ_lyr,'"area" >=1 AND "area_ratio_R" >= 0.9',1)

# end=time.time()
# print(f"finish:{end-start}")

arcpy.MakeFeatureLayer_management(lake_waterway_iwG,lake_waterway_iwG_lyr)
# arcpy.MakeFeatureLayer_management(lake_waterway_niwG,lake_waterway_niwG_lyr)


GLAKES_join(lake_waterway_iwG_lyr,lake_aGm_point_lyr,lake_waterway_iwG_SJ,lake_waterway_iwG_SJ_lyr)
add_Res_flag(lake_waterway_iwG_SJ_lyr)

arcpy.AddField_management(lake_waterway_iwG_SJ_lyr, 'operate', "Double")
calculateOperateByAttribute(lake_waterway_iwG_SJ_lyr,'"area" >= 3',1)
calculateOperateByAttribute(lake_waterway_iwG_SJ_lyr,'"flag" = 1 And "area" > 1 And "area_ratio_G" > 0.1',1)
calculateOperateByAttribute(lake_waterway_iwG_SJ_lyr,'"flag" = 2',2)
calculateOperateByAttribute(lake_waterway_iwG_SJ_lyr,'"flag" = 3',3)
calculateOperateByAttribute(lake_waterway_iwG_SJ_lyr,'"flag" = 4',4)

# arcpy.AddField_management(lake_waterway_niwG_lyr, 'flag', "Short")
# add_Res_flag(lake_waterway_niwG_lyr)

# arcpy.AddField_management(lake_waterway_niwG_lyr, 'operate', "Double")
# calculateOperateByAttribute(lake_waterway_niwG_lyr,'"area" >= 3',1)
# calculateOperateByAttribute(lake_waterway_niwG_lyr,'"flag" = 3',3)
# calculateOperateByAttribute(lake_waterway_niwG_lyr,'"flag" = 4',4)

# arcpy.MakeFeatureLayer_management(lake_niwR,lake_niwR_lyr)
# arcpy.AddField_management(lake_niwR_lyr, 'operate', "Double")

# selectByAttribute(lake_arm_lyr,'NEW_SELECTION', '"area_arm"<0.005')
# calculateField(lake_arm_lyr,'operate',0)