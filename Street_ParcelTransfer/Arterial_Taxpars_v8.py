import arcpy, os, time
from log_module import logger

###############################################################time ###########################################################################################
timestream = time.strftime("%m%d%y")
begin_time = time.time()
#####Variables#################################################################################################################################################

filename = 'Arterial_Taxpars_v7'
base = r'Database Connections\sde@gisdb06.sde.sde'
geo = 'arterial_taxpars' + timestream
workingpath = r'C:\Nightly Scripts\ArterialAttribution'
secondbase = workingpath + '\\' + geo + '.gdb'

taxpars = base + '\\' + 'sde.SDE.TaxPars'
strcenterlines = base + '\\' + 'sde.SDE.PlanningDepartmentRoadClass'
taxparsarterial = secondbase + '\\' + 'taxparsarterial1'
strcenterlinesbuffer = secondbase + '\\' + 'StreetCenterlines_buffer'
streetcenterline_reord = secondbase + '\\' + 'StreetCenterlines_reord'
streetcenterline_dissolve = secondbase + '\\' + 'streetcenterline_dissolve'
parcelfunctionalclass = base + '\\' + 'sde.SDE.ParcelFunctionalClass'
taxfields = ['StreetName', 'RoadClassification', 'StreetNumber', 'StreetCommunity', 'APPEARANCE']#4
streetfields = ['FULLNAME', 'APPRdClass', 'OBJECTID', 'APPEARANCE']#3
sorting = [['FULLNAME', "ASCENDING"], ['COMMUNITY', "ASCENDING"]]
stats = [['ToAddr_R', 'MAX'], ['FromAddr_R', 'MIN']]#not in use
PrimaryComm = 'PrimaryComm'
fieldsdissolve = 'FULLNAME;APPRdClass;APPEARANCE'
value = []                     
APP = []
sl_value = []
sl_APP = []
logger('start', filename,'','','')
arcpy.env.overwriteOutput = True

################################formatting#######################################################################################################################################################

print('copying')
try:
    arcpy.CreateFileGDB_management (workingpath, geo)
    arcpy.CopyFeatures_management(taxpars, taxparsarterial)
    print('copied')
    logger('succeed', filename, 'created GDB & copied taxpars', begin_time, '')
except:
    logger('failed', filename, 'created GDB & copied taxpars', begin_time, arcpy.GetMessages())
    print('created GDB & copied taxpars failed')
try:
    arcpy.Sort_management(strcenterlines, streetcenterline_reord, sorting)
    print('sorted streets')
    logger('succeed', filename, 'sorted', begin_time, '')
except:
    logger('failed', filename, 'sorted', begin_time, arcpy.GetMessages())
    print('sorted')
arcpy.MakeFeatureLayer_management(streetcenterline_reord, 'featurelayer')
print('removed out of county roads')
try:
    print('start dissolve')
    arcpy.Dissolve_management('featurelayer', streetcenterline_dissolve, fieldsdissolve, '', "SINGLE_PART", "DISSOLVE_LINES")
    print('dissolve completed')
    logger('succeed', filename, 'dissolved', begin_time, '')
except:
    logger('failed', filename, 'dissolved', begin_time, arcpy.GetMessages())
    print('dissolve failed')
arcpy.AddField_management(taxparsarterial, taxfields[1], 'TEXT')
print('added field')
arcpy.AddField_management(taxparsarterial, taxfields[4], 'TEXT')
print('added field')
logger('succeed', filename, 'added field', begin_time, '')
arcpy.Buffer_analysis(streetcenterline_dissolve, strcenterlinesbuffer, '1000 feet', 'FULL', 'ROUND', 'NONE', '', 'GEODESIC')
print('created buffers')
logger('succeed', filename, 'buffer analysis', begin_time, '')

with arcpy.da.UpdateCursor(strcenterlinesbuffer, streetfields) as space:
    for s in space:
        s[0] = s[0].replace('  ', ' ').replace("'", "")
        s[1] = s[1].replace(' ', '')
        s[3] = s[3].replace(' ', '')
        space.updateRow(s)
del s, space

with arcpy.da.UpdateCursor(taxparsarterial, taxfields) as taxspace:
    for tx in taxspace:
        try:
            tx[0] = tx[0].replace('  ', ' ')
        except:
            continue
        taxspace.updateRow(tx)
del tx, taxspace

