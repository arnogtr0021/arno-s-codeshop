# encoding:utf-8
import arcpy
import csv

# define the coordinate system as GCS_WGS_1984
sp = arcpy.SpatialReference(4326)

# set the work path
path = r'F:\GIS\data'

# set the file name
file_name = 'point_jiangsu.shp'

# create feature class
fc = arcpy.CreateFeatureclass_management(path, file_name, "POINT", "", "", "", sp)

# add fields
arcpy.AddField_management(fc, "name", "TEXT", 50)
arcpy.AddField_management(fc, "type", "TEXT", 50)
arcpy.AddField_management(fc, "city", "TEXT", 50)
arcpy.AddField_management(fc, "longitude", "DOUBLE")
arcpy.AddField_management(fc, "latitude", "DOUBLE")

# insert cursor
cursor = arcpy.InsertCursor(fc)

# batch geoprocessing
with open(r"F:\jiangsu.csv", "rb") as f:
    reader = csv.reader(f)
    for line in reader:
        point = arcpy.Point()
        point.X = line[1]
        point.Y = line[2]
        row = cursor.newRow()
        row.shape = point
        row.setValue("name", line[0])
        row.setValue("type", line[3])
        row.setValue("city", line[4])
        row.setValue("longitude", line[1])
        row.setValue("latitude", line[2])
        cursor.insertRow(row)
