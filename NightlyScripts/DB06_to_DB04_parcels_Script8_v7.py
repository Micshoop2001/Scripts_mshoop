import arcpy
import os
import time
from datetime import timedelta
from datetime import datetime
###############################################################time & log setup###########################################################################################
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
Header = "DB06_to_DB04_v4, script8 parcel update"
print('Start DB06_to_DB04_v4, script8 parcel update ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################
fullDisplayTen = r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.Parcel' #this will be path for Display 10
homefile = r'Database Connections\displayadmin@GISDB04.Display10.sde'
addfield_list = [['LOTNUMBER', 'TEXT', '8', 'LOTNUMBER'], ['EDITOR', 'TEXT', '50', 'EDITOR'], ['SECID', 'LONG', '10', 'SECID'],
                 ['Problem', 'TEXT', '128', 'Problem'], ['GISid', 'TEXT', '30', 'GISid']]
#####Actions##########################################################################################################################################################################################################
arcpy.env.workspace = homefile
arcpy.env.overwriteOutput = True

individual_field = arcpy.ListFields(fullDisplayTen)

##AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})

for directions in addfield_list:
    if directions[1] in('GlobalID', 'LONG'):  #may have to change globalid to a text field
        try:
            arcpy.AddField_management(fullDisplayTen, directions[0], directions[1], directions[2], '0', '', directions[3], 'NULLABLE', 'NON_REQUIRED')###We need to build on this
            print('{} field added to Parcel. '.format(directions[0]) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('{} field added to Parcel. '.format(directions[0]) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!{} field added to Parcel failed!!!!!!!!!!!!!!!!!!!!!!!! '.format(directions[0])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!{} field added to Parcel failed!!!!!!!!!!!!!!!'.format(directions[0])
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    else: 
        try:
            arcpy.AddField_management(fullDisplayTen, directions[0], directions[1], '0', '0', directions[2], directions[3], 'NULLABLE', 'NON_REQUIRED')###We need to build on this
            print('{} field added to Parcel. '.format(directions[0]) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('{} field added to Parcel. '.format(directions[0]) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!{} field added to Parcel failed!!!!!!!!!!!!!!!!!!!!!!!! '.format(directions[0])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!{} field added to Parcel failed!!!!!!!!!!!!!!!'.format(directions[0])
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

#### Cleanup ###########################################################################################    

try:
    arcpy.ClearWorkspaceCache_management(homefile)
    print('{} cleared workspace'.format(homefile))
    track.write('\n' + '\n' + '{} cleared workspace'.format(homefile) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(homefile) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(homefile)
        + '\n' + arcpy.GetMessages() + '\n'+ '\n')


track.write('\n' + '\n' + 'DB06_to_DB04_v4 script 8, script8 parcel update completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n')
track.write('\n' + '\n' + 'TokenParcelFields' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4 script 8, parcel update completed')
#Written by Michael Shoop 
#Version #7 completed 6/18/20 #DB06_to_DB04_parcels_Script8_v7



                 
