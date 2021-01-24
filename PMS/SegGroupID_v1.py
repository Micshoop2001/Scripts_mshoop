import arcpy
from log_module import logger
import time

begin_time = time.time()
filename = 'SegGroupID_v1'
base = r'\\files03\gis\Development\PMS\publicWorks.gdb'
streetcenterline_db06 = base + '\\' + 'streetCenterlinesPW'
streetcenterline_reord = base + '\\' + 'StreetCenterLines_reord2'
values = ['start']
jur = ['start']
num = []
interval = 10
sorting = [['RouteID', "ASCENDING"], ['ToAddr_R', "ASCENDING"]]

arcpy.env.overwriteOutput = True #not currently needed
logger('start', filename,'','','')

try:
    if arcpy.Exists(streetcenterline_reord):
        arcpy.Delete_management(streetcenterline_reord)
        print('found a copy deleted old sort')
    logger('succeed', filename, 'if exists delete', begin_time, '')
except:
    logger('failed', filename, 'if exists delete', begin_time, arcpy.GetMessages())


print('starting sort')
try:
    #Sort_management (in_dataset, out_dataset, sort_field, {spatial_sort_method})
    arcpy.Sort_management(streetcenterline_db06, streetcenterline_reord, sorting)
    logger('succeed', filename, 'sort', begin_time, '')
except:
    logger('failed', filename, 'sort', begin_time, arcpy.GetMessages())   
print('sorted')

try:    
    arcpy.AddField_management(streetcenterline_reord, 'Segment_GroupID', 'TEXT')
    logger('succeed', filename, 'sort', begin_time, '')
except:
    logger('failed', filename, 'sort', begin_time, arcpy.GetMessages())   
print('sorted')


print('starting SegmentGroupID update')
try:
    with arcpy.da.UpdateCursor(streetcenterline_reord, ('Segment_GroupID', 'RouteID', 'MaintResp')) as cursor:
        for row in cursor:
            if row[1] == values[0] and row[2] != jur[0]: #RouteID is same but MaintResp different increment by 10
                del jur[:]
                num[0] += interval
                if num[0] > 90:
                    segnum = str(num[0])
                else:
                    segnum = '0' + str(num[0])
                row[0] = segnum
                jur.append(row[2])
                cursor.updateRow(row)
                print(str(row[1]) + '-' + segnum)
            elif row[1] == values[0] and row[2] == jur[0]: #RouteID and MaintResp same print same number as last time
                if num[0] > 90:
                    segnum = str(num[0])
                else:
                    segnum = '0' + str(num[0])
                row[0] = segnum
                cursor.updateRow(row)
                print(str(row[1]) + '-' + segnum)         
            else:                                         #Else we start a new count from 10
                del values[:]
                del num[:]
                del jur[:]
                values.append(row[1])
                num.append(interval)
                jur.append(row[2])
                segnum = '0' + str(num[0])
                row[0] = segnum
                cursor.updateRow(row)
                print(str(row[1]) + '-' + segnum)
    logger('succeed', filename, 'SegmentGroupID update', begin_time, '')

except:
    logger('failed', filename, 'SegmentGroupID update', begin_time, arcpy.GetMessages())
               
del row, cursor

logger('end', filename, 'end', begin_time, '')

