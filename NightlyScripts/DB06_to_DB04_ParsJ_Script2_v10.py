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
Header = "Start DB06_to_DB04_v4 script 2, ParsJ"
print('Start DB06_to_DB04_v4 script 2, ParsJ ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
track.close()
#####Variables##########################################################################################################################################################################################################
fullhomefile = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.ParcelFeatures\sde.SDE.Parcel' #this will be path for DB06
fullhomefileParsJ = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.ParsJ' #this will be path for DB06
DBosix = r'Database Connections\sde@gisdb06.sde.sde\sde.'
zzfullhomefileParsJ = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.zzParsJ' #this will be path for DB06
homefile_cama = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.CAMA' #this will be path for DB06
dbo_cama = r'Database Connections\sde@gisdb06.sde.sde\sde.dbo.CAMA'
six = r'Database Connections\sde@gisdb06.sde.sde'
oldfullhomefileParsJ = fullhomefileParsJ + '_old'
path, basename = os.path.split(fullhomefile)
data = os.path.basename(fullhomefileParsJ)
zzdata = os.path.basename(fullhomefileParsJ)
parsj_list = [oldfullhomefileParsJ, zzfullhomefileParsJ, homefile_cama]
#### relationship variables #####################################################################################################
parcel = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.ParcelFeatures\sde.'
display10dispayadmin = r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.'
relationship_delete_list = ['ParcelAnno', 'ParLotAnno', 'ParAnno']
#####Delete Relationship###########################################################################################
arcpy.env.workspace = six
arcpy.env.overwriteOutput = True

for reldelete in relationship_delete_list:
    relationship_full = parcel + reldelete
    relationship_dten = display10dispayadmin + reldelete
    relationship_pathlist = [relationship_full, relationship_dten]
    for rel in relationship_pathlist:
        try:
            arcpy.Delete_management(rel, "RelationshipClass")
            print('{} relationship deleted.'.format(reldelete) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track = open(logtime,"a")
            track.write('{} relationship deleted.'.format(reldelete) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')            
            track.close()
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!{} relationship deleted not executed!!!!!!!!!!!!!!!!!!!'.format(reldelete)
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track = open(logtime,"a")
            track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} relationship deleted not executed!!!!!!!!!!!!!!!!!!!'.format(reldelete)
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.close()
track = open(logtime,"a")            
track.write('\n' + '\n' + 'TokenDeleterelationships' + '\n' + '\n')
track.close()
#####Deletes and old###########################################################################################
for pars in parsj_list:
    try:
        if arcpy.Exists(pars):
            try:
                arcpy.Delete_management(pars)####Delete all the matching old DB06 
                print('{} deleted from DB06. '.format(data) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track = open(logtime,"a")
                track.write('{} deleted from DB06. '.format(data) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track.close()
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{}_old deleted from DB06 failed!!!!!!!!!!!!!!!!!!!'.format(data)
                    + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track = open(logtime,"a")
                track.write('!!!!!!!!!!!!!!!!!{}_old deleted from DB06 failed!!!!!!!!!!!!!!!!!!!!!!'.format(data)
                    + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.close()
            if pars == oldfullhomefileParsJ:
                try:
                    arcpy.Rename_management(fullhomefileParsJ, oldfullhomefileParsJ) ####Make existing DB06 stuff old DB06 stuff
                    print('{} renamed from DB06 to {}_old. '.format(data, data) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                    track = open(logtime,"a")
                    track.write('{} renamed from DB06 to {}_old. '.format(data, data) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                    track.close()
                except:
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!{} Rename failed!!!!!!!!!!!!!!!!!!!'.format(data)
                        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                    track = open(logtime,"a")
                    track.write('!!!!!!!!!!!!!!!!!{} Rename failed!!!!!!!!!!!!!!!!!!!!!!'.format(data)
                        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                    track.close()
        else:
            print('{} not found.'.format(data) + '\n')
            track = open(logtime,"a")
            track.write('{} not found.'.format(data) + '\n')
            track.close()
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} exists function failed!!!!!!!!!!!!!!!!!!!'.format(data)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track = open(logtime,"a")
        track.write('!!!!!!!!!!!!!!!!!{} exists function failed!!!!!!!!!!!!!!!!!!!!!!'.format(data)
            + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.close()

#####CAMA COPY###########################################################################################

try:
    arcpy.TableToTable_conversion(dbo_cama, six, 'CAMA')
    print('CAMA copied over.')
    track = open(logtime,"a")
    track.write('\n' + 'CAMA copied over.' + '\n')
    track.write('\n' + '\n' + 'TokenCamaCopy' + '\n' + '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!CAMA copied over failed!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track = open(logtime,"a")
    track.write('!!!!!!!!!!!!!!!!!!!!!!!!!CAMA copied over failed!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.close()
    
#### PARSJ #####################################################################################################

try:
    arcpy.CopyFeatures_management(fullhomefile, zzfullhomefileParsJ)
    print('{} DB06 copied to DB06 as {}.'.format(basename, data))
    track = open(logtime,"a")
    track.write('{} DB06 copied to DB06 as {}.'.format(basename, data) + '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!{} DB06 copied to DB06 as {} failed!!!!!!!!!!!!!!!'.format(basename, zzdata)
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track = open(logtime,"a")
    track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} DB06 copied to DB06 as {} failed!!!!!!!!!!!!!!!'.format(basename, zzdata)
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.close()
try:
    arcpy.JoinField_management(zzfullhomefileParsJ, "MAPNUMBER", homefile_cama, "ParcelNumber")
    #arcpy.AddJoin_management('Parcel_Layer', "MAPNUMBER", homefile_cama, "ParcelNumber", "KEEP_ALL")
    print('Parcels layer field MAPNUMBER joined to CAMA field ParcelNumber.' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track = open(logtime,"a")
    track.write('Parcels layer field MAPNUMBER joined to CAMA field ParcelNumber.' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!Parcel layer field MAPNUMBER join to CAMA field ParcelNumber failed!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track = open(logtime,"a")
    track.write('!!!!!!!!!!!!!!!!!Parcel layer field MAPNUMBER join to CAMA field ParcelNumber failed!!!!!!!!!!!!!!!!'
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.close()
try:
    arcpy.CopyFeatures_management(zzfullhomefileParsJ, fullhomefileParsJ)
    print('{} layer copied to DB06 as {}.'.format(basename, data))
    track = open(logtime,"a")
    track.write('{} layer copied to DB06 as {}.'.format(basename, data) + '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!{} layer copied to DB06 as {} failed!!!!!!!!!!!!!!!'.format(basename, data)
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track = open(logtime,"a")
    track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} layer copied to DB06 as {} failed!!!!!!!!!!!!!!!'.format(basename, data)
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.close()
    
#### Cleanup ###########################################################################################
####name cleanup #######################################################################################

try:
    arcpy.ClearWorkspaceCache_management(path)
    print('{} cleared workspace'.format(path))
    track = open(logtime,"a")
    track.write('\n' + '\n' + '{} cleared workspace'.format(path) + '\n'+ '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(path) + '\n' + arcpy.GetMessages())
    track = open(logtime,"a")
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(path) + '\n' + arcpy.GetMessages() + '\n'+ '\n')
    track.close()  
print('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track = open(logtime,"a")
track.write('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + 'DB06_to_DB04_v3 script 2, ParsJ completed %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
track.write('\n' + '\n' + 'TokenParsJ' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v3 script 2, ParsJ completed')

#Written by Michael Shoop 
#Version #4 completed 06/22/20 #DB06_to_DB04_ParsJ_Script2_v10
    
