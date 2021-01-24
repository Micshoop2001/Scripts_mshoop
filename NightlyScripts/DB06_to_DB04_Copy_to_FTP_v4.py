import arcpy
import os
import time
import datetime
import shutil
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
track = open(logtime,"a") #We probably need to make a new log
Header = "Start DB06_to_DB04 Copy_to_FTP_v3"
print('Start DB06_to_DB04 Copy_to_FTP_v3' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
#####Variables####################################################################################################################################################################
homefile = r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.'
DB06 = r'Database Connections\displayadmin@GISDB04.Display10.sde'
ftp_site = r'\\ftp001\GIS\GISUSERS\Spartanburg_County_Data'
shapefiles_ftp = r'\\ftp001\GIS\GISUSERS\Spartanburg_County_Data'
firedistrict = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.FireEMSCityESN\sde.'
parcel = r'Database Connections\displayadmin@GISDB04.Display10.sde\Display10.DISPLAYADMIN.Preliminary_Flood_Data\Display10.DISPLAYADMIN.'

ftp_data = ['BoundaryLine', 'BoundaryLineAnno', 'Easement', 'OtherLines', 'Parcel', 'ParcelAnno', 'ParcelLotAnno',
            'Subdivision', 'County_Line', 'Soils', 'spot_elevation', 'StreetCenterlines', 'StructurePts', 'FireDistricts',
            'Municipalities', 'FloodPlains', 'Stream', 'CellTowers', 'Community', 'GSPEnvironsZone', 'RailroadTrack',
            'SchoolDistricts', 'SewerDist', 'ZIPCode_ESRI', 'MillTowns', 'TaxPars', 'TaxDistDissolve', 'LakesAll', 'WaterDistricts', 'CAMA']

arcpy.env.overwriteOutput = True
arcpy.env.workspace = shapefiles_ftp
for ftp in ftp_data:
    if ftp in ('FloodPlains'):
        fullhomefile = parcel + ftp
    else:
        fullhomefile = homefile + ftp

    if ftp == 'CAMA':
        ftp_item = shapefiles_ftp + '\\' + ftp + '.dbf'
        CAMA_item = ftp + '.dbf'
    else:
        ftp_item = shapefiles_ftp + '\\' + ftp + '.shp'
    
    try:
        if arcpy.Exists(ftp_item):
            try:
                arcpy.Delete_management(ftp_item)####Delete all the matching old display 10 in DB04
                print('{} deleted from FTP site. '.format(ftp) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track.write('{} deleted from FTP site. '.format(ftp) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{} deleted from FTP site failed!!!!!!!!!!!!!!!!!!!'.format(ftp)
                    + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.write('!!!!!!!!!!!!!!!!!{} deleted from FTP site failed!!!!!!!!!!!!!!!!!!!!!!'.format(ftp)
                    + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        else:
            print('\n' + '{} not in FTP site.'.format(ftp))
            track.write('\n' + '{} not in FTP site.'.format(ftp))
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} exists function failed!!!!!!!!!!!!!!!!!!!'.format(ftp)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!{} exists function failed!!!!!!!!!!!!!!!!!!!!!!'.format(ftp)
            + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        
    
    if ftp == 'CAMA':
        try:
            arcpy.TableToTable_conversion(fullhomefile, shapefiles_ftp, CAMA_item)
            print('CAMA copied to FTP site.')
            track.write('CAMA copied to FTP site.' + '\n')
        except:
            print('!!!!!!!CAMA copied to FTP site failed!!!!!!!!!!!!' + '%s total minutes' % (round((time.time() - begin_time)/60,2))
                + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!CAMA copied to FTP site failed!!!!!!!!!!!!'
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    else:
        try:
            arcpy.CopyFeatures_management(fullhomefile,  ftp_item)
            print('{} copied to FTP site'.format(ftp))
            track.write('{} copied to FTP site'.format(ftp) + '\n')
        except:
            print('!!!!!!!!!!!{} copied to FTP site failed!!!!!!!!!!!'.format(ftp)
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.write('!!!!!!!!!!!{} copied to FTP site failed!!!!!!!!!!!'.format(ftp)
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')

    
#### Cleanup ###########################################################################################    
try:
    arcpy.ClearWorkspaceCache_management(DB06)
    print('{} cleared workspace'.format(DB06))
    track.write('\n' + '\n' + '{} cleared workspace'.format(DB06) + '\n'+ '\n')
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(DB06) + '\n' + arcpy.GetMessages())
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(DB06)
        + '\n' + arcpy.GetMessages() + '\n'+ '\n')

print('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + 'DB06_to_DB04 Copy_to_FTP_v3 completed completed %s total minutes' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n')
track.write('\n' + '\n' + 'TokenFTPcopy' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04 Copy_to_FTP_v3 completed')
#Written by Michael Shoop 
#Version #3 completed 06/18/20 #DB06_to_DB04_Copy_to_FTP_v4

