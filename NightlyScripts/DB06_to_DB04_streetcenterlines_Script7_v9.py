import arcpy
import os
import time
from datetime import timedelta
from datetime import datetime
#import smtplib
#import shutil
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
Header = "Start DB06_to_DB04_v4 script 7, streetcenterlines"
print('Start DB06_to_DB04_v4 script 7, streetcenterlines ' + fulltime + '\n')
track.write('\n' + '\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################
fullDisplayTen = r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.StreetCenterLines' #this will be path for Display 10
oldDisplayTen = fullDisplayTen + '_old'
streetcenterline_db06 = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.StreetCenterlines'
path, data = os.path.split(fullDisplayTen)
expressionSeg = "getClass(str('!ROADSEGID!'))"

Segmentid_code2 = '''def getClass(seg_value):
                        if 'u' in seg_value:
                            seg_one = seg_value.replace('u', '')
                        else:
                            seg_one = seg_value
                        if '"' in seg_one:
                            seg_two = seg_one.replace('"', '')
                        else:
                            seg_two = seg_one
                        
                        if '.' in seg_two:
                            seg_three = seg_two.replace('.', '')
                        else:
                            seg_three = seg_two
                        if '-' in seg_three:
                            seg_list = seg_three.split('-', 1)
                            seg_four = seg_list[1]
                        else:
                            seg_four = '0'
                        if seg_four.startswith('0'):
                            seg_five = seg_four.replace('0', '')
                        else:
                            seg_five = seg_four
                        if seg_five == '' or seg_five == ' ':
                            seg_six = None
                            return seg_six
                        else:
                            return int(seg_five)'''
                                       
roadid = '!ROADSEGID!'
###############StreetCenterlines#########################################################################################not changed yet

FULLNAME = '"FULLNAME \"FULLNAME\" true true false 60 Text 0 0 ,First,#,' + streetcenterline_db06 + ',FullName,-1,-1;'
MAINTERESP = 'MAINTERESP \"MAINTERESPON\" true true false 4 Text 0 0 ,First,#,' + streetcenterline_db06 + ',OwnedBy,-1,-1;'
LOWLEFTADD = 'LOWLEFTADD \"LOWLEFTADD\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',FromAddr_L,-1,-1;'
LOWERRIGHT = 'LOWERRIGHT \"LOWERRIGHTADD\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',FromAddr_R,-1,-1;'
HIGHLEFTAD = 'HIGHLEFTAD \"HIGHLEFTADD\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',ToAddr_L,-1,-1;'
HIGHRIGHTA = 'HIGHRIGHTA \"HIGHRIGHTADD\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',ToAddr_R,-1,-1;'
PUBLWORKSS = 'PUBLWORKSS \"PUBLWORKSSEGNUM\" true true false 8 Text 0 0 ,First,#,' + streetcenterline_db06 + ',RouteID,-1,-1;'
COUNTYORDC = 'COUNTYORDC \"COUNTYORDCLASS\" true true false 4 Text 0 0 ,First,#,' + streetcenterline_db06 + ',PZClass,-1,-1;' #check this
STATEHWYCL = 'STATEHWYCL \"STATEHWYCLASS\" true true false 4 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_FunctCls,-1,-1;'
COMMUNITY = 'COMMUNITY \"COMMUNITY\" true true false 60 Text 0 0 ,First,#,' + streetcenterline_db06 + ',PrimaryComm,-1,-1;'
ROADSEGID = 'ROADSEGID \"ROADSEGID\" true true false 10 Text 0 0 ,First,#,' + streetcenterline_db06 + ',RoadSegID,-1,-1;'
ROADID = 'ROADID \"ROADID\" true true false 60 Text 0 0 ,First,#,' + streetcenterline_db06 + ',HighwayNum,-1,-1;'
LEFTCOMM = 'LEFTCOMM \"LEFTCOMM\" true true false 60 Text 0 0 ,First,#,' + streetcenterline_db06 + ',MSAGComm_L,-1,-1;'
RIGHTCOMM = 'RIGHTCOMM \"RIGHTCOMM\" true true false 60 Text 0 0 ,First,#,' + streetcenterline_db06 + ',MSAGComm_R,-1,-1;'
LEFTZIP = 'LEFTZIP \"LEFTZIP\" true true false 4 Long 0 0 ,First,#,' + streetcenterline_db06 + ',PostCode_L,-1,-1;'
RIGHTZIP = 'RIGHTZIP \"RIGHTZIP\" true true false 4 Long 0 0 ,First,#,' + streetcenterline_db06 + ',PostCode_R,-1,-1;'
LEFTESN = 'LEFTESN \"LEFTESN\" true true false 4 Long 0 0 ,First,#,' + streetcenterline_db06 + ',ESN_L,-1,-1;'
RIGHTESN = 'RIGHTESN \"RIGHTESN\" true true false 4 Long 0 0 ,First,#,' + streetcenterline_db06 + ',ESN_R,-1,-1;'
PREDIR = 'PREDIR \"PREDIR\" true true false 5 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_PreDir,-1,-1;'
STNAME = 'STNAME \"STNAME\" true true false 50 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_Name,-1,-1;'
TYPE = 'TYPE \"TYPE\" true true false 10 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_PosType,-1,-1;'
SUFQUAL = 'SUFQUAL \"SUFQUAL\" true true false 16 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_PosMod,-1,-1;'
SUFDIR = 'SUFDIR \"SUFDIR\" true true false 10 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_PosDir,-1,-1;'
created_user = 'created_user \"created_user\" true true false 255 Text 0 0 ,First,#,' + streetcenterline_db06 + ',created_user,-1,-1;'
created_date = 'created_date \"created_date\" true true false 8 Date 0 0 ,First,#,' + streetcenterline_db06 + ',created_date,-1,-1;'
last_edited_user = 'last_edited_user \"last_edited_user\" true true false 255 Text 0 0 ,First,#,' + streetcenterline_db06 + ',last_edited_user,-1,-1;'
last_edited_date = 'last_edited_date \"last_edited_date\" true true false 8 Date 0 0 ,First,#,' + streetcenterline_db06 + ',last_edited_date,-1,-1;'
RESP_AGENCY = 'RESP_AGENCY \"RESP_AGENCY\" true true false 50 Text 0 0 ,First,#,' + streetcenterline_db06 + ',MaintResp,-1,-1;'
City_Left = 'City_Left \"City_Left\" true true false 20 Text 0 0 ,First,#,' + streetcenterline_db06 + ',IncMuni_L,-1,-1;'
City_Right = 'City_Right \"City_Right\" true true false 20 Text 0 0 ,First,#,' + streetcenterline_db06 + ',IncMuni_R,-1,-1;'
F_ZLEV = 'F_ZLEV \"F_ZLEV\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',F_ZLEV,-1,-1;'
T_ZLEV = 'T_ZLEV \"T_ZLEV\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',T_ZLEV,-1,-1;'
SPEED = 'SPEED \"SPEED\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',SpeedLimit,-1,-1;'
COST = 'COST \"COST\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',COST,-1,-1;'
FT_Cost = 'FT_Cost \"FT_Cost\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',FT_COST,-1,-1;'
TF_Cost = 'TF_Cost \"TF_Cost\" true true false 8 Double 0 0 ,First,#,' + streetcenterline_db06 + ',TF_COST,-1,-1;'
OneWay = 'OneWay \"OneWay\" true true false 2 Text 0 0 ,First,#,' + streetcenterline_db06 + ',OneWay,-1,-1;'
LOW_Cross = 'LOW_Cross \"LOW_Cross\" true true false 85 Text 0 0 ,First,#,' + streetcenterline_db06 + ',Low_Cross,-1,-1;'
HIGH_Cross = 'HIGH_Cross \"HIGH_Cross\" true true false 85 Text 0 0 ,First,#,' + streetcenterline_db06 + ',High_Cross,-1,-1;'
PRE_MOD = 'PRE_MOD \"PRE_MOD\" true true false 15 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_PreMod,-1,-1;'
PRE_TYPE = 'PRE_TYPE \"PRE_TYPE\" true true false 20 Text 0 0 ,First,#,' + streetcenterline_db06 + ',St_PreType,-1,-1;'
ROADWAY_ONLY = 'ROADWAY_ONLY \"ROADWAY_ONLY\" true true false 50 Text 0 0 ,First,#,' + streetcenterline_db06 + ',RoadWyOnly,-1,-1"'


append_specialvariables_one = FULLNAME + MAINTERESP + LOWLEFTADD + LOWERRIGHT + HIGHLEFTAD + HIGHRIGHTA + PUBLWORKSS\
                              + COUNTYORDC + STATEHWYCL + COMMUNITY + ROADSEGID + ROADID + LEFTCOMM + RIGHTCOMM + LEFTZIP + RIGHTZIP
append_specialvariables_two = LEFTESN + RIGHTESN + PREDIR + STNAME + TYPE + SUFQUAL + SUFDIR + created_user + created_date\
                              + last_edited_user + last_edited_date + RESP_AGENCY + City_Left + City_Right + F_ZLEV + T_ZLEV
append_specialvariables_three = SPEED + COST + FT_Cost + TF_Cost + OneWay + LOW_Cross + HIGH_Cross + PRE_MOD + PRE_TYPE + ROADWAY_ONLY
append_specialvariables_all = append_specialvariables_one + append_specialvariables_two + append_specialvariables_three
###############StreetCenterlines#########################################################################################
arcpy.env.workspace = fullDisplayTen
arcpy.env.overwriteOutput = True
try:
    if arcpy.Exists(fullDisplayTen):
        try:
            arcpy.Delete_management(oldDisplayTen)####Delete all the matching old display 10 in DB04
            print('Streetcenterline_old deleted from display10. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('Streetcenterline_old deleted from display10. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!Streetcenterline_old deleted from display10 failed!!!!!!!!!!!!!!!!!!!'
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!Streetcenterline_old deleted from display10 failed!!!!!!!!!!!!!!!!!!!!!!'
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        try:
            arcpy.CopyFeatures_management(fullDisplayTen, oldDisplayTen) ####Make existing display 10 stuff old display 10 stuff
            print('Streetcenterline copy from display10 to structurepts_old. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('Streetcenterline copy from display10 to Structurepts_old. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!Streetcenterline copy failed!!!!!!!!!!!!!!!!!!!'
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!Streetcenterline copy failed!!!!!!!!!!!!!!!!!!!!!!'
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        try:
            arcpy.TruncateTable_management(fullDisplayTen)
            print('Streetcenterline data deleted from DB04. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('Streetcenterline data deleted from DB04. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!Streetcenterline data deleted from DB04 failed!!!!!!!!!!!!!!!!!!!'
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!Streetcenterline data deleted from DB04 failed!!!!!!!!!!!!!!!!!!!!!!'
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    else:
        print('Streetcenterline not found on DB04.'+ '\n')
        track.write('Streetcenterline not found on DB04.' + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!Streetcenterline exists function failed!!!!!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!Streetcenterline exists function failed!!!!!!!!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
try:
    arcpy.Append_management(streetcenterline_db06, fullDisplayTen, "NO_TEST", append_specialvariables_all, "")
    print('Streetcenterline data appended to Streetcenterline in DB04. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('Streetcenterline data appended to Streetcenterline in DB04. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!Streetcenterline data append to Streetcenterline in DB04 failed!!!!!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!Streetcenterline data append to Streetcenterline in DB04 failed!!!!!!!!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

try:
    arcpy.MakeFeatureLayer_management(fullDisplayTen, 'SEGMENTID_layer')
    print('FeatureLayer for StreetCenterLines created' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('FeatureLayer for StreetCenterLines created' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!FeatureLayer for StreetCenterLines created failed!!!!!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!FeatureLayer for StreetCenterLines created failed!!!!!!!!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

try:
    arcpy.CalculateField_management('SEGMENTID_layer', 'SEGMENTID', expressionSeg, 'PYTHON_9.3', Segmentid_code2)
    print('calculate SEGMENTID' + '%s total minutes' % (time.time() - begin_time) + '\n')
    track.write('calculate SEGMENTID' + ' %s total minutes' % (time.time() - begin_time) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!calculate SEGMENTID failed!!!!!!!!!!!!!!!!!!!!!!!! '
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!calculate SEGMENTID failed!!!!!!!!!!!!!!!' + ' %s total minutes' % (round((time.time() - begin_time)/60,2))
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
try:
    arcpy.AddGeometryAttributes_management('SEGMENTID_layer', 'LENGTH', 'FEET_US')
    print('Calculated Geometry for P1_Shape_Len' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('Calculated Geometry for P1_Shape_Len' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!Calculated Geometry for P1_Shape_Len failed!!!!!!!!!!!!!!!!!!!!!!!! '
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!Calculated Geometry for P1_Shape_Len failed!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
try:
    arcpy.DeleteField_management(fullDisplayTen, 'P1_Shape_Len')
    print('{} field deleted in display10. '.format('P1_Shape_Len') + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('{} field deleted in display10. '.format('P1_Shape_Len') + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!{} field deleted in display10 failed!!!!!!!!!!!!!!!!!!!'.format('P1_Shape_Len')
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!{} field deleted in display10 failed!!!!!!!!!!!!!!!!!!!!!!'.format('P1_Shape_Len')
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    
try:
    arcpy.AlterField_management(fullDisplayTen, 'LENGTH', 'P1_Shape_Len')
    print('{} field changed to {}.'.format('LENGTH', 'P1_Shape_Len'))
    track.write('{} field changed to {}.'.format('LENGTH', 'P1_Shape_Len') + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!{} field change to {} in display10 failed!!!!!!!!!!!!!!!!'.format('LENGTH', 'P1_Shape_Len')
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!{} field change to {} in display10 failed!!!!!!!!!!!!!!!'.format('LENGTH', 'P1_Shape_Len')
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
#### Cleanup ###########################################################################################    

try:
    arcpy.ClearWorkspaceCache_management(path)
    print('{} cleared workspace'.format(path))
    track.write('\n' + '\n' + '{} cleared workspace'.format(path) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(path) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(path) + '\n' + arcpy.GetMessages()
        + '\n'+ '\n')


track.write('\n' + '\n' + 'DB06_to_DB04_v3 script 7, streetcenterlines completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n')
track.write('\n' + '\n' + 'TokenStrCenterLine' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4 script 7, streetcenterlines completed')
#Written by Michael Shoop 
#Version #8 completed 6/5/20 #DB06_to_DB04_streetcenterlines_Script7_v8







