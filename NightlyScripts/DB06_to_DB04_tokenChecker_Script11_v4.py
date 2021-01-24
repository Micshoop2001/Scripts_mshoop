#read text from log

#import mmap #we may possibly use this method if the simplier method proves slow.

import time
###############################################################time & log setup###########################################################################################
#Time##
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
trackerlog = script_working + '\\DB06_to_DB04_v4' + timestream + '.txt'
#Start Log
track = open(logtime,"a") #We probably need to make a new log
Header = 'Start DB06_to_DB04_v4 token validation'
print('Start DB06_to_DB04_v4 token validation ' + fulltime + '\n')
track.write('\n' + '\n' + '\n' + '\n' + '\n' + Header + '\n' + fulltime + '\n')
##############################################################variables#################################################################################################
added =[]
##############################################################list######################################################################################################
tokenlist = [["TokenServerDisco", "Server disconnect"], ["Token911Dissolve", "911 Dissolve of composite"],
             ["Token911fieldadd", "911 fields add and calc"], ["Token911privileges", "911 privileges establish"],
             ["Token911versioning", "911 versioning establish"],
             ["TokenStrpts_strCenterlineFields", "StructurePts and Streetcenterline Field updates"],
             ["TokenDeleterelationships", "relationships delete"], ["TokenCamaCopy", "CAMA copy over"],
             ["TokenParsJ", "ParsJ create"], ["TokenAPpars", "APpars create"], ["TokenTaxpars", "Taxpars create"],
             ["TokenTaxDistDissolve", "TaxDistDissolve create"], ["TokenStandardCopy", "Standard copy"],
             ["TokenStrucPts", "StructurePts completed"], ["TokenStrCenterLine", "StreetCenterLines completed"],
             ["TokenParcelFields", "Parcel field build"], ["TokenFTPcopy", "FTP copy"], ["TokenIndex", "indexing"],
             ["TokenServerConnect", "Server connect"]]
 
with open(trackerlog, 'rt') as f:
    for l in f:
        print(l)
        for token in tokenlist:           
            if token[0] in l:
                added.append(token)
                break
            else:
                continue
print(added)

final_missing = [i for i in added + tokenlist if i not in added]
print(final_missing)
track.write('\n' + '\n' + 'tokens present' + '\n')
for x in added:
    print(x[0] + ' found')
    track.write('\n' + x[1] + ' ' + x[0] + ' found' + '\n')

for y in final_missing:
    print(y[0] + ' not found')
    track.write('\n' + y[1] + ' ' + y[0] + ' not found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' + '\n')

#####Cleanup##########################################################################################################################################################################################################
    
track.write('\n' + '\n' + 'DB06_to_DB04_v4, token validation completed %s total seconds' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n' + fulltime)
track.close()
print('%s total seconds' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4, token validation completed')
#Written by Michael Shoop 
#Version #4 completed 06/15/20 #DB06_to_DB04_token validation







        
