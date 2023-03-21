#!/bin/sh

source activate /home/malle/miniconda3/envs/SetUp_sites_jm2

cd /home/lud11/malle/PTCLM5/soil_grids_tiles_europe/larger_extent

BOUNDS="-118875 8530326 6844969 2820165"  # ulx uly lrx lry
CELL_SIZE="250 250"

IGH="+proj=igh +lat_0=0 +lon_0=0 +datum=WGS84 +units=m +no_defs" # proj string for Homolosine projection
SG_URL="/vsicurl?max_retry=3&retry_delay=1&list_dir=no&url=https://files.isric.org/soilgrids/latest/data"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/silt/silt_0-5cm_mean.vrt" \
    "silt_0-5cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/silt/silt_5-15cm_mean.vrt" \
    "silt_5-15cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/silt/silt_15-30cm_mean.vrt" \
    "silt_15-30cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/silt/silt_30-60cm_mean.vrt" \
    "silt_30-60cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/silt/silt_60-100cm_mean.vrt" \
    "silt_60-100cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/sand/sand_0-5cm_mean.vrt" \
    "sand_0-5cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/sand/sand_5-15cm_mean.vrt" \
    "sand_5-15cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/sand/sand_15-30cm_mean.vrt" \
    "sand_15-30cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/sand/sand_30-60cm_mean.vrt" \
    "sand_30-60cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/sand/sand_60-100cm_mean.vrt" \
    "sand_60-100cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/clay/clay_0-5cm_mean.vrt" \
    "clay_0-5cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/clay/clay_5-15cm_mean.vrt" \
    "clay_5-15cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/clay/clay_15-30cm_mean.vrt" \
    "clay_15-30cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/clay/clay_30-60cm_mean.vrt" \
    "clay_30-60cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/clay/clay_60-100cm_mean.vrt" \
    "clay_60-100cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/cec/cec_0-5cm_mean.vrt" \
    "cec_0-5cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/cec/cec_5-15cm_mean.vrt" \
    "cec_5-15cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/cec/cec_15-30cm_mean.vrt" \
    "cec_15-30cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/nitrogen/nitrogen_0-5cm_mean.vrt" \
    "nitrogen_0-5cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/nitrogen/nitrogen_5-15cm_mean.vrt" \
    "nitrogen_5-15cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/nitrogen/nitrogen_15-30cm_mean.vrt" \
    "nitrogen_15-30cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/phh2o/phh2o_0-5cm_mean.vrt" \
    "phh2o_0-5cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/phh2o/phh2o_5-15cm_mean.vrt" \
    "phh2o_5-15cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/phh2o/phh2o_15-30cm_mean.vrt" \
    "phh2o_15-30cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/soc/soc_0-5cm_mean.vrt" \
    "soc_0-5cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/soc/soc_5-15cm_mean.vrt" \
    "soc_5-15cm_mean.tif"

gdal_translate -projwin $BOUNDS -projwin_srs "$IGH" -tr $CELL_SIZE \
    -co "TILED=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "BIGTIFF=YES" \
    $SG_URL"/soc/soc_15-30cm_mean.vrt" \
    "soc_15-30cm_mean.tif"
