import arcpy
import datetime
from log_module import logger
import time

begin_time = time.time()
filename = 'Split_Attr_v1'
base = r'\\files03\gis\Development\PMS\publicWorks.gdb'

streetcenterline_db06 = base + '\\' + 'StreetCenterLines_reord2'
streetcenterline_dissolve = base + '\\' + 'StreetCenterLines_Dissolve'
split_points = base + '\\' + 'PWtestPointsworking'
street_dissolve_split = base + '\\' + 'street_dissolve_split'
pointfields = ['FullName', 'FromAddr_R', 'ToAddr_R', 'MAX', 'OBJECTID', 'FROM_WIDTH', 'TO_WIDTH', #6
               'FROM_CURB', 'TO_CURB', 'FROM_LENGTH', 'TO_LENGTH', 'From_Sub_Name', 'To_Sub_Name', #12
               'From_Sub', 'To_Sub','Date_Created', 'Low_Cross', 'High_Cross'] #17
streetfields = ['Width', 'Surface', 'Length', 'Curbing', 'In_Sub', 'MAX', 'MIN_FromAddr_R', 'MAX_ToAddr_R', #7
                'NewPt', 'OBJECTID', 'Low_Cross', 'High_Cross', 'Sub_Name', 'St_FunctCls', 'Traffic_Count'] #14
streetlist = ['highstreet', 'lowstreet'] 
values = []
maxpointslist = []
otherpointslist = []
arcpy.env.overwriteOutput = True
logger('start', filename,'','','')
##############################################Splitting  ##########################################################################################
#Start with split
if arcpy.Exists(street_dissolve_split):
    arcpy.Delete_management(street_dissolve_split)
    print('found a copy deleted old street_dissolve_split')

arcpy.SplitLineAtPoint_management (streetcenterline_dissolve, split_points, street_dissolve_split, "5 feet")
print('starting MAX field update')


#filling in 'MAX' field with 'MAX_ToAddr_R'
with arcpy.da.UpdateCursor(street_dissolve_split, streetfields)as cursor:
    for row in cursor:
        row[5] = row[7]
        row[8] = 'N'
        if row[13] == 'Local':
            row[14] = 'LOW'
        elif row[13] in ('Collector', 'COLL'):
            row[14] = 'MEDIUM'
        elif row[13] in ('Minor Arterial', 'Major Arterial', 'Interstate'):
            row[14] = 'HIGH'
        else:
            row[14] is None
        cursor.updateRow(row)
