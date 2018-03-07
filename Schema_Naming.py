#-------------------------------------------------------------------------------
# Name:        Creating fc's and schemas as defined in CSV's files
# Purpose:     SchemaGen.py | Arcadis | Mumbai GEC GIS | UK GIS | BimtoGIS
#
# Author:      Sanjay kumar Rajbhar | Arcadis Mumbai GEC GIS
#
# Created:     21/12/2017
# Copyright:   (c) sri00571 2017
# Licence:     <your licence>
#Version: SchemaGen_V1.py -  adeded in_memoery support for outputfeatureclass to increase processing speeds.
#
#------------------------------ -------------------------------------------------
import arcpy
import os
import re
import csv
import io
from arcpy import env
env.overwriteOutput = True
Workspace =  arcpy.GetParameterAsText(0)
env.workspace = Workspace

def replaceClean(text):
    for ch in [')','(','-','/','\\','.']:
        if ch in text:

            text = text.replace(ch,"")

    for ch in ['<']:
        if ch in text:
            text = text.replace(ch,"_LessThan_")

    for ch in ['>']:
        if ch in text:
            text = text.replace(ch,"_GreaterThan_")



    for ch in ['__']:
        if ch in text:
            text = text.replace(ch,"_")

    return text




#reading fdtocreat.csv to create feature Datasets
with open ('fdtocreat.csv', 'rb') as fdcsvfile:
    reader = csv.reader(fdcsvfile)

    listfc=map(tuple,reader)

    try:
        for f in listfc:

            inmem_fc = f[0]
            inmem_geotype = f[1]
            arcpy.CreateFeatureclass_management('in_memory','inmem_fc',inmem_geotype,'','','',27700)
            print "Creating Field for____ " + inmem_fc

            with open (inmem_fc + ".csv", 'rb') as lpolecsv:
                reader =csv.reader(lpolecsv)
                lpole_fields=map(tuple,reader)

                for field in lpole_fields:

                    print "********" + inmem_fc +' :::::: ' +replaceClean((field)[0])
                    #print field

                    arcpy.AddField_management("in_memory/inmem_fc", replaceClean((field)[0]), field[1],field[2],field[3], replaceClean((field)[4]),'','','','')

                    arcpy.FeatureClassToFeatureClass_conversion("in_memory/inmem_fc",Workspace,inmem_fc)
                arcpy.Delete_management("in_memory")
    except Exception as e:
        e = sys.exc_info()[1]
        print e
        arcpy.AddError("Error Occured")