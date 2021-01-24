import arcpy, os, time
#from log_module import logger

begin_time = time.time()
filename = 'StreetDiss_v1'
#base = r'C:\mshoop\OtherWork\Mark_Cash\Parcel_Arterial\sample_data.gdb'
base = r'Database Connections\sde@GISDB06.sde'
geo = 'taxpars999'
workingpath = 'C:\mshoop\OtherWork\Mark_Cash\Parcel_Arterial'
secondbase = workingpath + '\\' + geo + '.gdb'
thirdbase = r'C:\mshoop\OtherWork\Mark_Cash\Parcel_Arterial\working'

taxpars = base + '\\' + 'sde.SDE.TaxPars'
strcenterlines = base + '\\' + 'sde.SDE.StreetCenterlines'
taxparsarterial = secondbase + '\\' + 'taxparsarterial1'
strcenterlinesbuffer = secondbase + '\\' + 'StreetCenterlines_buffer'
streetcenterline_reord = secondbase + '\\' + 'StreetCenterlines_reord'
streetcenterline_dissolve = secondbase + '\\' + 'streetcenterline_dissolve'
taxfields = ['StreetName', 'arterial', 'StreetNumber', 'StreetCommunity']#3
streetfields = ['FullName', 'St_FunctCls', 'MAX_ToAddr_R', 'OBJECTID']#3
sorting = [['FullName', "ASCENDING"], ['PrimaryComm', "ASCENDING"]]
stats = [['ToAddr_R', 'MAX'], ['FromAddr_R', 'MIN']]
idlist = []
jobs = []
PrimaryComm = 'PrimaryComm'
PriCoNo = ['CAMPOBELLO GREENVILLE', 'CHESNEE CHEROKEE', 'CHESNEE RUTHERFORD', 'COWPENS CHEROKEE', 'GREER GREENVILLE', 'LANDRUM GREENVILLE', #5
                 'PACOLET CHEROKEE', 'PACOLET UNION', 'PAULINE UNION', 'SPARTANBURG CHEROKEE', 'SPARTANBURG UNION', 'WOODRUFF LAURENS', 'GREENVILLE', #12
           'SIMPSONVILLE']  #13
