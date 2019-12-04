#-------------------------------------------------------------------
# Python Script to generate Cycles soil file at crop locations
#-------------------------------------------------------------------

import re
import rasterio
import rasterio.mask
import geopandas as gpd
import numpy as np
import fiona

from rasterio.mask import mask
from shapely.geometry import mapping
from rasterio import Affine
from shapely.geometry import Point
from joblib import Parallel, delayed

#-------------------------------------------------------------------
# Inputs for function
#-------------------------------------------------------------------

user_CN = 75  #User will need to supply curve number

#Directory containing ISRIC soil raster files
in_dir  = '/location/of/ISRIC/soil/raster/layers'

#Slope Raster Dataset
slope_file = '/location/of/elevation/slope/raster/tif/file'

#Crop Raster Dataset
landuse_file = '/location/of/landuse/raster/tif/file'

#Shapefile Representing area of interest Assuming projection system is same
crop_clip_filename = '/location/of/clip/shape/file'

#-------------------------------------------------------------------
# Outputs 
#-------------------------------------------------------------------

#Location to place Cycles Soil files
cycles_output_dir = '/soil/results/created/here/'
cycles_filename = 'Cycles' #Note Lat and Lon added to file name
cycles_output_crop_raster = '/location/of/clipped/crop/raster/tif/file'
cycles_output_crop_shapefile = '/location/of/clipped/crop/shape/file'

#-------------------------------------------------------------------

print_messages = False #True

if(print_messages):
    print(in_dir)

#-------------------------------------------------------------------

with fiona.open(crop_clip_filename, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# extract the raster values values within the polygon 
with rasterio.open(landuse_file) as src:
     out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
     out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open(cycles_output_crop_raster, "w", **out_meta) as dest:
    dest.write(out_image)

src = rasterio.open(cycles_output_crop_raster)
array = src.read(1)
#print(array.shape)

row, col = np.where(array == 4)      #Crop id value equals 4
elev = np.extract(array == 4, array) #Crop id value equals 4

T1 = out_transform * Affine.translation(0.5, 0.5) # reference the pixel centre
rc2xy = lambda r, c: (c, r) * T1  

d = gpd.GeoDataFrame({'col':col,'row':row,'elev':elev})
d['x'] = d.apply(lambda row: rc2xy(row.row,row.col)[0], axis=1)
d['y'] = d.apply(lambda row: rc2xy(row.row,row.col)[1], axis=1)
d['geometry'] = d.apply(lambda row: Point(row['x'], row['y']), axis=1)
d.to_file(cycles_output_crop_shapefile, driver='ESRI Shapefile')

if(print_messages):
    print( 'Number of Crop points: ' + str(len(d))  )


#-------------------------------------------------------------------
#https://www.isric.org/projects/soil-property-maps-africa-1-km-resolution
#https://www.isric.org/projects/soil-property-maps-africa-250-m-resolution

layers = [1,2,3,4,5,6,7] 
thickness_layers = [0.05,0.10,0.15,0.30,0.30,0.40,1.00]


def Create_Cycles_Soil_File(row):

    if(print_messages):
        print( 'Point: ' + str(row[1].x) + ' ' + str(row[1].y) )

    #Point Coordinates
    lons = [row[1].x] 
    lats = [row[1].y]
    cycles_file = cycles_output_dir + cycles_filename + '_' + str(row[1].x) + '_' + str(row[1].y) + '.soil'

    f = open(cycles_file, "w")

    curve_number = user_CN 
    total_layers = len(layers)
    header = 'LAYER\tTHICK\tCLAY\tSAND\tORGANIC\tBD\tFC\tPWP\tNO3\tNH4\n'

    slope_value = -999
    with rasterio.open(slope_file) as src:
        for val in src.sample(zip(lons, lats)):
            slope_value = val[0]

    location_line = '# x = ' + str(row[1].x) + ' y = ' + str(row[1].y) + '\n'
    curve_line = 'CURVE_NUMBER ' + str(curve_number) + '\n'
    slope_line = 'SLOPE ' + str(slope_value) + '\n'
    layers_line = 'TOTAL_LAYERS ' + str(total_layers) + '\n'

    if(print_messages):
        print(location_line)
        print(curve_line)
        print(slope_line)
        print(layers_line)
        print(header)

    f.write(location_line);    
    f.write(curve_line);
    f.write(slope_line);
    f.write(layers_line);
    f.write(header);

    for layer_id in layers: 

        clay_file = in_dir + 'CLYPPT_M_sl' + str(layer_id) + '_250m.tif'
        sand_file = in_dir + 'SNDPPT_M_sl' + str(layer_id) + '_250m.tif'
        organic_file = in_dir + 'ORCDRC_M_sl' + str(layer_id) + '_250m.tif'
        bd_file = in_dir + 'BLDFIE_M_sl' + str(layer_id) + '_250m.tif'

        clay_value = -999
        with rasterio.open(clay_file) as src:
            for val in src.sample(zip(lons, lats)):
                clay_value = val[0]

        sand_value = -999
        with rasterio.open(sand_file) as src:
            for val in src.sample(zip(lons, lats)):
                sand_value = val[0]

        organic_value = -999
        with rasterio.open(organic_file) as src:
            for val in src.sample(zip(lons, lats)):
                organic_value = val[0] / 10

        bd_value = -999
        with rasterio.open(bd_file) as src:
            for val in src.sample(zip(lons, lats)):
                bd_value = val[0] / 1000.0


        thickness = thickness_layers[layer_id - 1] #Zero based
        FC = -999
        PWP = -999
        NO3 = 1
        NH4 = 1

        #LAYER THICK CLAY SAND ORGANIC BD FC PWP NO3 NH4
        line = str(layer_id) + '\t' + str(thickness) + '\t' + str(clay_value) + '\t' + str(sand_value) + '\t' + str(organic_value) + '\t' + str(bd_value) + '\t' + str(FC)+ '\t' + str(PWP)+ '\t' + str(NO3)+ '\t' + str(NH4) + '\n'
        if(print_messages):
            print(line)
        f.write(line);

    f.close()


element_information = Parallel(n_jobs=-1)(delayed(Create_Cycles_Soil_File)(row) for row in d.iterrows())



