# -*- coding: utf-8 -*-
"""
Desc:
Created on 25.08.22 10:38
@author: malle
"""

import os
import elevation
import richdem as rd
from pathlib import Path
import pandas as pd
import numpy as np
import csv
from haversine import inverse_haversine, Direction

bf_out = Path('/home/storage/malle/PTCLM5_input/new_runs')

bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')

hab_in = ['R3', 'R4', 'S2', 'S6', 'T1', 'T3']

for hab in hab_in:
    print(hab)

    bf_out_hab = bf_out / hab
    bf_out_hab.mkdir(exist_ok=True, parents=True)
    out_csv = bf_out_hab / 'all_slopes_std.csv'

    eva_in = pd.read_csv(bf_hea_all / Path('sel_' + hab + '.csv'))
    coords_splot_int = list(zip(eva_in['Latitude'], eva_in['Longitude'], eva_in['plot_id']))
    coords_splot = list(zip(eva_in['Latitude'], eva_in['Longitude']))  # input for haversine needs to be (lat,lon)

    column_name = ["PlotID", "Slope", "STD"]  # The name of the columns
    with open(out_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_name)

    for splot in coords_splot_int:
        name = splot[2]
        lat = splot[0]
        lon = splot[1]
        in_coord = (lat, lon)

        in_west = inverse_haversine(in_coord, 0.125, Direction.WEST)
        in_east = inverse_haversine(in_coord, 0.125, Direction.EAST)
        in_north = inverse_haversine(in_coord, 0.125, Direction.NORTH)
        in_south = inverse_haversine(in_coord, 0.125, Direction.SOUTH)
        coords_bb = (in_west[1], in_south[0], in_east[1], in_north[0])

        # in_sw = inverse_haversine(in_coord, 0.25, pi * 1.25)
        # in_ne = inverse_haversine(in_coord, 0.25, pi * 0.25)
        # coords_bb = (in_sw[1],in_sw[0],in_ne[1],in_ne[0])

        dem_path = bf_out / 'out_EU1.tif'
        elevation.clip(bounds=coords_bb, output=dem_path)
        shasta_dem = rd.LoadGDAL(str(dem_path))
        os.remove(dem_path)
        slope = rd.TerrainAttribute(shasta_dem, attrib='slope_degrees')
        slope_mean = np.array(np.mean(slope))
        std_all = np.std(shasta_dem)
        data = [name, str(slope_mean), str(std_all)]

        with open(out_csv, 'a') as f:
            writer = csv.writer(f)  # this is the writer object
            writer.writerow(data)
