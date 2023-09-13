# coding: utf-8
import arcpy, os
from arcpy import env, Raster
from arcpy.sa import Slope, Aspect, Reclassify, RemapRange, EucDistance, Plus

# Slope analysis
env.workspace = arcpy.GetParameterAsText(0)
env.extent = arcpy.GetParameterAsText(1)

inRaster = arcpy.GetParameterAsText(1)
outMeasurement = 'DEGREE'
zFactor = '1'
method = 'PLANAR'
zUnit = 'METER'

arcpy.CheckOutExtension('Spatial')

slope_analysis = Slope(inRaster, outMeasurement, zFactor, method, zUnit)
slope_analysis.save('slope_analysis')

# Aspect analysis
inRaster = arcpy.GetParameterAsText(1)
method = 'PLANAR'
zUnit = 'METER'

arcpy.CheckOutExtension('Spatial')

aspect_analysis = Aspect(inRaster, method, zUnit)
aspect_analysis.save('aspect_analysis')

# Distance analysis
env.extent = arcpy.GetParameterAsText(1)
in_source_data = arcpy.GetParameterAsText(2)
maxDistance = 5000
cell_size = 3
out_direction_size = ''

arcpy.CheckOutExtension('Spatial')

distance_analysis = EucDistance(in_source_data, maxDistance, cell_size, out_direction_size)
distance_analysis.save('distance_analysis')

# Reclassify
# height_reclassify
inRaster = arcpy.GetParameterAsText(1)
reclassField = 'VALUE'
"""
weight: 0.1
0-500m: no sensitivity (value:1)
500-800m: low sensitivity (value:2)
800-1000m: middle sensitivity (value:3)
1000-1300m: high sensitivity (value:4)
above 1300m: extremely high sensitivity (value:5)
"""
remap = RemapRange([[0, 500, 1], [500, 800, 2], [800, 1000, 3], [1000, 1300, 4], [1300, 10000, 5]])

arcpy.CheckOutExtension('Spatial')

height_reclassify = Reclassify(inRaster, reclassField, remap, 'NODATA')
height_reclassify.save('height_reclassify')

# slope_reclassify
inRaster = 'slope_analysis'
reclassField = 'VALUE'
"""
weight: 0.2
0-10 degrees: no sensitivity (value:1)
10-25 degrees: low sensitivity (value:2)
25-45 degrees: middle sensitivity (value:3)
45-60 degrees: high sensitivity (value:4)
above 60 degrees: extremely high sensitivity (value:5)
"""
remap = RemapRange([[0, 10, 1], [10, 25, 2], [25, 45, 3], [45, 60, 4], [60, 90, 5]])

arcpy.CheckOutExtension('Spatial')

slope_reclassify = Reclassify(inRaster, reclassField, remap, 'NODATA')
slope_reclassify.save('slope_reclassify')

# NDVI_reclassify
inRaster = arcpy.GetParameterAsText(2)
reclassField = "VALUE"
"""
weight: 0.3
0-0.3: no sensitivity (value:1)
0.3-0.5: low sensitivity (value:2)
below 0: high sensitivity (value:4)
above 0.5: extremely high sensitivity (value:5)
"""
remap = RemapRange([[0, 0.3, 1], [0.3, 0.5, 2], [-100, 0, 4], [0.5, 100, 5]])

arcpy.CheckOutExtension('Spatial')

ndvi_reclassify = Reclassify(inRaster, reclassField, remap, 'NODATA')
ndvi_reclassify.save('ndvi_reclassify')

# distance_reclassify
inRaster = 'distance_analysis'
reclassField = 'VALUE'
"""
over 800m range: low sensitivity (value:2)
300-800m range: middle sensitivity (value:3)
0-300m range: high sensitivity (value:4)
river system: extremely high sensitivity (value:5)
"""
remap = RemapRange([[0, 1, 5], [1, 300, 4], [300, 800, 3], [800, 5000, 2]])

arcpy.CheckOutExtension('Spatial')

distance_reclassify = Reclassify(inRaster, reclassField, remap, 'NODATA')
distance_reclassify.save('distance_reclassify')

# aspect_reclassify
inRaster = 'aspect_analysis'
reclassField = 'VALUE'
"""
plat and south: no sensitivity (value:1)
east south and west south: low sensitivity (value:2)
east and west: middle sensitivity (value:3)
east north and west north: high sensitivity (value:4)
north: extremely high sensitivity (value:5)
"""
remap = RemapRange([[-1, 0, 1], [0, 22.5, 5], [22.5, 67.5, 4], [67.5, 112.5, 3], [112.5, 157.5, 2], [157.5, 202.5, 1],
                    [202.5, 247.5, 2], [247.5, 292.5, 3], [292.5, 337.5, 4], [337.5, 360, 5]])

arcpy.CheckOutExtension('Spatial')

aspect_reclassify = Reclassify(inRaster, reclassField, remap, 'NODATA')
aspect_reclassify.save('aspect_reclassify')

# raster
inRas_1 = Raster('height_reclassify')
inRas_2 = Raster('slope_reclassify')
inRas_3 = Raster('NDVI_reclassify')
inRas_4 = Raster('distance_reclassify')
inRas_5 = Raster('aspect_reclassify')

w1 = 0.1
w2 = 0.2
w3 = 0.3
w4 = 0.3
w5 = 0.1

eco = Plus(Plus(Plus(Plus(w1 * inRas_1, w2 * inRas_2), w3 * inRas_3), w4 * inRas_4), w5 * inRas_5)
eco.save('eco')

# reclassify eco_system
inRaster = 'eco'
reclassField = 'VALUE'
remap = RemapRange([[0, 1, 1], [1, 2, 2], [2, 3, 3], [3, 4, 4], [4, 5, 5]])

arcpy.CheckOutExtension('Spatial')

eco_Reclassify = Reclassify(inRaster, reclassField, remap, 'NODATA')
eco_Reclassify.save('eco_analysis')

print 'Finished'
