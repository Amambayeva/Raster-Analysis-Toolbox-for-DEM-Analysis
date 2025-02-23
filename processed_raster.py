import arcpy
import numpy as np
from arcpy.sa import *

# set workspace and use overwrite if you need to overwrite file. for us we decided to go with overwrite #because we tried many times the code, if you need this code once you can comment the 7 line
arcpy.env.workspace = r"C:\Users\Lenovo\Desktop\dataIP"
arcpy.env.overwriteOutput = True

# input raster (DEM file)
input_raster = r"C:\Users\Lenovo\Desktop\dataIP\Merge_file.tif"

# convert raster to NumPy array
raster_array = arcpy.RasterToNumPyArray(input_raster)

# apply a threshold (set values less than 100 to 0)
raster_array[raster_array < 100] = 0

# normalize the data to the range 0-1
raster_array = (raster_array - raster_array.min()) / (raster_array.max() - raster_array.min())

# get the cell size and extent from the input raster
input_raster_obj = arcpy.Raster(input_raster)
cell_size = input_raster_obj.meanCellWidth
extent = input_raster_obj.extent

# we converted again the NumPy array to a raster with the original extent and cell size
output_raster = r"C:\Users\Lenovo\Desktop\dataIP\processed_raster.tif"
output_raster_obj = arcpy.NumPyArrayToRaster(raster_array, arcpy.Point(extent.XMin, extent.YMin), cell_size, cell_size)

# get the spatial reference from the input raster
spatial_ref = input_raster_obj.spatialReference

# save the processed raster
output_raster_obj.save(output_raster)

# define the spatial reference for the output raster
arcpy.management.DefineProjection(output_raster, spatial_ref)

print(f"Processed raster saved at: {output_raster}")


#the output should looks like this:Processed raster saved at: C:\Users\Lenovo\Desktop\dataIP\processed_raster.tif
#this means your file been saved succsesfully!
