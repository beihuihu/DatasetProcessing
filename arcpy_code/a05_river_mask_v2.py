import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

# load input features and make layer
version='v16_250104'
output_dir = os.path.join(r'J:\lakemapping\postprocess',version)
auxiliary_dataset_gdb=r'J:\lakemapping\auxiliary_dataset.gdb'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    arcpy.CreateFileGDB_management(output_dir, "1_temp_files.gdb")
    arcpy.CreateFileGDB_management(output_dir, "2_polygon_iw_River.gdb")
    arcpy.CreateFileGDB_management(output_dir, "3_polygon_after_rivermask.gdb")
temp_file_gdb=os.path.join(output_dir,f'1_temp_files.gdb')
river_mask_gdb=os.path.join(output_dir,f'2_polygon_iw_River.gdb')
after_mask_gdb=os.path.join(output_dir,f'3_polygon_after_rivermask.gdb')

GLAKES=r'D:\lakemapping\0_auxiliary_data\GLAKES\GLAKES.gdb\GLAKES'
GLAKES_new_gdb=r'D:\lakemapping\0_auxiliary_data\GLAKES\GLAKES_after_30p_land_mask.gdb'
GLAKES_niwSHIFT=os.path.join(GLAKES_new_gdb,'au1_GLAKES_niwSHIFT')
GLAKES_iwSHIFT_afm_keep_arid=os.path.join(GLAKES_new_gdb,'au2_GLAKES_iwSHIFT_after_mask_gt3ha_keep_arid')

GLAKES_lyr='GLAKES'
GLAKES_niwSHIFT_lyr='au1_GLAKES_niwSHIFT'
GLAKES_iwSHIFT_afm_keep_arid_lyr='au2_GLAKES_iwSHIFT_after_mask_gt3ha_keep_arid'

# GLAKES_Res=os.path.join(auxiliary_dataset_gdb,'GLAKES_Res')
# arcpy.MakeFeatureLayer_management(GLAKES_Res,'GLAKES_Res')

# GRWL_river=os.path.join(auxiliary_dataset_gdb,'GRWL_DNRiver')
# arcpy.MakeFeatureLayer_management(GRWL_river,'GRWL_river')

# osm_river=os.path.join(auxiliary_dataset_gdb,'osm_natural_water_river')
# arcpy.MakeFeatureLayer_management(osm_river,'osm_river')

# osm_reservoir=os.path.join(auxiliary_dataset_gdb,'osm_natural_water_reservoir')
# arcpy.MakeFeatureLayer_management(osm_reservoir,'osm_reservoir')

# GeoDAR=r'D:\lakemapping\0_auxiliary_data\GeoDAR\GeoDAR_v10_v11\GeoDAR_v11_reservoirs.shp'
# arcpy.MakeFeatureLayer_management(GeoDAR,'GeoDAR')
lakes_iwBR=os.path.join(river_mask_gdb,'total_lakes_iwBR')
total_lakes_arm=os.path.join(river_mask_gdb,'total_lakes_arm')
lakes_iwBR_afterMask=os.path.join(after_mask_gdb,'lakes_iwBR_afterMask')
lakes_iwBR_lyr='lakes_iwBR'
total_lakes_arm_lyr='lakes_arm'
lakes_iwBR_afm_lyr='lakes_iwBR_afm'

lake_iwBR_aGm_iwSHIFT=os.path.join(temp_file_gdb,'total_iwBR_aGm_iwSHIFT')
lake_iwBR_aGm_iwSHIFT_singlepart=os.path.join(temp_file_gdb,'total_iwBR_aGm_iwSHIFT_singlepart')
lake_iwBR_aGm_iwSHIFT_point=os.path.join(temp_file_gdb,'total_iwBR_aGm_iwSHIFT_point')
lake_iwBR_aGm_iwSHIFT_singlepart_lyr='lake_iwBR_aGm_iwSHIFT_singlepart'

lake_iwBR_aGm_niwSHIFT=os.path.join(temp_file_gdb,'total_iwBR_aGm_niwSHIFT')
lake_iwBR_aGm_niwSHIFT_singlepart=os.path.join(temp_file_gdb,'total_iwBR_aGm_niwSHIFT_singlepart')
lake_iwBR_aGm_niwSHIFT_point=os.path.join(temp_file_gdb,'total_iwBR_aGm_niwSHIFT_point')
lake_iwBR_aGm_niwSHIFT_singlepart_lyr='lake_iwBR_aGm_niwSHIFT_singlepart'

# print('iwSHIFT')
# arcpy.analysis.Clip(lakes_iwBR,GLAKES_iwSHIFT_afm_keep_arid,lake_iwBR_aGm_iwSHIFT)
# arcpy.management.MultipartToSinglepart(lake_iwBR_aGm_iwSHIFT, lake_iwBR_aGm_iwSHIFT_singlepart)
# arcpy.MakeFeatureLayer_management(lake_iwBR_aGm_iwSHIFT_singlepart,lake_iwBR_aGm_iwSHIFT_singlepart_lyr)
# print('calculate area')
# arcpy.AddField_management(lake_iwBR_aGm_iwSHIFT_singlepart_lyr, 'area_aGm', "Double")
# arcpy.CalculateField_management(lake_iwBR_aGm_iwSHIFT_singlepart_lyr, "area_aGm",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
# arcpy.management.FeatureToPoint(lake_iwBR_aGm_iwSHIFT_singlepart_lyr,lake_iwBR_aGm_iwSHIFT_point,'INSIDE')

print('niwSHIFT')
arcpy.analysis.Clip(lakes_iwBR,GLAKES_niwSHIFT,lake_iwBR_aGm_niwSHIFT)
arcpy.management.MultipartToSinglepart(lake_iwBR_aGm_niwSHIFT, lake_iwBR_aGm_niwSHIFT_singlepart)
arcpy.MakeFeatureLayer_management(lake_iwBR_aGm_niwSHIFT_singlepart,lake_iwBR_aGm_niwSHIFT_singlepart_lyr)
print('calculate area')
arcpy.AddField_management(lake_iwBR_aGm_niwSHIFT_singlepart_lyr, 'area_aGm', "Double")
arcpy.CalculateField_management(lake_iwBR_aGm_niwSHIFT_singlepart_lyr, "area_aGm",  "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
arcpy.management.FeatureToPoint(lake_iwBR_aGm_niwSHIFT_singlepart_lyr,lake_iwBR_aGm_niwSHIFT_point,'INSIDE')