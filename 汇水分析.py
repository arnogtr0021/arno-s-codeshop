# coding: utf-8
import arcpy
from arcpy import env
from arcpy.sa import Fill, FlowAccumulation, FlowDirection, ExtractByAttributes

work_space = arcpy.GetParameterAsText(0)

# fill
env.workspace = work_space

in_surface_raster = arcpy.GetParameterAsText(1)
arcpy.CheckOutExtension('Spatial')
out_fill = Fill(in_surface_raster)
out_fill.save('fill')

# flow direction
env.workspace = work_space

in_surface_raster = 'fill'
force_flow = ''
out_drop_raster = ''
flow_direction_type = 'D8'

arcpy.CheckOutExtension('Spatial')

out_flow_direction = FlowDirection(in_surface_raster, force_flow, out_drop_raster, flow_direction_type)
out_flow_direction.save('direction')

# flow accumulation
env.workspace = work_space

in_flow_dir_raster = 'direction'
in_weight_raster = ''
data_type = 'FLOAT'

arcpy.CheckOutExtension('Spatial')

out_flow_accumulation = FlowAccumulation(in_flow_dir_raster, in_weight_raster, data_type)
out_flow_accumulation.save('accumulation')

# extract by attributes
env.workspace = work_space

in_raster = 'accumulation'
value = arcpy.GetParameterAsText(2)
in_sql_clause = 'VALUE > ' + value

arcpy.CheckOutExtension('Spatial')

att_extract = ExtractByAttributes(in_raster, in_sql_clause)
att_extract.save('flow')

print 'Accomplished'
