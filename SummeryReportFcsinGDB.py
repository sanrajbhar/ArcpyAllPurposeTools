#-------------------------------------------------------------------------------
# Name:        module1
# Purpose: Recruisvely get all the FCs, Fcs in Datsets within GDB, with spatial referece, FeatureType, feaureCount.
#
# Author:      Sanjaykumar Rajbhar/GEC -Mumbai   -----------------
#                                                     -------
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

def AttrbuteCompletness(projectname, fcs):
    with open(projectname + "_AttrbuteCompletness.txt", "w") as AttrbuteCompletness:

        AttrbuteCompletness.write("FC,SRC system,GeometryType,TotalCount,NotnullCount\n")
        for fc in fcs:

           desc = arcpy.Describe(os.path.join(ws,fc))
           result = arcpy.GetCount_management(fc)
           Tcount = int(result.getOutput(0))

           fields = arcpy.ListFields(fc)
           for field in fields:
                Fname= field.name
                if Fname not in ('OBJECTID','SHAPE','SHAPE_Length','SHAPE_Area','Shape','Shape_Length' ,'Shape_Area'):    #Put list of fiels that is not required in report- it helps in run faster
                    cur = arcpy.SearchCursor(fc)
                    NotnullCount = 0
                    for row in cur:
                        if not row.getValue(Fname) in [None, " ", "",0]:
                            NotnullCount += 1
                        arcpy.AddMessage ("-{},{},{},{}\n".format(fc.encode('utf-8'),Fname,str(Tcount),str(NotnullCount)))
                        AttrbuteCompletness.write("{},{},{},{}\n".format(fc.encode('utf-8'),Fname,str(Tcount),str(NotnullCount)))
                    #arcpy.AddMessage("**Done Attribute compleness report")


def SummeryReport(projectname, fcs):
    with open(projectname + "_SummeryReport.txt", "w") as SummeryReport:
        SummeryReport.write("FC,SRC system,GeometryType,TotalCount \n")

        for fc in fcs:

           desc = arcpy.Describe(os.path.join(ws,fc))
           result = arcpy.GetCount_management(fc)
           Tcount = int(result.getOutput(0))
           arcpy.AddMessage ("-{},{},{},{}\n".format(fc.encode('utf-8'), desc.spatialReference.name , desc.shapeType,Tcount))
           SummeryReport.write ("{},{},{},{}\n".format(fc.encode('utf-8'),desc.spatialReference.name , desc.shapeType, Tcount) )
           #arcpy.AddMessage("**Done SummeryReport")


arcpy.AddMessage("**Started SummeryReport")
SummeryReport(projectname, fcs)
arcpy.AddMessage("**-**Done SummeryReport")

arcpy.AddMessage("**Started Attribute compleness report")
AttrbuteCompletness(projectname, fcs)
arcpy.AddMessage("**-**Done Attribute compleness report")





