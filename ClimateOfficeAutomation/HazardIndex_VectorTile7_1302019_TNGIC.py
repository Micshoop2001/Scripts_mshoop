import arcpy
import os
import time


#Variables
origin = r'E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\Transfer_file_newvariables.gdb'
archive = r'E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\Archive.gdb'
intersectlist = []
haznumlist = []
intersectlistre = []
deletefields = []
timestr = time.strftime("%m%d%y")

#################################################################################################################
#SQL statements for selecting hazard index data
lowhitemp = '"temp_max_grid" BETWEEN 100 AND 104.999'
midhitemp = '"temp_max_grid" BETWEEN 105 AND 114.999'
highhitemp = '"temp_max_grid" >= 115'

lowlowtemp = '"temp_min_grid" BETWEEN 0 AND -9.999'
midlowtemp = '"temp_min_grid" BETWEEN -10 AND -19.999'
highlowtemp = '"temp_min_grid" <= -20'

lowwgust = '"wg__grid" BETWEEN 40 AND 49.999'
midwgust = '"wg__grid" BETWEEN 50 AND 59.999'
highwgust = '"wg__grid" >= 60'

lowrainfall = '"ra__grid" BETWEEN 1 and 2.999'
midrainfall = '"ra__grid" BETWEEN 3 and 4.999'
highrainfall = '"ra__grid" >= 5'

lowsnowfall = '"sn__grid" BETWEEN 2 AND 3.999'
midsnowfall = '"sn__grid" BETWEEN 4 AND 7.999'
highsnowfall = '"sn__grid" >= 8'

lowiceaccum = '"ic__grid" BETWEEN 0.01 AND 0.099'
midiceaccum = '"ic__grid" BETWEEN 0.1 AND 0.249'
highiceaccum = '"ic__grid" >= 0.25'

lowwspd = '"wsp__grid" BETWEEN 40 AND 49.999'
midwspd = '"wsp__grid" BETWEEN 50 AND 59.999'
highwspd = '"wsp__grid" >= 60'

lowcon = '"con__grid" BETWEEN 3 AND 5'
midcon = '"con__grid" BETWEEN 5.99 AND 6'
highcon = '"con__grid" BETWEEN 6.99 AND 10'

Nada = 'haz_index IS NULL'

######################################################################################################################
#Nested Dictionary with SQL statements
weatherlist =  {'ic_inchpolyclip': {lowiceaccum: 'low,', midiceaccum: 'medium,', highiceaccum: 'high,'},
               'sn_inchpolyclip': {lowsnowfall: 'low,', midsnowfall: 'medium,', highsnowfall: 'high,'},
               'temp_maxfehrpolyclip': {lowhitemp: 'low,', midhitemp: 'medium,', highhitemp: 'high,'}, 
               'temp_minfehrpolyclip': {lowlowtemp: 'low,', midlowtemp: 'medium,', highlowtemp: 'high,'},
               'wg_mphpolyclip': {lowwgust: 'low,', midwgust: 'medium,', highwgust: 'high,'},
               'ra_inchespolyclip': {lowrainfall: 'low,', midrainfall: 'medium,', highrainfall: 'high,'},
               'con_polyclip': {lowcon: 'low,', midcon: 'medium', highcon: 'high,'},
               'ic_inch5polyclip': {lowiceaccum: 'low,', midiceaccum: 'medium,', highiceaccum: 'high,'},
               'sn_inch5polyclip': {lowsnowfall: 'low,', midsnowfall: 'medium,', highsnowfall: 'high,'},
               'temp_maxfehr5polyclip': {lowhitemp: 'low,', midhitemp: 'medium,', highhitemp: 'high,'}, 
               'temp_minfehr5polyclip': {lowlowtemp: 'low,', midlowtemp: 'medium,', highlowtemp: 'high,'}, 
               'wg_mph5polyclip': {lowwgust: 'low,', midwgust: 'medium,', highwgust: 'high,'},
               'ra_inches5polyclip': {lowrainfall: 'low,', midrainfall: 'medium,', highrainfall: 'high,'},
               'con_5polyclip': {lowcon: 'low,', midcon: 'medium', highcon: 'high,'}}

#############################################################################################################################
#Creation of hazard index fields and using SQL statements to define measurement within hazard index
arcpy.env.workspace = origin
arcpy.env.overwriteOutput = True
print('modules and variables done')

