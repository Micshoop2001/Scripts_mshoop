
# coding: utf-8

# In[ ]:


import arcpy
import os, sys
from arcgis.gis import GIS
import shutil
import time
from datetime import timedelta
from datetime import datetime

timestream = datetime.now() - timedelta(days= 1)
timestr = timestream.strftime("%m%d%y")

prjPath = r'E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\VectorTile_NewNDFD\VectorTile_NewNDFD.aprx'
#sd_fs_name = 'Hazard_Index48hrs_WFL1'
clean, cleaner = os.path.split(prjPath)
sd_fs_name = 'hdfd_update_WFL1'
portal = 'http://www.arcgis.com'
user = 'mshoop'
password = 'mom2468392'

shrOrg = True
shrEveryone = True
shrGroups = ''

relPath = sys.path[0]
sddraft = r'E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\WebUpdate.sddraft'
sd = r'E:\Grad_School\Archive_2\Thesis\State_Climate_Office\TCO_Automation\WebUpdate.sd'

print('Creating SD file')
arcpy.env.overwriteOutput = True
prj = arcpy.mp.ArcGISProject(prjPath)
mp = prj.listMaps()[0]


    
arcpy.mp.CreateWebLayerSDDraft(mp, sddraft, sd_fs_name, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS', '', True, True)
arcpy.StageService_server(sddraft, sd)

print('Connecting to {}'.format(portal))
gis = GIS(portal, user, password)

print('Search for original SD on portal..')
sdItem = gis.content.search('{} AND owner:{}'.format(sd_fs_name, user), item_type= 'Service Definition')[0]
print('Found SD: {}, ID: {} n Uploading and overwriting...'.format(sdItem.title, sdItem.id))
sdItem.update(data=sd)
print('Overwriting existing feature service..')
fs = sdItem.publish(overwrite=True)

if shrOrg or shrEveryone or shrGroups:
    print('Setting sharing options..')
    fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)
    
print('Finished updating: {} - ID: {}'.format(fs.title, fs.id))
    
for monsters in os.listdir(clean):
    if monsters.endswith(timestr):
        print('delete file?' + monsters)
        shutil.rmtree(monsters)

print('deleted files from yesterday')
