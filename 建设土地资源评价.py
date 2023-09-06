# coding: utf-8
import arcpy
from arcpy import env, Raster
from arcpy.sa import Slope, Reclassify, RemapValue, FocalStatistics, NbrRectangle

# slope analysis
env.workspace = arcpy.GetParameterAsText(0)
in_raster = arcpy.GetParameterAsText(1)
out_measurement = 'DEGREE'
z_factor = '1'
method = 'PLANAR'
z_unit = 'METER'

arcpy.CheckOutExtension('Spatial')

slope_analysis = Slope(in_raster, out_measurement, z_factor, method, z_unit)

# reclassify the slope analysis
reclass_field = 'VALUE'
remap = RemapValue([[0, 3, 5], [3, 8, 4], [8, 15, 3], [15, 25, 2], [25, 90, 1]])

arcpy.CheckOutExtension('Spatial')

slope_reclassify = Reclassify(slope_analysis, reclass_field, remap, "NODATA")
slope_reclassify.save('slope_reclassify')

# reclassify the height
remap = RemapValue([[0, 3500, 0], [3500, 5000, 1], [5000, 10000, 5]])

arcpy.CheckOutExtension('Spatial')

height_reclassify = Reclassify(in_raster, reclass_field, remap, "NODATA")
height_reclassify.save('height_reclassify')

in_raster_1 = Raster('slope_reclassify')
in_raster_2 = Raster('height_reclassify')

out_raster = in_raster_1 * 10 + in_raster_2
out_raster.save('out_raster')

# landuse

remap = RemapValue(
    [[55, 1], [51, 4], [50, 5], [45, 1], [41, 3], [40, 4], [35, 1], [31, 2], [30, 3], [25, 1], [21, 1], [20, 2],
     [15, 1], [11, 1], [10, 1]])

arcpy.CheckOutExtension('Spatial')
landuse = Reclassify(out_raster, reclass_field, remap, "NODATA")
landuse.save('landuse')

# focal statistics
neighborhood = NbrRectangle(5, 5, "cell")

arcpy.CheckOutExtension('Spatial')
focal_statistics = FocalStatistics(in_raster, neighborhood, "RANGE")
focal_statistics.save('focal_statistics')

# reclassify the focal statistics
remap = RemapValue([[0, 100, 0], [100, 200, 1], [200, 10000, 2]])

arcpy.CheckOutExtension('Spatial')
focal_statistics_reclassify = Reclassify(focal_statistics, reclass_field, remap, "NODATA")
focal_statistics_reclassify.save('focal_statistics_reclassify')

in_raster_1 = Raster('landuse')
in_raster_2 = Raster('focal_statistics_reclassify')

out_raster_1 = in_raster_1 * 10 + in_raster_2
out_raster_1.save('out_raster_1')

remap = RemapValue(
    [[52, 3], [51, 4], [50, 5], [42, 2], [41, 3], [40, 4], [32, 1], [31, 2], [30, 3], [22, 1], [21, 1], [20, 2],
     [12, 1], [11, 1], [10, 1]])

arcpy.CheckOutExtension('Spatial')
value = Reclassify(out_raster_1, reclass_field, remap, "NODATA")
value.save('value')
