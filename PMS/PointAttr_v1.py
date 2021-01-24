import arcpy
from log_module import logger
import time

begin_time = time.time()
filename = 'PointAttr_v1'
base = r'\\files03\gis\Development\PMS\publicWorks.gdb'
streetcenterline_dissolve = base + '\\' + 'StreetCenterLines_Dissolve'
split_points = base + '\\' + 'PWtestPointsworking'
streetcenterline_db06 = base + '\\' + 'StreetCenterLines_reord2'

fields = ['FullName', 'FromAddr_R', 'ToAddr_R', 'MAX', 'OBJECTID', 'FROM_WIDTH', 'TO_WIDTH',  #6
          'FROM_LENGTH', 'TO_LENGTH', 'FROM_CURB', 'TO_CURB', 'From_Sub', 'To_Sub', 'From_Sub_Name', #13
          'To_Sub_Name', 'NewPt', 'Date_Created', 'Low_Cross', 'High_Cross'] #18

linefields = ['MIN_FromAddr_R', 'MAX_ToAddr_R', 'OBJECTID', 'FullName', 'Sub_Name', #4
              'Width', 'Length', 'Surface', 'Curbing', 'In_Sub', 'Sub_Base', 'Low_Cross', 'High_Cross'] #12
values = []
num = []
addrlist = []
needextend = 0

arcpy.env.overwriteOutput = True

logger('start', filename,'','','')
arcpy.MakeFeatureLayer_management(streetcenterline_dissolve, 'str_dissolve')


for f in fields:
    if f in ('FromAddr_R', 'ToAddr_R'): 
        arcpy.AddField_management(split_points, f, 'LONG')
    elif f in ('FullName', 'Low_Cross', 'High_Cross'):
        arcpy.AddField_management(split_points, f, 'TEXT')
    else:
        pass
    print('added field {}'.format(f)) 
try:
    with arcpy.da.UpdateCursor(split_points, fields) as cursor:
        for row in cursor:        
            querypointog = """{} = {}""".format('OBJECTID', row[4])
            arcpy.MakeFeatureLayer_management(split_points, 'addrofPoint', querypointog)
            addrline = arcpy.SelectLayerByLocation_management('str_dissolve', 'INTERSECT', 'addrofPoint', '5 feet')
            arcpy.MakeFeatureLayer_management('str_dissolve', 'addrline')

            with arcpy.da.SearchCursor('addrline', linefields) as afill:
                for a in afill:
                    print(str(a[0]) + ' ' + str(a[1]) + ' ' + str(a[3]))
                    values.extend([a[0], a[1], a[2], a[3], a[11], a[12]])
            del a, afill
            
            row[1] = int(values[0])
            row[2] = int(values[1])
            row[0] = str(values[3])
            row[17] = str(values[4])
            row[18] = str(values[5])
            if row[16] is None:
                row[16] = time.strftime('%d/%m/%Y')
            cursor.updateRow(row)
            
            del values[:]
    del cursor, row
    logger('succeed', filename, 'fill in point data', begin_time, '')
except:
    logger('failed', filename, 'fill in point data', begin_time, arcpy.GetMessages())