del row, cursor        
print('field update completed')
logger('succeed', filename, 'filling out MAX field', begin_time, '')
##############################################Start main cursor##########################################################################################
#we now go through our list of points
with arcpy.da.SearchCursor(split_points, pointfields) as cursor:  
    for row in cursor:
        #when we go to a point row we set up these queries for the segment that was split and point we are on.
        queryline = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0], 'MAX_ToAddr_R', int(row[2]), 'MIN_FromAddr_R', int(row[1]))
        print(queryline)
        querywholestreet = """{} = '{}'""".format('FullName', row[0])
        print(querywholestreet)
        querypoint = """{} = '{}' AND {} = {}""".format('FullName', row[0], "MAX", row[3]) #Max is populated in AverageAlt
        print(querypoint)
        queryfromstreet = """{} = '{}'""".format('FullName', row[16])
        print(queryfromstreet)
        querytostreet = """{} = '{}'""".format('FullName', row[17])
        print(querytostreet)
        
        #We then use these queries to make layers of that specific data
        arcpy.MakeFeatureLayer_management(street_dissolve_split, 'StreetLine', queryline)
        arcpy.MakeFeatureLayer_management(split_points, 'StreetofPoint', querypoint)
        arcpy.MakeFeatureLayer_management(street_dissolve_split, 'WholeStreet', querywholestreet)
        arcpy.MakeFeatureLayer_management(split_points, 'split_points')
        arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'extendedStreets', querywholestreet)
        arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'tostreet', querytostreet)
        arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'fromstreet', queryfromstreet)

        #Here we are selecting two segments on either side of the split segment
        intersect = arcpy.SelectLayerByLocation_management('WholeStreet', 'INTERSECT', 'StreetofPoint')
        arcpy.MakeFeatureLayer_management(intersect, 'splitsegmentlines')
        intersecttwo = arcpy.SelectLayerByLocation_management('WholeStreet', 'INTERSECT', 'splitsegmentlines', '5 feet')
        intersecttwocount = arcpy.GetCount_management(intersecttwo)
        intersecttwolinecount = int(intersecttwocount.getOutput(0))
        print('intersecttwo count ' + str(intersecttwolinecount)) 
        attrselect = arcpy.SelectLayerByLocation_management(intersecttwo, 'INTERSECT', 'StreetofPoint', '5 feet', 'REMOVE_FROM_SELECTION')
        intersectcount = arcpy.GetCount_management(attrselect)
        intersectlinecount = int(intersectcount.getOutput(0))
        print('attrselect count ' + str(intersectlinecount))
        if intersectlinecount < 1:
            addressing = 'ToAddr_R'
            intersectzero = arcpy.SelectLayerByLocation_management('extendedStreets', 'INTERSECT', 'splitsegmentlines', '5 feet')
            attrselectzero = arcpy.SelectLayerByLocation_management(intersectzero, 'INTERSECT', 'StreetofPoint', '5 feet', 'REMOVE_FROM_SELECTION')
            intersectcountzero = arcpy.GetCount_management(attrselectzero)
            intersectlinecountzero = int(intersectcountzero.getOutput(0))
            print('attrselect count ' + str(intersectlinecountzero))
            if intersectlinecountzero < 1:
                #need to write in what to do for null value (this is taken care of by basing it off the fromstreet)
                print('we will now need to use the from street for {}'.format('FullName'))
                needextend = 2 ##'fromstreet',
                nonmulti = 2
            else:
                arcpy.MakeFeatureLayer_management(attrselectzero, 'StreetHighlow')
                needextend = 0
        else:
            arcpy.MakeFeatureLayer_management(attrselect, 'StreetHighlow')
            addressing = 'MAX_ToAddr_R'
            needextend = 1
            
        #This is just a quick way to catalogue the max values of those two segments, adding OBJECTID TO keep duplicates from happening.
        if needextend == 2:
            print('Couldnt find adjacent road segements, switching to from')
        else:
            with arcpy.da.SearchCursor('StreetHighlow', (addressing, 'OBJECTID'))as addrcompare:
                for addr in addrcompare:
                    print('high and low of each adjacent segment ' + str(addr[0]))
                    uniquevalue = [addr[0], addr[1]]
                    if uniquevalue[0] == 0:
                        pass
                    else:
                        values.append(uniquevalue)
            logger('succeed', filename, 'collected values', begin_time, '')    
            del addr, addrcompare
            for val in values:
                print('adjacent values are ' + str(val)) 

