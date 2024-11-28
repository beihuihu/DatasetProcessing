import arcpy
from arcpy.sa import *
import os
import time
arcpy.env.overwriteOutput = True

version='v14_241115'
sub_v='_v1'
output_dir = os.path.join(r'J:\lakemapping\postprocess',version)
mwBG_gdb=os.path.join(output_dir,f'5_polygon_afm_mwBL_BigGLAKES{sub_v}.gdb')
mwBG_point_gdb=os.path.join(output_dir,f'5_polygon_afm_mwBL_BigGLAKES{sub_v}_point.gdb')
# mwBL_gdb=os.path.join(output_dir,f'4_polygon_afm_mergeWith_BigLake{sub_v}.gdb')
temp_gdb=os.path.join(output_dir,'7_correct_temp_file.gdb')
new_PLD_gdb=r'J:\lakemapping\PLD\PLD.gdb'
PLD_point_gdb=r'J:\lakemapping\PLD\PLD_point.gdb'
c_arid_lake_mwPLD=os.path.join(mwBG_gdb,'c_arid_lake_mwPLD')
c_arid_lake_mwPLD_lyr='c_arid_lake_mwPLD'

eight_continents=['Asia','Siberia','Africa','Europe','Oceania_Anta','North_America','Arctic','South_America']

def selectByLocation(inputFeature,overlapType,selectionFeature,selectionType='NEW_SELECTION'):
    arcpy.SelectLayerByLocation_management(inputFeature,overlapType,selectionFeature,selection_type=selectionType)
    
def selectByAttribute(inputFeature,selectionType='NEW_SELECTION',code=''):
    arcpy.management.SelectLayerByAttribute(inputFeature,selectionType,code)
    
def calculateField(inputFeature,field,code):
    arcpy.CalculateField_management(inputFeature, field,code)

grid=os.path.join(temp_gdb,'Global_grid_shp_1degree')
grid_lyr='Global_grid_shp_1degree'
arcpy.MakeFeatureLayer_management(grid,grid_lyr)

# for i in range(0,8):#[1,3,4,5]:
#     continent=eight_continents[i]
#     print(continent)
#     b_lake_afm_merge_with_BL=os.path.join(mwBL_gdb,f'b{i+1}_{continent}_polygon_afm_mwBL')
#     b_lake_afm_merge_with_BL_lyr=f'b{i+1}_{continent}_lake_afm_merge_with_BL'
#     arcpy.MakeFeatureLayer_management(b_lake_afm_merge_with_BL, b_lake_afm_merge_with_BL_lyr)
#     b_lake_afm_merge_with_BL_point=os.path.join(mwBG_point_gdb,f'b{i+1}_{continent}_polygon_afm_mwBL_point')
#     b_lake_afm_merge_with_BL_point_lyr=f'b{i+1}_{continent}_lake_afm_merge_with_BL_point'
#     arcpy.management.FeatureToPoint(b_lake_afm_merge_with_BL_lyr,b_lake_afm_merge_with_BL_point,'INSIDE')
#     arcpy.MakeFeatureLayer_management(b_lake_afm_merge_with_BL_point, b_lake_afm_merge_with_BL_point_lyr)
#     arcpy.management.DeleteIdentical(b_lake_afm_merge_with_BL_point_lyr,['lake_area','Shape_Area','Shape_Length'],'20 Meters')

# for i in range(2,8):#[3]:#
#     continent=eight_continents[i]
#     print(continent)
#     c_lake_afm_mw_BL_BG=os.path.join(mwBG_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG')
#     c_lake_afm_mw_BL_BG_lyr=f'c{i+1}_{continent}_lake_afm_mw_BL_BG'
#     arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG,c_lake_afm_mw_BL_BG_lyr)

#     c_lake_afm_mw_BL_BG_point=os.path.join(mwBG_point_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG_point')
#     c_lake_afm_mw_BL_BG_point_lyr='c_lake_afm_mw_BL_BG_point'
    
#     c_lake_afm_mw_BL_BG_pi=os.path.join(temp_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG_pi')
#     c_lake_afm_mw_BL_BG_pi_lyr=f'c{i+1}_{continent}_lake_afm_mw_BL_BG_pi'

