## Methods to create Cycles soil files using ISRIC (https://www.isric.org/) soil datasets.

## Method One [ Known Point Location ] 

### The Cycles_Soil_from_ISRIC.py python file inputs are:

1. Longitude of crop location
2. Latitude of crop location
3. A curve number
4. Input directory of ISRIC seven soil layers [ CLYPPT_M_sl, SNDPPT_M_sl, ORCDRC_M_sl, BLDFIE_M_sl]
5. Slope raster dataset

### Output:
1. Single Cycles soil file (*.soil)

## Method Two [ Using Polygon Shapefile to clip crop raster dataset ]

### The Cycles_SoilFile_WithPolygon.py python file inputs are:

1. A curve number
2. Input directory of ISRIC seven soil layers [ CLYPPT_M_sl, SNDPPT_M_sl, ORCDRC_M_sl, BLDFIE_M_sl]
3. Slope raster dataset
4. Crop raster dataset
5. Shapefile representing region of interest (i..e can be watershed, political boundary)

### Outputs:
1. Raster file of crops withing region of interest
2. Point shape file representing crops
3. Many Cycles soil files (*.soil) in specified directory


## Method Three [ Using CSV Text file with Lon and Lat values ]

### The Cycles_SoilFile_LoadCSV.py python file inputs are:

1. A curve number
2. Input directory of ISRIC seven soil layers [ CLYPPT_M_sl, SNDPPT_M_sl, ORCDRC_M_sl, BLDFIE_M_sl]
3. Slope raster dataset
4. CSV text file (with no header) with Lon and Lat values

### Outputs:
1. Many Cycles soil files (*.soil) in specified directory

