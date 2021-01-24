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
track = open(logtime,"a") #We probably need to make a new log
Header = "DB06_to_DB04_v4, script9 indexing update"
print('Start DB06_to_DB04_v4, script9 indexing update ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################
display10dispayadmin = r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.' #this will be path for Display 10

spatiallist = ['BoundaryLine', 'BoundaryLineAnno', 'MiscTextAnno', 'OtherLines', 'Parcel', 'ParcelAnno', 'StreetCenterLines',
               'Subdivision', 'TaxDistDissolve', 'TaxPars']

runattributeindex = [['CAMA', 'ParcelNumber', 'ParNum', 'NON_UNIQUE', 'NON_ASCENDING'], ['Parcel', 'MAPNUMBER', 'MapDex']]
#### relationship variables #####################################################################################################
parcel = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.ParcelFeatures\sde.'

Pars_ADMINASSO_ParcelAnno = parcel + 'ParcelAnno'
Pars_ADMINASSO_ParLotAnno = parcel + 'ParLotAnno'
Pars_ADMINASSO_ParcelLotAnno = parcel + 'ParcelLotAnno'
Pars_ADMINASSO_ParAnno = parcel + 'ParAnno'
parsadminassoparcel_ADMINPLAN_Parcel = parcel + 'Parcel'

rel_list = [[Pars_ADMINASSO_ParcelAnno, Pars_ADMINASSO_ParAnno], [Pars_ADMINASSO_ParcelLotAnno, Pars_ADMINASSO_ParLotAnno]]
#####Variables##########################################################################################################################################################################################################
arcpy.env.overwriteOutput = True

for fc in spatiallist:                          
    try:
        fcmerge = display10dispayadmin + fc######LIST CONNECTED
        #add a spatialindex to display 10 items
        arcpy.AddSpatialIndex_management(fcmerge) #Do we really need to do this? reference ESRI Spatial index. Appears that SQL probably stores in a binary format.
        #Also using the defualt spatial grid could be an issue but not sure.
        print('In NewD10.sde\Display10.DISPLAYADMIN Spatial index added to {}.'.format(fc))######LIST CONNECTED
        track.write('In NewD10.sde\Display10.DISPLAYADMIN Spatial index added to {}.'.format(fc)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    except:
        print('arcpy.AddSpatialIndex_management failed to add spatial index to {}!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(fc)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + arcpy.GetMessages() + '\n')######LIST CONNECTED
        print(arcpy.GetMessages())
        track.write('!!!!!!!!!!!!!!!arcpy.AddSpatialIndex_management failed to add spatial index to {}!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(fc)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + arcpy.GetMessages() + '\n')######LIST CONNECTED

                              
for runattribute in runattributeindex:
    runattributemerge = display10dispayadmin + runattribute[0]
    runattributezero = runattribute[0]
    runattributeone = runattribute[1]
    runattributetwo = runattribute[2]
    try:
        if runattributezero.startswith('Parcel'):
            #add index to display 10 items
            arcpy.AddIndex_management(runattributemerge, runattributeone, runattributetwo)
            print('In NewD10.sde\Display10.DISPLAYADMIN attribute index added to {}.'.format(runattribute[0])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('In NewD10.sde\Display10.DISPLAYADMIN attribute index added to {}.'.format(runattribute[0])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
        else:
            runattributethree = runattribute[3]
            runattributefour = runattribute[4]
            arcpy.AddIndex_management(runattributemerge, runattributeone, runattributetwo, runattributethree, runattributefour)
            print('In NewD10.sde\Display10.DISPLAYADMIN attribute index added to {}.'.format(runattribute[0])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.write('In NewD10.sde\Display10.DISPLAYADMIN attribute index added to {}.'.format(runattribute[0])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    except:
        print('arcpy.AddIndex_management failed to add index to {}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(runattribute[0])
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + arcpy.GetMessages() + '\n')
        track.write('!!!!!!!!!!!!!!!!!!!arcpy.AddIndex_management failed to add index to {}!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(runattribute)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + arcpy.GetMessages() + '\n')
print('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')

#Build relationships################################################################
                                     
rel_par = parsadminassoparcel_ADMINPLAN_Parcel
for rel in rel_list:                                     
    try:
        arcpy.CreateRelationshipClass_management(rel_par, rel[0], rel[1], "COMPOSITE", "spartasso.ADMINASSO.ParcelAnno",
                                                 "spartasso.ADMINASSO.Parcel", "FORWARD", "ONE_TO_MANY", "NONE", "OBJECTID", "FeatureID")
        print('{} relationship created'.format(rel[0]) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
        track.write('{} relationship created'.format(rel[0]) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
    except:
        print('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!{} relationship create failed!!!!!!!!!!!!!!!!!!!!!!'.format(rel[0])
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
        track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!!{} relationship create failed!!!!!!!!!!!!!!!!!!!!!!'.format(rel[0])
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + arcpy.GetMessages() + '\n' + '\n')

#Build relationships################################################################



track.write('\n' + '\n' + 'DB06_to_DB04_v4 script 9, indexing update completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n')
track.write('\n' + '\n' + 'TokenIndex' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4 script 9, indexing update completed')
#Written by Michael Shoop 
#Version #4 completed 06/18/20 #DB06_to_DB04_indexing_Script9_v6
