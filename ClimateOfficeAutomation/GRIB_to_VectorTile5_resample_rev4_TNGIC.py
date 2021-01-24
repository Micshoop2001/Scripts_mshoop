import arcpy
import os
import time
from arcpy.sa import*
arcpy.CheckOutExtension("Spatial")
import gdal

#Variables, folder making, time and overwrite
homefile = r'E://Grad_School//Archive_2//Thesis//State_Climate_Office//TCO_Automation'
boundary = r'E://Grad_School//Archive_2//Thesis//State_Climate_Office//TCO_Automation//Transfer_file.gdb//TNBoundary'
transfer_file = r'E://Grad_School//Archive_2//Thesis//State_Climate_Office//TCO_Automation//Transfer_file_newvariables.gdb'
tifflist = []
mergeraster = []
clippedgroup = []
singlegroup = []
vectorgroup = []

binlist = ['ds.apt.bin', 'ds.snow.bin', 'ds.wgust.bin', 'ds.qpf.bin','ds.conhazo.bin', 'ds.iceaccum.bin']
timestr = time.strftime("%m%d%y")
binpaths = r'E://Grad_School//Archive_2//Thesis//State_Climate_Office//TCO_Automation//ndfd_conus' + timestr
bombsite = homefile + '//' + 'NDFD_Daily_Rasters_' + timestr
print('imports and variables setup')
begin_time = time.time()
fehrclip = homefile + '//' + 'temp_max_TNfehr.tif'
arcpy.env.snapRaster = fehrclip
try:
    os.mkdir(bombsite)
    print('folder created')
except:
    print('file already made')
  
arcpy.env.workspace = bombsite
arcpy.env.overwriteOutput = True

arcpy.CreateFileGDB_management(bombsite, 'NDFD_resample_' + timestr)#these used? need time gdb

resamplelocation = bombsite + '//' + 'NDFD_resample_' + timestr + '.gdb' #these used? need time gdb

#GRIB2 pulling out rasters and converting to mosaicked tiffs
for weather in binlist:
    ndfd_data = binpaths + '//' + weather
    if weather == 'ds.wgust.bin':
            forcast = 'wg_'
    elif weather == 'ds.apt.bin':
            forcast = 'apt_'         
    elif weather == 'ds.snow.bin':
            forcast = 'sn_'
    elif weather == 'ds.iceaccum.bin':    
            forcast = 'ic_'
    elif weather == 'ds.wspd.bin':
            forcast = 'wsp_'
    elif weather == 'ds.qpf.bin':   
            forcast = 'ra_'
    elif weather == 'ds.conhazo.bin':
            forcast = 'con_'
    gdalopen = gdal.Open(ndfd_data, gdal.GA_ReadOnly)
    numero = gdalopen.RasterCount
    print(numero)
    numa = 0
    merge_name = forcast + '.tif'
    
    if numero <= 1:
        print('only one record in ' + weather)
        subout = forcast + str(numa)
        suboutpath = bombsite + '//' + subout
        castle = arcpy.Describe(ndfd_data)
        keep = castle.spatialReference
        print(subout + ' created')
        asciioutput = bombsite + '//' + forcast + str(numa) + '_ascii.txt'
        arcpy.RasterToASCII_conversion(ndfd_data, asciioutput)
        print('raster to ascii worked')
        tiffnopath = forcast + str(numa) + '_ti.tif'
        tiffoutput = str(bombsite) + '//' + tiffnopath
        arcpy.ASCIIToRaster_conversion(asciioutput, tiffoutput)
        print('ascii to raster worked')
        arcpy.DefineProjection_management(tiffoutput, keep)
        print(tiffnopath + ' proj. defined')
        singlegroup.append(tiffnopath)

    else:  
        for num in range(numero):
            print(numa)
            subout = forcast + str(numa)
            suboutpath = bombsite + '//' + subout
            arcpy.ExtractSubDataset_management(ndfd_data, suboutpath, numa)
            print(str(numa) + 'extract completed')
            castle = arcpy.Describe(suboutpath)
            keep = castle.spatialReference
            remask = arcpy.sa.ExtractByMask(suboutpath, fehrclip)
            print('extract done')
            test_save = suboutpath + '_clip'
            remask.save(test_save)
            asciioutput = bombsite + '//' + forcast + str(numa) + '_ascii.txt'
            arcpy.RasterToASCII_conversion(test_save, asciioutput)
            print('raster to ascii done')
            tiffnopath = forcast + str(numa) + '_ti.tif'
            tiffoutput = str(bombsite) + '//' + tiffnopath
            tifflist.append(tiffoutput)
            arcpy.ASCIIToRaster_conversion(asciioutput, tiffoutput, "FLOAT")
            print('ascii to raster done')
            arcpy.DefineProjection_management(tiffoutput, keep)
            numa += 1

        
        
        if weather == 'ds.apt.bin':
            m_temp_min = 'temp_min.tif'
            m_temp_max = 'temp_max.tif'
            try:
                arcpy.MosaicToNewRaster_management(tifflist, bombsite, m_temp_max, '#', '32_BIT_FLOAT', '#', '1', 'MAXIMUM', 'FIRST')
                arcpy.MosaicToNewRaster_management(tifflist, bombsite, m_temp_min, '#', '32_BIT_FLOAT', '#', '1', 'MINIMUM', 'FIRST')
                mergeraster.append(m_temp_min)
                mergeraster.append(m_temp_max)
            except:
                print('ds file failed')
       
        elif weather == 'ds.wgust.bin' or weather == 'ds.wspd.bin' or weather == 'ds.qpf.bin' or weather == 'ds.conhazo.bin':
            try:
                arcpy.MosaicToNewRaster_management(tifflist, bombsite, merge_name, '#', '32_BIT_FLOAT', '#', '1', 'MAXIMUM', 'FIRST')
                mergeraster.append(merge_name)
            except:
                print('ds file failed')
        else:
            arcpy.MosaicToNewRaster_management(tifflist, bombsite, merge_name, '#', '32_BIT_FLOAT', '#', '1', 'SUM', 'FIRST')
            mergeraster.append(merge_name)
        print(weather + ' merged')
        del tifflist[:]

