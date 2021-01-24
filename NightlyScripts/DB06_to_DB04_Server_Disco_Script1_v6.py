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
track = open(logtime,"w+") #We probably need to make a new log
Header = "Start DB06_to_DB04_v4 script 1, Server Disconnect"
print('Start DB06_to_DB04_v4 script 1, Server Disconnect ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################

homefile = r'Database Connections\sde@gisdb06.sde.sde' #this will be path for DB06
DisplayTen = r'Database Connections\displayadmin@GISDB04.Display10.sde'   #this will be path for Display 10
serverlist = [DisplayTen, homefile]

#ReCompPars, ReCompAdd###################################################       DISCONNECT AND RECONCILE           #####################################################################
arcpy.env.workspace = homefile
arcpy.env.overwriteOutput = True


print('Stopping ArcGIS Server and disconneting users')
try:
    os.system('NET STOP "ArcGIS Server"') ###DO WE NEED ONE OF THESE FOR EACH SERVER?
    print('\n' + '\n' + 'ArcGIS Server stopped' + '\n'+ '\n')
    track.write('ArcGIS Server stopped' + '\n')
except:
    print('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!failed ArcGIS Server stop!!!!!!!!!!!!!!!!!!!!!!' + '\n'+ '\n')
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!failed ArcGIS Server stop!!!!!!!!!!!!!!!!!!!!!!' + '\n' + arcpy.GetMessages() + '\n' + '\n')


for x in serverlist:
    y = os.path.basename(x)
    try:
        arcpy.ListUsers(x)
        print('\n' + '\n' + 'list users on {}'.format(y) + '\n'+ '\n')
        track.write('list users on {}'.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
        arcpy.AcceptConnections(x, False)
        print('\n' + '\n' + 'accept connections false on {}'.format(y) + '\n'+ '\n')
        track.write('accept connections false on {}'.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
        arcpy.DisconnectUser(x, 'ALL')
        print('{} users disconnected. '.format(y) + '%s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
        track.write('{} users disconnected. '.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
    except:
        print('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!disconnect for {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(y) + '\n'+ '\n')
        track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!disconnect for {} failed!!!!!!!!!!!!!!!!!!!!!!'.format(y) + '\n' + arcpy.GetMessages() + '\n' + '\n')       
    versionList = arcpy.ListVersions(x)

    try:
        arcpy.ReconcileVersions_management(x, 'ALL_VERSIONS', 'sde.DEFAULT', versionList, 'LOCK_ACQUIRED', 'NO_ABORT', 'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', 'DELETE_VERSION')
        print('{} version management complete. '.format(y) + '%s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
        track.write('{} version management complete. '.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} version management failed!!!!!!!!!!!!!!!!!!!'.format(y) + '%s total seconds' % (round((time.time() - begin_time)/60,2))
              + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} version management failed!!!!!!!!!!!!!!!!!!!!!!'.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2))
              + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    try:
        arcpy.Compress_management(x)
        print('{} compression complete. '.format(y) + '%s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n')
        track.write('{} compression complete. '.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} compression failed!!!!!!!!!!!!!!!!!!!'.format(y) + '%s total seconds' % (round((time.time() - begin_time)/60,2))
              + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} compression failed!!!!!!!!!!!!!!!!!!!'.format(y) + ' %s total seconds' % (round((time.time() - begin_time)/60,2))
              + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

print('\n' + '\n' + '%s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + '%s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')

track.write('\n' + '\n' + 'DB06_to_DB04_v4 script 1, Server Disconnect completed %s total seconds' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
track.write('\n' + '\n' + 'TokenServerDisco' + '\n' + '\n')
track.close()
print('%s total seconds' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4 script 1, Server Disconnect completed')
#Written by Michael Shoop 
#Version #4 completed 06/15/20 #DB06_to_DB04_Server_Disco_Script1_v6
