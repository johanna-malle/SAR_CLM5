# -*- coding: utf-8 -*-
"""
Desc: script to fetch CHELSA data at all selected EVA locations
Created on 10.10.22 15:16
@author: malle
"""

from pathlib import Path
import pandas as pd
import numpy as np
import urllib.request
import xarray as xr
import datetime

bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')

bf_in = Path('/home/lud11/malle/PTCLM5/met_input/W5E5_daily')
bf_copy = Path('/home/lud11/malle/PTCLM5/met_input')

hab_in = ['R3', 'R4', 'S2', 'S6', 'T1', 'T3']
year_in_all = range(1979, 2017)
month_in_all = range(1, 13)

var_in_all = ['tas', 'rsds', 'pr']

# create yearly csvs for each variable -> not very efficient but it works...
for var_in in var_in_all:
    print(var_in)
    for year_in in year_in_all:
        print(year_in)
        TSTART = datetime.datetime.now()
        for month_in in month_in_all:
            url = f'https://files.isimip.org/ISIMIP3a/SecondaryInputData/climate/atmosphere/obsclim/global/daily/' \
                  f'historical/CHELSA-W5E5v1.0/' \
                  f'chelsa-w5e5v1.0_obsclim_{var_in}_30arcsec_global_daily_{year_in}{month_in:02}.nc'
            savename = Path('/home/malle/Desktop/temp_download') / url.split('/')[-1]
            if not savename.is_file():
                urllib.request.urlretrieve(url, savename)

            file_temp_in = xr.open_dataset(savename)
            print(month_in)

            for hab in hab_in:
                print(hab)
                eva_in = pd.read_csv(bf_hea_all / Path('sel_'+hab+'.csv'))
                coords_splot_int = list(zip(eva_in['Latitude'], eva_in['Longitude'], eva_in['plot_id']))

                bf_chelsa = Path('/home/storage/malle/PTCLM5_input/new_runs/'+hab+'/chelsa_daily')
                bf_chelsa.mkdir(parents=True, exist_ok=True)

                data1_lin_all = file_temp_in.interp(lon=eva_in['Longitude'], lat=eva_in['Latitude'], method="nearest")
                _, id_unique = np.unique(np.vstack((data1_lin_all['lat'], data1_lin_all['lon'])), return_index=True,
                                         axis=1)
                data1_lin = data1_lin_all.isel(lat=id_unique, lon=id_unique)

                for splot in coords_splot_int:
                    name = splot[2]
                    lat = splot[0]
                    lon = splot[1]

                    file_out1 = bf_chelsa / str(name) / var_in / f'{var_in}_{year_in}{month_in:02}.csv'
                    Path(bf_chelsa, str(name), var_in).mkdir(parents=True, exist_ok=True)
                    if file_out1.is_file():
                        pass
                    else:
                        data_out = data1_lin.sel(lon=lon, lat=lat)
                        df = data_out.to_dataframe()
                        df1 = df.to_csv(file_out1, columns=[var_in])

            file_temp_in.close()
            savename.unlink()
        TEND1 = datetime.datetime.now()
        print(f' Saved all locations & habitats for {var_in}, year:{year_in}; took: {TEND1-TSTART} [HH:MM:SS]')
