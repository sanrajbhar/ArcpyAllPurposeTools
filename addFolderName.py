#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sri00571
#
# Created:     06/03/2018
# Copyright:   (c) sri00571 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import arcpy, os
import sys


######
#Unsure if OP wants full directory path, or just the name of the folder. If just the name is desired, replace dirname = os.path.dirname(fc) with dirname = os.path.basename(os.path.dirname(fc)). ?
##
# The input (base) directory
workspace = arcpy.GetParameterAsText(0)
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True


# Generate an empty list, which will be populated with walk below
fcs = []

# Walk through all directories and directories and list all feature classes
walk = arcpy.da.Walk(workspace, datatype="FeatureClass")
for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        fcs.append(os.path.join(dirpath, filename))

# Loop through the fcs list, add field and add the directory name
for fc in fcs:

    addedName = os.path.dirname(fc).split("\\")[-1]
    arcpy.AddMessage("processing {0} in {1} with {2}".format(os.path.basename(fc), os.path.dirname(fc),addedName))
    arcpy.AddField_management(fc, field_name = "folder", field_type = "TEXT", field_length = 250)
    dirname = os.path.basename(os.path.dirname(fc))
    with arcpy.da.UpdateCursor(fc, "folder") as cursor:
        for row in cursor:
            row[0] = dirname
            print row
            cursor.updateRow(row)
