# -*- coding: utf-8 -*-
"""
Desc: combine w5e5 and chelsa point data to create clm5 forcing files at all locations...
Created on 11.10.22 11:21
@author: malle
"""

from pathlib import Path
import pandas as pd
import numpy as np
import xarray as xr
import netCDF4
import os
import glob
import cftime
import datetime
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import time


def datetime_to_cftime(dates, kwargs={}):
    return [
        cftime.DatetimeNoLeap(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second,
            date.microsecond,
            **kwargs)
        for date in dates
    ]


def overwrite_data(splot, bf_hab, year_test, copy_file):
    start = time.time()
    path_input_chelsa = bf_hab / 'chelsa_daily'
    path_input_w5e5 = bf_hab / 'w5e5_daily'

    outfolder = bf_hab / 'combined_nc'

    name = splot[2]
    lat = splot[0]
    lon = splot[1]

    input = xr.open_dataset(copy_file)

    outfile = outfolder / Path(str(name) + str(year_test) + '_temp.nc')
    outfile_final = outfolder / Path(str(name)) / Path('CLM5_forcing_' + str(year_test) + '.nc')
    Path(outfolder / str(name)).mkdir(parents=True, exist_ok=True)

    if outfile_final.exists():
        pass

    else:
        print('file does not exist yet... run: ' + str(year_test))

        if outfile.exists():
            outfile.unlink()
        input.to_netcdf(outfile)
        # start with general stuff
        dset = netCDF4.Dataset(outfile, 'r+')
        dset['LATIXY'][:] = lat
        dset['LONGXY'][:] = lon
        dset['EDGEN'][:] = np.ceil(lat)
        dset['EDGES'][:] = np.floor(lat)
        dset['EDGEE'][:] = np.ceil(lon)
        dset['EDGEW'][:] = np.floor(lon)
        dset.close()

        test = xr.open_dataset(outfile)
        # now overwrite data
        # first temp - get data (chelsa)
        # input temp is in Kelvin => already correct!
        temp_all = pd.concat(map(pd.read_csv, glob.glob(
            os.path.join(str(path_input_chelsa) + '/' + str(name) + '/tas/', '*' + str(year_test) + '*.csv'))),
                             ignore_index=True)

        cut_leap = temp_all.time != str(year_test) + '-02-29'
        temp_all_time = np.array(datetime_to_cftime(pd.to_datetime(temp_all[cut_leap].time.sort_values())),
                                 dtype=object)
        id_time = temp_all[cut_leap].time.sort_values().index
        if len(id_time) != 365:
            len_act = int(len(id_time) / 365)
            id_time = id_time[::len_act]
            temp_all_time = temp_all_time[::len_act]

        input2 = test.assign_coords(time_2=("time_2", temp_all_time))
        input2['TBOT_2'] = (['time_2', 'lat', 'lon'], temp_all.tas.values[id_time].reshape(365, 1, 1))
        input2.TBOT_2.attrs = {'long_name': input.TBOT.attrs['long_name'], 'units': input.TBOT.attrs['units'],
                               'mode': input.TBOT.attrs['mode']}

        # precip (chelsa)
        p_all = pd.concat(map(pd.read_csv, glob.glob(
            os.path.join(str(path_input_chelsa) + '/' + str(name) + '/pr/', '*' + str(year_test) + '*.csv'))),
                          ignore_index=True)
        cut_leap = p_all.time != str(year_test) + '-02-29'
        # input precip from chelsa is in kg m-2 s-1
        # 1 kg rain over 1 m2 => 1 mm .. / s => already correct units!
        id_time = p_all[cut_leap].time.sort_values().index
        if len(id_time) != 365:
            len_act = int(len(id_time) / 365)
            id_time = id_time[::len_act]

        input2['PRECTmms_2'] = (['time_2', 'lat', 'lon'], p_all.pr.values[id_time].reshape(365, 1, 1))
        input2.PRECTmms_2.attrs = {'long_name': input.PRECTmms.attrs['long_name'],
                                   'units': input.PRECTmms.attrs['units'], 'mode': input.PRECTmms.attrs['mode']}

        # pressure (w5e5)
        pr_all = pd.concat(map(pd.read_csv, glob.glob(
            os.path.join(str(path_input_w5e5) + '/' + str(name) + '/ps/', '*' + str(year_test) + '.csv'))),
                           ignore_index=True)
        cut_leap = pr_all.time != str(year_test) + '-02-29'
        idx = pd.to_datetime(pr_all[cut_leap].time).dt.year == year_test
        if len(idx) != 365:
            len_act = int(len(idx) / 365)
            idx[::] = False
            idx[::len_act] = True

        # input pressure is in Pa => already correct!
        input2['PSRF_2'] = (['time_2', 'lat', 'lon'], pr_all[cut_leap].ps.values[idx].reshape(365, 1, 1))
        input2.PSRF_2.attrs = {'long_name': input.PSRF.attrs['long_name'], 'units': input.PSRF.attrs['units'],
                               'mode': input.PSRF.attrs['mode']}

        # RH (w5e5) (could also use specific humidity (huss) TBD)
        # input rh is in % => already correct!
        rh_all = pd.concat(map(pd.read_csv, glob.glob(
            os.path.join(str(path_input_w5e5) + '/' + str(name) + '/hurs/', '*' + str(year_test) + '.csv'))),
                           ignore_index=True)
        cut_leap = rh_all.time != str(year_test) + '-02-29'
        idx = pd.to_datetime(rh_all[cut_leap].time).dt.year == year_test
        if len(idx) != 365:
            len_act = int(len(idx) / 365)
            idx[::] = False
            idx[::len_act] = True

        input2['RH_2'] = (['time_2', 'lat', 'lon'], rh_all[cut_leap].hurs.values[idx].reshape(365, 1, 1))
        input2.RH_2.attrs = {'long_name': input.RH.attrs['long_name'], 'units': input.RH.attrs['units'],
                             'mode': input.RH.attrs['mode']}

        # LWR (w5e5)
        # input lwr is in w/m2 => already correct!
        lwr_all = pd.concat(map(pd.read_csv, glob.glob(
            os.path.join(str(path_input_w5e5) + '/' + str(name) + '/rlds/', '*' + str(year_test) + '.csv'))),
                            ignore_index=True)
        cut_leap = lwr_all.time != str(year_test) + '-02-29'
        idx = pd.to_datetime(lwr_all[cut_leap].time).dt.year == year_test
        if len(idx) != 365:
            len_act = int(len(idx) / 365)
            idx[::] = False
            idx[::len_act] = True

        input2['FLDS_2'] = (['time_2', 'lat', 'lon'], lwr_all[cut_leap].rlds.values[idx].reshape(365, 1, 1))
        input2.FLDS_2.attrs = {'long_name': input.FLDS.attrs['long_name'], 'units': input.FLDS.attrs['units'],
                               'mode': input.FLDS.attrs['mode']}

        # SWR (chelsa)
        # input swr is in w/m2 => already correct!
        swr_all = pd.concat(map(pd.read_csv, glob.glob(
            os.path.join(str(path_input_chelsa) + '/' + str(name) + '/rsds/', '*' + str(year_test) + '*.csv'))),
                            ignore_index=True)
        cut_leap = swr_all.time != str(year_test) + '-02-29'
        id_time = swr_all[cut_leap].time.sort_values().index
        if len(id_time) != 365:
            len_act = int(len(id_time) / 365)
            id_time = id_time[::len_act]

        input2['FSDS_2'] = (['time_2', 'lat', 'lon'], swr_all.rsds.values[id_time].reshape(365, 1, 1))
        input2.FSDS_2.attrs = {'long_name': input.FSDS.attrs['long_name'], 'units': input.FSDS.attrs['units'],
                               'mode': input.FSDS.attrs['mode']}

        # Wind (W5e5)
        # input wind is in m/s => already correct!
        wind_all = pd.concat(map(pd.read_csv, glob.glob(
            os.path.join(str(path_input_w5e5) + '/' + str(name) + '/sfcWind/', '*' + str(year_test) + '*.csv'))),
                             ignore_index=True)
        cut_leap = wind_all.time != str(year_test) + '-02-29'
        idx = pd.to_datetime(wind_all[cut_leap].time).dt.year == year_test
        if len(idx) != 365:
            len_act = int(len(idx) / 365)
            idx[::] = False
            idx[::len_act] = True

        input2['WIND_2'] = (['time_2', 'lat', 'lon'], wind_all[cut_leap].sfcWind.values[idx].reshape(365, 1, 1))
        input2.WIND_2.attrs = {'long_name': input.WIND.attrs['long_name'], 'units': input.WIND.attrs['units'],
                               'mode': input.WIND.attrs['mode']}

        # also ZBOT (observational height)
        zbot_t = wind_all[cut_leap].sfcWind.values[idx].reshape(365, 1, 1)
        zbot_t[:] = 10  # all data at 10m
        input2['ZBOT_2'] = (['time_2', 'lat', 'lon'], zbot_t)
        input2.ZBOT_2.attrs = {'long_name': input.ZBOT.attrs['long_name'], 'units': input.ZBOT.attrs['units'],
                               'mode': input.ZBOT.attrs['mode']}

        input3 = input2.drop_vars(['PRECTmms', 'TBOT', 'RH', 'PSRF', 'WIND', 'FLDS', 'FSDS', 'ZBOT'])

        input4 = input3.drop('time')
        input6 = input4.rename_vars({'time_2': 'time', 'PRECTmms_2': 'PRECTmms', 'TBOT_2': 'TBOT', 'RH_2': 'RH',
                                     'PSRF_2': 'PSRF', 'WIND_2': 'WIND', 'FLDS_2': 'FLDS', 'FSDS_2': 'FSDS',
                                     'ZBOT_2': 'ZBOT'})
        input7 = input6.rename({'time_2': 'time'})
        input7.time.attrs = {'long_name': input.time.attrs['long_name']}

        input7.attrs = {'history': 'File was created by J.Malle, PC ' + os.uname().nodename +
                                   ',created on ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'institution': 'Swiss Federal Institute for Forest, Snow and Landscape Research WSL',
                        'title': 'CLM5 input file based on W5E5 and CHELSA data'}
        input7.time.encoding = {'dtype': 'float64'}

        ref_encod = input.WIND.encoding

        input7.WIND.encoding = {'_FillValue': ref_encod['_FillValue'], 'missing_value': ref_encod['_FillValue']}
        input7.PRECTmms.encoding = {'_FillValue': ref_encod['_FillValue'], 'missing_value': ref_encod['_FillValue']}
        input7.PSRF.encoding = {'_FillValue': ref_encod['_FillValue'], 'missing_value': ref_encod['_FillValue']}
        input7.FLDS.encoding = {'_FillValue': ref_encod['_FillValue'], 'missing_value': ref_encod['_FillValue']}
        input7.FSDS.encoding = {'_FillValue': ref_encod['_FillValue'], 'missing_value': ref_encod['_FillValue']}
        input7.TBOT.encoding = {'_FillValue': ref_encod['_FillValue'], 'missing_value': ref_encod['_FillValue']}
        input7.RH.encoding = {'_FillValue': ref_encod['_FillValue'], 'missing_value': ref_encod['_FillValue']}

        input7.to_netcdf(outfile_final)
        outfile.unlink()
        del test, temp_all, temp_all_time

        end = time.time()
        print("Time Taken for 1 splot:{}".format(end - start))


