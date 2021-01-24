import arcpy
from log_module import logger
import time

begin_time = time.time()
filename = 'StreetDiss_v1'
base = r'\\files03\gis\Development\PMS\publicWorks.gdb'

streetcenterline_db06 = base + '\\' + 'StreetCenterLines_reord2'
streetcenterline_dissolve = base + '\\' + 'StreetCenterLines_Dissolve'
streetcenterline_temp = base + '\\' + 'StreetCenterLines_temp'
split_points = base + '\\' + 'PWtestPointsworking'
splitpoints_original = base + '\\' + 'PWtestPoints'
maxplaces = [streetcenterline_dissolve, split_points]
featurelayer = 'streetcenterline_layer'
county = 'COUNTY'
maintresp = 'MaintResp'
stats = [['ToAddr_R', 'MAX'], ['FromAddr_R', 'MIN']]
countySQL = """{} = '{}'""".format(arcpy.AddFieldDelimiters(streetcenterline_db06, maintresp), county)
fieldsdissolve = str('FullName;RouteID;Segment_GroupID;MaintResp;PrimaryComm;Low_Cross;High_Cross' +
                  ';Sub_Name;Width;Surface;Curbing;In_Sub;Sub_Base;SpeedLimit;St_FunctCls;Length' +
                     ';Low_Cross;High_Cross')
                    
arcpy.env.overwriteOutput = True
print('start of script')
logger('start', filename,'','','')

print('copy beginning')
try:
    arcpy.CopyFeatures_management(streetcenterline_db06, streetcenterline_temp)
    arcpy.CopyFeatures_management(splitpoints_original, split_points)
    print('copy done')
    arcpy.MakeFeatureLayer_management(streetcenterline_temp, featurelayer, countySQL)
    print('created feature')
    logger('succeed', filename, 'CopyFeatures_management', begin_time, '')
except:
    logger('failed', filename, 'CopyFeatures_management', begin_time, arcpy.GetMessages())
try:
    if arcpy.Exists(streetcenterline_dissolve):
        arcpy.Delete_management(streetcenterline_dissolve)
        print('found a copy deleted old dissolve')
    logger('succeed', filename, 'if exists delete', begin_time, '')
except:
    logger('failed', filename, 'if exists delete', begin_time, arcpy.GetMessages())

try:
    arcpy.Dissolve_management(featurelayer, streetcenterline_dissolve,fieldsdissolve, stats, "SINGLE_PART", "DISSOLVE_LINES")
    print('dissolve completed')
    logger('succeed', filename, 'dissolve', begin_time, '')
except:
    logger('failed', filename, 'dissolve', begin_time, arcpy.GetMessages())

try:
    arcpy.Snap_edit(split_points, [[streetcenterline_dissolve, "EDGE", "75 feet"]])
    print('snap completed')
    logger('succeed', filename, 'Snap', begin_time, '')
except:
    logger('failed', filename, 'Snap', begin_time, arcpy.GetMessages())

print('started adding fields')

for m in maxplaces:
    arcpy.AddField_management(m, 'MAX', 'LONG')
    arcpy.AddField_management(m, 'NewPt', 'TEXT')
    arcpy.AddField_management(m, 'Traffic_Count', 'TEXT')
    print('added new field in {}'.format(m))  



#arcpy.Delete_management(featurelayer)
#arcpy.Delete_management(streetcenterline_temp)

logger('end', filename, 'end', begin_time, '')

