#-------------------------------------------------------------------------------
# Name:        module1
# Purpose: Recruisvely get all the FCs, Fcs in Datsets within GDB, with spatial referece, FeatureType, feaureCount.
#
# Author:      Sanjaykumar Rajbhar/GEC -Mumbai
#
# Created:     06/08/2017
# Copyright:   (c) DELL 2017
# Licence:     <your licence>
# Remark:	change your gdb name arcpy.env.workspace = ws = <Your Path to GDB>/ check Out.txt in same director

#-------------------------------------------------------------------------------
import arcpy,os
import csv

arcpy.env.overwriteOutput = True

def listFcsInGDB(gdb):
    ''' list all Feature Classes in a geodatabase, including inside Feature Datasets '''
    arcpy.env.workspace = gdb
    print 'Processing ', arcpy.env.workspace

    fcs = []
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            #yield os.path.join(fds, fc)
            fcs.append(os.path.join(fds, fc))
    return fcs

#Chnage this parameter to work- Set GDB path

arcpy.env.workspace = ws = arcpy.GetParameterAsText(0)

fcs = listFcsInGDB(ws)

projectname = arcpy.GetParameterAsText(1)

with open(projectname + "_SummeryReport.txt", "w") as SummeryReport, open(projectname + "_AttrbuteCompletness.txt", "w") as AttrbuteCompletness:
    SummeryReport.write("FC,SRC system,GeometryType,TotalCount \n")
    AttrbuteCompletness.write("FC,SRC system,GeometryType,TotalCount,NotnullCount\n")
    for fc in fcs:

       desc = arcpy.Describe(os.path.join(ws,fc))
       result = arcpy.GetCount_management(fc)
       Tcount = int(result.getOutput(0))



       fields = arcpy.ListFields(fc)
       for field in fields:
            Fname= field.name
            cur = arcpy.da.SearchCursor(fc)
            NotnullCount = 0
            for row in cur:
                if ('OBJECTID','SHAPE','SHAPE_Length','SHAPE_Area' ) not in Fname  and not row.getValue(Fname) in [None, " ", "",0]:
                    NotnullCount += 1
                arcpy.AddMessage ("-{},{},{},{}\n".format(fc.encode('utf-8'),Fname,str(Tcount),str(NotnullCount)))
                AttrbuteCompletness.write("{},{},{},{}\n".format(fc.encode('utf-8'),Fname,str(Tcount),str(NotnullCount)))
            arcpy.AddMessage("**Done Attribute compleness report")

       arcpy.AddMessage ("-{},{},{},{}\n".format(fc.encode('utf-8'), desc.spatialReference.name , desc.shapeType,Tcount))
       SummeryReport.write ("{},{},{},{}\n".format(fc.encode('utf-8'),desc.spatialReference.name , desc.shapeType, Tcount) )
       arcpy.AddMessage("**Done SummeryReport")