print('giant mergers done')
print('now for general cleaning up')
print('......')
print('......')
print(mergeraster)

# Converting tiffs from international measurements to US measurements      
for TN in mergeraster:
    if TN.startswith('temp_min') or TN.startswith('temp_max'):
         fullblister = bombsite + '//' + TN
         fehr = Raster(fullblister)
         heit = (fehr-273.15) * (9/5) + 32 
         notiff = TN.replace('.tif', '')
         notifffehr = notiff + 'fehr.tif'
         addfehr = bombsite + '//' + notifffehr
         heit.save(addfehr)
         clippedgroup.append(notifffehr)
         vectorgroup.append(notifffehr)
         print(TN + ' converted to F')
    #kg/m2 to inches
    elif TN.startswith('ic_'):
         icetransfer = bombsite + '//' + TN
         frozen = Raster(icetransfer)
         iceconvert = frozen * 0.039370
         icestrip = TN.replace('.tif', '')
         notiffice = icestrip + 'inch.tif'
         addice = bombsite + '//' + notiffice
         iceconvert.save(addice)
         clippedgroup.append(notiffice)
         vectorgroup.append(notiffice)
         print(TN + ' converted to inches from kgm2')
    #meters to inches
    elif TN.startswith('sn_'):
         snowtransfer = bombsite + '//' + TN
         snowman = Raster(snowtransfer)
         snowconvert = snowman * 39.370 
         snowstrip = TN.replace('.tif', '')
         notiffsnow = snowstrip + 'inch.tif'
         addsnow = bombsite + '//' + notiffsnow
         snowconvert.save(addsnow)
         clippedgroup.append(notiffsnow)
         vectorgroup.append(notiffsnow)
         print(TN + ' converted from meters to inches')
    #ms-1 to mph
    elif TN.startswith('wg_') or TN.startswith('wsp_'):
         windtransfer = bombsite + '//' + TN
         windgust = Raster(windtransfer)
         windconvert = windgust * 2.236936271
         windstrip = TN.replace('.tif', '')
         notiffwind = windstrip + 'mph.tif'
         addwind = bombsite + '//' + notiffwind
         windconvert.save(addwind)
         clippedgroup.append(notiffwind)
         vectorgroup.append(notiffwind)
         print(TN + ' converted from ms-1 to mph')
    #kg/m2 to inches
    elif TN.startswith('ra_'):
         raintransfer = bombsite + '//' + TN
         rain = Raster(raintransfer)
         rainconvert = rain * 0.039370080320721
         rainstrip = TN.replace('.tif', '')
         notiffrain = rainstrip + 'inches.tif'
         addrain = bombsite + '//' + notiffrain
         rainconvert.save(addrain)
         clippedgroup.append(notiffrain)
         vectorgroup.append(notiffrain)
         print(TN + ' converted from kg/m2 to inches')
    else:
         clippedgroup.append(TN)
         vectorgroup.append(TN)
         print(TN + 'clipped to TN boundary')
print('......')
print('......')   
   

for single in singlegroup:
    singlestrip = single.replace('.tif', '')
    resampler = singlestrip + 'clipp.tif'
    singleoutput = bombsite + '//' + resampler                         
    singlepath = bombsite + '//' + single
    singlemask = arcpy.sa.ExtractByMask(singlepath, fehrclip)
    print(single + ' extracted by mask')
    singlemask.save(singleoutput)
    clippedgroup.append(resampler)
    vectorgroup.append(resampler)
print('singles now are ready to convert with multi rasters')

for clgr in clippedgroup:    
    clgrpath = bombsite + '//' + clgr
    clgrstrip = clgr.replace('.tif', '')
    clgradd = clgrstrip + '5'
    clgroutraster = resamplelocation + '//' +  clgradd
    arcpy.management.Resample(clgrpath, clgroutraster, "5000 5000", "NEAREST")
    vectorgroup.append(clgradd)


arcpy.env.workspace = transfer_file
arcpy.env.overwriteOutput = True

#Converting tiffs to vector polygons
for vec in vectorgroup:
    if vec.endswith('5'):
        TN_clippedfull = resamplelocation + '//' + vec
        TN_point_strip = vec
    else:
        TN_clippedfull = bombsite + '//' + vec
        TN_point_strip = vec.replace('.tif', '')
        
    TN_point_path = transfer_file + '//' + TN_point_strip
    arcpy.conversion.RasterToPoint(TN_clippedfull, TN_point_path, "Value")
    print(TN_point_strip + ' done')
    
    TN_poly = TN_point_strip + 'poly'
    TN_poly_path = transfer_file + '//' + TN_poly 
    arcpy.analysis.CreateThiessenPolygons(TN_point_path, TN_poly_path, "ALL")
    print(TN_poly + ' done')
    
    TN_polyclip = TN_point_strip + 'polyclip'
    TN_polyclip_path = transfer_file + '//' + TN_polyclip
    arcpy.analysis.Clip(TN_poly_path, boundary, TN_polyclip_path, None)
    print(TN_polyclip + ' done')



arcpy.CheckInExtension("Spatial")      
print('all done with raster conversions and editing :)')
print ('%s total seconds' % (time.time() - begin_time))
