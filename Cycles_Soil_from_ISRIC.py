import rasterio

#-------------------------------------------------------------------
# Inputs for function

#Script to generate Cycles soil file
#Point Coordinates
lons = [29.884522] #User will need to supply longitude value
lats = [7.783639]  #User will need to supply latitude value
user_CN = 75       #User will need to supply curve number

# Directory containing ISRIC soil raster files
in_dir  = '/location/of/ISRIC/soil/raster/layers'
slope_file = '/location/of/elevation/raster/file'

#-------------------------------------------------------------------
# Outputs 

# Cycles soil file
cycles_file = '/location/of/cycles_test.soil'

#-------------------------------------------------------------------

print_messages = True

if(print_messages):
    print(in_dir)

#https://www.isric.org/projects/soil-property-maps-africa-1-km-resolution
#https://www.isric.org/projects/soil-property-maps-africa-250-m-resolution

layers = [1,2,3,4,5,6,7] 
thickness_layers = [0.05,0.10,0.15,0.30,0.30,0.40,1.00]

f = open(cycles_file, "w")

curve_number = user_CN 
total_layers = len(layers)
header = 'LAYER\tTHICK\tCLAY\tSAND\tORGANIC\tBD\tFC\tPWP\tNO3\tNH4\n'

slope_value = -999
with rasterio.open(slope_file) as src:
    for val in src.sample(zip(lons, lats)):
        slope_value = val[0]



curve_line = 'CURVE_NUMBER ' + str(curve_number) + '\n'
slope_line = 'SLOPE ' + str(slope_value) + '\n'
layers_line = 'TOTAL_LAYERS ' + str(total_layers) + '\n'

if(print_messages):
    print(curve_line)
    print(slope_line)
    print(layers_line)
    print(header)

f.write(curve_line);
f.write(slope_line);
f.write(layers_line);
f.write(header);

for layer_id in layers: 

    clay_file = in_dir + 'CLYPPT_M_sl' + str(layer_id) + '_250m.tif'
    #silt_file = in_dir + 'SLTPPT_M_sl' + str(layer_id) + '_250m.tif'
    sand_file = in_dir + 'SNDPPT_M_sl' + str(layer_id) + '_250m.tif'
    organic_file = in_dir + 'ORCDRC_M_sl' + str(layer_id) + '_250m.tif'
    bd_file = in_dir + 'BLDFIE_M_sl' + str(layer_id) + '_250m.tif'

    clay_value = -999
    with rasterio.open(clay_file) as src:
        for val in src.sample(zip(lons, lats)):
            clay_value = val[0]

    #silt_value = -999
    #with rasterio.open(silt_file) as src:
    #    for val in src.sample(zip(lons, lats)):
    #        silt_value = val[0]

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