################## determining high and low segment ############################################################################################
            
            if len(values) < 2: #this is good
                print('value less than two')
                if row[2] > values[0][0]:
                    side = 'low'
                    queryorder = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0],
                                                                            addressing, int(values[0][0]), 'OBJECTID', int(values[0][1]))
                    nonmulti = 2
                    print('row[2] high, low side value 0 equal ' + queryorder)
         
                elif row[2] < values[0][0]:        
                    side = 'high'
                    queryorder = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0], addressing,
                                                                            int(values[0][0]), 'OBJECTID', int(values[0][1]))
                    nonmulti = 2
                    print('value 0 high, high side value 0 equal ' + queryorder)
                    
                else: #is good
                    nonmulti = 0
                    pointselect = arcpy.SelectLayerByLocation_management('split_points', 'INTERSECT', 'splitsegmentlines')
                    arcpy.MakeFeatureLayer_management(pointselect, 'Selectedpoints')
                    with arcpy.da.SearchCursor('Selectedpoints', 'MAX')as maxpoints:
                        for maxp in maxpoints:
                            maxpointslist.append(maxp[0])
                    del maxp, maxpoints
                    for maxpoint in maxpointslist:
                        if maxpoint != row[3]:
                            otherpoint = maxpoint
                        else:
                            currentpoint = maxpoint
                    if otherpoint > currentpoint:
                        buildlist = ['lowstreet', 'highstreet']
                        finalmax = otherpoint
                    else:
                        buildlist = ['highstreet', 'lowstreet']
                        finalmax = row[2]
                    
            else:
                #now based on which value is greater than the other we write some queries
                if values[0][0] > values[1][0]: 
                    queryorder = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0], addressing, int(values[1][0]),
                                                                                'OBJECTID', int(values[1][1]))
                    queryorderhigh = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0], addressing, int(values[0][0]),
                                                                                    'OBJECTID', int(values[0][1]))
                    print('value 0 high, low side value 1 equal ' + queryorder)
                    print('value 0 high, high side value 0 equal ' + queryorderhigh)
                    nonmulti = 1
                elif values[0][0] < values[1][0]: 
                    queryorder = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0], addressing, int(values[0][0]),
                                                                                'OBJECTID', int(values[0][1]))
                    queryorderhigh = """{} = '{}' AND {} = {} AND {} = {}""".format('FullName', row[0], addressing, int(values[1][0]),
                                                                                    'OBJECTID', int(values[1][1]))
                    print('value 1 high, low side value 0 equal ' + queryorder)
                    print('value 1 high, high side value 1 equal ' + queryorderhigh)
                    nonmulti = 1
                
                else: #this is tested, works well
                    nonmulti = 0
                    print('hit the else, which should mean both sides are equal')
                    pointselect = arcpy.SelectLayerByLocation_management('split_points', 'INTERSECT', 'splitsegmentlines')
                    arcpy.MakeFeatureLayer_management(pointselect, 'Selectedpoints')
                    with arcpy.da.SearchCursor('Selectedpoints', 'MAX')as maxpoints:
                        for maxp in maxpoints:
                            maxpointslist.append(maxp[0])
                    del maxp, maxpoints
                    if len(maxpointslist) == 2:
                        for maxpoint in maxpointslist:
                            if maxpoint != row[3]:
                                otherpoint = maxpoint
                            else:
                                currentpoint = maxpoint
                        if otherpoint > currentpoint:
                            buildlist = ['lowstreet', 'highstreet']
                            finalmax = otherpoint
                        else:
                            buildlist = ['highstreet', 'lowstreet']
                            finalmax = row[2]
                               
                    else:
                        for maxpoint in maxpointslist:
                            if maxpoint == row[3]:
                                currentpoint = maxpoint
                            else:
                                otherpointslist.append(maxpoint)
                        if otherpointslist[0] > otherpointslist[1]:
                            otherpoint = otherpointslist[0]                    
                        else:
                            otherpoint = otherpointslist[1]
                        finalmax = otherpoint
                        buildlist = ['lowstreet', 'highstreet']


