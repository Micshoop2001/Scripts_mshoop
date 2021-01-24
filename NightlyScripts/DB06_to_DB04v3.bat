sc \\GISDB04 stop "ArcGIS Server"
sc \\agserv stop "ArcGIS Server"

del \\ftp001\GIS\GISUSERS\Spartanburg_County_Data\*.* /F /S /Q

"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_Server_Disco_Script1_v6.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\911_Dissolve_1_v10.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\911_FieldEdit_2_v5.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\911_NameChange_3_v5.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06StrptsFields_StrCenterLFields_v3.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_ParsJ_Script2_v10.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_SJ1_APpars_Script3_v9.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_TC2_Script4_v8.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_standard_copy_Script5_v7.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_structurepts_Script6_v10.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_streetcenterlines_Script7_v9.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_parcels_Script8_v7.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_Copy_to_FTP_v4.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_indexing_Script9_v6.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_Server_Con_Script10_v8.py"
"C:\Nightly Scripts\DB6_to_DB4_scripts\DB06_to_DB04_tokenChecker_Script11_v4.py"

sc \\agserv start "ArcGIS Server"
sc \\GISDB04 start "ArcGIS Server"