################################Selection and calculating##########################################################################################################################################  
with arcpy.da.SearchCursor(strcenterlinesbuffer, streetfields) as cursor:
    for row in cursor:
        print('\n' + row[0])
        RCDict = {'I': 'Interstate', 'A': 'Arterial', 'C': 'Collector', 'L': 'Local', 'LL': 'Limited Local', 'RLA': 'Residential Local Attached',
                  'RLD': 'Residential Local Detached', 'RL': 'Restrictive Local', 'MUN': 'Municipal', 'UN': 'Unknown', '': 'Unknown',
                  'INT': 'Interstate'}
        value.append(RCDict[row[1]])
        APP.append(row[3])
        expression = "'{}'".format(value[0])
        expressionAPP = "'{}'".format(APP[0])     
        queryparcelone = """{} IN ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #17
        queryparceltwo = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #35
        queryparcelthree = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """#53
        queryparcelfour = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #71
        queryparcelfive = """'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', """ #89
        queryparcelsix = """'{}') """ #90
        queryparcelcomb = queryparcelone + queryparceltwo + queryparcelthree + queryparcelfour + queryparcelfive + queryparcelsix
        queryparcel =  queryparcelcomb.format('StreetName', row[0], row[0].replace(' S ', ''), row[0].replace(' N ', ''), #4
                                            row[0].replace(' W ', ''), row[0].replace(' E ', ''),  #6
                                            row[0].replace(' S', ''), row[0].replace(' N', ''), row[0].replace(' E', ''), row[0].replace(' W', ''), row[0].replace('W ', ''), #11
                                            row[0].replace('E ', ''), row[0].replace('N ', ''), row[0].replace('S ', ''), row[0].replace(' LN', ' LA'), #15
                                            row[0].replace('CC', 'CCC'), row[0].replace('LL', 'L'), row[0].replace('TT', 'T'), row[0].replace('MM', 'M'), #19
                                            row[0].replace('NN', 'N'), row[0].replace('SS', 'S'), row[0].replace('OO', 'O'), row[0].replace(' DR', ' RD'), #23
                                            row[0].replace(' RD', ' DR'), 'S ' + row[0], 'N ' + row[0], 'E ' + row[0], 'W ' + row[0], #28
                                            row[0].replace('CC', 'C'), row[0].replace('DD', 'D'), row[0].replace('EE', 'E'), row[0].replace('FF', 'F'), #32
                                            row[0].replace('GG', 'G'), row[0].replace('PP', 'P'), row[0].replace('RR', 'R'), row[0].replace('MTN', 'MT'), #36
                                            row[0].replace('MT', 'MTN'), row[0].replace('MTN', 'MOUNTAIN'), row[0].replace('MT', 'MOUNTAIN'), row[0].replace('MOUNTAIN', 'MT'), #40 
                                            row[0].replace('MOUNTAIN', 'MTN'), row[0].replace('C', 'CC'), row[0].replace('L', 'LL'), row[0].replace('T', 'TT'), #44
                                            row[0].replace('M', 'MM'), row[0].replace('N', 'NN'), row[0].replace('S', 'SS'), row[0].replace('O', 'OO'), #48
                                            row[0].replace('M', 'MM'), row[0].replace('D', 'DD'), row[0].replace('E', 'EE'), row[0].replace('F', 'FF'), #52
                                            row[0].replace('G', 'GG'), row[0].replace('P', 'PP'), row[0].replace('R', 'RR'), row[0].replace('MTN', 'MOUNT'), #56
                                            row[0].replace('MT', 'MOUNT'), row[0].replace('MOUNTAIN', 'MOUNT'), #58
                                            row[0].replace('S ', 'SOUTH '), row[0].replace('N ', 'NORTH '), #60
                                            row[0].replace('E ', 'EAST '), row[0].replace('W ', 'WEST '), row[0].replace('RL', 'REAL'), row[0].replace('TRCE', 'TER'), #64
                                            row[0].replace('GRAVLEY', 'GRAVELY'), row[0].replace('HL', 'HILL'), row[0].replace('WHEATLEY', 'WHEATLY'), #67
                                            row[0].replace('RODGE', 'RIDGE'), row[0].replace('MOUNTAIN VIEW', 'MOUNTAINVIEW'), row[0].replace('B J', 'BJ'), #70
                                            row[0].replace('CHSE', 'CHASE'), row[0].replace('CLF', 'CLIFF'), row[0].replace('VW', 'VIEW'), row[0].replace('CANADAY', 'CANADY'), #74
                                            row[0].replace('KING LINE', 'KING LINE ST'), row[0].replace('COLLINS', 'COLLIN'), row[0].replace('WOODLAND', 'WOODLAWN'), #77
                                            row[0].replace('PT', 'PTE'), row[0].replace('ST', 'ST EXT'), row[0].replace('TANGLEWOOD CT', 'TANGLERIDGE DR'), #80 
                                            row[0].replace('PT', 'POINT'), row[0].replace('NATHANEL', 'NATHANIEL'), row[0].replace(' LN', '  LN'), #83
                                            row[0].replace('SHADYVALE', 'SHADY VALE'), row[0].replace('TRL', 'TRAIL'), row[0].replace('GLENDAL', 'GRENDAL'), #86
                                            row[0].replace('FIELDS', 'FIELD'), row[0].replace('O', '0'), row[0].replace('LINE', 'LN'), row[0].replace('REAL', 'RL')) #90
            
        
                                                                        
        querystrbuffer = """{} = '{}' AND {} = '{}' AND {} = {}""".format(streetfields[0], row[0], streetfields[1], row[1], streetfields[2], row[2])
        #print(queryparcel + '\n' + querystrbuffer)
        selectparcels = 'selectedparcels'
        try:
            arcpy.MakeFeatureLayer_management(taxparsarterial, 'streetparcels', queryparcel)
            arcpy.MakeFeatureLayer_management(strcenterlinesbuffer, 'streetbuffer', querystrbuffer)
        
            intersect = arcpy.SelectLayerByLocation_management('streetparcels', 'INTERSECT', 'streetbuffer', '5 feet', 'NEW_SELECTION')
            arcpy.MakeFeatureLayer_management(intersect, selectparcels, queryparcel)
            intersectcount = arcpy.GetCount_management(selectparcels)
            intersectlinecount = int(intersectcount.getOutput(0))
            if intersectlinecount == 0:
                pass
            else:
                print(selectparcels + ' ' + str(row[2]) + ' ' + str(intersectlinecount))
                #CalculateField_management (in_table, field, expression, {expression_type}, {code_block}) '!Add_SubNum!'
                with arcpy.da.UpdateCursor(selectparcels, taxfields) as selector:
                    for sl in selector:
                        if sl[1] is not None:
                            splitter = sl[1].split(', ')
                            if value[0] in splitter:
                                sl[1] = sl[1]
                            else:
                                sl_value.append(sl[1])
                                sl[1] = value[0] + ', ' + sl_value[0]
                        else:
                            sl[1] = value[0] 
                        if sl[4] is not None:
                            splitterAPP = sl[4].split(', ')
                            if APP[0] in splitterAPP:
                                sl[4] = sl[4]
                            else:
                                sl_APP.append(sl[4])
                                sl[4] = APP[0] + ', ' + sl_APP[0]      
                        else:
                            sl[4] = APP[0] 
                        selector.updateRow(sl)
                        #arcpy.CalculateField_management(sl, taxfields[1], expression, 'PYTHON_9.3')
                        #arcpy.CalculateField_management(sl, taxfields[4], expressionAPP, 'PYTHON_9.3')
                        del sl_value[:]
                        del sl_APP[:]
                        
                del sl, selector
            arcpy.Delete_management(selectparcels)
            arcpy.Delete_management('streetbuffer')
            arcpy.Delete_management('streetparcels')
        except:
            logger('failed', filename, 'make street feature layers failed', begin_time, arcpy.GetMessages())
        del value[:]
        del APP[:]
logger('succeed', filename, 'arterial data written', begin_time, '')
################################copy and cleanup#######################################################################################################################################################     
del row, cursor

#try:
    #if arcpy.Exists(parcelfunctionalclass):
        #arcpy.Delete_management(parcelfunctionalclass)
    #logger('succeed', filename, 'ParcelFunctionalClass deleted from GISDB06', begin_time, '')
#except:
    #logger('failed', filename, 'ParcelFunctionalClass deleted from GISDB06', begin_time, arcpy.GetMessages())
try:
    arcpy.CopyFeatures_management(taxparsarterial, parcelfunctionalclass)
    logger('succeed', filename, 'ParcelFunctionalClass copied to GISDB06', begin_time, '')
except:
    logger('failed', filename, 'ParcelFunctionalClass deleted from GISDB06', begin_time, arcpy.GetMessages())
#try:
    #arcpy.Delete_management(secondbase)
    #logger('succeed', filename, 'delete gdb', begin_time, '')
#except:
    #logger('failed', filename, 'delete gdb', begin_time, arcpy.GetMessages())
print('completed run')
print('script complete')


