# -*- coding: utf-8 -*-
"""
Desc: extract canopy and soil related info from the global surfacedata file for all of our EVA point locations
Created on 14.10.22 16:31
@author: malle
"""

from pathlib import Path
import pandas as pd
import numpy as np
import xarray as xr
import csv
import rioxarray

bf_lai = Path('/home/lud11/malle/PTCLM5')
in_lai=bf_lai / 'mksrf_lai_histclm52deg005_earthstatmirca_2005.cdf5.c220228.nc'
in_soil_color = bf_lai / 'mksrf_soilcolor_histclm52deg005_earthstatmirca_2005.cdf5.c220228.nc'

bf_bed_in = Path('/home/lud11/malle/PTCLM5/soil_grids')

bf_out = Path('/home/storage/malle/PTCLM5_input/new_runs')
bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')
hab_in = ['R3', 'R4', 'S2', 'S6', 'T1', 'T3']

column_name_LAI = ["PlotID", "LAI_01", "LAI_02", "LAI_03", "LAI_04", "LAI_05", "LAI_06", "LAI_07", "LAI_08", "LAI_09",
                   "LAI_10", "LAI_11", "LAI_12"]  # The name of the columns
column_name_SAI = ["PlotID", "SAI_01", "SAI_02", "SAI_03", "SAI_04", "SAI_05", "SAI_06", "SAI_07", "SAI_08", "SAI_09",
                   "SAI_10", "SAI_11", "SAI_12"]  # The name of the columns
column_name_HTOP = ["PlotID", "HTOP_01", "HTOP_02", "HTOP_03", "HTOP_04", "HTOP_05", "HTOP_06", "HTOP_07", "HTOP_08",
                    "HTOP_09", "HTOP_10", "HTOP_11", "HTOP_12"]  # The name of the columns
column_name_HBOT = ["PlotID", "HBOT_01", "HBOT_02", "HBOT_03", "HBOT_04", "HBOT_05", "HBOT_06", "HBOT_07", "HBOT_08",
                    "HBOT_09", "HBOT_10", "HBOT_11", "HBOT_12"]  # The name of the columns
column_name_HDiff = ["PlotID", "HDiff_01", "HDiff_02", "HDiff_03", "HDiff_04", "HDiff_05", "HDiff_06", "HDiff_07",
                     "HDiff_08", "HDiff_09", "HDiff_10", "HDiff_11", "HDiff_12"]  # The name of the columns

column_name_soil = ["PlotID", "SoilColor"]
column_name_bed = ["PlotID", "Depth"]

pft_in_all = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # just calc all for all for now...

