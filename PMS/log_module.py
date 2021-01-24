import time

def logger(place, filename, function, begin_time, GetMessages):
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
    #begin_time = time.time()#needs to be in main script
    script_working = r'C:\Nightly Scripts\PMS_log'
    logtime = script_working + '\\PMS_' + timestream + '.txt'
    #####Variables#########################################################################################################
    #Start Log
    track = open(logtime,"a")
    
    if place == 'start':
        print(filename + ' ' + fulltime + '\n')
        track.write('\n' + '\n' + filename + '\n' + fulltime + '\n')
    elif place == 'succeed':
        print('{} for {} succeeded'.format(function, filename) + ' %s total seconds' % (time.time() - begin_time) + '\n' + '\n')
        track.write('{} for {} succeeded'.format(function, filename) + ' %s total seconds' % (time.time() - begin_time) + '\n' + '\n')
    elif place == 'failed':
        print('!!!!!!!!!!!!!!!!!!!!!!!!!{} for {} failed!!!!!!!!!!!!!!!!!!!'.format(function, filename)
              + ' %s total seconds' % (time.time() - begin_time) + '\n' + str(GetMessages) + '\n' + '\n')
        track.write('!!!!!!!!!!!!!!!!!!!!!!!!!{} for {} failed!!!!!!!!!!!!!!!!!!!'.format(function, filename) + ' %s total seconds' % (time.time() - begin_time)
                    + '\n' + str(GetMessages) + '\n' + '\n')
    else:
        print('Script completed' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
        track.write('Script completed' + ' %s total minutes' % (round((time.time() - begin_time)/60,2)) + '\n' + '\n')
        
    track.close()
