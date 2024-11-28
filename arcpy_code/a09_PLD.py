import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

# load input features and make layer
version='v13_241021'
stastic_v=version
output_dir = os.path.join(r'J:\lakemapping\postprocess',version)
new_PLD_gdb='J:\lakemapping\PLD\PLD.gdb'
PLD_point_gdb=r'J:\lakemapping\PLD\PLD_point.gdb'
temp_gdb=os.path.join(output_dir,'7_correct_temp_file.gdb')

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)

for region in ['na']:#[1,3,4,5]:
    print(region)
    PLD_region=os.path.join(new_PLD_gdb,'PLD_'+region)
    PLD_region_point=os.path.join(PLD_point_gdb,'PLD'+region+'_point')
    PLD_region_pi=os.path.join(new_PLD_gdb,'PLD'+region+'_pi')
    PLD_region_pi_lyr='PLD'+region+'_pi'
    PLD_region_lyr='PLD'+region
    arcpy.MakeFeatureLayer_management(PLD_region,PLD_region_lyr)
    arcpy.AddField_management(PLD_region_lyr,'pld_c3','Short')
    arcpy.AddField_management(PLD_region_lyr,'pld_c100','Short')
    selectByAttribute(PLD_region_lyr,'NEW_SELECTION',"ref_area<0.03")
    arcpy.CalculateField_management(PLD_region_lyr,'pld_c3',1)
    selectByAttribute(PLD_region_lyr,'NEW_SELECTION',"ref_area>0.03 and ref_area<1")
    arcpy.CalculateField_management(PLD_region_lyr,'pld_c100',1)
    selectByAttribute(PLD_region_lyr,'NEW_SELECTION','')
    arcpy.management.FeatureToPoint(PLD_region_lyr,PLD_region_point,'INSIDE')

    arcpy.analysis.PairwiseIntersect([PLD_region_lyr, grid_lyr],PLD_region_pi,join_attributes='NO_FID')
    arcpy.MakeFeatureLayer_management(PLD_region_pi,PLD_region_pi_lyr)
    selectByLocation(PLD_region_pi_lyr,'SHARE_A_LINE_SEGMENT_WITH',grid_lyr,'NEW_SELECTION')
    arcpy.CalculateField_management(PLD_region_pi_lyr,'ref_area', "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
    PLD_region_pi_point=os.path.join(PLD_point_gdb,'PLD'+region+'_pi_point')
    selectByAttribute(PLD_region_pi_lyr,"NEW_SELECTION","")
    arcpy.management.FeatureToPoint(PLD_region_pi_lyr,PLD_region_pi_point,'INSIDE')
