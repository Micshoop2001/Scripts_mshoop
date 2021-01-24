import arcpy
import os
import time
from datetime import timedelta
from datetime import datetime
###############################################################time & log setup#########################################
#Time
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
track = open(logtime,"a")
Header = "Start DB06StrptsFields_StrCenterLFields_v1 "
print('Start DB06StrptsFields_StrCenterLFields_v1 ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##############################################################################################################
structurepts_db06 = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.StructurePts'
streetcenterline_db06 = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.StreetCenterlines'
infraList = [[structurepts_db06, 'infra_layer'], [streetcenterline_db06, 'infra_layeragain']]

LSt_NameCalcNull = 'St_PosMod IS NULL' ##SQL Statement
LSt_Nameexpr = str('!St_Name!' + "' '" + '!St_PosType!')
LSt_NameCalc = 'St_PosMod IS NOT NULL' ##SQL Statement
av = '!ATT_PosTyp!.replace("AVE", "AV")'
ldg = '!ATT_PosTyp!.replace("LNDG", "LDG")'
trc = '!ATT_PosTyp!.replace("TRCE", "TRC")'
tr = '!ATT_PosTyp!.replace("TRL", "TR")'
crsg = '!ATT_PosTyp!.replace("XING", "CRSG")'

infraFieldList = [['LSt_PreDir', '!St_PreDir!', ''], ['LSt_PosDir', '!St_PosDir!', ''],
                  ['LSt_Name', '!St_Name!', LSt_NameCalcNull], ['LSt_Name', LSt_Nameexpr, LSt_NameCalc],
                  ['LSt_PosTyp', '!St_PosType!', LSt_NameCalcNull], ['LSt_PosTyp', '!St_PosMod!', LSt_NameCalc]]
ATTlist = ['!LSt_PosTyp!', av, ldg, trc, tr, crsg]
#### Field changes #####################################################################################################

for infra, layer in infraList:
    path, data = os.path.split(infra)
    
    try:
        arcpy.MakeFeatureLayer_management(infra, layer)
        print('FeatureLayer for {} created'.format(data) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        track.write('FeatureLayer for {} created'.format(data) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!FeatureLayer for {} created failed!!!!!!!!!!!!!!!!!!!'.format(data)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!FeatureLayer for {} created failed!!!!!!!!!!!!!!!!!!!!!!'.format(data)
            + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    for infrafield in infraFieldList:  
        try:
            arcpy.SelectLayerByAttribute_management(layer, 'NEW_SELECTION', infrafield[2])
            print('SelectLayerByAttribute were {} is NULL'.format(infrafield[2]) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('SelectLayerByAttribute were {} is NULL'.format(infrafield[2]) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!SelectLayerByAttribute were {} is NULL failed!!!!!!!!!!!!!!!!!!!!!!!! '.format(infrafield[2])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!SelectLayerByAttribute were {} is NULL failed!!!!!!!!!!!!!!!'.format(infrafield[2])
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')    
        try:
            arcpy.CalculateField_management(layer, infrafield[0], infrafield[1], 'PYTHON_9.3')
            print('{} is calculated in {}'.format(infrafield[0], data) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('{} is calculated in {}'.format(infrafield[0], data) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!{} is calculated in {} failed!!!!!!!!!!!!!!!!!!!!!!!! '.format(infrafield[0], data)
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!{} is calculated in {} failed!!!!!!!!!!!!!!!'.format(infrafield[0], data)
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    if infra == streetcenterline_db06:
        for ATT in ATTlist:
            try:
                arcpy.CalculateField_management(layer, 'ATT_PosTyp', ATT, 'PYTHON_9.3')
                print('{} is calculated in {}'.format('ATT_PosTyp', data) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track.write('{} is calculated in {}'.format('ATT_PosTyp', data) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            except:
                print('!!!!!!!!!!!!!!!!!!{} is calculated in {} failed!!!!!!!!!!!!!!!!!!!!!!!! '.format('ATT_PosTyp', data)
                    + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.write('!!!!!!!!!!!!!{} is calculated in {} failed!!!!!!!!!!!!!!!'.format('ATT_PosTyp', data)
                    + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    del layer



#### Cleanup ###########################################################################################    

try:
    arcpy.ClearWorkspaceCache_management(path)
    print('{} cleared workspace'.format(path))
    track.write('\n' + '\n' + '{} cleared workspace'.format(path) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(path) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(path) + '\n' + arcpy.GetMessages()
        + '\n'+ '\n')


track.write('\n' + '\n' + 'DB06StrptsFields_StrCenterLFields_v1 completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n')
track.write('\n' + '\n' + 'TokenStrpts_strCenterlineFields' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06StrptsFields_StrCenterLFields_v1 completed')
#Written by Michael Shoop 
#Version #8 completed 7/1/20 #DB06StrptsFields_StrCenterLFields_v1
