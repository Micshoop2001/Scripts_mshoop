import arcpy
import os
import time
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
Header = "Start Composite_911_v1 "
print('Start Composite_911_v1 ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables####################################################################################################################################################################
Composite_911_db06 = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.Composite_911'
rootpath = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.'
rootpathfire = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.FireEMSCityESN\sde.SDE.'
composite911_CITY = 'InsideAB'
composite911_OOC = 'N'
composite911_delete = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.Composite_911_temp'
composite911_delete_full = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.Composite_911_temp_full'
appendlist = [["Community", "MSAGComm", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["ZIPCodes", "ZipCode;State;MSAGComm;County", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["Municipalities_911", "CITY", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["FireDistricts_911", "FireDept", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["Jurisdiction", "Jurisdiction", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["ESN", "FireDept;Jurisdiction;EMS_Fullname;ESN", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["FireBeats", "FireDept;FIRE", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["LawBeats", "LAW;Jurisdiction", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["PSAP", "PSAP", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["City", "MSAGComm;CITY", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["CONTRACTOR", "Contractor;CONTRACT", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["EMS", "EMS;EMS_Fullname", [["created_date", "MAX"], ["last_edited_date", "MAX"]]],
              ["HEAVY_DUTY", "MSAGComm", [["created_date", "MAX"], ["last_edited_date", "MAX"]]]]

compositelist = [[composite911_delete, 'Composite911_Layer', 'Composite_911_temp'], [composite911_delete_full, 'Composite911_Layer_full', 'Composite_911_temp_full']]                  
arcpy.env.workspace = rootpath 
arcpy.env.overwriteOutput = True
composite911_SQL = """{} = '{}' OR {} IS NULL""".format(arcpy.AddFieldDelimiters(Composite_911_db06, composite911_CITY), composite911_OOC,
                                                        arcpy.AddFieldDelimiters(Composite_911_db06, composite911_CITY))

for composite in compositelist:
    try:
        arcpy.CopyFeatures_management(Composite_911_db06, composite[0])
        print('{} for composite_911 created'.format(composite[2]) + '%s total seconds' % (time.time() - begin_time) + '\n')
        track.write('{} for composite_911 created'.format(composite[2]) + ' %s total seconds' % (time.time() - begin_time) + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} for composite_911 created!!!!!!!!!!!!!!!!!!!'.format(composite[2]) + '%s total seconds' % (time.time() - begin_time) + '\n' + '\n'
            + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} for composite_911 created!!!!!!!!!!!!!!!!!!!!!!'.format(composite[2]) + ' %s total seconds' % (time.time() - begin_time) + '\n' + '\n'
            + arcpy.GetMessages() + '\n' + '\n')

    try:
        arcpy.MakeFeatureLayer_management(composite[0], composite[1])
        print('{} FeatureLayer for composite_911 created'.format(composite[2]) + '%s total seconds' % (time.time() - begin_time) + '\n')
        track.write('{} FeatureLayer for composite_911 created'.format(composite[2]) + ' %s total seconds' % (time.time() - begin_time) + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} FeatureLayer for composite_911 created!!!!!!!!!!!!!!!!!!!'.format(composite[2]) + '%s total seconds' % (time.time() - begin_time)
            + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} FeatureLayer for composite_911 created!!!!!!!!!!!!!!!!!!!!!!'.format(composite[2]) + ' %s total seconds' % (time.time() - begin_time)
            + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
skirtRemoval = '''try:
    arcpy.SelectLayerByAttribute_management('Composite911_Layer', "NEW_SELECTION", composite911_SQL)
    print('Selecting composite data outside of county' + '%s total seconds' % (time.time() - begin_time) + '\n')
    track.write('Selecting composite data outside of county' + ' %s total seconds' % (time.time() - begin_time) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!Selecting composite data outside of county failed!!!!!!!!!!!!!!!!!!!' + '%s total seconds' % (time.time() - begin_time)
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!Selecting composite data outside of county failed!!!!!!!!!!!!!!!!!!!!!!' + ' %s total seconds' % (time.time() - begin_time)
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

try:
    arcpy.DeleteFeatures_management('Composite911_Layer')
    print('Deleting composite data outside of county' + '%s total seconds' % (time.time() - begin_time) + '\n')
    track.write('Deleting composite data outside of county' + ' %s total seconds' % (time.time() - begin_time) + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!Deleting composite data outside of county failed!!!!!!!!!!!!!!!!!!!' + '%s total seconds' % (time.time() - begin_time)
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!Deleting composite data outside of county failed!!!!!!!!!!!!!!!!!!!!!!' + ' %s total seconds' % (time.time() - begin_time)
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')'''

    
for append, items, stats in appendlist:
    if append in ('Community', 'ZIPCodes'): 
        fullhomefile = rootpath + append
        featurelayer = 'Composite911_Layer_full'
    else:
        fullhomefile = rootpathfire + append
        featurelayer = 'Composite911_Layer'
    try:
        if arcpy.Exists(fullhomefile):
            try:
                arcpy.Delete_management(fullhomefile)
                print('{} deleted from DB06.'.format(append) + '%s total seconds' % (time.time() - begin_time) + '\n')
                track.write('{} deleted from DB06.'.format(append) + ' %s total seconds' % (time.time() - begin_time) + '\n')
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{} deleted from DB06 failed!!!!!!!!!!!!!!!!!!!'.format(append) + '%s total seconds' % (time.time() - begin_time)
                    + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.write('!!!!!!!!!!!!!!!!{} deleted from DB06 failed!!!!!!!!!!!!!!!!!'.format(append) + ' %s total seconds' % (time.time() - begin_time)
                    + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n') 
    except:
        print('!!!!!!!!!!!!!!!!!!!{} Exist on DB06 failed!!!!!!!!!!!!!!!!!!!'.format(append) + '%s total seconds' % (time.time() - begin_time)
            + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!!!{} Exist on DB06 failed!!!!!!!!!!!!!!!!!!!'.format(append) + ' %s total seconds' % (time.time() - begin_time)
            + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    try:
        arcpy.Dissolve_management(featurelayer, fullhomefile, items, stats, "MULTI_PART", "DISSOLVE_LINES")
        print('Dissolve of {} by fields {} completed'.format(append, items) + '\n')
        track.write('\n' + 'Dissolve of {} by fields {} completed'.format(append, items) + '\n')
    except:
        print('\n' + '\n' + 'Dissolve of {} by fields {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, items) + '\n' + '\n')
        print('\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('\n' + '\n' + 'Dissolve of {} by fields {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(append, items) + '\n' + arcpy.GetMessages() + '\n' + '\n')

arcpy.Delete_management('Composite911_Layer')
arcpy.Delete_management('Composite911_Layer_full')
arcpy.Delete_management(composite911_delete)
arcpy.Delete_management(composite911_delete_full)
track.write('\n' + '\n' + 'Script completed %s total seconds' % (time.time() - begin_time) + '\n' + '\n')
track.write('\n' + '\n' + 'Token911Dissolve' + '\n' + '\n')
track.close()
print('%s total seconds' % (time.time() - begin_time))
print('Script completed')
#Written by Michael Shoop 
#Version #1 completed 06/16/20 #Start Composite_911_v9 
