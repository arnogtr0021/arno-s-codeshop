# coding: utf-8
import arcpy
from arcpy import env
from arcpy.sa import Slope, Aspect

# work space
env.workspace = arcpy.GetParameterAsText(0)

# slope analysis
in_raster = arcpy.GetParameterAsText(1)
out_measurement = 'DEGREE'
z_factor = '1'
method = 'PLANAR'
z_unit = 'METER'

arcpy.CheckOutExtension('Spatial')

slope_analysis = Slope(in_raster, out_measurement, z_factor, method, z_unit)
slope_analysis.save('slope_analysis')

# aspect analysis
in_raster = arcpy.GetParameterAsText(1)
method = 'PLANAR'
z_unit = 'METER'

arcpy.CheckOutExtension('Spatial')

aspect_analysis = Aspect(in_raster, method, z_unit)
aspect_analysis.save('aspect_analysis')
