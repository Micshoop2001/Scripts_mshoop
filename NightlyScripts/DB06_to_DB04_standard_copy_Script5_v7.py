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
Header = "DB06_to_DB04_v4, script5 standard copy"
print('Start DB06_to_DB04_v4, script5 standard copy ' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables##########################################################################################################################################################################################################
homefile = r'Database Connections\sde@gisdb06.sde.sde\sde.' #this will be path for DB06
DB06 = r'Database Connections\sde@gisdb06.sde.sde'
DisplayTen =  r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.'  #this will be path for Display 10
featureclass = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.Soils'
table = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.CAMA'
firedistrict = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.FireEMSCityESN\sde.'
parcel = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.ParcelFeatures\sde.'
homeDisplayTen = r'Database Connections\displayadmin@GISDB04.Display10.sde'
FCDescribe = arcpy.Describe(featureclass)
tableDescribe = arcpy.Describe(table)
transfer_list = ['BoundaryLine', 'BoundaryLineAnno', 'Easement', 'LeadLine', 'MiscTextAnno', 'OtherAcreageAnno',
                 'OtherLines', 'ParcelAnno', 'ParcelLotAnno', 'Subdivision', 'TieLine', 'Municipalities', 'CAMA', 'WaterDistricts',
                 'TaxPars', 'TaxDistDissolve', 'APpars', 'ParsJ', 'GSPEnvironsZone', 'GSP_E_Zone', 'Parcel', 'FireDistricts', 'Zoning']

print('starting copies')
#####Actions##########################################################################################################################################################################################################
arcpy.env.workspace = DB06
arcpy.env.overwriteOutput = True


DB6_features = arcpy.ListFeatureClasses()
DB6_tables = arcpy.ListTables()

for items in transfer_list:
    print('Reviewing and copying {} over'.format(items)) 
    fullDisplayTen = DisplayTen + items  
    oldDisplayTen = DisplayTen + items + '_old'
    if items in ('Parcel', 'ParcelAnno', 'ParcelLotAnno', 'Subdivision', 'Easement', 'LeadLine', 'TieLine',
                 'MiscTextAnno', 'OtherAcreageAnno', 'BoundaryLine', 'BoundaryLineAnno', 'OtherLines'):
       fullhomefile = parcel + items
    elif items in ('FireDistricts', 'Municipalities'):
       fullhomefile = firedistrict + items
    else:
       fullhomefile = homefile + items
    try:
        if arcpy.Exists(fullDisplayTen):
            try:
                arcpy.Delete_management(oldDisplayTen)####Delete all the matching old display 10 in DB04
                print('{}_old deleted from display10. '.format(items) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track.write('{}_old deleted from display10. '.format(items) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{}_old deleted from display10 failed!!!!!!!!!!!!!!!!!!!'.format(items)
                    + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.write('!!!!!!!!!!!!!!!!!{}_old deleted from display10 failed!!!!!!!!!!!!!!!!!!!!!!'.format(items)
                    + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            try:
                arcpy.Rename_management(fullDisplayTen, oldDisplayTen) ####Make existing display 10 stuff old display 10 stuff
                print('{} renamed from display10 to {}_old. '.format(items, items) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track.write('{} renamed from display10 to {}_old. '.format(items, items) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{} Rename failed!!!!!!!!!!!!!!!!!!!'.format(items)
                    + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.write('!!!!!!!!!!!!!!!!!{} Rename failed!!!!!!!!!!!!!!!!!!!!!!'.format(items)
                    + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        else:
            print('\n' + '{} not in display10.'.format(items))
            track.write('\n' + '{} not in display10.'.format(items))
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} exists function failed!!!!!!!!!!!!!!!!!!!'.format(items)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} exists function failed!!!!!!!!!!!!!!!!!!!!!!'.format(items)
            + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        
    try:
        datadescribe = arcpy.Describe(fullhomefile)
        print('\n' + '{} data identified as a featureclass'.format(items) + '\n' + '\n')
        track.write('\n' + '{} data identified as a featureclass'.format(items) + '\n' + '\n')
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} describe failed!!!!!!!!!!!!!!!!!!!'.format(items)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} describe failed!!!!!!!!!!!!!!!!!!!!!!'.format(items)
            + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    
    if datadescribe.dataType == FCDescribe.dataType:    
        try:
            arcpy.CopyFeatures_management(fullhomefile, fullDisplayTen)####Copy all the matching stuff in from DB06 to DB04
            print('{} DB06 copied to Display 10 as {}.'.format(items, items))
            track.write('{} DB06 copied to Display 10 as {}.'.format(items, items) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!{} DB06 copied to Display 10 as {} failed!!!!!!!!!!!!!!!'.format(items, items)
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!!!!!!!!!{} DB06 copied to Display 10 as {} failed!!!!!!!!!!!!'.format(items, items)
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    elif datadescribe.dataType == tableDescribe.dataType:
        try:
            arcpy.TableToGeodatabase_conversion(fullhomefile, homeDisplayTen)####Copy all the matching stuff in from DB06 to DB04
            print('{} DB06 copied to Display 10 as {}.'.format(items, items))
            track.write('{} DB06 copied to Display 10 as {}.'.format(items, items) + '\n')
        except:
            print('!!!!!!!!!!!!!!!!!!!{} DB06 table copied to Display 10 as {} failed!!!!!!!!!!!'.format(items, items)
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!!!{} DB06 table copied to Display 10 as {} failed!!!!!!!!!!!'.format(items, items)
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    else:
        continue


#####Cleanup##########################################################################################################################################################################################################
    
try:
    arcpy.ClearWorkspaceCache_management(DB06)
    print('{} cleared workspace'.format(DB06))
    track.write('\n' + '\n' + '{} cleared workspace'.format(DB06) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(DB06) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(DB06)
        + '\n' + arcpy.GetMessages() + '\n'+ '\n')

try:
    arcpy.ClearWorkspaceCache_management(homeDisplayTen)
    print('{} cleared workspace'.format(homeDisplayTen))
    track.write('\n' + '\n' + '{} cleared workspace'.format(homeDisplayTen) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(homeDisplayTen) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(homeDisplayTen)
        + '\n' + arcpy.GetMessages() + '\n'+ '\n')
        

track.write('\n' + '\n' + 'DB06_to_DB04_v4, standard copy completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n' + fulltime)
track.write('\n' + '\n' + 'TokenStandardCopy' + '\n' + '\n')
track.close()
print('%s total seconds' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v3, standard copy completed')
#Written by Michael Shoop 
#Version #4 completed 06/18/20 #DB06_to_DB04_standard_copy_Script5_v7



        