#################HighLine and LowLine creation ##################################################################################################################
                    
        if nonmulti == 1: 
            #creating the low value line and using it to select the low part of the split segment
            if needextend == 0:
                arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'LowLine', queryorder)
            else:
                arcpy.MakeFeatureLayer_management(street_dissolve_split, 'LowLine', queryorder)
            lowstreet = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', 'LowLine')
            arcpy.MakeFeatureLayer_management(lowstreet, 'lowstreet')
            lowstreetcount = arcpy.GetCount_management('lowstreet')
            lowstreetcountprint = int(lowstreetcount.getOutput(0))
            print('lowstreet count ' + str(lowstreetcountprint))
            print('created lowstreet')
            logger('succeed', filename, 'created lowstreet', begin_time, '')
            arcpy.SelectLayerByAttribute_management('StreetLine', "CLEAR_SELECTION")
        
            #reversing to create the high part of the split segment
            if needextend == 0:
                arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'HighLine', queryorderhigh)
            else:
                arcpy.MakeFeatureLayer_management(street_dissolve_split, 'HighLine', queryorderhigh)
            highstreet = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', 'HighLine')
            arcpy.MakeFeatureLayer_management(highstreet, 'highstreet')
            highstreetcount = arcpy.GetCount_management('highstreet')
            highstreetcountprint = int(highstreetcount.getOutput(0))
            print('highstreet count ' + str(highstreetcountprint))
            print('created highstreet')
            logger('succeed', filename, 'created highstreet', begin_time, '')
            
        elif nonmulti == 2: #this is a for single value selection (one line to show high or low)      
            if needextend == 0:
                arcpy.MakeFeatureLayer_management(streetcenterline_db06, 'Line', queryorder)
                selectstreet = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', 'Line')
            elif needextend == 2:
                if row[16] == None:
                    crossstreetone = 'tostreet'
                    side = 'high'
                    print('unfortunetly fromstreet doesnt exist for some reason so switching to to street')
                else:
                    crossstreetone = 'fromstreet'
                    side = 'low'
                    print('so we are using the fromstreet')
                selectstreet = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', crossstreetone)
            else:
                arcpy.MakeFeatureLayer_management(street_dissolve_split, 'Line', queryorder)
                selectstreet = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', 'Line')
            if side == 'low':
                sidelist = ['lowstreet', 'highstreet']
            else:
                sidelist = ['highstreet', 'lowstreet']
            arcpy.MakeFeatureLayer_management(selectstreet, sidelist[0])
            logger('succeed', filename, 'created ' + sidelist[0], begin_time, '')
            arcpy.SelectLayerByAttribute_management('splitsegmentlines', "CLEAR_SELECTION")
            reverseselection = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', sidelist[0])
            if needextend == 2:
                unselectstreet = arcpy.SelectLayerByLocation_management(reverseselection, 'INTERSECT', crossstreetone, '10 feet', 'REMOVE_FROM_SELECTION')
            else:
                unselectstreet = arcpy.SelectLayerByLocation_management(reverseselection, 'INTERSECT', 'Line', '10 feet', 'REMOVE_FROM_SELECTION')
            arcpy.MakeFeatureLayer_management(unselectstreet, sidelist[1])
            logger('succeed', filename, 'created ' + sidelist[1], begin_time, '') 
            
        else: 
            queryorderhigh = """{} = '{}' AND {} = {}""".format('FullName', row[0], 'MAX', otherpoint)        
            arcpy.MakeFeatureLayer_management(split_points, 'otherpoint', queryorderhigh)
            maxpointselect = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', 'otherpoint')
            arcpy.MakeFeatureLayer_management(maxpointselect, buildlist[1])
            logger('succeed', filename, 'created ' + buildlist[1], begin_time, '')
            lowstreet = arcpy.SelectLayerByLocation_management('splitsegmentlines', 'INTERSECT', 'otherpoint', '10 feet', 'SWITCH_SELECTION')
            arcpy.MakeFeatureLayer_management(lowstreet, buildlist[0])
            logger('succeed', filename, 'created ' + buildlist[0], begin_time, '')
            highstreetcount = arcpy.GetCount_management('highstreet')
            highstreetcountprint = int(highstreetcount.getOutput(0))
            print('highstreet count ' + str(highstreetcountprint))
            lowstreetcount = arcpy.GetCount_management('lowstreet')
            lowstreetcountprint = int(lowstreetcount.getOutput(0))
            print('lowstreet count ' + str(lowstreetcountprint))
        
 #################taking point attributes and filling in the values for the low and high split segments. ############################################################
            
        for s in streetlist:    
            with arcpy.da.UpdateCursor(s, streetfields)as makeaddr:
                for addr in makeaddr:
                    #This is for the 00100 and 00025 thing for RoadSegmentID
                    if row[15] > datetime.datetime(2020, 12, 25) or row[15] is None: 
                        addr[8] = 'Y'
                    else: addr[8] = 'N'
                    #addr[8] = 'N'
                    if s == 'lowstreet':
                        if row[5] is not None:
                            addr[0] = row[5]#width
                        if row[9] is not None:
                            addr[2] = row[9]#Length
                        if row[7] is not None:
                            addr[3] = row[7]#curbing
                        if row[13] is not None:
                            addr[4] = row[13]#in sub
                        addr[5] = row[3]#max
                        if row[11] is not None:
                            addr[12] = row[11]#Sub_Name
                        print('filling in lowstreet OBJECTID ' + str(addr[9]))
                    else:
                        print('filling in highstreet OBJECTID ' + str(addr[9]))
                        if row[6] is not None:
                            addr[0] = row[6]  #width
                        if row[12] is not None:    
                            addr[12] = row[12] #Sub_Name
                        if row[10] is not None:
                            addr[2] = row[10] #Length
                        if row[8] is not None:
                            addr[3] = row[8]  #curbing
                        if row[14] is not None:
                            addr[4] = row[14] #in sub
                        if nonmulti == 0:
                            addr[5] = finalmax
                        else: addr[5] = addr[7] #MAX this field is to keep linear addr direction states same from beginning
                    makeaddr.updateRow(addr)
            del makeaddr, addr
        del values[:]
        del maxpointslist[:]
        del otherpointslist[:]
        print('values filled in for ' + row[0])
        print('completed {} MAX {}'.format(row[0], row[3]) + '\n' + '\n' + '\n')
del row, cursor         
print('script completed')
logger('end', filename, 'end', begin_time, '')
