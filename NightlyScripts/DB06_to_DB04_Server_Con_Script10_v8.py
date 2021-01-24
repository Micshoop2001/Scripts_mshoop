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
Header = "DB06_to_DB04_v4, script10 connecting servers"
print('Start DB06_to_DB04_v4, script10 connecting servers ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################
homefile = r'Database Connections\sde@gisdb06.sde.sde' #this will be path for DB06
DisplayTen = r'Database Connections\displayadmin@GISDB04.Display10.sde'   #this will be path for Display 10
serverlist = [DisplayTen, homefile]
#####Cleanup##########################################################################################################################################################################################################
arcpy.env.workspace = homefile
arcpy.env.overwriteOutput = True

print('Conneting users')

for x in serverlist:
    y = os.path.basename(x)
    try:
        arcpy.AcceptConnections(x, True)
        print('\n' + '\n' + 'Connected users on {}'.format(y) + '\n')
        track.write('Conneted users on {}'.format(y) + '\n')
    except:
        print('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!failed to connect users to {}!!!!!!!!!!!!!!!!!!!!!!'.format(y)
            + '\n'+ '\n')
        track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!failed to connect users to {}!!!!!!!!!!!!!!!!!!!!!!'.format(y)
            + '\n' + arcpy.GetMessages() + '\n' + '\n')
    try:
        arcpy.ClearWorkspaceCache_management(x)
        print('{} cleared workspace'.format(y))
        track.write('\n' + '\n' + '{} cleared workspace'.format(y) + '\n'+ '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(y) + '\n' + arcpy.GetMessages())
        track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(y)
            + '\n' + arcpy.GetMessages() + '\n'+ '\n')
    try:
        arcpy.Compress_management(x)
        print('{} compression complete. '.format(y) + '%s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
        track.write('{} compression complete. '.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} compression failed!!!!!!!!!!!!!!!!!!!'.format(y) + '%s total seconds' % (round((time.time() - begin_time)/60,2))
              + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} compression failed!!!!!!!!!!!!!!!!!!!'.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2))
              + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
 
try:
    os.system('NET START "ArcGIS Server"')
    print('Starting Server' + '\n')
    track.write('Starting Server' + '\n')
except:
    print('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!Starting Server failed!!!!!!!!!!!!!!!!!!!!!!' + '\n'+ '\n')
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!Starting Server failed!!!!!!!!!!!!!!!!!!!!!!' + '\n'
        + arcpy.GetMessages() + '\n' + '\n')
#Log Cleanup & Closing#################################################
print('Begin log cleanup')
try:
    for monsters in os.listdir(script_working):
        if monsters.endswith(timetravel):
            print('delete file?' + monsters)
            os.remove(monsters)
            print('\n' + '\n' + monsters +' successfully deleted' + '\n'+ '\n')
            track.write('\n' + '\n' + monsters +' successfully deleted' + '\n'+ '\n')
except:
    print('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!log deletion failed!!!!!!!!!!!!!!!!!!!!!!' + '\n'+ '\n')
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!log deletion failed!!!!!!!!!!!!!!!!!!!!!!'
        + '\n' + arcpy.GetMessages() + '\n' + '\n')


track.write('\n' + '\n' + 'DB06_to_DB04_v4 script 10, script10 connecting servers completed %s total seconds' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n' + fulltime)
track.write('\n' + '\n' + 'TokenServerConnect' + '\n' + '\n')
track.close()
print('%s total seconds' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4 script 10, script10 connecting servers completed')
#Written by Michael Shoop 
#Version #4 completed 06/16/20 #DB06_to_DB04_connecting servers_Script10_v7
