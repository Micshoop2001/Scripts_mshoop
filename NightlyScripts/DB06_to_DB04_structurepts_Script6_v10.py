import arcpy
import os
import time
from datetime import timedelta
from datetime import datetime
###############################################################time & log setup###########################################################################################
#Time##
timestream = time.strftime("%m%d%y")
timecop = datetime.now() - timedelta(days= 3) #log maintenance
timetravel = timecop.strftime("%m%d%y") #log maintenance
propmonth = time.strftime('%B')
propday = time.strftime('%d')
propyear = time.strftime('%Y')
militaryhour = time.strftime('%H')
propminute = time.strftime('%M')
propsecond = time.strftime('%S')
dytextdate = propmonth + ' ' + propday + ', ' + propyear
HMStextdate = militaryhour + ':' + propminute + ' ' + propsecond + ' Seconds '
fulltime = 'Date: ' + dytextdate + ' Time: ' + HMStextdate
begin_time = time.time()

script_working = r'C:\Nightly Scripts\DB6_to_DB4_Log'
logtime = script_working + '\\DB06_to_DB04_v4' + timestream + '.txt'

#Start Log
track = open(logtime,"a") #We probably need to make a new log
Header = 'Start DB06_to_DB04_v4 script 6, structurepts'
print('Start DB06_to_DB04_v4 script 6, structurepts ' + fulltime + '\n')
track.write('\n' + '\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################
fullDisplayTen = r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.StructurePts' #this will be path for Display 10
structurepts_db06 = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.StructurePts'
oldDisplayTen = fullDisplayTen + '_old'
field_delete = []
fullhomefile, data = os.path.split(fullDisplayTen)
expressionAUNUM = '!Add_SubNum!'
expressoAUNUM = '!Add_NumSuf!'
NadaAUNUM = 'Add_NumSuf IS NULL'##SQL Statement
NadoAUNUM = 'Add_NumSuf IS NOT NULL'##SQL Statement

####StructurePts###########################################################################################

FULLNAME = '"FULLNAME \"FULLNAME\" true true false 50 Text 0 0 ,First,#,' + structurepts_db06 + ',FullName,-1,-1;'
STADD = 'STADD \"STADD\" true true false 6 Text 0 0 ,First,#,' + structurepts_db06 + ',Add_Number,-1,-1;'
PREDIR = 'PREDIR \"PREDIR\" true true false 2 Text 0 0 ,First,#,' + structurepts_db06 + ',St_PreDir,-1,-1;'
STREETNAME = 'STREETNAME \"STREETNAME\" true true false 26 Text 0 0 ,First,#,' + structurepts_db06 + ',St_Name,-1,-1;'
TYPE = 'TYPE \"TYPE\" true true false 4 Text 0 0 ,First,#,' + structurepts_db06 + ',St_PosType,-1,-1;'
SUFDIR = 'SUFDIR \"SUFDIR\" true true false 10 Text 0 0 ,First,#,' + structurepts_db06 + ',St_PosDir,-1,-1;'
SUFQUAL = 'SUFQUAL \"SUFQUAL\" true true false 16 Text 0 0 ,First,#,' + structurepts_db06 + ',St_PosMod,-1,-1;'
COMMUNITY = 'COMMUNITY "COMMUNITY" true true false 15 Text 0 0 ,First,#,' + structurepts_db06 + ',MSAGComm,0,14;'
ZIP = 'ZIP \"ZIP\" true true false 5 Text 0 0 ,First,#,' + structurepts_db06 + ',Post_Code,-1,-1;'
Y_COORD = 'Y_COORD \"Y_COORD\" true true false 8 Double 0 0 ,First,#,' + structurepts_db06 + ',Y_Coord,-1,-1;'
X_COORD = 'X_COORD \"X_COORD\" true true false 8 Double 0 0 ,First,#,' + structurepts_db06 + ',X_Coord,-1,-1;'
CODE = 'CODE "Code" true true false 15 Text 0 0 ,First,#,' + structurepts_db06 + ',StructType,-1,-1;'
COMMENTS = 'COMMENTS "COMMENTS" true true false 50 Text 0 0 ,First,#,' + structurepts_db06 + ',SbDivision,0,49;'
created_user = 'created_user \"created_user\" true true false 255 Text 0 0 ,First,#,' + structurepts_db06 + ',created_user,-1,-1;'
created_date = 'created_date \"created_date\" true true false 8 Date 0 0 ,First,#,' + structurepts_db06 + ',created_date,-1,-1;'
last_edited_user = 'last_edited_user \"last_edited_user\" true true false 255 Text 0 0 ,First,#,' + structurepts_db06 + ',last_edited_user,-1,-1;'
last_edited_date = 'last_edited_date \"last_edited_date\" true true false 8 Date 0 0 ,First,#,' + structurepts_db06 + ',last_edited_date,-1,-1"'

append_specialvariables_all = FULLNAME + STADD + PREDIR + STREETNAME + TYPE + SUFDIR + SUFQUAL + COMMUNITY + ZIP\
                              + CODE + Y_COORD + X_COORD + COMMENTS + created_user + created_date + last_edited_user + last_edited_date

####StructurePts###########################################################################################
arcpy.env.workspace = fullhomefile
arcpy.env.overwriteOutput = True

try:
    if arcpy.Exists(fullDisplayTen):
        try:
            arcpy.Delete_management(oldDisplayTen)####Delete all the matching old display 10 in DB04
            print('Structurepts_old deleted from display10. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('Structurepts_old deleted from display10. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!Structurepts_old deleted from display10 failed!!!!!!!!!!!!!!!!!!!'
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!Structurepts_old deleted from display10 failed!!!!!!!!!!!!!!!!!!!!!!'
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        try:
            arcpy.CopyFeatures_management(fullDisplayTen, oldDisplayTen) ####Make existing display 10 stuff old display 10 stuff
            print('structurepts copy from display10 to structurepts_old. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('Structurepts copy from display10 to Structurepts_old. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!Structurepts copy failed!!!!!!!!!!!!!!!!!!!'
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!Structurepts copy failed!!!!!!!!!!!!!!!!!!!!!!'
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        try:
            arcpy.TruncateTable_management(fullDisplayTen)
            print('Structurepts data deleted in display10. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('Structurepts data deleted in display10. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!Structurepts data deleted in display10 failed!!!!!!!!!!!!!!!!!!!'
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!Structurepts data deleted in display10 failed!!!!!!!!!!!!!!!!!!!!!!'
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    else:
        print('Structurepts not found in display10.'+ '\n')
        track.write('Structurepts not found in display10.' + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!Structurepts exists function failed!!!!!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!Structurepts exists function failed!!!!!!!!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
try:
    arcpy.Append_management(structurepts_db06, fullDisplayTen, "NO_TEST", append_specialvariables_all, "")
    print('Structurepts data appended to Structurepts in display10. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('Structurepts data appended to Structurepts in display10. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!Structurepts data append to Structurepts in display10 failed!!!!!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!Structurepts data append to Structurepts in display10 failed!!!!!!!!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

#AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias},
# {field_is_nullable}, {field_is_required}, {field_domain})

try:
    arcpy.MakeFeatureLayer_management(fullDisplayTen, 'AUNUM_COMM')
    print('FeatureLayer for StructurePts created' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('FeatureLayer for StructurePts created' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!FeatureLayer for StructurePts created failed!!!!!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!FeatureLayer for StructurePts created failed!!!!!!!!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
try:
    arcpy.AddJoin_management('AUNUM_COMM', 'FULLNAME', structurepts_db06, 'FullName')
    print('addjoin GISDB04 to GISDB06 based on FullName' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('addjoin GISDB04 to GISDB06 based on FullName' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!addjoin GISDB04 to GISDB06 based on FullName failed!!!!!!!!!!!!!!!!!!!!!!!! '
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!addjoin GISDB04 to GISDB06 based on FullName failed!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

try:
    #calculate StructurePts, Field:TestField, expression: Write in Add_SubNum were Add_NumSuf is NULL
    arcpy.SelectLayerByAttribute_management('AUNUM_COMM', 'NEW_SELECTION', NadaAUNUM)
    print('SelectLayerByAttribute were Add_NumSuf is NULL' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('SelectLayerByAttribute were Add_NumSuf is NULL' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!SelectLayerByAttribute were Add_NumSuf is NULL failed!!!!!!!!!!!!!!!!!!!!!!!! '
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!SelectLayerByAttribute were Add_NumSuf is NULL failed!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

try:
    arcpy.CalculateField_management('AUNUM_COMM', 'AUNUMBER', expressionAUNUM, 'PYTHON_9.3')
    print('Add_SubNum is calculated in AUNUMBER' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('Add_SubNum is calculated in AUNUMBER' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!Add_SubNum is calculated in AUNUMBER failed!!!!!!!!!!!!!!!!!!!!!!!! '
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!Add_SubNum is calculated in AUNUMBER failed!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

try:
    #calculate StructurePts, Field:TestField, expression: Write in Add_NumSuf were Add_NumSuf is NOT NULL
    arcpy.SelectLayerByAttribute_management('AUNUM_COMM', 'NEW_SELECTION', NadoAUNUM)
    print('SelectLayerByAttribute were Add_NumSuf is NOT NULL' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('SelectLayerByAttribute were Add_NumSuf is NOT NULL' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!SelectLayerByAttribute were Add_NumSuf is NOT NULL failed!!!!!!!!!!!!!!!!!!!!!!!! '
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!SelectLayerByAttribute were Add_NumSuf is NOT NULL failed!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                
try:
    arcpy.CalculateField_management('AUNUM_COMM', 'AUNUMBER', expressoAUNUM, 'PYTHON_9.3')
    print('Add_NumSuf is calculated in AUNUMBER' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('Add_NumSuf is calculated in AUNUMBER' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!Add_NumSuf is calculated in AUNUMBER failed!!!!!!!!!!!!!!!!!!!!!!!! '
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!Add_NumSuf is calculated in AUNUMBER failed!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')



track.write('\n' + '\n' + 'DB06_to_DB04_v4 script 6, structurepts completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n')
track.write('\n' + '\n' + 'TokenStrucPts' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4 script 6, structurepts completed')
#Written by Michael Shoop 
#Version #9 completed 6/18/20 #DB06_to_DB04_structurepts_Script6_v10










    