#     c_lake_afm_mw_BL_BG_pi_point=os.path.join(temp_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG_pi_point')
#     c_lake_afm_mw_BL_BG_pi_point_lyr='c_lake_afm_mw_BL_BG_pi_point'
#     selectByAttribute(c_lake_afm_mw_BL_BG_lyr,'NEW_SELECTION',"lake_type=4")#gt 100
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_lyr,'lake_type',5)
#     selectByAttribute(c_lake_afm_mw_BL_BG_lyr,'NEW_SELECTION',"lake_type=3")#bt 1~100
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_lyr,'lake_type',4)
#     selectByAttribute(c_lake_afm_mw_BL_BG_lyr,'NEW_SELECTION',"lake_type=2") #bt 0.03~1
#     selectByAttribute(c_lake_afm_mw_BL_BG_lyr,'SUBSET_SELECTION',"lake_area>=0.1 and lake_area<1")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_lyr,'lake_type',3)

#     print('start transform to point')
#     selectByAttribute(c_lake_afm_mw_BL_BG_lyr,'NEW_SELECTION','')  
#     arcpy.management.FeatureToPoint(c_lake_afm_mw_BL_BG_lyr,c_lake_afm_mw_BL_BG_point,'INSIDE')
#     arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG_point,c_lake_afm_mw_BL_BG_point_lyr)

#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c1','Short')#0
#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c3','Short')#1
#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c10','Short')#2
#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c100','Short')#3
    
#     print('start calculate field')
#     selectByAttribute(c_lake_afm_mw_BL_BG_point_lyr,'NEW_SELECTION',"lake_type=0")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c1',1)
#     selectByAttribute(c_lake_afm_mw_BL_BG_point_lyr,'NEW_SELECTION',"lake_type=1")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c3',1)
#     selectByAttribute(c_lake_afm_mw_BL_BG_point_lyr,'NEW_SELECTION',"lake_type=2")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c10',1)
#     selectByAttribute(c_lake_afm_mw_BL_BG_point_lyr,'NEW_SELECTION',"lake_type=3")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c100',1)

#     print('start pairwise intersect')
#     arcpy.analysis.PairwiseIntersect([c_lake_afm_mw_BL_BG_lyr, grid_lyr],c_lake_afm_mw_BL_BG_pi,join_attributes='NO_FID')
#     arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG_pi,c_lake_afm_mw_BL_BG_pi_lyr)
#     selectByLocation(c_lake_afm_mw_BL_BG_pi_lyr,'SHARE_A_LINE_SEGMENT_WITH',grid_lyr,'NEW_SELECTION')
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_lyr,'lake_area', "!shape.geodesicArea@SQUAREKILOMETERS!", "PYTHON_9.3")
    
#     print('start transform to point')
#     selectByAttribute(c_lake_afm_mw_BL_BG_pi_lyr,'NEW_SELECTION','')  
#     arcpy.management.FeatureToPoint(c_lake_afm_mw_BL_BG_pi_lyr,c_lake_afm_mw_BL_BG_pi_point,'INSIDE')
#     arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG_pi_point,c_lake_afm_mw_BL_BG_pi_point_lyr)

#     print('start calculate field')
#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a1','Double')
#     selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION',"lake_type = 0")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a1','!lake_area!')

#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a3','Double')
#     selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION',"lake_type = 1")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a3','!lake_area!')

#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a10','Double')
#     selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION',"lake_type = 2")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a10','!lake_area!')

#     arcpy.AddField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a100','Double')
#     selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION',"lake_type = 3")
#     arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a100','!lake_area!')

