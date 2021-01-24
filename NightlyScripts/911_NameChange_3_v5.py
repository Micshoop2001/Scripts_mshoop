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
Header = "Start 911_NameChange_3_v3 "
print('Start 911_NameChange_3_v3 ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables####################################################################################################################################################################
rootpathfire = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.FireEMSCityESN\sde.SDE.'
rootpath = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.'
fire, sde = os.path.split(rootpathfire)
jury, beat = os.path.split(rootpath)
change_list = {'City':{'MSAGComm':'NAME', 'CITY':'FULLNAME', 'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'CONTRACTOR':{'Contractor':'NAME', 'CONTRACT':'CONTRACTOR_TYPE', 'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'EMS':{'EMS':'NAME', 'EMS_Fullname':'FULLNAME', 'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'FireBeats':{'FIRE':'NAME', 'FireDept':'FULLNAME', 'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'HEAVY_DUTY':{'MSAGComm':'NAME', 'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'LawBeats':{'LAW':'NAME', 'Jurisdiction':'FULLNAME', 'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'PSAP':{'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'ESN':{'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'Jurisdiction':{'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'FireDistricts_911':{'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'Municipalities_911':{'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'ZIPCodes':{'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'},
               'Community':{'MAX_created_date':'created_date', 'MAX_last_edited_date':'last_edited_date'}}

#####privilege variables#####################################################################################################################################################
privilege_list = [['AdminEditor', 'GRANT', 'GRANT'], ['GISViewer', 'GRANT', '#']]

arcpy.env.overwriteOutput = True
##### NameChange privilege ################################################################################################################################################

for weather, dictindex in change_list.items():
    if weather in ('Community', 'ZIPCodes'):
        full_911_path = rootpath +  weather
        for privilege in privilege_list:
            try:
                arcpy.ChangePrivileges_management(full_911_path, privilege[0], privilege[1], privilege[2])
                print('{} has {} privileges given'.format(weather, privilege[0]) + '%s total seconds' % (time.time() - begin_time) + '\n')
                track.write('{} has {} privileges given'.format(weather, privilege[0]) + ' %s total seconds' % (time.time() - begin_time) + '\n')
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{} has {} privileges given failed!!!!!!!!!!!!!!!!!!!'.format(weather, privilege[0])
                    + '%s total seconds' % (time.time() - begin_time) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} has {} privileges given failed!!!!!!!!!!!!!!!!!!!'.format(weather, privilege[0])
                    + ' %s total seconds' % (time.time() - begin_time) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
          
    else:
        full_911_path = rootpathfire +  weather
        
    arcpy.env.workspace = full_911_path
    for ind in dictindex:
        try:
            arcpy.AlterField_management(full_911_path, ind, dictindex[ind])
            print('{} field changed to {} in {}.'.format(ind, dictindex[ind], weather))
            track.write('{} field changed to {} in {}.'.format(ind, dictindex[ind], weather) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!{} field change to {} in {} failed!!!!!!!!!!!!!!!!'.format(ind, dictindex[ind], weather)
                + '%s total seconds' % (time.time() - begin_time) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!{} field change to {} in {} failed!!!!!!!!!!!!!!!'.format(ind, dictindex[ind], weather)
                + ' %s total seconds' % (time.time() - begin_time) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

####Versioning###########################################################################################
            
try:
    arcpy.RegisterAsVersioned_management(fire, "NO_EDITS_TO_BASE")
    print('\n' + '\n' + '{} registered for versioning.'.format(fire) + '\n' + '\n')
    track.write('\n' + '\n' + '{} registered for versioning.'.format(fire) + '\n' + '\n')
except:
    print('!!!!!!!!!!!!!!!!!!{} registered for versioning failed!!!!!!!!!!!!!!!!'.format(fire) + '%s total seconds' % (time.time() - begin_time)
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!{} registered for versioning failed!!!!!!!!!!!!!!!'.format(fire) + ' %s total seconds' % (time.time() - begin_time)
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')


####Cleanup###########################################################################################
    
try:
    arcpy.ClearWorkspaceCache_management(jury)
    print('{} cleared workspace'.format(jury))
    track.write('\n' + '\n' + '{} cleared workspace'.format(jury) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(jury) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(jury)
        + '\n' + arcpy.GetMessages() + '\n'+ '\n')


track.write('\n' + '\n' + '911_NameChange_3_v5 , completed %s total seconds' % (time.time() - begin_time) + '\n' + '\n')
track.write('\n' + '\n' + 'Token911privileges' + '\n' + '\n')
track.write('\n' + '\n' + 'Token911versioning' + '\n' + '\n')
track.close()
print('%s total seconds' % (time.time() - begin_time))
print('911_NameChange_3_v5 , completed')
#Written by Michael Shoop 
#Version #4 completed 11/12/19 #DB06_to_DB04_streetcenterlines_Script7_v6