for weather, dictindex in weatherlist.items():
    clearday = weather.replace('polyclip', '')
    path = origin + '\\' + weather
    if clearday.endswith('5'):
        intersectlistre.append(path)
    else:
        intersectlist.append(path)
    if weather.startswith('temp_max'):
        conname = ' maximum temperature'
        namestrip = 'temp_max'
    elif weather.startswith('temp_min'):
        conname = ' minimum temperature'
        namestrip = 'temp_min'
    elif weather.startswith('ra'):
        conname = ' rain in 6 hours'
        namestrip = 'ra_'
    elif weather.startswith('con'):
        conname = ' categorical convection'
        namestrip = 'con_'
    elif weather.startswith('sn'):
        namestrip = 'sn_'
        conname = ' snowfall'
    elif weather.startswith('ic'):
        conname = ' ice accumulation'
        namestrip = 'ic_'
    elif weather.startswith('wg'):
        namestrip = 'wg_'
        conname = ' wind gust'
    elif weather.startswith('wsp'):
        namestrip = 'wsp_'
        conname = ' max wind speed'
    gridname = namestrip + '_grid'
    hazname = namestrip + '_index'
    haznum = namestrip + '_num'
    haznumlist.append(haznum)
    arcpy.management.AddField(path, gridname, 'DOUBLE')
    arcpy.management.AddField(path, hazname, 'TEXT')
    arcpy.management.AddField(path, haznum, 'LONG')
    arcpy.management.CalculateField(path, gridname, '!grid_code!', 'PYTHON3')
    hdfd_HI_individuals = arcpy.ListFields(path)
    arcpy.MakeFeatureLayer_management(path, 'weather')
    
    for ind in dictindex:
        arcpy.SelectLayerByAttribute_management('weather', 'NEW_SELECTION', ind)
        ind_haz_index = dictindex[ind] + conname
        ind_haz_fullquote = '"{}"'.format(ind_haz_index)
        arcpy.management.CalculateField('weather', hazname, ind_haz_fullquote, 'PYTHON3')
        print(ind_haz_index + ' calculated for haz_index')
        if ind_haz_index.startswith('high'):
            haznumber = 5
        elif ind_haz_index.startswith('medium'):
            haznumber = 4
        elif ind_haz_index.startswith('low'):
            haznumber = 3
        else:
            haznumber = 0
        arcpy.management.CalculateField('weather', haznum, haznumber, 'PYTHON3')
        print(str(haznumber) + ' calculated for haz_num')
    Nado =  hazname + ' IS NULL' 
    arcpy.SelectLayerByAttribute_management('weather', 'NEW_SELECTION', Nado)
    arcpy.management.CalculateField('weather', haznum, 0, 'PYTHON3')
    arcpy.Delete_management('weather')
    print(weather + ' has field' + gridname + ' added')
print('weatherlist fields built')

################################################################################################################################
#Merging the vector polygons together, deleting extra fields and archiving
intersect_vector = origin + '\\' + 'hdfd_HI_data'
intersectre_vector = origin + '\\' + 'hdfd_HI_data_5'
listforintersect = [[intersectlist, intersect_vector], [intersectlistre, intersectre_vector]]
for inter in listforintersect:
    enterlist = inter[0]
    interfile = inter[1]
    arcpy.analysis.Intersect(enterlist, interfile, 'ALL', None, 'INPUT')
    arcpy.management.AddField(interfile, 'haz_index', 'LONG')
    arcpy.env.workspace = interfile
    hdfd_HI_datafields = arcpy.ListFields(interfile)
    arcpy.MakeFeatureLayer_management(interfile, 'hazardindex')
    expression = '!ic__num!' ' + ' '!sn__num!' ' + ' '!temp_max_num!' ' + ' '!temp_min_num!' ' + ' '!ra__num!' ' + ' '!wg__num!' ' + ' '!con__num!' 
    arcpy.SelectLayerByAttribute_management('hazardindex', 'NEW_SELECTION', Nada)
    arcpy.management.CalculateField('hazardindex', 'haz_index', expression, 'PYTHON3')
    arcpy.Delete_management("hazardindex")
    
    for java in hdfd_HI_datafields:
        if java.name.startswith('FID'):
            deletefields.append(java.name)
        elif java.name.startswith('Input'):
            deletefields.append(java.name)
        elif java.name.startswith('point'):
            deletefields.append(java.name)
        elif java.name.startswith('grid'):
            deletefields.append(java.name)
    arcpy.management.DeleteField(interfile, deletefields)

    splittwo = os.path.basename(interfile)
    uniontwo = os.path.join(archive,splittwo)
    archivefile = uniontwo + timestr
    arcpy.CopyFeatures_management(interfile, archivefile)


               
print('All done and ready for transfer')