if __name__ == '__main__':
    bf_copy = Path('/home/lud11/malle/PTCLM5/met_input')
    copy_file = bf_copy / 'ptclm5_2016-04_copy.nc'

    bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')

    hab_in = ['R4', 'S2', 'T1', 'T3']  # 'S6' 'R3']
    year_in_all = range(1995, 2017)  # range(1979, 2017)

    for year_in in year_in_all:
        print(year_in)
        start1 = time.time()
        for hab in hab_in:
            print(hab)
            eva_in = pd.read_csv(bf_hea_all / Path('sel_' + hab + '.csv'))
            coords_splot_int = list(zip(eva_in['Latitude'], eva_in['Longitude'], eva_in['plot_id']))
            coords_splot = list(zip(eva_in['Latitude'], eva_in['Longitude']))  # input haversine needs to be lat,lon

            bf_hab = Path('/home/storage/malle/PTCLM5_input/new_runs/' + hab)

            with ThreadPoolExecutor(max_workers=6) as executor:
                results = executor.map(
                    partial(
                        overwrite_data,
                        bf_hab=bf_hab,
                        year_test=year_in,
                        copy_file=copy_file
                    ),
                    coords_splot_int,
                )

            end1 = time.time()
            print("Time Taken for hab in year: {}".format(end1 - start1))
