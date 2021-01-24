import arcpy
import os
import time
import datetime
###############################################################time & log setup###########################################################################################
#Time
timestream = time.strftime("%m%d%y")
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
Header = "911_Fieldedit_2_v4 "
print('Start 911_Fieldedit_2_v4 ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables####################################################################################################################################################################
rootpathfire = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.FireEMSCityESN\sde.SDE.'
rootpath = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.'
filldate = time.strftime('11/6/2017')                                     
arcpy.env.overwriteOutput = True
expressiondate = "calc(str('!MAX_created_date!'))"
created_date = '''def calc(MAX_created_date):
                    filldate = time.strftime('11/6/2017')
                    return filldate'''
                    

fieldaddlist = [["Community", "created_user"], ["Community", "last_edited_user"], 
               ["ZIPCodes", "created_user"], ["ZIPCodes", "last_edited_user"], ["Municipalities_911", "created_user"],
               ["Municipalities_911", "last_edited_user"], ["FireDistricts_911", "created_user"],
               ["FireDistricts_911", "last_edited_user"], ["Jurisdiction", "created_user"],
               ["Jurisdiction", "last_edited_user"], ["ESN", "created_user"], ["ESN", "last_edited_user"],
               ["FireBeats", "created_user"], ["FireBeats", "last_edited_user"], 
               ["LawBeats", "created_user"], ["LawBeats", "last_edited_user"], ["PSAP", "created_user"],
               ["PSAP", "last_edited_user"], ["City", "created_user"], ["City", "last_edited_user"],
               ["CONTRACTOR", "created_user"], ["CONTRACTOR", "last_edited_user"], ["EMS", "created_user"],
               ["EMS", "last_edited_user"], ["HEAVY_DUTY", "created_user"], ["HEAVY_DUTY", "last_edited_user"]]

for append, items in fieldaddlist:
    expressionuser = '"911GIS"'
    print(items + '  This is the field')
    append_layer = 'layer_' + append
    if append in ('Community', 'ZIPCodes'): 
        fullhomefile = rootpath + append
    else:
        fullhomefile = rootpathfire + append
    arcpy.env.workspace = fullhomefile
    arcpy.env.overwriteOutput = True
    try:
        arcpy.MakeFeatureLayer_management(fullhomefile, append_layer)
        print('FeatureLayer {} for composite_911 created'.format(append) + '%s total seconds' % (time.time() - begin_time) + '\n')
        track.write('FeatureLayer {} for composite_911 created'.format(append) + ' %s total seconds' % (time.time() - begin_time) + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!FeatureLayer for composite_911 created!!!!!!!!!!!!!!!!!!!' + '%s total seconds' % (time.time() - begin_time)
            + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!FeatureLayer for composite_911 created!!!!!!!!!!!!!!!!!!!!!!' + ' %s total seconds' % (time.time() - begin_time)
            + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

    try:
        arcpy.AddField_management(append_layer, items, 'TEXT', '', '', 255) 
        print('for {} the field {} was added'.format(append, items) + '\n')
        track.write('\n' + 'for {} the field {} was added'.format(append, items) + '\n')
    except:
        print('\n' + '\n' + 'for {} the field {} was added failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, items) + '\n' + '\n')
        print('\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('\n' + '\n' + 'for {} the field {} was added failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, items)
            + '\n' + arcpy.GetMessages() + '\n' + '\n')
    try:
        arcpy.CalculateField_management(append_layer, items, expressionuser, "PYTHON_9.3")
        print('Calculating{} field {} completed'.format(append, items) + '\n')
        track.write('\n' + 'Calculating{} field {} completed'.format(append, items) + '\n')
    except:
        print('\n' + '\n' + 'Calculating{} field {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, items) + '\n' + '\n')
        print('\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('\n' + '\n' + 'Calculating{} field {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, items)
            + '\n' + arcpy.GetMessages() + '\n' + '\n')
    try:
        arcpy.CalculateField_management(append_layer, "MAX_created_date", expressiondate, "PYTHON_9.3", created_date )
        print('Calculating{} field {} completed'.format(append, "MAX_created_date") + '\n')
        track.write('\n' + 'Calculating{} field {} completed'.format(append, "MAX_created_date") + '\n')
    except:
        print('\n' + '\n' + 'Calculating{} field {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, "MAX_created_date") + '\n' + '\n')
        print('\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('\n' + '\n' + 'Calculating{} field {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, "MAX_created_date")
            + '\n' + arcpy.GetMessages() + '\n' + '\n')
    arcpy.Delete_management(append_layer)

track.write('\n' + '\n' + 'Script completed %s total seconds' % (time.time() - begin_time) + '\n' + '\n')
track.write('\n' + '\n' + 'Token911fieldadd' + '\n' + '\n')
track.close()
print('%s total seconds' % (time.time() - begin_time))
print('Script completed')
#Written by Michael Shoop 
#Version #1 completed 12/20/19 #Start Composite_911_v1 
