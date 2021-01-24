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
Header = "Start DB06_to_DB04_v4 script 3, SJ1 & APpars"
print('Start DB06_to_DB04_v4 script 3, SJ1 & APpars' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################
homefile = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.' #this will be path for DB06
parcel = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.ParcelFeatures\sde.'
gisdb06 = r'Database Connections\sde@gisdb06.sde.sde'
path_StructurePts = homefile + 'StructurePts' #this will be path for DB06
path_Parcel = parcel + 'Parcel' #this will be path for DB06
path_SJ1 = homefile + 'SJ1' #this will be path for DB06
Display10_DISPLAYADMIN_zzSJ1_quotes = "{}".format(path_StructurePts)
#variables APpars4##################################################################
path_APpars = homefile + 'APpars' #this will be path for DB06
path_GSP_E_Zone = homefile + 'GSP_E_Zone' #this will be path for DB06
path_zzAPpars = homefile + 'zzAPpars' #this will be path for DB06
db_six, parcelonly = os.path.split(path_Parcel)
APparsIntersect = "'{}' #; '{}' #;".format(path_GSP_E_Zone, path_Parcel)

arcpy.env.workspace = gisdb06
#####UpdateSJ1###########################################################################################

#####APpars4#############################################################################################

print('\n' + '\n' + 'Starting APpars update' + '\n' + '\n')
try:
    if arcpy.Exists(path_APpars):
        try:
            arcpy.Delete_management(path_APpars, "FeatureClass")
            print('APpars deleted from DB06. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('APpars deleted from DB06. ' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!APpars delete from DB06 failed!!!!!!!!!!!!!!!!!!!' + '%s total minutes' % (round((time.time() - begin_time)/60,2))
                + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!APpars delete from DB06 failed!!!!!!!!!!!!!!!!!!!!!!' + ' %s total minutes' % (round((time.time() - begin_time)/60,2))
                + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    else:
        print('APpars not found on DB06.'+ '\n')
        track.write('APpars not found on DB06.'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!APpars exists function failed!!!!!!!!!!!!!!!!!!!' + '%s total minutes' % (round((time.time() - begin_time)/60,2))
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('!!!!!!!!!!!!!!!!!APpars exists function failed!!!!!!!!!!!!!!!!!!!!!!' + ' %s total minutes' % (round((time.time() - begin_time)/60,2))
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')      
try:
    arcpy.Intersect_analysis(APparsIntersect, path_APpars, "NO_FID", "", "INPUT")
    print('Intersect between GSP_E_Zone & parcel to zzAPpars on DB06. ' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.write('Intersect between GSP_E_Zone & parcel to zzAPpars on DB06. ' % (round((time.time() - begin_time)/60,2)) + '\n')
except:
    print('Intersect between GSP_E_Zone & parcel to zzAPpars on DB06 delayed?' + '%s total minutes' % (round((time.time() - begin_time)/60,2))
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.write('Intersect between GSP_E_Zone & parcel to zzAPpars on DB06 delayed?' + ' %s total minutes' % (round((time.time() - begin_time)/60,2))
        + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

print('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')


#### Cleanup ###########################################################################################    
try:
    arcpy.ClearWorkspaceCache_management(gisdb06)
    print('{} cleared workspace'.format(gisdb06))
    track.write('\n' + '\n' + '{} cleared workspace'.format(gisdb06) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(gisdb06) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(gisdb06) + '\n'
        + arcpy.GetMessages() + '\n'+ '\n')

print('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + 'DB06_to_DB04_v5 script 3, SJ1 & APpars completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n')
track.write('\n' + '\n' + 'TokenAPpars' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v3 script 5, SJ1 & APpars completed')
#Written by Michael Shoop 
#Version #4 completed 06/18/19 #DB06_to_DB04_SJ1 & APpars_Script3_v9
