# -*- coding: utf-8 -*-
"""
Desc: script to update clm5 surface datafile for all point locations
Created on 25.08.22 09:49
@author: malle
"""

import pandas as pd
import numpy as np
from pathlib import Path
import netCDF4
import xarray as xr

bf_in = Path('/home/malle/CLM5_install/surfdata_copy')
bf_out_all = Path('/home/malle/CLM5_install/surfdata_eva')
bf_out_all.mkdir(parents=True, exist_ok=True)

bf_data_all = Path('/home/storage/malle/PTCLM5_input/new_runs')
bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')
hab_in = ['R3', 'R4', 'S2', 'S6', 'T1', 'T3']

surf_in = bf_in / 'surfdata_942323_hist_16pfts_Irrig_CMIP6_simyr2000_c220824.nc'
input = xr.open_dataset(surf_in)

for hab in hab_in:
    print(hab)

    bf_data = bf_data_all / hab
    bf_out = bf_out_all / hab
    bf_out.mkdir(parents=True, exist_ok=True)

    eva_in = pd.read_csv(bf_hea_all / Path('sel_' + hab + '.csv'))
    eva_in.set_index(eva_in.plot_id, inplace=True)

    coords_splot_int = list(zip(eva_in['Latitude'], eva_in['Longitude'], eva_in['plot_id']))
    coords_splot = list(zip(eva_in['Latitude'], eva_in['Longitude']))  # input for haversine needs to be (lat,lon)

    # slope
    out_slope = bf_data / 'all_slopes_std.csv'
    data_slope = pd.read_csv(out_slope, sep=",", header=0, low_memory=False)

    # canopy
    bf_canopy = bf_data / 'canopy'

    out_lai_1 = bf_canopy / 'all_lai_pft1.csv'
    out_lai_2 = bf_canopy / 'all_lai_pft2.csv'
    out_lai_3 = bf_canopy / 'all_lai_pft3.csv'
    out_lai_4 = bf_canopy / 'all_lai_pft4.csv'
    out_lai_5 = bf_canopy / 'all_lai_pft5.csv'
    out_lai_6 = bf_canopy / 'all_lai_pft6.csv'
    out_lai_7 = bf_canopy / 'all_lai_pft7.csv'
    out_lai_8 = bf_canopy / 'all_lai_pft8.csv'
    out_lai_9 = bf_canopy / 'all_lai_pft9.csv'
    out_lai_10 = bf_canopy / 'all_lai_pft10.csv'
    out_lai_11 = bf_canopy / 'all_lai_pft11.csv'
    out_lai_12 = bf_canopy / 'all_lai_pft12.csv'
    out_lai_13 = bf_canopy / 'all_lai_pft13.csv'
    out_lai_14 = bf_canopy / 'all_lai_pft14.csv'

    out_sai_1 = bf_canopy / 'all_sai_pft1.csv'
    out_sai_2 = bf_canopy / 'all_sai_pft2.csv'
    out_sai_3 = bf_canopy / 'all_sai_pft3.csv'
    out_sai_4 = bf_canopy / 'all_sai_pft4.csv'
    out_sai_5 = bf_canopy / 'all_sai_pft5.csv'
    out_sai_6 = bf_canopy / 'all_sai_pft6.csv'
    out_sai_7 = bf_canopy / 'all_sai_pft7.csv'
    out_sai_8 = bf_canopy / 'all_sai_pft8.csv'
    out_sai_9 = bf_canopy / 'all_sai_pft9.csv'
    out_sai_10 = bf_canopy / 'all_sai_pft10.csv'
    out_sai_11 = bf_canopy / 'all_sai_pft11.csv'
    out_sai_12 = bf_canopy / 'all_sai_pft12.csv'
    out_sai_13 = bf_canopy / 'all_sai_pft13.csv'
    out_sai_14 = bf_canopy / 'all_sai_pft14.csv'

    out_htop_1 = bf_canopy / 'all_HTOP_pft1.csv'
    out_htop_2 = bf_canopy / 'all_HTOP_pft2.csv'
    out_htop_3 = bf_canopy / 'all_HTOP_pft3.csv'
    out_htop_4 = bf_canopy / 'all_HTOP_pft4.csv'
    out_htop_5 = bf_canopy / 'all_HTOP_pft5.csv'
    out_htop_6 = bf_canopy / 'all_HTOP_pft6.csv'
    out_htop_7 = bf_canopy / 'all_HTOP_pft7.csv'
    out_htop_8 = bf_canopy / 'all_HTOP_pft8.csv'
    out_htop_9 = bf_canopy / 'all_HTOP_pft9.csv'
    out_htop_10 = bf_canopy / 'all_HTOP_pft10.csv'
    out_htop_11 = bf_canopy / 'all_HTOP_pft11.csv'
    out_htop_12 = bf_canopy / 'all_HTOP_pft12.csv'
    out_htop_13 = bf_canopy / 'all_HTOP_pft13.csv'
    out_htop_14 = bf_canopy / 'all_HTOP_pft14.csv'

    out_bot_1 = bf_canopy / 'all_HBOT_pft1.csv'
    out_bot_2 = bf_canopy / 'all_HBOT_pft2.csv'
    out_bot_3 = bf_canopy / 'all_HBOT_pft3.csv'
    out_bot_4 = bf_canopy / 'all_HBOT_pft4.csv'
    out_bot_5 = bf_canopy / 'all_HBOT_pft5.csv'
    out_bot_6 = bf_canopy / 'all_HBOT_pft6.csv'
    out_bot_7 = bf_canopy / 'all_HBOT_pft7.csv'
    out_bot_8 = bf_canopy / 'all_HBOT_pft8.csv'
    out_bot_9 = bf_canopy / 'all_HBOT_pft9.csv'
    out_bot_10 = bf_canopy / 'all_HBOT_pft10.csv'
    out_bot_11 = bf_canopy / 'all_HBOT_pft11.csv'
    out_bot_12 = bf_canopy / 'all_HBOT_pft12.csv'
    out_bot_13 = bf_canopy / 'all_HBOT_pft13.csv'
    out_bot_14 = bf_canopy / 'all_HBOT_pft14.csv'

    data_lai1 = pd.read_csv(out_lai_1, sep=",", header=0, low_memory=False)
    data_lai2 = pd.read_csv(out_lai_2, sep=",", header=0, low_memory=False)
    data_lai3 = pd.read_csv(out_lai_3, sep=",", header=0, low_memory=False)
    data_lai4 = pd.read_csv(out_lai_4, sep=",", header=0, low_memory=False)
    data_lai5 = pd.read_csv(out_lai_5, sep=",", header=0, low_memory=False)
    data_lai6 = pd.read_csv(out_lai_6, sep=",", header=0, low_memory=False)
    data_lai7 = pd.read_csv(out_lai_7, sep=",", header=0, low_memory=False)
    data_lai8 = pd.read_csv(out_lai_8, sep=",", header=0, low_memory=False)
    data_lai9 = pd.read_csv(out_lai_9, sep=",", header=0, low_memory=False)
    data_lai10 = pd.read_csv(out_lai_10, sep=",", header=0, low_memory=False)
    data_lai11 = pd.read_csv(out_lai_11, sep=",", header=0, low_memory=False)
    data_lai12 = pd.read_csv(out_lai_12, sep=",", header=0, low_memory=False)
    data_lai13 = pd.read_csv(out_lai_13, sep=",", header=0, low_memory=False)
    data_lai14 = pd.read_csv(out_lai_14, sep=",", header=0, low_memory=False)

    data_sai1 = pd.read_csv(out_sai_1, sep=",", header=0, low_memory=False)
    data_sai2 = pd.read_csv(out_sai_2, sep=",", header=0, low_memory=False)
    data_sai3 = pd.read_csv(out_sai_3, sep=",", header=0, low_memory=False)
    data_sai4 = pd.read_csv(out_sai_4, sep=",", header=0, low_memory=False)
    data_sai5 = pd.read_csv(out_sai_5, sep=",", header=0, low_memory=False)
    data_sai6 = pd.read_csv(out_sai_6, sep=",", header=0, low_memory=False)
    data_sai7 = pd.read_csv(out_sai_7, sep=",", header=0, low_memory=False)
    data_sai8 = pd.read_csv(out_sai_8, sep=",", header=0, low_memory=False)
    data_sai9 = pd.read_csv(out_sai_9, sep=",", header=0, low_memory=False)
    data_sai10 = pd.read_csv(out_sai_10, sep=",", header=0, low_memory=False)
    data_sai11 = pd.read_csv(out_sai_11, sep=",", header=0, low_memory=False)
    data_sai12 = pd.read_csv(out_sai_12, sep=",", header=0, low_memory=False)
    data_sai13 = pd.read_csv(out_sai_13, sep=",", header=0, low_memory=False)
    data_sai14 = pd.read_csv(out_sai_14, sep=",", header=0, low_memory=False)

    data_htop1 = pd.read_csv(out_htop_1, sep=",", header=0, low_memory=False)
    data_htop2 = pd.read_csv(out_htop_2, sep=",", header=0, low_memory=False)
    data_htop3 = pd.read_csv(out_htop_3, sep=",", header=0, low_memory=False)
    data_htop4 = pd.read_csv(out_htop_4, sep=",", header=0, low_memory=False)
    data_htop5 = pd.read_csv(out_htop_5, sep=",", header=0, low_memory=False)
    data_htop6 = pd.read_csv(out_htop_6, sep=",", header=0, low_memory=False)
    data_htop7 = pd.read_csv(out_htop_7, sep=",", header=0, low_memory=False)
    data_htop8 = pd.read_csv(out_htop_8, sep=",", header=0, low_memory=False)
    data_htop9 = pd.read_csv(out_htop_9, sep=",", header=0, low_memory=False)
    data_htop10 = pd.read_csv(out_htop_10, sep=",", header=0, low_memory=False)
    data_htop11 = pd.read_csv(out_htop_11, sep=",", header=0, low_memory=False)
    data_htop12 = pd.read_csv(out_htop_12, sep=",", header=0, low_memory=False)
    data_htop13 = pd.read_csv(out_htop_13, sep=",", header=0, low_memory=False)
    data_htop14 = pd.read_csv(out_htop_14, sep=",", header=0, low_memory=False)

    data_hbot1 = pd.read_csv(out_bot_1, sep=",", header=0, low_memory=False)
    data_hbot2 = pd.read_csv(out_bot_2, sep=",", header=0, low_memory=False)
    data_hbot3 = pd.read_csv(out_bot_3, sep=",", header=0, low_memory=False)
    data_hbot4 = pd.read_csv(out_bot_4, sep=",", header=0, low_memory=False)
    data_hbot5 = pd.read_csv(out_bot_5, sep=",", header=0, low_memory=False)
    data_hbot6 = pd.read_csv(out_bot_6, sep=",", header=0, low_memory=False)
    data_hbot7 = pd.read_csv(out_bot_7, sep=",", header=0, low_memory=False)
    data_hbot8 = pd.read_csv(out_bot_8, sep=",", header=0, low_memory=False)
    data_hbot9 = pd.read_csv(out_bot_9, sep=",", header=0, low_memory=False)
    data_hbot10 = pd.read_csv(out_bot_10, sep=",", header=0, low_memory=False)
    data_hbot11 = pd.read_csv(out_bot_11, sep=",", header=0, low_memory=False)
    data_hbot12 = pd.read_csv(out_bot_12, sep=",", header=0, low_memory=False)
    data_hbot13 = pd.read_csv(out_bot_13, sep=",", header=0, low_memory=False)
    data_hbot14 = pd.read_csv(out_bot_14, sep=",", header=0, low_memory=False)

    # soil
    bf_soil = bf_data / 'soil_stuff'
    out_silt = bf_soil / 'silt.csv'
    out_sand = bf_soil / 'sand.csv'
    out_clay = bf_soil / 'clay.csv'
    out_soil_color = bf_soil / 'soil_color.csv'
    out_bedrock = bf_soil / 'bedrock_depth.csv'

    data_soil_color = pd.read_csv(out_soil_color, sep=",", header=0, low_memory=False)
    data_sand = pd.read_csv(out_sand, sep=",", header=0, low_memory=False)
    data_clay = pd.read_csv(out_clay, sep=",", header=0, low_memory=False)
    data_silt = pd.read_csv(out_silt, sep=",", header=0, low_memory=False)
    data_bedrock = pd.read_csv(out_bedrock, sep=",", header=0, low_memory=False)

    for splot in coords_splot_int:
        name = splot[2]
        lat = splot[0]
        lon = splot[1]

        slope_in = data_slope.iloc[np.where(data_slope.PlotID == name)]
        std = slope_in.STD.values

        soil_co_in = data_soil_color.iloc[np.where(data_soil_color.PlotID == name)]
        so_co = soil_co_in.SoilColor.values

        sand_in = data_sand.iloc[np.where(data_sand.PlotID == name)]
        sand_frac = np.round(sand_in.values[0, 1:]*0.1, 2)  # convert g/kg to percent
        sand_frac_layers = [sand_frac[0], sand_frac[0], sand_frac[1], sand_frac[2], sand_frac[3], sand_frac[3],
                            sand_frac[4], sand_frac[4], sand_frac[4], sand_frac[4]]
        if np.any(np.isin(sand_frac_layers, 3276.8)):
            # sand_frac_layers=input.PCT_SAND.values
            print('problem at location '+name)
        if np.any(np.isin(sand_frac_layers, -32768)):
            # sand_frac_layers=input.PCT_SAND.values
            print('problem at location ' + name)

        clay_in = data_clay.iloc[np.where(data_clay.PlotID == name)]
        clay_frac = np.round(clay_in.values[0, 1:]*0.1, 2)  # convert g/kg to percent
        clay_frac_layers = [clay_frac[0], clay_frac[0], clay_frac[1], clay_frac[2], clay_frac[3], clay_frac[3],
                            clay_frac[4], clay_frac[4], clay_frac[4], clay_frac[4]]
        if np.any(np.isin(clay_frac_layers, 3276.8)):
            # clay_frac_layers = input.PCT_CLAY.values
            print('problem at location ' + name)
        if np.any(np.isin(clay_frac_layers, -32768)):
            # sand_frac_layers=input.PCT_CLAY.values
            print('problem at location ' + name)

        zbedrock_in = data_bedrock.iloc[np.where(data_bedrock.PlotID == name)]
        zbedrock_m = zbedrock_in.values[0, 1]/100  # convert from cm to m

        # now canopy stuff again.. dumb way of doing it but since it's already there... improve later
        lai_in_pft = data_lai1.iloc[np.where(data_lai1.PlotID == name)]
        lai_1 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai1.iloc[np.where(data_sai1.PlotID == name)]
        sai_1 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot1.iloc[np.where(data_hbot1.PlotID == name)]
        hbot_1 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop1.iloc[np.where(data_htop1.PlotID == name)]
        htop_1 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai2.iloc[np.where(data_lai2.PlotID == name)]
        lai_2 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai2.iloc[np.where(data_sai2.PlotID == name)]
        sai_2 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot2.iloc[np.where(data_hbot2.PlotID == name)]
        hbot_2 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop2.iloc[np.where(data_htop2.PlotID == name)]
        htop_2 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai3.iloc[np.where(data_lai3.PlotID == name)]
        lai_3 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai3.iloc[np.where(data_sai3.PlotID == name)]
        sai_3 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot3.iloc[np.where(data_hbot3.PlotID == name)]
        hbot_3 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop3.iloc[np.where(data_htop3.PlotID == name)]
        htop_3 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai4.iloc[np.where(data_lai4.PlotID == name)]
        lai_4 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai4.iloc[np.where(data_sai4.PlotID == name)]
        sai_4 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot4.iloc[np.where(data_hbot4.PlotID == name)]
        hbot_4 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop4.iloc[np.where(data_htop4.PlotID == name)]
        htop_4 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai5.iloc[np.where(data_lai5.PlotID == name)]
        lai_5 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai5.iloc[np.where(data_sai5.PlotID == name)]
        sai_5 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot5.iloc[np.where(data_hbot5.PlotID == name)]
        hbot_5 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop5.iloc[np.where(data_htop5.PlotID == name)]
        htop_5 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai6.iloc[np.where(data_lai6.PlotID == name)]
        lai_6 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai6.iloc[np.where(data_sai6.PlotID == name)]
        sai_6 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot6.iloc[np.where(data_hbot6.PlotID == name)]
        hbot_6 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop6.iloc[np.where(data_htop6.PlotID == name)]
        htop_6 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai7.iloc[np.where(data_lai7.PlotID == name)]
        lai_7 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai7.iloc[np.where(data_sai7.PlotID == name)]
        sai_7 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot7.iloc[np.where(data_hbot7.PlotID == name)]
        hbot_7 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop7.iloc[np.where(data_htop7.PlotID == name)]
        htop_7 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai8.iloc[np.where(data_lai8.PlotID == name)]
        lai_8 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai8.iloc[np.where(data_sai8.PlotID == name)]
        sai_8 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot8.iloc[np.where(data_hbot8.PlotID == name)]
        hbot_8 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop8.iloc[np.where(data_htop8.PlotID == name)]
        htop_8 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai9.iloc[np.where(data_lai9.PlotID == name)]
        lai_9 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai9.iloc[np.where(data_sai9.PlotID == name)]
        sai_9 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot9.iloc[np.where(data_hbot9.PlotID == name)]
        hbot_9 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop9.iloc[np.where(data_htop9.PlotID == name)]
        htop_9 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai10.iloc[np.where(data_lai10.PlotID == name)]
        lai_10 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai10.iloc[np.where(data_sai10.PlotID == name)]
        sai_10 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot10.iloc[np.where(data_hbot10.PlotID == name)]
        hbot_10 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop10.iloc[np.where(data_htop10.PlotID == name)]
        htop_10 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai11.iloc[np.where(data_lai11.PlotID == name)]
        lai_11 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai11.iloc[np.where(data_sai11.PlotID == name)]
        sai_11 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot11.iloc[np.where(data_hbot11.PlotID == name)]
        hbot_11 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop11.iloc[np.where(data_htop11.PlotID == name)]
        htop_11 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai12.iloc[np.where(data_lai12.PlotID == name)]
        lai_12 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai12.iloc[np.where(data_sai12.PlotID == name)]
        sai_12 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot12.iloc[np.where(data_hbot12.PlotID == name)]
        hbot_12 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop12.iloc[np.where(data_htop12.PlotID == name)]
        htop_12 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai13.iloc[np.where(data_lai13.PlotID == name)]
        lai_13 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai13.iloc[np.where(data_sai13.PlotID == name)]
        sai_13 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot13.iloc[np.where(data_hbot13.PlotID == name)]
        hbot_13 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop13.iloc[np.where(data_htop13.PlotID == name)]
        htop_13 = htop_in_pft.values[0, 1:]

        lai_in_pft = data_lai14.iloc[np.where(data_lai14.PlotID == name)]
        lai_14 = lai_in_pft.values[0, 1:]
        sai_in_pft = data_sai14.iloc[np.where(data_sai14.PlotID == name)]
        sai_14 = sai_in_pft.values[0, 1:]
        hbot_in_pft = data_hbot14.iloc[np.where(data_hbot14.PlotID == name)]
        hbot_14 = hbot_in_pft.values[0, 1:]
        htop_in_pft = data_htop14.iloc[np.where(data_htop14.PlotID == name)]
        htop_14 = htop_in_pft.values[0, 1:]

        surf_out = bf_out / Path('surfdata_'+str(name)+'.nc')
        if surf_out.is_file():
            surf_out.unlink()
        input.to_netcdf(surf_out)

        dset = netCDF4.Dataset(surf_out, 'r+')
        dset['LATIXY'][:] = lat
        dset['LONGXY'][:] = lon
        dset['LANDFRAC_PFT'][:] = 1
        dset['PCT_NATVEG'][:] = 100
        dset['PCT_LAKE'][:] = 0
        dset['PCT_GLACIER'][:] = 0
        dset['PCT_URBAN'][:] = 0
        dset['PCT_CROP'][:] = 0
        dset['PCT_NAT_PFT'][:] = 0
        if hab == 'R3':  # update these ....
            dset['PCT_NAT_PFT'][0] = 0.7
            dset['PCT_NAT_PFT'][1] = 0.1
            dset['PCT_NAT_PFT'][7] = 0.1
            dset['PCT_NAT_PFT'][9] = 0.5
            dset['PCT_NAT_PFT'][10] = 1.4
            dset['PCT_NAT_PFT'][13] = 96.2
            dset['PCT_NAT_PFT'][14] = 1
        elif hab == 'R4':
            dset['PCT_NAT_PFT'][0] = 29.6
            dset['PCT_NAT_PFT'][1] = 0.2
            dset['PCT_NAT_PFT'][7] = 0.1
            dset['PCT_NAT_PFT'][9] = 0.3
            dset['PCT_NAT_PFT'][10] = 3.1
            dset['PCT_NAT_PFT'][12] = 66.7
        elif hab == 'S2':
            dset['PCT_NAT_PFT'][0] = 18.6
            dset['PCT_NAT_PFT'][1] = 12.8
            dset['PCT_NAT_PFT'][7] = 0.3
            dset['PCT_NAT_PFT'][9] = 2.7
            dset['PCT_NAT_PFT'][11] = 20.9
            dset['PCT_NAT_PFT'][13] = 44.7
        elif hab == 'S6':
            dset['PCT_NAT_PFT'][0] = 44.4
            dset['PCT_NAT_PFT'][1] = 0.4
            dset['PCT_NAT_PFT'][5] = 0.1
            dset['PCT_NAT_PFT'][7] = 0.1
            dset['PCT_NAT_PFT'][9] = 7.4
            dset['PCT_NAT_PFT'][10] = 11.4
            dset['PCT_NAT_PFT'][13] = 32.2
            dset['PCT_NAT_PFT'][14] = 4
        elif hab == 'T1':
            dset['PCT_NAT_PFT'][0] = 0.6
            dset['PCT_NAT_PFT'][1] = 1.3
            dset['PCT_NAT_PFT'][5] = 0.7
            dset['PCT_NAT_PFT'][7] = 39.9
            dset['PCT_NAT_PFT'][9] = 2.2
            dset['PCT_NAT_PFT'][10] = 12.7
            dset['PCT_NAT_PFT'][13] = 42.6
        elif hab == 'T3':
            dset['PCT_NAT_PFT'][0] = 6
            dset['PCT_NAT_PFT'][1] = 30.2
            dset['PCT_NAT_PFT'][3] = 2.1
            dset['PCT_NAT_PFT'][5] = 0.6
            dset['PCT_NAT_PFT'][7] = 4.5
            dset['PCT_NAT_PFT'][9] = 3.5
            dset['PCT_NAT_PFT'][10] = 11.6
            dset['PCT_NAT_PFT'][13] = 41.5
        else:
            raise ValueError("Problem... no PFT specified")

        # now more soil stuff
        dset['STD_ELEV'][:] = np.round(std, 3)

        dset['SOIL_COLOR'][:] = so_co
        dset['zbedrock'][:] = zbedrock_m
        dset['PCT_SAND'][:] = sand_frac_layers
        dset['PCT_CLAY'][:] = clay_frac_layers

        dset['MONTHLY_LAI'][:, 1] = np.round(lai_1, 3)
        dset['MONTHLY_LAI'][:, 2] = np.round(lai_2, 3)
        dset['MONTHLY_LAI'][:, 3] = np.round(lai_3, 3)
        dset['MONTHLY_LAI'][:, 4] = np.round(lai_4, 3)
        dset['MONTHLY_LAI'][:, 5] = np.round(lai_5, 3)
        dset['MONTHLY_LAI'][:, 6] = np.round(lai_6, 3)
        dset['MONTHLY_LAI'][:, 7] = np.round(lai_7, 3)
        dset['MONTHLY_LAI'][:, 8] = np.round(lai_8, 3)
        dset['MONTHLY_LAI'][:, 9] = np.round(lai_9, 3)
        dset['MONTHLY_LAI'][:, 10] = np.round(lai_10, 3)
        dset['MONTHLY_LAI'][:, 11] = np.round(lai_11, 3)
        dset['MONTHLY_LAI'][:, 12] = np.round(lai_12, 3)
        dset['MONTHLY_LAI'][:, 13] = np.round(lai_13, 3)
        dset['MONTHLY_LAI'][:, 14] = np.round(lai_14, 3)

        dset['MONTHLY_SAI'][:, 1] = np.round(sai_1, 3)
        dset['MONTHLY_SAI'][:, 2] = np.round(sai_2, 3)
        dset['MONTHLY_SAI'][:, 3] = np.round(sai_3, 3)
        dset['MONTHLY_SAI'][:, 4] = np.round(sai_4, 3)
        dset['MONTHLY_SAI'][:, 5] = np.round(sai_5, 3)
        dset['MONTHLY_SAI'][:, 6] = np.round(sai_6, 3)
        dset['MONTHLY_SAI'][:, 7] = np.round(sai_7, 3)
        dset['MONTHLY_SAI'][:, 8] = np.round(sai_8, 3)
        dset['MONTHLY_SAI'][:, 9] = np.round(sai_9, 3)
        dset['MONTHLY_SAI'][:, 10] = np.round(sai_10, 3)
        dset['MONTHLY_SAI'][:, 11] = np.round(sai_11, 3)
        dset['MONTHLY_SAI'][:, 12] = np.round(sai_12, 3)
        dset['MONTHLY_SAI'][:, 13] = np.round(sai_13, 3)
        dset['MONTHLY_SAI'][:, 14] = np.round(sai_14, 3)

        dset['MONTHLY_HEIGHT_TOP'][:, 1] = np.round(htop_1, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 2] = np.round(htop_2, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 3] = np.round(htop_3, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 4] = np.round(htop_4, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 5] = np.round(htop_5, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 6] = np.round(htop_6, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 7] = np.round(htop_7, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 8] = np.round(htop_8, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 9] = np.round(htop_9, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 10] = np.round(htop_10, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 11] = np.round(htop_11, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 12] = np.round(htop_12, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 13] = np.round(htop_13, 3)
        dset['MONTHLY_HEIGHT_TOP'][:, 14] = np.round(htop_14, 3)

        dset['MONTHLY_HEIGHT_BOT'][:, 1] = np.round(hbot_1, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 2] = np.round(hbot_2, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 3] = np.round(hbot_3, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 4] = np.round(hbot_4, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 5] = np.round(hbot_5, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 6] = np.round(hbot_6, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 7] = np.round(hbot_7, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 8] = np.round(hbot_8, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 9] = np.round(hbot_9, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 10] = np.round(hbot_10, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 11] = np.round(hbot_11, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 12] = np.round(hbot_12, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 13] = np.round(hbot_13, 3)
        dset['MONTHLY_HEIGHT_BOT'][:, 14] = np.round(hbot_14, 3)

        # dset['SLOPE'][:] = np.round(slope,3)
        dset.close()
