import arcpy
from log_module import logger
import time
begin_time = time.time()
filename = 'RoadSegID_v1'
base = r'\\files03\gis\Development\PMS\publicWorks.gdb'
split_points = base + '\\' + 'PWtestPointsworking'
street_dissolve_split = base + '\\' + 'street_dissolve_split'
street_RoadSegID = base + '\\' + 'street_dissolve_split_roadsegid3'
streetcenterline_temp = base + '\\' + 'StreetCenterLines_temp'
streetcenterline_dissolve = base + '\\' + 'StreetCenterLines_Dissolve'
deletefcs = [streetcenterline_temp, streetcenterline_dissolve, street_dissolve_split, split_points] #split_points
num = []
values = ['start']
sorting = [['RouteID', "ASCENDING"], ['MAX', "ASCENDING"]]
cleanupfields = ['NewPt', 'MAX']
cleanupfeatureclasses = [street_RoadSegID, split_points]

arcpy.AddField_management(street_dissolve_split, 'ROADSEGMENT_ID', 'TEXT')
streetfields = ['Segment_GroupID', 'ROADSEGMENT_ID', 'NewPt', 'RouteID'] 

arcpy.env.overwriteOutput = True 

logger('start', filename,'','','')
if arcpy.Exists(street_RoadSegID):
    arcpy.Delete_management(street_RoadSegID)
    
arcpy.Sort_management(street_dissolve_split, street_RoadSegID, sorting)

with arcpy.da.UpdateCursor(street_RoadSegID, streetfields) as cursor:
    for row in cursor: #This is a field that accounts for old versus new segment splits
        if row[2] == 'Y':
            interval = 50
        else: interval = 100
        if row[0] == values[0][0] and row[3] == values[0][1]: #if Segment_Group and routeid same as Segment_Group and routeid on previous row
            num[0] += interval
            if num[0] > 9950:
                segnum = str(num[0])
            elif num[0] > 950:
                segnum = '0' + str(num[0])
            elif num[0] > 50:
                segnum = '00' + str(num[0])
            else:
                segnum = '000' + str(num[0])
            row[1] = segnum
            cursor.updateRow(row)
            print('if ' + str(row[3]) + '-' + str(row[0]) + '-' + segnum)
        else:                   #if Segment_Group and routeid not the same 
            del values[:]
            del num[:]
            uniquevalue = [row[0], row[3]]
            values.append(uniquevalue)
            num.append(interval)
            if interval == 50:
                segnum = '000' + str(num[0])
            else: segnum = '00' + str(num[0])
            row[1] = segnum
            cursor.updateRow(row)
            print('else ' + str(row[3]) + '-' + str(row[0]) + '-' + segnum)           
del row, cursor
logger('succeed', filename, 'Road SegmentID completed', begin_time, '')
################### Cleanup #########################################################################################################################3

for c in cleanupfeatureclasses:
    arcpy.management.DeleteField(c, cleanupfields)
for d in deletefcs:
    arcpy.Delete_management(d)
print('cleanup completed' + '\n' + 'script completed')
logger('succeed', filename, 'cleanup completed', begin_time, '')
logger('end', filename, 'end', begin_time, '')



