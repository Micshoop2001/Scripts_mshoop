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
Header = "Start DB06_to_DB04_v4 script 4, TC2"
print('Start DB06_to_DB04_v4 script 4, TC2' + fulltime + '\n')
track.write('\n' + '\n' + Header + '\n' + fulltime + '\n')
track.close()
#####Variables##########################################################################################################################################################################################################
##################TC2##################################################################
tc_two_zzTaxPars = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.TaxPars' #this will be path for DB06
tc_two_zzTaxDistDissolve = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.TaxDistDissolve' #this will be path for DB06
fullhomefileParsJ = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.ParsJ'
path_APpars = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.APpars'
tableDistricts = r'Database Connections\sde@gisdb06.sde.sde\sde.SDE.TableDistricts' ##This is just a stand in till we know the DB06 location
item_list = [tc_two_zzTaxPars, tc_two_zzTaxDistDissolve]
###########Section1 Actions#############################################################################################################################################################################################
db_six, zztaxes = os.path.split(tc_two_zzTaxPars)
zzTaxDistDissolve = 'TaxDistDissolve'
arcpy.env.workspace = db_six
#### privilege variables #####################################################################################################
tax_list = [tc_two_zzTaxPars, tc_two_zzTaxDistDissolve, fullhomefileParsJ, path_APpars]
privilege_list = [['AdminEditor', 'GRANT', 'GRANT'], ['GISViewer', 'GRANT', '#']]
###TC2#########################################################################################################
arcpy.env.overwriteOutput = True
print('Starting parcel to zzTaxPars and zzTaxDistDissolve.')
for item in item_list:
    db_dan, xxtaxes = os.path.split(item)
    olditem = item + '_old'
    db_old, oldtaxes = os.path.split(olditem)
    try:
        if arcpy.Exists(item):
            try:
                arcpy.Delete_management(olditem)
                print('{} deleted from DB06.'.format(oldtaxes) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track = open(logtime,"a")
                track.write('{} deleted from DB06.'.format(oldtaxes) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
                track.close()
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{} deleted from DB06 failed!!!!!!!!!!!!!!!!!!!'.format(oldtaxes)
                    + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track = open(logtime,"a")
                track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} deleted from DB06 failed!!!!!!!!!!!!!!!!!!!'.format(oldtaxes)
                    + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.close()
            try:
                arcpy.Rename_management(item, olditem)  ####Make existing DB06 stuff old DB06 stuff
                print('{} renamed from DB06 to {}. '.format(xxtaxes, oldtaxes) + '%s total minutes' % (
                    round((time.time() - begin_time) / 60, 2)) + '\n')
                track = open(logtime, "a")
                track.write('{} renamed from DB06 to {}. '.format(xxtaxes, oldtaxes) + ' %s total minutes' % (
                    round((time.time() - begin_time) / 60, 2)) + '\n')
                track.close()
            except:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!{} Rename failed!!!!!!!!!!!!!!!!!!!'.format(oldtaxes)
                      + '%s total minutes' % (round((time.time() - begin_time) / 60, 2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track = open(logtime, "a")
                track.write('!!!!!!!!!!!!!!!!!{} Rename failed!!!!!!!!!!!!!!!!!!!!!!'.format(oldtaxes)
                            + ' %s total minutes' % (round((time.time() - begin_time) / 60, 2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
                track.close()
        else:
            print('{} doesnt exist on DB06.'.format(xxtaxes) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
            track = open(logtime,"a")
            track.write('{} doesnt exist on DB06.'.format(xxtaxes) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
            track.close()
    except:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} Exist on DB06 failed!!!!!!!!!!!!!!!!!!!'.format(xxtaxes)
            + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track = open(logtime,"a")
        track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} Exist on DB06 failed!!!!!!!!!!!!!!!!!!!'.format(xxtaxes)
            + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
        track.close()
#################################################################################################################################################
try:
    #JoinField_management(in_data, in_field, join_table, join_field, {fields;fields...})
    arcpy.CopyFeatures_management(fullhomefileParsJ, tc_two_zzTaxPars)
    print('{} copied as TaxPars'.format('ParsJ') + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track = open(logtime,"a")
    track.write('{} copied as TaxPars'.format('ParsJ') + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!{} copied as TaxPars failed!!!!!!!!!!!!!!!!!!!'.format('ParsJ')
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track = open(logtime,"a")
    track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} copied as TaxPars failed!!!!!!!!!!!!!!!!!!!'.format('ParsJ')
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.close()
track = open(logtime,"a")
track.write('\n' + '\n' + 'TokenTaxpars' + '\n' + '\n')
track.close()
try:
    arcpy.JoinField_management(tc_two_zzTaxPars, 'District' ,tableDistricts, 'Code')
    print('{} joined to {}'.format(zztaxes, 'TableDistricts') + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track = open(logtime,"a")
    track.write('{} joined to {}'.format(zztaxes, 'TableDistricts') + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!{} joined to {} failed!!!!!!!!!!!!!!!!!!!'.format(zztaxes, 'TableDistricts')
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track = open(logtime,"a")
    track.write('!!!!!!!!!!!!!!!!!!{} joined to {} failed!!!!!!!!!!!!!!!!!!!'.format(zztaxes, 'TableDistricts')
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.close()

try:
    arcpy.Dissolve_management(tc_two_zzTaxPars, tc_two_zzTaxDistDissolve, "Code;Description;FullDescription", "", "MULTI_PART", "DISSOLVE_LINES")
    print('D drive parcel data dissolved to DB06 as zzTaxDistDissolve.' + '\n')
    track = open(logtime,"a")
    track.write('D drive parcel data dissolved to DB06 as zzTaxDistDissolve.' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
    track.close()
except:
    print('\n' + '\n' + 'D drive parcel data dissolved to DB06 as zzTaxDistDissolve failed!!!!!!!!!!!!!!!!!!!!!!' + '\n' + '\n')
    print('\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track = open(logtime,"a")
    track.write('\n' + '\n' + 'D drive parcel data dissolved to DB06 as zzTaxDistDissolve failed!!!!!!!!!!!!!!!!!!!!!!'
        + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
    track.close()

print('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track = open(logtime,"a")
track.write('\n' + '\n' + 'TokenTaxDistDissolve' + '\n' + '\n')
track.write('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')                                 
track.close()
#### Cleanup ##################################################################################################
print('establishing priviliges' + '\n' + '\n')
track = open(logtime,"a")
track.write('establishing priviliges' + '\n' + '\n')
track.close()
for tax in tax_list:
    simple = os.path.basename(tax)
    for privilege in privilege_list:   
        try:
            arcpy.ChangePrivileges_management(tax, privilege[0], privilege[1], privilege[2])
            print('{} has {} privileges given'.format(simple, privilege[0]) + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track = open(logtime,"a")
            track.write('{} has {} privileges given'.format(simple, privilege[0]) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n')
            track.close()
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!{} has {} privileges given failed!!!!!!!!!!!!!!!!!!!'.format(simple, privilege[0])
                + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track = open(logtime,"a")
            track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} has {} privileges given failed!!!!!!!!!!!!!!!!!!!'.format(simple, privilege[0])
                + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n' + arcpy.GetMessages() + '\n' + '\n')
            track.close()
try:
    arcpy.ClearWorkspaceCache_management(db_six)
    print('{} cleared workspace'.format(db_six))
    track = open(logtime,"a")
    track.write('\n' + '\n' + '{} cleared workspace'.format(db_six) + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
    track.close()
except:
    print('!!!!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(db_six)
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + arcpy.GetMessages())
    track = open(logtime,"a")
    track.write('\n' + '\n' + '!!!!!!!!!!!!!!!!!!!{} cleared workspace!!!!!!!!!!!!!!!!!!!!!!!'.format(db_six)
        + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + arcpy.GetMessages() + '\n'+ '\n')
    track.close()

print('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track = open(logtime,"a")
track.write('\n' + '\n' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n'+ '\n')
track.write('\n' + '\n' + 'DB06_to_DB04_v4 script 4, TC2 completed' + '%s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
track.write('\n' + '\n' + 'TokenTaxpars' + '\n' + '\n')
track.write('\n' + '\n' + 'TokenTaxDistDissolve' + '\n' + '\n')
track.close()
print('%s total minutes' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4 script 4, TC2 completed')


#Written by Michael Shoop 
#Version #4 completed 06/23/20 #DB06_to_DB04_TC2_Script4_v8
