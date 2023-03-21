# -*- coding: utf-8 -*-
"""
Desc: script to extract soilgrid data for the points of interest...
Created on 06.10.22 10:48
@author: malle
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pyproj
import csv
import rioxarray

bf_soilgrid = Path('/home/lud11/malle/PTCLM5/soil_grids_tiles_filled')

# only select sites which are included in the new EVA request:
bf_eva = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_cleaned/EVA.172/cleaned.eva')
eva_in_new = pd.read_csv(bf_eva / 'hea.csv')
eva_in_new.set_index(eva_in_new.plot_id, inplace=True)

igh = "+proj=igh +lat_0=0 +lon_0=0 +datum=WGS84 +units=m +no_defs"  # proj string for Homolosine projection
igh_proj = pyproj.CRS(igh)
wgs84 = pyproj.CRS("EPSG:4326")  # LatLon with WGS84 datum used by GPS units and Google Earth
xx, yy = pyproj.transform(wgs84, igh_proj, list(eva_in_new['Latitude']), list(eva_in_new['Longitude']))
coords_splot = list(zip(yy, xx, eva_in_new['plot_id']))  # input for haversine needs to be (lat,lon)

print(np.min(xx), np.max(xx))
print(np.min(yy), np.max(yy))

igh = "+proj=igh +lat_0=0 +lon_0=0 +datum=WGS84 +units=m +no_defs"  # proj string for Homolosine projection
igh_proj = pyproj.CRS(igh)
wgs84 = pyproj.CRS("EPSG:4326")  # LatLon with WGS84 datum used by GPS units and Google Earth

bf_out = Path('/home/storage/malle/PTCLM5_input/new_runs')
bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')
hab_in = ['R3', 'R4', 'S2', 'S6', 'T1', 'T3']

soil_list_chem = ['cec', 'phh2o', 'soc', 'nitrogen']

for hab in hab_in:
    print(hab)

    bf_out_hab = bf_out / hab
    bf_out_hab.mkdir(exist_ok=True, parents=True)

    out_soil = bf_out_hab / 'soil_stuff'
    out_soil.mkdir(parents=True, exist_ok=True)

    eva_in = pd.read_csv(bf_hea_all / Path('sel_' + hab + '.csv'))
    xx, yy = pyproj.transform(wgs84, igh_proj, list(eva_in['Latitude']), list(eva_in['Longitude']))
    coords_splot = list(zip(yy, xx, eva_in['plot_id']))  # input for haversine needs to be (lat,lon)

    for soil_info in ['clay', 'sand', 'silt', 'cec', 'phh2o', 'soc', 'nitrogen']:
        out_csv = out_soil / Path(soil_info+'.csv')
        if soil_info == 'nitrogen':  #
            column_name = ["PlotID", "0-5cm_mean [cg/kg]", "5-15cm_mean [cg/kg]", "15-30cm_mean [cg/kg]",
                           "nitrogen [cg/kg]"]
        elif soil_info == 'cec':  # bulk density
            column_name = ["PlotID", "0-5cm_mean [mmol(c)/kg]", "5-15cm_mean [mmol(c)/kg]", "15-30cm_mean [mmol(c)/kg]",
                           "cec [mmol(c)/kg]"]
        elif soil_info == 'phh2o':  # organic carbon density
            column_name = ["PlotID", "0-5cm_mean [pHx10]", "5-15cm_mean [pHx10]", "15-30cm_mean [pHx10]",
                           "phh2o [pH]"]
        elif soil_info == 'soc':   # Soil organic carbon
            column_name = ["PlotID", "0-5cm_mean [dg/kg]", "5-15cm_mean [dg/kg]", "15-30cm_mean [dg/kg]", "soc [dg/kg]"]
        elif soil_info == 'bdod':  # bulk density
            column_name = ["PlotID", "0-5cm_mean [cg/cm3]", "5-15cm_mean [cg/cm3]", "15-30cm_mean [cg/cm3]",
                           "30-60cm_mean [cg/cm3]", "60-100cm_mean [cg/cm3]"]
        elif soil_info == 'ocd':  # organic carbon density
            column_name = ["PlotID", "0-5cm_mean [g/dm3]", "5-15cm_mean [g/dm3]", "15-30cm_mean [g/dm3]",
                           "30-60cm_mean [dg/kg]", "60-100cm_mean [dg/kg]"]
        else:
            column_name = ["PlotID", "0-5cm_mean [g/kg]", "5-15cm_mean [g/kg]", "15-30cm_mean [g/kg]",
                           "30-60cm_mean [g/kg]", "60-100cm_mean [g/kg]"]

        with open(out_csv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name)

        if soil_info in soil_list_chem:
            sg_layer_all = [soil_info+'_0-5cm_mean_filled.tif', soil_info+'_5-15cm_mean_filled.tif',
                            soil_info+'_15-30cm_mean_filled.tif']
            num_col_csv = len(column_name) - 2
        else:
            sg_layer_all = [soil_info + '_0-5cm_mean_filled.tif', soil_info + '_5-15cm_mean_filled.tif',
                            soil_info + '_15-30cm_mean_filled.tif', soil_info + '_30-60cm_mean_filled.tif',
                            soil_info + '_60-100cm_mean_filled.tif']
            num_col_csv = len(column_name) - 1

        for coords in coords_splot:
            x_in = coords[1]
            y_in = coords[0]

            out_num = np.zeros(len(column_name))
            out_num[0] = coords[2]

            for num_in in range(num_col_csv):
                sg_layer = sg_layer_all[num_in]
                file_in = bf_soilgrid / Path(sg_layer)
                rds = rioxarray.open_rasterio(file_in)
                value = rds.sel(x=x_in, y=y_in, method="nearest").values
                out_num[num_in+1] = value

                if out_num[num_in + 1] == 32768:
                    print('still problems with splot_id: ' + str(coords[2]))

            if soil_info in soil_list_chem:
                if soil_info == 'phh2o':
                    out_num[4] = np.round(np.mean(out_num[1:4]), 1) / 10
                else:
                    out_num[4] = np.round(np.mean(out_num[1:4]), 2)

            with open(out_csv, 'a') as f:
                writer = csv.writer(f)  # this is the writer object
                writer.writerow(out_num)

            del out_num

        print('done with ' + soil_info)