with arcpy.da.UpdateCursor(split_points, fields) as cursor:
    for row in cursor:
        average = (row[1] + row[2])/2.0 #Caluculating the average address between original line. Number coming up wrong :(
        print(average)

        #This is the set of SQL queries that isolate the road segment needed
        queryline = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0], 'MAX_ToAddr_R', int(row[2]), 'MIN_FromAddr_R', int(row[1]))
        querypoint = """{} = '{}' AND {} = {} AND {} = {} AND {} = {}""".format('FullName', row[0], 'ToAddr_R', row[2], 'FromAddr_R', row[1], 'OBJECTID', row[4])
        querywhole = """{} = '{}'""".format('FullName', row[0])
        queryfromstreet = """{} = '{}'""".format('FullName', row[17])
        querytostreet = """{} = '{}'""".format('FullName', row[18])

        #isolating road segment
        arcpy.MakeFeatureLayer_management(streetcenterline_dissolve, 'StreetLine', queryline)
        arcpy.MakeFeatureLayer_management(split_points, 'StreetofPoint')
        arcpy.MakeFeatureLayer_management(streetcenterline_dissolve, 'streetsall', querywhole)
        arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'tostreet', querytostreet)
        arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'fromstreet', queryfromstreet)
        arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'extendedStreets', querywhole)

        try:
            #selecting points on isolated line and counting them (we may have to set up a system to make sure there is just one line segment)
            arcpy.SelectLayerByLocation_management('StreetofPoint', 'INTERSECT', 'StreetLine')
            result = arcpy.GetCount_management('StreetofPoint')
            count = int(result.getOutput(0))
            print(count)
            logger('succeed', filename, 'select points that intersect line segment', begin_time, '')
        except:
            logger('failed', filename, 'select points that intersect line segment', begin_time, arcpy.GetMessages())

            
        if count > 1:
            #We have multiple points so we need to split them in order and assign linear numbers
            tempstreetline = base + '\\' + 'temp_' + row[0]
            fill_name = tempstreetline.replace(' ', '_')
            print(fill_name)

            try:
                #Creating points for each side of the selected line segment
                arcpy.FeatureVerticesToPoints_management('StreetLine', fill_name, 'BOTH_ENDS')
                logger('succeed', filename, 'create end points on line', begin_time, '')
            except:
                logger('failed', filename, 'create end points on line', begin_time, arcpy.GetMessages())


            #tempstreetline count, should be two
            tempcount = arcpy.GetCount_management(fill_name)
            tempstreetlinecount = int(tempcount.getOutput(0))
            print('tempstreetline endpoint count ' + str(tempstreetlinecount))

            #looks like tempstreetline needs to be a layer for SelectLayerByLocation_management
            arcpy.MakeFeatureLayer_management(fill_name, 'tempstreetpoints')
            

            try:
                #So tempstreetline originally went into the selectlayerbylocation but had to make a layer: tempstreetpoints
                #This selects streets in street line that touch the two points in tempstreetpoints
                intersect = arcpy.SelectLayerByLocation_management('streetsall', 'INTERSECT', 'tempstreetpoints')
                intersectcount = arcpy.GetCount_management(intersect)
                intersectlinecount = int(intersectcount.getOutput(0))
                print('Streets touched by endpoints ' + str(intersectlinecount))
            
                #This takes the selection from above and removes the line segment the points are located on
                attrselect = arcpy.SelectLayerByAttribute_management(intersect, 'REMOVE_FROM_SELECTION', queryline)
                intersectrevcount = arcpy.GetCount_management(attrselect)
                intersectlinerevcount = int(intersectrevcount.getOutput(0))
                print('attrselect count ' + str(intersectlinerevcount))
                      
                if intersectlinerevcount < 1:
                    addressing = 'ToAddr_R'
                    
                    intersectzero = arcpy.SelectLayerByLocation_management('extendedStreets', 'INTERSECT', 'tempstreetpoints', '5 feet')
                    attrselectzero = arcpy.SelectLayerByLocation_management(intersectzero, 'INTERSECT', 'StreetofPoint',
                                                                            '5 feet', 'REMOVE_FROM_SELECTION')
                    intersectcountzero = arcpy.GetCount_management(attrselectzero)
                    intersectlinecountzero = int(intersectcountzero.getOutput(0))
                    print('intersectlinecountzero ' + str(intersectlinecountzero))
                    if intersectlinecountzero < 1:
                        #need to write in what to do for null value (this is taken care of by basing it off the fromstreet)
                        needextend = 2 ##'fromstreet',
                        nonmulti = 1           
                    else:
                        arcpy.MakeFeatureLayer_management(attrselectzero, 'StreetHighlow')
                else:     
                    arcpy.MakeFeatureLayer_management(attrselect, 'StreetHighlow')
                    addressing = 'MAX_ToAddr_R'
                logger('succeed', filename, 'select lines on either side of segment', begin_time, '')
            except:
                logger('failed', filename, 'select lines on either side of segment', begin_time, arcpy.GetMessages())

            #remaining selected lines are entered into a list
            if needextend == 2:
                print('Couldnt find adjacent road segements, switching to from')
            else:
                try:
                    with arcpy.da.UpdateCursor('StreetHighlow', addressing)as addrcompare:
                        for addr in addrcompare:
                            print(addr[0])
                            values.append(addr[0])
                    del addr, addrcompare
                    logger('succeed', filename, 'gathering values from selected lines', begin_time, '')
                except:
                    logger('failed', filename, 'gathering values from selected lines', begin_time, arcpy.GetMessages())

                if len(values) < 2: 
                    print('count less than 2')
                    if row[2] > values[0]:
                        queryorder = """{} = {}""".format(addressing, int(row[2]))
                        num.append(values[0])
                        nonmulti = 0
                    else:
                        queryorder = """{} = {}""".format(addressing, int(values[0]))
                        num.append(row[1])
                        nonmulti = 1
                    print(queryorder)
                
                else:
                    print('values are ' + str(values[0]) + ' and ' + str(values[1]))

                    #establishing query for high side of line segment. Also recording low address number
                    if values[0] > values[1]:
                        queryorder = """{} = {}""".format(addressing, int(values[0]))
                        num.append(values[1])
                    else:
                        queryorder = """{} = {}""".format(addressing, int(values[1]))
                        num.append(values[0])
                    print(queryorder)
                    nonmulti = 1

                #Here we select the line that contains the highest end address and call it finalstreet
                arcpy.MakeFeatureLayer_management('StreetHighlow', 'finalStreet', queryorder)
            
            #We then use final street to select the point related to it.
            if needextend == 2:
                finalstreet = 'StreetLine'
                StreetHighlow = 'fromstreet'
                nonmulti = 0
                num.append(row[1])
            else:
                finalstreet = 'finalStreet'
                StreetHighlow = 'StreetHighlow'
                
            deletepoint = arcpy.SelectLayerByLocation_management('tempstreetpoints', 'INTERSECT', finalstreet, '10 feet')
            if nonmulti == 0:
                deletepointtwo = arcpy.SelectLayerByLocation_management(deletepoint, 'INTERSECT', StreetHighlow,
                                                                        '10 feet', 'REMOVE_FROM_SELECTION')
                arcpy.DeleteFeatures_management(deletepointtwo)
                arcpy.SelectLayerByAttribute_management(deletepoint, "CLEAR_SELECTION")
            else:    
                arcpy.DeleteFeatures_management(deletepoint)
                arcpy.SelectLayerByAttribute_management(deletepoint, "CLEAR_SELECTION")
                
            deletepointcount = arcpy.GetCount_management('tempstreetpoints')
            deletepointcountzero = int(deletepointcount.getOutput(0))
            print('deletepointcountzero count ' + str(deletepointcountzero))

            #We then establish the distance from beginning low address to each point
            pointdistancetable = base + '\\' + 'temp_pointdistancetable'
            pointdistancetabletwo = pointdistancetable + '2'
            arcpy.PointDistance_analysis('tempstreetpoints', 'StreetofPoint', pointdistancetable)

            pointdistancecount = arcpy.GetCount_management(pointdistancetable)
            pointdistancecountzero = int(pointdistancecount.getOutput(0))
            print('pointdistancecountzero count ' + str(pointdistancecountzero))
            
            #Needed to add field for addresses field
            arcpy.AddField_management(pointdistancetable, 'orderAddr', 'LONG')
            print('added field')

            
            sorting = [['DISTANCE', "ASCENDING"]]
            arcpy.Sort_management(pointdistancetable, pointdistancetabletwo, sorting)
            with arcpy.da.UpdateCursor(pointdistancetabletwo, 'orderAddr')as makeaddr:
                for make in makeaddr:
                    num[0] += 4
                    make[0] = num[0]
                    makeaddr.updateRow(make)
            print('order address filled in ' + str(num))
            del make, makeaddr
            logger('succeed', filename, 'Max value for point assignment determined', begin_time, '')
            arcpy.MakeFeatureLayer_management(split_points, 'StreetofPointtwo', querypoint)
            StreetofPointtwoc = arcpy.GetCount_management('StreetofPointtwo')
            StreetofPointtwocount = int(StreetofPointtwoc.getOutput(0))
            print('Number of points queried ' + str(StreetofPointtwocount))
            
            lutDict = dict([(r[0], (r[1])) for r in arcpy.da.SearchCursor(pointdistancetabletwo, ["NEAR_FID","orderAddr"])])
            with arcpy.da.UpdateCursor('StreetofPointtwo', ["OBJECTID","MAX"]) as updateRows:
                for updateRow in updateRows:
                    print(updateRow)
                    joinFieldValue = updateRow[0]
                    updateRow[1] = lutDict[joinFieldValue]   
                    updateRows.updateRow(updateRow)
                    print(str(updateRow) + ' updated') 
            del updateRow, updateRows
            logger('succeed', filename, 'Max value for point updated', begin_time, '')
            deletelist = [fill_name, pointdistancetable, pointdistancetabletwo]
            for l in deletelist:
                arcpy.Delete_management(l)#test for cleanup!!!!!!!
                print('deleted ' + l)
            
                    
        else:
            row[3] = average
            print(row[3])
            cursor.updateRow(row)
            arcpy.Delete_management('StreetLine')
            arcpy.Delete_management('StreetofPoint')
            logger('succeed', filename, 'Max value for point updated', begin_time, '')
        print('point completed')

        #del make, makeaddr  #tempstreetline
        
        del values[:], num[:]
del row, cursor
print('print completed?')
logger('end', filename, 'end', begin_time, '')
