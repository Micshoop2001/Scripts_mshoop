import arcpy
import os

#path_filename = r'C:\\'
homefile = r"Database Connections\GISDB06.sde"
path_filename = r"C:\mshoop\Scripts\TestScript\File_Geodatabases\mxd_pathchange"

arcpy.env.overwriteOutput = True
what = os.chdir(path_filename)
when = os.getcwd()

print('{} is the new path'.format(when))

for (dirname, dirs, files) in os.walk('.'):
    for filename in files:      
        if filename.endswith('.mxd'):
            print(filename)
            wholemxdpath = path_filename + '\\' + filename
            print(wholemxdpath)
            mxd = arcpy.mapping.MapDocument(wholemxdpath)
            layers = arcpy.mapping.ListLayers(mxd)
            print(layers)
            print('\n' + '\n')
            for layer in arcpy.mapping.ListLayers(mxd):
                if layer.isGroupLayer == True:
                    continue
                elif layer.isFeatureLayer == True:
                
                    try:
                        if 'Display10.DISPLAYADMIN.' in layer.dataSource:
                            print("{} -> {}".format(layer.name, layer.dataSource))
                            layer_DS = layer.dataSource
                            if 'Display10.DISPLAYADMIN.' in layer.name:
                                newlayer = layer.name.replace('Display10.DISPLAYADMIN.', '')
                            else:
                                newlayer = layer.name
                            
                            layer_join = 'sde.SDE.' + newlayer
                            print(layer_join)
                            print("{} workspace path  and dataset name {}".format(homefile, layer_join))
                            try:
                                layer.replaceDataSource(homefile, "SDE_WORKSPACE", layer_join)
                                print('{} replaced with {}'.format(layer_DS, homefile))
                            except:
                                print('!!!!!!!!!!!!!! {} has failed for some reason !!!!!!!!!!!!!!!!'.format(newlayer) + arcpy.GetMessages() + '\n' + '\n')
                        else:
                            continue
                    except:
                        print('!!!!!!!!!!!!!!!!!!!!if Display10.DISPLAYADMIN. in layer.dataSource: for {} not recognized!!!!!!!!!!!!!!!!!!!!!!'.format(layer)
                              + arcpy.GetMessages() + '\n' + '\n')
                else: continue
            try:
                mxd.save()
                print('save worked')
            except:
                print('save doesnt work' + arcpy.GetMessages())
            del mxd
        else:
            continue