# arcpy.MakeFeatureLayer_management(c_arid_lake_mwPLD, c_arid_lake_mwPLD_lyr)
# # arcpy.AddField_management(c_arid_lake_mwPLD_lyr,'lake_type','Short')
# # selectByAttribute(c_arid_lake_mwPLD_lyr,'NEW_SELECTION',"lake_area<0.01")
# # arcpy.CalculateField_management(c_arid_lake_mwPLD_lyr,'lake_type',0)
# # selectByAttribute(c_arid_lake_mwPLD_lyr,'NEW_SELECTION',"lake_area>=0.01 and lake_area <0.03")
# # arcpy.CalculateField_management(c_arid_lake_mwPLD_lyr,'lake_type',1)
# selectByAttribute(c_arid_lake_mwPLD_lyr,'NEW_SELECTION',"lake_area>=0.03 and lake_area <0.1")
# arcpy.CalculateField_management(c_arid_lake_mwPLD_lyr,'lake_type',2)
# selectByAttribute(c_arid_lake_mwPLD_lyr,'NEW_SELECTION',"lake_area>=0.1 and lake_area <1")
# arcpy.CalculateField_management(c_arid_lake_mwPLD_lyr,'lake_type',3)
# selectByAttribute(c_arid_lake_mwPLD_lyr,'NEW_SELECTION',"lake_area>=1 and lake_area <100")
# arcpy.CalculateField_management(c_arid_lake_mwPLD_lyr,'lake_type',4)
# selectByAttribute(c_arid_lake_mwPLD_lyr,'NEW_SELECTION',"lake_area>=100")
# arcpy.CalculateField_management(c_arid_lake_mwPLD_lyr,'lake_type',5)
# merge_list=[]
# for i in range(0,8):#[1,3,4,5]:
#     continent=eight_continents[i]
#     print(continent)
#     c_lake_afm_mw_BL_BG_pi_point=os.path.join(mwBG_point_gdb,'c'+str(i+1)+'_'+continent+'_polygon_afm_mwBL_BG_pi_point')
#     c_lake_afm_mw_BL_BG_pi_point_lyr='c'+str(i+1)+'_'+continent+'_lake_afm_mw_BL_BG_pi_point'
#     arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG_pi_point,c_lake_afm_mw_BL_BG_pi_point_lyr)
#     # arcpy.AddField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a1','Double')
#     # arcpy.AddField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a3','Double')
#     # arcpy.AddField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a100','Double')
#     # selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION',"lake_type=0")
#     # arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a1','!lake_area!')
#     # selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION',"lake_type=1")
#     # arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a3','!lake_area!')
#     # selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION',"lake_type=2")
#     # arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a100','!lake_area!')
#     # selectByAttribute(c_lake_afm_mw_BL_BG_pi_point_lyr,'NEW_SELECTION','')
#     merge_list.append(c_lake_afm_mw_BL_BG_pi_point_lyr)
# total_lake_afm_mw_BL_BG_pi_point=os.path.join(mwBG_point_gdb,'total_polygon_afm_mwBL_BG_pi_point')
# arcpy.Merge_management(merge_list,total_lake_afm_mw_BL_BG_pi_point)

for i in range(0,4):#[3]:#
    continent=eight_continents[i]
    print(continent)
    c_lake_afm_mw_BL_BG=os.path.join(mwBG_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG')
    c_lake_afm_mw_BL_BG_lyr=f'c{i+1}_{continent}_lake_afm_mw_BL_BG'
    arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG,c_lake_afm_mw_BL_BG_lyr)

    c_lake_afm_mw_BL_BG_point=os.path.join(mwBG_point_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG_point')
    c_lake_afm_mw_BL_BG_point_lyr='c_lake_afm_mw_BL_BG_point'
    
    c_lake_afm_mw_BL_BG_pi=os.path.join(temp_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG_pi')
    c_lake_afm_mw_BL_BG_pi_lyr=f'c{i+1}_{continent}_lake_afm_mw_BL_BG_pi'

    c_lake_afm_mw_BL_BG_pi_point=os.path.join(temp_gdb,f'c{i+1}_{continent}_polygon_afm_mwBL_BG_pi_point')
    c_lake_afm_mw_BL_BG_pi_point_lyr='c_lake_afm_mw_BL_BG_pi_point'

    selectByAttribute(c_lake_afm_mw_BL_BG_lyr,'NEW_SELECTION',"lake_area>=0.1 and lake_area<1")
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_lyr,'lake_type',3)

    arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG_point,c_lake_afm_mw_BL_BG_point_lyr)

    selectByAttribute(c_lake_afm_mw_BL_BG_point_lyr,'NEW_SELECTION',"lake_area>=0.1 and lake_area<1")
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_point_lyr,'lake_type',3)
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c10',0)
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_point_lyr,'hu_c100',1)

    arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG_pi,c_lake_afm_mw_BL_BG_pi_lyr)
    selectByLocation(c_lake_afm_mw_BL_BG_pi_lyr,'WITHIN',c_lake_afm_mw_BL_BG_lyr,'NEW_SELECTION')
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_lyr,'lake_type', 3)

    arcpy.MakeFeatureLayer_management(c_lake_afm_mw_BL_BG_pi_point,c_lake_afm_mw_BL_BG_pi_point_lyr)
    selectByLocation(c_lake_afm_mw_BL_BG_pi_point_lyr,'WITHIN',c_lake_afm_mw_BL_BG_lyr,'NEW_SELECTION')
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'lake_type',3)
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a10',0)
    arcpy.CalculateField_management(c_lake_afm_mw_BL_BG_pi_point_lyr,'hu_a100','!lake_area!')