import arcpy
import urllib.request
import os
import time
import csv
from datetime import timedelta, datetime

#Modules
def Oz(FileName, stump, Time, F_Scale, Location, County, State, Lat, Lon, Comments):
    arcpy.CreateFeatureclass_management(bombsite, FileName, "POINT", "", "", "", spatialref)
    arcpy.AddField_management(stump, Time, "SHORT")
    arcpy.AddField_management(stump, F_Scale, "TEXT")
    arcpy.AddField_management(stump, Location, "TEXT")
    arcpy.AddField_management(stump, County, "TEXT")
    arcpy.AddField_management(stump, State, "TEXT")
    arcpy.AddField_management(stump, Lat, "FLOAT")
    arcpy.AddField_management(stump, Lon, "FLOAT")
    arcpy.AddField_management(stump, Comments, "TEXT", "", "", fieldlength)
    arcpy.AddField_management(stump, "Date", "TEXT")
    arcpy.AddField_management(stump, "Count", "SHORT")

    
def Avalon(Tango, Stump, Time, F_Scale, Location, County, State, Lat, Lon, Comments, Wizard):
    with arcpy.da.InsertCursor(Stump, ("SHAPE@XY", Time, F_Scale, Location, County, State, Lat, Lon, Comments))as wizard:
        for players in Tango:
            Timez = players[0]
            TimeInt2 = int(Timez)
            F_Scalez = players[1]
            Countyz = players[3]
            State = players[4]
            Latz = players[5]
            numLat = float(Latz)
            Lonz = players[6]
            numLon = float(Lonz)
            Commentsz = players[7]
            Locationz = players[2]
            wizard.insertRow(((float(numLon), float(numLat)), TimeInt2, F_Scalez, Locationz, Countyz, State, numLat, numLon, Commentsz))

#time setup
timestream = datetime.now() - timedelta(days= 1)
timestr = timestream.strftime("%m%d%y")
propmonth = timestream.strftime('%B')
propday = timestream.strftime('%d')
propyear = timestream.strftime('%Y')
dytextdate = propmonth + ' ' + propday + ', ' + propyear
begin_time = time.time()
#add day of week at beginning?

#Variables
placeholder_spot = r"E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\NOAA_DATA_PULL"
basicurl = r"http://www.spc.noaa.gov/climo/reports"
torncsv = 'yesterday_torn.csv'
hailcsv = 'yesterday_hail.csv'
windcsv = 'yesterday_wind.csv'
tornrawscv = 'yesterday_raw_torn.csv'
weatherlistOne = [torncsv, windcsv, hailcsv, tornrawscv]
weatherlist = [torncsv, windcsv, hailcsv]
spatialsurogate = r"E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\NOAA_DATA_PULL\SpatialReference\SpatialReference.shp"
spatialref = arcpy.Describe(spatialsurogate).spatialReference
fieldlength = 300
partarch = r'E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\NOAA_DATA_PULL\Archive'
bombsite = partarch + '\\' + 'SPC_Daily_' + timestr
boundary = r'E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\NOAA_DATA_PULL\Boundary\TNBoundary.shp'

#Folder creation
try:
    os.mkdir(bombsite)
    print('folder created')
except:
    print('folder already made')

#Set workspace environment for Arcpy and os
curdir = os.getcwd()
print(curdir)
newdir = os.chdir(bombsite)
curdir = os.getcwd()
print(curdir)
arcpy.env.workspace = bombsite
arcpy.env.overwriteOutput = True

#Pulling data from SPC website
for climateOne in weatherlistOne:
    stringcobbleone = basicurl + '/' + climateOne
    print(stringcobbleone)
    req = urllib.request.Request(stringcobbleone)
    reqopen = urllib.request.urlopen(req)
    output = open(climateOne, 'wb')
    output.write(reqopen.read())
    output.close
    