countySQL = """{} NOT IN('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(arcpy.AddFieldDelimiters(streetcenterline_reord, PrimaryComm),
                                                                                                     PriCoNo[0], PriCoNo[1], PriCoNo[2], PriCoNo[3], PriCoNo[4],
                                                                                                     PriCoNo[5], PriCoNo[6], PriCoNo[7], PriCoNo[8], PriCoNo[9],
                                                                                                     PriCoNo[10], PriCoNo[11], PriCoNo[12], PriCoNo[13])

fieldsdissolve = 'FullName;St_FunctCls'
value = []                     

arcpy.env.overwriteOutput = True
print('copying')
#CreateFileGDB_management (out_folder_path, out_name, {out_version})
arcpy.CreateFileGDB_management (workingpath, geo)
arcpy.CopyFeatures_management(taxpars, taxparsarterial)
print('copied')
arcpy.Sort_management(strcenterlines, streetcenterline_reord, sorting)
print('sorted streets')
arcpy.RemoveDomainFromField_management(streetcenterline_reord, 'St_FunctCls')
print('removed domain')
arcpy.MakeFeatureLayer_management(streetcenterline_reord, 'featurelayer')#removed out of county query for now
print('removed out of county roads')
print('start dissolve')
arcpy.Dissolve_management('featurelayer', streetcenterline_dissolve, fieldsdissolve, stats, "SINGLE_PART", "DISSOLVE_LINES")
print('dissolve completed')
arcpy.AddField_management(taxparsarterial, taxfields[1], 'TEXT')
print('added field')
arcpy.Buffer_analysis(streetcenterline_dissolve, strcenterlinesbuffer, '1000 feet', 'FULL', 'ROUND', 'NONE', '', 'GEODESIC')
print('created buffers')

    
with arcpy.da.SearchCursor(strcenterlinesbuffer, streetfields) as cursor:
    for row in cursor:
        print('\n' + row[0])
        value.append(row[1])
        expression = "'{}'".format(value[0])
        splitter = row[0].split(' ')
        splitcount = len(splitter)
        if splitcount == 2:
            splitfirstspacetwo = splitter[0] + '  ' + splitter[1]
            splitsecondspacetwo = splitter[0] + splitter[1]
            splitsecondspace = row[0]
            splitfirstspace = row[0]
            splitthirdspace = row[0]
            splitfourthspace = row[0]
            splitfirstspacefour = row[0]
            splitsecondspacefour = row[0]
            splitthirdspacefour = row[0]
            splitfourthspacefour = row[0]
            splitfifthspacefour = row[0]
            splitsixthspacefour = row[0]
        elif splitcount == 3:
            splitsecondspace = splitter[0] + ' ' + splitter[1] + '  ' + splitter[2]
            splitfirstspace = splitter[0] + '  ' + splitter[1] + ' ' + splitter[2]
            splitthirdspace = splitter[0] + splitter[1] + ' ' + splitter[2]
            splitfourthspace = splitter[0] + ' ' + splitter[1] + splitter[2]
            splitfirstspacefour = row[0]
            splitsecondspacefour = row[0]
            splitthirdspacefour = row[0]
            splitfourthspacefour = row[0]
            splitfifthspacefour = row[0]
            splitsixthspacefour = row[0]
            splitfirstspacetwo = row[0]
            splitsecondspacetwo = row[0]
        elif splitcount == 4:
            splitfirstspacefour = splitter[0] + ' ' + splitter[1] + ' ' + splitter[2] + '  ' + splitter[2]
            splitsecondspacefour = splitter[0] + ' ' + splitter[1] + '  ' + splitter[2] + ' ' + splitter[2]
            splitthirdspacefour = splitter[0] + '  ' + splitter[1] + ' ' + splitter[2] + ' ' + splitter[2]
            splitfourthspacefour = splitter[0] + splitter[1] + ' ' + splitter[2] + ' ' + splitter[2]
            splitfifthspacefour = splitter[0] + ' ' + splitter[1] + splitter[2] + ' ' + splitter[2]
            splitsixthspacefour = splitter[0] + ' ' + splitter[1] + ' ' + splitter[2] + splitter[2]
            splitsecondspace = row[0]
            splitfirstspace = row[0]
            splitthirdspace = row[0]
            splitfourthspace = row[0]
            splitfirstspacetwo = row[0]
            splitsecondspacetwo = row[0]
        else:
            splitsecondspace = row[0]
            splitfirstspace = row[0]
            splitthirdspace = row[0]
            splitfourthspace = row[0]
            splitfirstspacefour = row[0]
            splitsecondspacefour = row[0]
            splitthirdspacefour = row[0]
            splitfourthspacefour = row[0]
            splitfifthspacefour = row[0]
            splitsixthspacefour = row[0]
            splitfirstspacetwo = row[0]
            splitsecondspacetwo = row[0]
            
        queryparcelone = """{} IN ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #17
        queryparceltwo = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #35
        queryparcelthree = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """#53
        queryparcelfour = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #71
        queryparcelfive = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #89
        queryparcelsix = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') """ #105
        queryparcelcomb = queryparcelone + queryparceltwo + queryparcelthree + queryparcelfour + queryparcelfive + queryparcelsix
        queryparcel =  queryparcelcomb.format('StreetName', row[0], row[0].replace(' S ', ''), row[0].replace(' N ', ''), #4
                                            row[0].replace(' W ', ''), row[0].replace(' E ', ''), row[0].replace(' ', '   '), row[0].replace(' ', '  '), row[0].replace(' ', '    '), #9
                                            row[0].replace(' S', ''), row[0].replace(' N', ''), row[0].replace(' E', ''), row[0].replace(' W', ''), row[0].replace('W ', ''), #14
                                            row[0].replace('E ', ''), row[0].replace('N ', ''), row[0].replace('S ', ''), row[0].replace(' LN', ' LA'), #18
                                            row[0].replace('CC', 'CCC'), row[0].replace('LL', 'L'), row[0].replace('TT', 'T'), row[0].replace('MM', 'M'), #22
                                            row[0].replace('NN', 'N'), row[0].replace('SS', 'S'), row[0].replace('OO', 'O'), row[0].replace(' DR', ' RD'), #26
                                            row[0].replace(' RD', ' DR'), 'S ' + row[0], 'N ' + row[0], 'E ' + row[0], 'W ' + row[0], splitfirstspace, #32
                                            splitsecondspace, row[0].replace('CC', 'C'), row[0].replace('DD', 'D'), row[0].replace('EE', 'E'), row[0].replace('FF', 'F'), #37
                                            row[0].replace('GG', 'G'), row[0].replace('PP', 'P'), row[0].replace('RR', 'R'), row[0].replace('MTN', 'MT'), #41
                                            row[0].replace('MT', 'MTN'), row[0].replace('MTN', 'MOUNTAIN'), row[0].replace('MT', 'MOUNTAIN'), row[0].replace('MOUNTAIN', 'MT'), #45 
                                            row[0].replace('MOUNTAIN', 'MTN'), row[0].replace('C', 'CC'), row[0].replace('L', 'LL'), row[0].replace('T', 'TT'), #49
                                            row[0].replace('M', 'MM'), row[0].replace('N', 'NN'), row[0].replace('S', 'SS'), row[0].replace('O', 'OO'), #53
                                            row[0].replace('M', 'MM'), row[0].replace('D', 'DD'), row[0].replace('E', 'EE'), row[0].replace('F', 'FF'), #57
                                            row[0].replace('G', 'GG'), row[0].replace('P', 'PP'), row[0].replace('R', 'RR'), row[0].replace('MTN', 'MOUNT'), #61
                                            row[0].replace('MT', 'MOUNT'), row[0].replace('MOUNTAIN', 'MOUNT'), splitfirstspacefour, splitsecondspacefour,  #65
                                            splitthirdspacefour, splitfourthspacefour, splitfifthspacefour, splitsixthspacefour, splitthirdspace, splitfourthspace, #71
                                            splitfirstspacetwo, splitsecondspacetwo, row[0].replace('S ', 'SOUTH '), row[0].replace('N ', 'NORTH '), #75
                                            row[0].replace('E ', 'EAST '), row[0].replace('W ', 'WEST '), row[0].replace('RL', 'REAL'), row[0].replace('TRCE', 'TER'), #79
                                            row[0].replace('GRAVLEY', 'GRAVELY'), row[0].replace('HL', 'HILL'), row[0].replace('WHEATLEY', 'WHEATLY'), #82
                                            row[0].replace('RODGE', 'RIDGE'), row[0].replace('MOUNTAIN VIEW', 'MOUNTAINVIEW'), row[0].replace('B J', 'BJ'), #85
                                            row[0].replace('CHSE', 'CHASE'), row[0].replace('CLF', 'CLIFF'), row[0].replace('VW', 'VIEW'), row[0].replace('CANADAY', 'CANADY'), #89
                                            row[0].replace('KING LINE', 'KING LINE ST'), row[0].replace('COLLINS', 'COLLIN'), row[0].replace('WOODLAND', 'WOODLAWN'), #92
                                            row[0].replace('PT', 'PTE'), row[0].replace('ST', 'ST EXT'), row[0].replace('TANGLEWOOD CT', 'TANGLERIDGE DR'), #95 
                                            row[0].replace('PT', 'POINT'), row[0].replace('NATHANEL', 'NATHANIEL'), row[0].replace(' LN', '  LN'), #98
                                            row[0].replace('SHADYVALE', 'SHADY VALE'), row[0].replace('TRL', 'TRAIL'), row[0].replace('GLENDAL', 'GRENDAL'), #101
                                            row[0].replace('FIELDS', 'FIELD'), row[0].replace('O', '0'), row[0].replace('LINE', 'LN'), row[0].replace('REAL', 'RL')) #105
                                                                        
        querystrbuffer = """{} = '{}' AND {} = '{}' AND {} = {}""".format('FullName', row[0], 'St_FunctCls', row[1], 'OBJECTID', row[3])
        #print(queryparcel + '\n' + querystrbuffer)
        selectparcels = 'selectedparcels'
        arcpy.MakeFeatureLayer_management(taxparsarterial, 'streetparcels', queryparcel) 
        arcpy.MakeFeatureLayer_management(strcenterlinesbuffer, 'streetbuffer', querystrbuffer)
        intersect = arcpy.SelectLayerByLocation_management('streetparcels', 'INTERSECT', 'streetbuffer', '5 feet', 'NEW_SELECTION')
        arcpy.MakeFeatureLayer_management(intersect, selectparcels, queryparcel)
        intersectcount = arcpy.GetCount_management(selectparcels)
        intersectlinecount = int(intersectcount.getOutput(0))
        if intersectlinecount == 0:
            pass
        else:
            print(selectparcels + ' ' + str(row[3]) + ' ' + str(intersectlinecount))
            #CalculateField_management (in_table, field, expression, {expression_type}, {code_block}) '!Add_SubNum!'
            arcpy.CalculateField_management(selectparcels, 'arterial', expression, 'PYTHON_9.3')
        del value[:]
    
del row, cursor

print('completed run')
print('script complete')
