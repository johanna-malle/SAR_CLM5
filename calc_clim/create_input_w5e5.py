# -*- coding: utf-8 -*-
"""
Desc: fetch additional required met variables from 0.5 W5E5 data
Created on 05.10.22 13:48
@author: malle
"""

from pathlib import Path
import pandas as pd
import numpy as np
import urllib.request
import xarray as xr

bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')

bf_in = Path('/home/lud11/malle/PTCLM5/met_input/W5E5_daily')
bf_copy = Path('/home/lud11/malle/PTCLM5/met_input')

bf = Path('/home/lud11/malle/PTCLM5/met_input/W5E5_daily')
year_in_all = ['19790101-19801231', '19810101-19901231', '19910101-20001231', '20010101-20101231', '20110101-20191231']

bf_w5e5 = Path('/home/storage/malle/W5E5_global')

var_in_all = ['ps', 'hurs', 'rlds', 'sfcWind']

hab_in = ['R3', 'R4', 'S2', 'S6', 'T1', 'T3']

for var_in in var_in_all:
    print(var_in)
    for year_in in year_in_all:
        url = f'https://files.isimip.org/ISIMIP3a/SecondaryInputData/climate/atmosphere/obsclim/global/daily/' \
            f'historical/W5E5v2.0/{var_in}_W5E5v2.0_{year_in}.nc'

        w5e5_file = bf_w5e5 / var_in / Path(url.split('/')[-1])
        if w5e5_file.is_file():
            pass
        else:
            urllib.request.urlretrieve(url, w5e5_file)

        file_temp_in = xr.open_dataset(w5e5_file)

        datetimes = pd.to_datetime(file_temp_in['time'])
        day_all = datetimes.day
        month_all = datetimes.month
        year_all = datetimes.year

        if year_in == '20110101-20191231':
            year_run_range = range(2011, 2017)
        else:
            year_run_range = np.unique(year_all)

        for year_run in year_run_range:
            id_all = year_all == year_run
            print(year_run)

            time_start = datetimes[np.where(id_all)][0]
            time_end = datetimes[np.where(id_all)][-1]
            clipped_w5e5_time = file_temp_in.loc[{'time': slice(time_start, time_end)}]

            for hab in hab_in:
                print(hab)
                eva_in = pd.read_csv(bf_hea_all / Path('sel_' + hab + '.csv'))
                coords_splot_int = list(zip(eva_in['Latitude'], eva_in['Longitude'], eva_in['plot_id']))

                bf2 = Path('/home/storage/malle/PTCLM5_input/new_runs/' + hab + '/w5e5_daily')
                bf2.mkdir(parents=True, exist_ok=True)

                for splot in coords_splot_int:
                    name = splot[2]
                    lat = splot[0]
                    lon = splot[1]

                    file_out1 = bf2 / str(name) / var_in / f'{var_in}_{year_run}.csv'
                    if file_out1.is_file():
                        pass
                    else:
                        Path(bf2, str(name), var_in).mkdir(parents=True, exist_ok=True)
                        data_out = clipped_w5e5_time.interp(lon=lon, lat=lat, method="nearest")

                        df = data_out.to_dataframe()
                        df1 = df.to_csv(file_out1, columns=[var_in])