#Setting up to read csv files
for climate in weatherlist:
    newstringcobble = bombsite + '\\' + climate
    print(newstringcobble)
    climatestr = climate.replace('.csv', '')
    newreader = open(newstringcobble, 'r')
    print(newreader)
    csvreader = csv.reader(newreader, delimiter= ',')
    print(csvreader)
    header = csvreader.__next__()
    print(header)
    filenameT = climatestr + "_" + timestr + ".shp"
    filenameTclip = climatestr + '_clip_' + timestr + '.shp'
    print(filenameT)
    shortnameT = climatestr + ".shp"
    shortnameTclip = climatestr + '_clip_' + ".shp"
    print(shortnameT)
    fullpath = bombsite + '\\' + filenameT
    fullpathclip = bombsite + '\\' + filenameTclip
    print(fullpath)
    branchT = placeholder_spot + '\\' + shortnameT
    branchTclip = placeholder_spot + '\\' + shortnameTclip
    print(branchT)

    #establishing file headers and providing input for modules & running them
    if climate == torncsv:
        Time = "Time"
        F_Scale = "F_Scale"
        Location = "Location"
        County = "County"
        State = "State"
        Lat = "Lat"
        Lon = "Lon"
        Comments = "Comments"
        wizard = "gandalf"
        
        Time1 = header.index("Time")
        F_Scale1 = header.index("F_Scale")
        Location1 = header.index("Location")
        County1 = header.index("County")
        State1 = header.index("State")
        Lat1 = header.index("Lat")
        Lon1 = header.index("Lon")
        Comments1 = header.index("Comments")
        Oz(filenameT, fullpath,Time, F_Scale, Location, County, State, Lat, Lon, Comments)
        print ("oz1")
        Avalon(csvreader, fullpath, Time,F_Scale, Location, County, State, Lat, Lon, Comments, wizard)
        print("Avalon1")
        
    elif climate == hailcsv:
        TimeH = "Time"
        Size = "Size"
        LocationH = "Location"
        CountyH = "County"
        StateH = "State"
        LatH = "Lat"
        LonH = "Lon"
        CommentsH = "Comments"
        wizard = "warlock"
        
        Time2 = header.index("Time")
        F_Scale2 = header.index("Size")
        Location2 = header.index("Location")
        County2 = header.index("County")
        State2 = header.index("State")
        Lat2 = header.index("Lat")
        Lon2 = header.index("Lon")
        Comments2 = header.index("Comments")
        Oz(filenameT, fullpath, TimeH, Size, LocationH, CountyH, StateH, LatH, LonH, CommentsH)
        print ("oz2")
        Avalon(csvreader, fullpath, TimeH, Size, LocationH, CountyH, StateH, LatH, LonH, CommentsH, wizard)
        print("Avalon2")
        
    elif climate == windcsv:
        TimeW = "Time"
        Speed = "Speed"
        LocationW = "Location"
        CountyW = "County"
        StateW = "State"
        LatW = "Lat"
        LonW = "Lon"
        CommentsW = "Comments"
        wizard = "mage"

        Time3 = header.index("Time")
        F_Scale3 = header.index("Speed")
        Location3 = header.index("Location")
        County3 = header.index("County")
        State3 = header.index("State")
        Lat3 = header.index("Lat")
        Lon3 = header.index("Lon")
        Comments3 = header.index("Comments")
        Oz(filenameT, fullpath, TimeW, Speed, LocationW, CountyW, StateW, LatW, LonW, CommentsW)
        print("oz complete")
        Avalon(csvreader, fullpath, TimeW, Speed, LocationW, CountyW, StateW, LatW, LonW, CommentsW, wizard)
        print("Avalon complete")
    newreader.close

    #clip, calculate, copy without date
    arcpy.analysis.Clip(fullpath, boundary, fullpathclip, None)
    print('clip complete')
    SPC_fields = arcpy.ListFields(fullpathclip)
    time_expr = '"{}"'.format(dytextdate)
    arcpy.management.CalculateField(boundary, 'Date', time_expr, 'PYTHON3')
    arcpy.management.CalculateField(fullpathclip, 'Date', time_expr, 'PYTHON3')
    arcpy.management.CalculateField(fullpath, 'Date', time_expr, 'PYTHON3')
    arcpy.MakeFeatureLayer_management(fullpathclip, "myfeatures")
    result = arcpy.GetCount_management("myfeatures")
    result_expr = '"{}"'.format(result)
    arcpy.management.CalculateField(fullpathclip, 'Count', result_expr, 'PYTHON3')
    print('field calculations complete')
    arcpy.Copy_management(fullpath, branchT)
    arcpy.Copy_management(fullpathclip, branchTclip)
    print('copy for presentation in map')

#printing out stormreport map
maploc = placeholder_spot + '\StormReport_v2.aprx'
stormproject = arcpy.mp.ArcGISProject(maploc)
storm_report_map = stormproject.listLayouts("Storm_Report_Map*")[0]
PNG_date = 'Storm_Report_' + timestr + '.png'
PNG_spot = placeholder_spot + '\StormReport_pdf' + '\\' + PNG_date
storm_report_map.exportToPNG(PNG_spot, resolution = 600)
print('Map has successfully printed.')
print ('%s total seconds' % (time.time() - begin_time))














    
