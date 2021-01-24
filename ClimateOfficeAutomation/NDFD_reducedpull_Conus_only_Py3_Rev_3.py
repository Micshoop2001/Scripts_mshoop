#script for Python3

#import requests
import os
import time
import urllib.request
import urllib.error

print ('imports successful')

timestr = time.strftime('%m%d%y')

#GRIB2 data names and variables
ndfd_dsapt = 'ds.apt.bin'
ndfd_dsconhazo = 'ds.conhazo.bin'
ndfd_dscritfireo = 'ds.critfireo.bin'
ndfd_dsdryfireo = 'ds.dryfireo.bin'
ndfd_dsiceaccum = 'ds.iceaccum.bin'
ndfd_dsmaxrh = 'ds.maxrh.bin'
ndfd_dsmaxt = 'ds.maxt.bin'
ndfd_dsminrh = 'ds.minrh.bin'
ndfd_dsmint = 'ds.mint.bin'
ndfd_dsphail = 'ds.phail.bin'
ndfd_dspop12 = 'ds.pop12.bin'
ndfd_dsptornado = 'ds.ptornado.bin'
ndfd_dsptotsvrtstm = 'ds.ptotsvrtstm.bin'
ndfd_dsptotxsvrtstm = 'ds.ptotxsvrtstm.bin'
ndfd_dsptstmwinds = 'ds.ptstmwinds.bin'
ndfd_dspxhail = 'ds.pxhail.bin'
ndfd_dspxtornado = 'ds.pxtornado.bin'
ndfd_dspxtstmwinds = 'ds.pxtstmwinds.bin'
ndfd_qpf = 'ds.qpf.bin'
ndfd_dsrhm = 'ds.rhm.bin'
ndfd_dssky = 'ds.sky.bin'
ndfd_dssnow = 'ds.snow.bin'
ndfd_dstcwspdabv34c = 'ds.tcwspdabv34c.bin'
ndfd_dstcwspdabv34i = 'ds.tcwspdabv34i.bin'
ndfd_dstcwspdabv50c = 'ds.tcwspdabv50c.bin'
ndfd_dstcwspdabv50i = 'ds.tcwspdabv50i.bin'
ndfd_dstcwspdabv64c = 'ds.tcwspdabv64c.bin'
ndfd_dstcwspdabv64i = 'ds.tcwspdabv64i.bin'
ndfd_dstd = 'ds.td.bin'
ndfd_dstemp = 'ds.temp.bin'
ndfd_dswaveh = 'ds.waveh.bin'
ndfd_dswdir = 'ds.wdir.bin'
ndfd_dswgust = 'ds.wgust.bin'
ndfd_dswspd = 'ds.wspd.bin'
ndfd_dswwa = 'ds.wwa.bin'
ndfd_dswx = 'ds.wx.bin'
ndfd_lsl = 'ls-l'
ndfd_lslt = 'ls-lt'

ndfd_conus = r'http://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/VP.001-003' #continuous US

print('variables set')

superlist = [ndfd_dsiceaccum, ndfd_qpf, ndfd_dsconhazo, ndfd_dssnow,
             ndfd_dsapt, ndfd_dswgust, ndfd_dsptornado]

ndfd_conusf = r'E://Grad_School//Archive_2//Thesis//State_Climate_Office//TCO_Automation//ndfd_conus' + timestr

#Dated folder creation
try:
    os.mkdir(ndfd_conusf)
except:
    print('folder already exists')

#Assigning where data will be copied to
curdir = os.getcwd()
print(curdir)
newdir = os.chdir(ndfd_conusf)
curdir = os.getcwd()
print(curdir)

#Download of data   
for load in superlist:
    stringCoble = str(ndfd_conus + '/' + str(load))
    print (stringCoble)
    filer = urllib.request.Request(stringCoble)                    
    responseapt = urllib.request.urlopen(filer)
    print('this is were im telling it to go', responseapt)
    print('were we actually go', responseapt.geturl())
    output = open(load, 'wb')
    output.write(responseapt.read())
    output.close
                
    
    
print('hahahahaha yes!')