for hab in hab_in:
    print(hab)

    bf_out_hab = bf_out / hab
    bf_out_hab.mkdir(exist_ok=True, parents=True)

    bf_lai_out = bf_out_hab / 'canopy'
    bf_lai_out.mkdir(parents=True, exist_ok=True)

    bf_soil_out = bf_out_hab / 'soil_stuff'
    bf_soil_out.mkdir(parents=True, exist_ok=True)

    file_soil_color = bf_soil_out / 'soil_color.csv'
    file_bedrock = bf_soil_out / 'bedrock_depth.csv'

    eva_in = pd.read_csv(bf_hea_all / Path('sel_' + hab + '.csv'))
    coords_splot_int = list(zip(eva_in['Latitude'], eva_in['Longitude'], eva_in['plot_id']))
    coords_splot = list(zip(eva_in['Latitude'], eva_in['Longitude']))#input for haversine needs to be (lat,lon)

    #start with selection
    file_temp_in1 = xr.open_dataset(in_lai)
    file_temp_in2=file_temp_in1.assign_coords({"LON":file_temp_in1.LON,"LAT":file_temp_in1.LAT})
    file_temp_in=file_temp_in2.swap_dims({"lat": "LAT","lon":"LON"})
    data1_lin_all = file_temp_in.interp(LON=eva_in['Longitude'], LAT=eva_in['Latitude'], method="nearest")
    _, id_unique = np.unique(np.vstack((data1_lin_all['LAT'], data1_lin_all['LON'])), return_index=True, axis=1)
    data1_lin = data1_lin_all.isel(LAT=id_unique, LON=id_unique)
    del data1_lin_all
    file_temp_in1.close()

    print('done with lai selection')

    file_temp_in1 = xr.open_dataset(in_soil_color)
    file_temp_in2=file_temp_in1.assign_coords({"LON":file_temp_in1.LON,"LAT":file_temp_in1.LAT})
    file_temp_in=file_temp_in2.swap_dims({"lat": "LAT","lon":"LON"})
    data1_soil_all = file_temp_in.interp(LON=eva_in['Longitude'], LAT=eva_in['Latitude'], method="nearest")
    _, id_unique = np.unique(np.vstack((data1_soil_all['LAT'], data1_soil_all['LON'])), return_index=True, axis=1)
    data1_soil = data1_soil_all.isel(LAT=id_unique, LON=id_unique)
    del data1_soil_all
    file_temp_in1.close()

    print('done with soil color selection')

    #also depth to bedrock
    rds = rioxarray.open_rasterio(bf_bed_in / 'BDTICM_M_250m_ll.tif')

    with open(file_soil_color, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_name_soil)

    with open(file_bedrock, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_name_bed)

    for splot in coords_splot_int:
        name = splot[2]
        lat = splot[0]
        lon = splot[1]
        # print(str(name))    #map(round, data_lai_pft2.data)

        bedrock_value = rds.sel(x=lon, y=lat, method="nearest").values
        data = np.concatenate([np.array(name), bedrock_value], axis=None)
        with open(file_bedrock, 'a') as f:
            writer = csv.writer(f)  # this is the writer object
            writer.writerow(data)

        data_out_soil = data1_soil.SOIL_COLOR.sel(LON=lon,LAT=lat)
        if data_out_soil.data.size == 2:
            data = np.concatenate([np.array(name), data_out_soil.data[0]], axis=None)
        else:
            data = np.concatenate([np.array(name), data_out_soil.data], axis=None)
        with open(file_soil_color, 'a') as f:
            writer = csv.writer(f)  # this is the writer object
            writer.writerow(data)

    print('done with all soil stuff... moving in to canopy related things')

    # if hab == 'R3':
    #     pft_in_all = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # elif hab == 'R4':
    #     pft_in_all = [12,13,14]
    # elif hab == 'S2':
    #     pft_in_all = [9, 10, 11]
    # elif hab == 'S6':
    #     pft_in_all = [9, 10, 11]
    # elif hab == 'T1':
    #     pft_in_all = [3, 6, 7, 8]
    # elif hab == 'T3':
    #     pft_in_all = [1, 2, 3, 4, 5]

    for pft_in in pft_in_all:
        file_lai_out_pft2 = bf_lai_out / Path('all_lai_pft' + str(pft_in) + '.csv')
        file_sai_out_pft2 = bf_lai_out / Path('all_sai_pft'+str(pft_in)+'.csv')
        file_HTOP_out_pft2 = bf_lai_out / Path('all_HTOP_pft'+str(pft_in)+'.csv')
        file_BOT_out_pft2 = bf_lai_out / Path('all_HBOT_pft'+str(pft_in)+'.csv')
        file_Hdiff_out_pft2 = bf_lai_out / Path('all_HDiff_pft'+str(pft_in)+'.csv')
        file_Hdiff_perc_pft2 = bf_lai_out / Path('all_HDiff_perc_pft'+str(pft_in)+'.csv')


        with open(file_lai_out_pft2, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name_LAI)

        with open(file_sai_out_pft2, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name_SAI)

        with open(file_HTOP_out_pft2, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name_HTOP)

        with open(file_BOT_out_pft2, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name_HBOT)

        with open(file_Hdiff_out_pft2, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name_HDiff)

        with open(file_Hdiff_perc_pft2, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name_HDiff)

        for splot in coords_splot_int:
            name = splot[2]
            lat = splot[0]
            lon = splot[1]
            # print(str(name))    #map(round, data_lai_pft2.data)

            data_out_LAI = data1_lin.MONTHLY_LAI.sel(LON=lon, LAT=lat)
            data_out_SAI = data1_lin.MONTHLY_SAI.sel(LON=lon, LAT=lat)
            data_out_HBOT = data1_lin.MONTHLY_HEIGHT_BOT.sel(LON=lon, LAT=lat)
            data_out_HTOP = data1_lin.MONTHLY_HEIGHT_TOP.sel(LON=lon, LAT=lat)

            data_lai_pft2=data_out_LAI.sel(pft=pft_in)
            if len(data_lai_pft2) == 24:
                data = np.concatenate([np.array(name), data_lai_pft2.data[::2]], axis=None)
            else:
                data = np.concatenate([np.array(name), data_lai_pft2.data], axis=None)
            with open(file_lai_out_pft2, 'a') as f:
                writer = csv.writer(f)  # this is the writer object
                writer.writerow(data[0:13])

            data_sai_pft2 = data_out_SAI.sel(pft=pft_in)
            if len(data_sai_pft2) == 24:
                data = np.concatenate([np.array(name), data_sai_pft2.data[::2]], axis=None)
            else:
                data = np.concatenate([np.array(name), data_sai_pft2.data], axis=None)
            with open(file_sai_out_pft2, 'a') as f:
                writer = csv.writer(f)  # this is the writer object
                writer.writerow(data[0:13])

            data_htop_pft2 = data_out_HTOP.sel(pft=pft_in)
            if len(data_htop_pft2) == 24:
                data = np.concatenate([np.array(name), data_htop_pft2.data[::2]], axis=None)
            else:
                data = np.concatenate([np.array(name), data_htop_pft2.data], axis=None)
            with open(file_HTOP_out_pft2, 'a') as f:
                writer = csv.writer(f)  # this is the writer object
                writer.writerow(data[0:13])

            data_hbot_pft2 = data_out_HBOT.sel(pft=pft_in)
            if len(data_hbot_pft2) == 24:
                data = np.concatenate([np.array(name), data_hbot_pft2.data[::2]], axis=None)
            else:
                data = np.concatenate([np.array(name), data_hbot_pft2.data], axis=None)
            with open(file_BOT_out_pft2, 'a') as f:
                writer = csv.writer(f)  # this is the writer object
                writer.writerow(data[0:13])

            data_diff_pft2 = data_htop_pft2 - data_hbot_pft2
            if len(data_diff_pft2) == 24:
                data = np.concatenate([np.array(name), data_diff_pft2.data[::2]], axis=None)
            else:
                data = np.concatenate([np.array(name), data_diff_pft2.data], axis=None)
            with open(file_Hdiff_out_pft2, 'a') as f:
                writer = csv.writer(f)  # this is the writer object
                writer.writerow(data[0:13])

            data_diff_pft2_perc = ((data_htop_pft2 - data_hbot_pft2)/data_htop_pft2)*100
            if len(data_diff_pft2_perc) == 24:
                data = np.concatenate([np.array(name), data_diff_pft2_perc.data[::2]], axis=None)
            else:
                data = np.concatenate([np.array(name), data_diff_pft2_perc.data], axis=None)
            with open(file_Hdiff_perc_pft2, 'a') as f:
                writer = csv.writer(f)  # this is the writer object
                writer.writerow(data[0:13])
