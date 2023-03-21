# -*- coding: utf-8 -*-
"""
Desc: merge soil info, clm5 output and clim forcing for output dataframes
Created on 28.11.22 15:45
@author: malle
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os
import glob
import xarray as xr

bf_all = Path('/home/storage/malle/PTCLM5_output/new_runs')
out_all = Path('/home/storage/malle/PTCLM5_output/new_runs_df')
bf_all_met = Path('/home/storage/malle/PTCLM5_input/new_runs')

hab_in = ['S6', 'R4', 'S2', 'R3', 'T3', 'T1']

for hab in hab_in:
    print(hab)
    bf = bf_all / hab

    locations = [x for x in bf.iterdir() if x.is_dir()]
    locations1 = os.listdir(bf)

    # start with CLM5 output:
    # open 1 file to initialize our dataframe
    file_monthly = xr.open_dataset(glob.glob(str(locations[0]) + '/*.clm2.h1.1979-02-01-00000.nc')[0])
    file_monthly['FSDS_subcanopy'] = file_monthly['ftdd']*file_monthly['FSDSVD']+file_monthly['ftid'] * \
                                file_monthly['FSDSVD']+file_monthly['ftii']*file_monthly['FSDSVI']

    keys_all = list(file_monthly.keys())
    keys_sel = ['RH2M', 'TV', 'FSH_G', 'FSH_V', 'TSOI_10CM', 'FSDS_subcanopy', 'SOILWATER_10CM',
                'H2OSNO', 'FPSN', 'EFLX_LH_TOT']

    rows = [np.empty(len(keys_sel)) * np.nan for i in locations1]
    df_avg = pd.DataFrame(rows, columns=keys_sel)
    df_avg.index = locations1

    df_min = pd.DataFrame(rows, columns=keys_sel)
    df_min.index = locations1

    df_max = pd.DataFrame(rows, columns=keys_sel)
    df_max.index = locations1

    df_std = pd.DataFrame(rows, columns=keys_sel)
    df_std.index = locations1

    for loc_in in locations1:

        if len(glob.glob(str(bf / loc_in) + '/*.h0.*')) == 8:
            file_monthly = xr.open_dataset(glob.glob(str(bf / loc_in) + '/*.clm2.h1.1979-02-01-00000.nc')[0])
            file_monthly['FSDS_subcanopy'] = file_monthly['ftdd'] * file_monthly['FSDSVD'] + file_monthly['ftid'] * \
                                             file_monthly['FSDSVD'] + file_monthly['ftii'] * file_monthly['FSDSVI']
            for key in keys_sel:
                df_avg[key][loc_in] = np.mean(file_monthly[key])
                df_min[key][loc_in] = np.min(file_monthly[key])
                df_max[key][loc_in] = np.max(file_monthly[key])
                df_std[key][loc_in] = np.std(file_monthly[key])
        else:
            for key in keys_sel:
                df_avg[key][loc_in] = np.nan
                df_min[key][loc_in] = np.nan
                df_max[key][loc_in] = np.nan
                df_std[key][loc_in] = np.nan

    filepath_out = out_all / hab
    filepath_out.mkdir(parents=True, exist_ok=True)

    df_avg.to_csv(filepath_out / Path('EVA_avg_monthly_'+hab+'.csv'))
    df_min.to_csv(filepath_out / Path('EVA_min_monthly_'+hab+'.csv'))
    df_max.to_csv(filepath_out / Path('EVA_max_monthly_'+hab+'.csv'))
    df_std.to_csv(filepath_out / Path('EVA_std_monthly_'+hab+'.csv'))

    print('Done with saving monthly... now onto dailies')

    # now do the same with daily:
    rows = [np.empty(len(keys_sel)) * np.nan for i in locations1]
    df_avg = pd.DataFrame(rows, columns=keys_sel)
    df_avg.index = locations1

    df_min = pd.DataFrame(rows, columns=keys_sel)
    df_min.index = locations1

    df_max = pd.DataFrame(rows, columns=keys_sel)
    df_max.index = locations1

    df_std = pd.DataFrame(rows, columns=keys_sel)
    df_std.index = locations1

    for loc_in in locations1:
        if len(glob.glob(str(bf / loc_in) + '/*.h0.*')) == 8:
            files_daily = xr.open_mfdataset(glob.glob(str(bf / loc_in) + '/*.h0.*'))
            files_daily['FSDS_subcanopy'] = files_daily['ftdd'] * files_daily['FSDSVD'] + files_daily['ftid'] * \
                                        files_daily['FSDSVD'] + files_daily['ftii'] * files_daily['FSDSVI']
            for key in keys_sel:
                df_avg[key][loc_in] = np.mean(files_daily[key].values)
                df_min[key][loc_in] = np.min(files_daily[key].values)
                df_max[key][loc_in] = np.max(files_daily[key].values)
                df_std[key][loc_in] = np.std(files_daily[key].values)

        else:
            for key in keys_sel:
                df_avg[key][loc_in] = np.nan
                df_min[key][loc_in] = np.nan
                df_max[key][loc_in] = np.nan
                df_std[key][loc_in] = np.nan

    df_avg.to_csv(filepath_out / Path('EVA_avg_daily_'+hab+'.csv'))
    df_min.to_csv(filepath_out / Path('EVA_min_daily_'+hab+'.csv'))
    df_max.to_csv(filepath_out / Path('EVA_max_daily_'+hab+'.csv'))
    df_std.to_csv(filepath_out / Path('EVA_std_daily_'+hab+'.csv'))

    # now clim variables:
    bf = bf_all_met / hab / 'combined_nc'
    bf_dat = bf_all / hab
    locations = [x for x in bf.iterdir() if x.is_dir()]
    locations1 = os.listdir(bf_dat)

    # open 1 file to initialize our dataframe
    file_monthly = xr.open_dataset(locations[0] / 'CLM5_forcing_1980.nc')
    keys_all = list(file_monthly.keys())
    keys_to_remove = ['LONGXY', 'LATIXY', 'EDGEN', 'EDGES', 'EDGEE', 'EDGEW', 'ZBOT']
    keys_sel = [i for i in keys_all if i not in keys_to_remove]

    rows = [np.empty(len(keys_sel)) * np.nan for i in locations1]
    df_avg = pd.DataFrame(rows, columns=keys_sel)
    df_avg.index = locations1

    df_min = pd.DataFrame(rows, columns=keys_sel)
    df_min.index = locations1

    df_max = pd.DataFrame(rows, columns=keys_sel)
    df_max.index = locations1

    df_std = pd.DataFrame(rows, columns=keys_sel)
    df_std.index = locations1

    for loc_in in locations1:
        files_daily = xr.open_mfdataset(glob.glob(str(bf / loc_in) + '/*.nc'))
        for key in keys_sel:
            df_avg[key][loc_in] = np.mean(files_daily[key].values)
            df_min[key][loc_in] = np.min(files_daily[key].values)
            df_max[key][loc_in] = np.max(files_daily[key].values)
            df_std[key][loc_in] = np.std(files_daily[key].values)

    filepath_out = out_all / hab
    filepath_out.mkdir(parents=True, exist_ok=True)

    df_avg.to_csv(filepath_out / Path('MET_EVA_avg_daily_'+hab+'.csv'))
    df_min.to_csv(filepath_out / Path('MET_EVA_min_daily_'+hab+'.csv'))
    df_max.to_csv(filepath_out / Path('MET_EVA_max_daily_'+hab+'.csv'))
    df_std.to_csv(filepath_out / Path('MET_EVA_std_daily_'+hab+'.csv'))


# now combine all...
# only select sites which are included in the new EVA request:
bf_eva = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_cleaned/EVA.172/cleaned.eva')
all_data_sr_1 = pd.read_csv(bf_eva / 'vpl.csv')
all_data_sr_2 = pd.read_csv(bf_eva / 'vpl_add_on.csv')
all_data_sr = pd.concat([all_data_sr_1, all_data_sr_2])
all_data_sr.to_csv(bf_eva / 'vpl_all.csv')

all_data_hea_1 = pd.read_csv(bf_eva / 'hea.csv')
all_data_hea_2 = pd.read_csv(bf_eva / 'hea_add_on.csv')
all_data_hea = pd.concat([all_data_hea_1, all_data_hea_2])
all_data_hea.to_csv(bf_eva / 'hea_all.csv')

bf_all = Path('/home/storage/malle/PTCLM5_input/new_runs')
bf_prev = Path('/home/storage/malle/PTCLM5_input/previous_runs')

out_all = Path('/home/storage/malle/PTCLM5_output/new_runs_df')

bf_dat_all = Path('/home/storage/malle/PTCLM5_output/new_runs')

hab_in = ['S6', 'R4', 'S2', 'R3', 'T3', 'T1']

for hab in hab_in:
    print(hab)
    bf_out = out_all / hab

    # calculate sr indices:
    file_sr_out = bf_out / 'sr_area_lat_lon.csv'
    if file_sr_out.is_file():
        pass
    else:
        data_out = pd.read_csv(out_all / hab / Path('EVA_avg_monthly_'+hab+'.csv'))
        plot_id = data_out['Unnamed: 0']

        sel_sites = all_data_sr[all_data_sr['plot_id'].isin(plot_id)]
        sel_sites.set_index('plot_id', inplace=True, drop=False)

        hea_sel = all_data_hea[all_data_hea['plot_id'].isin(plot_id)]

        rel_area = hea_sel[['plot_id', 'plot_size', 'Latitude', 'Longitude']]
        rel_area.set_index('plot_id', inplace=True, drop=False)

        rel_area1 = rel_area.rename({'plot_id': 'plot_ID'}, axis=1)  # new method

        sr = sel_sites["plot_id"].value_counts(sort=False)
        all_in = pd.concat([rel_area1, sr], axis=1)
        all_in.rename({'plot_id': 'SR'}, axis=1, inplace=True)  # new method

        all_in.to_csv(file_sr_out, index=False)

    file_sr = pd.read_csv(file_sr_out)
    file_sr.set_index('plot_ID', inplace=True, drop=False)

    clm5_in = pd.read_csv(glob.glob(str(bf_out) + '/EVA_avg_daily_*')[0])
    clm5_in.set_index('Unnamed: 0', inplace=True, drop=True)

    met_in = pd.read_csv(glob.glob(str(bf_out) + '/MET_EVA_avg_daily_*')[0])
    met_in.set_index('Unnamed: 0', inplace=True, drop=True)

    # load other variables:
    bf_soil1 = bf_all / hab / 'soil_stuff'
    bf_soil2 = bf_prev / hab / 'soil_stuff'
    bf_soil3 = bf_all / hab / 'soil_stuff' / 'add_on'

    nit_in1 = pd.read_csv(bf_soil1 / 'nitrogen.csv')
    nit_in2 = pd.read_csv(bf_soil2 / 'nitrogen.csv')
    if hab != 'S6':
        nit_in3 = pd.read_csv(bf_soil3 / 'nitrogen.csv')
        nit_in = pd.concat([nit_in1, nit_in2, nit_in3])
    else:
        nit_in = pd.concat([nit_in1, nit_in2])
    nit_in.set_index('PlotID', inplace=True, drop=True)

    phh2o_in1 = pd.read_csv(bf_soil1 / 'phh2o.csv')
    phh2o_in2 = pd.read_csv(bf_soil2 / 'phh2o.csv')
    if hab != 'S6':
        phh2o_in3 = pd.read_csv(bf_soil3 / 'phh2o.csv')
        phh2o_in = pd.concat([phh2o_in1, phh2o_in2, phh2o_in3])
    else:
        phh2o_in = pd.concat([phh2o_in1, phh2o_in2])
    phh2o_in.set_index('PlotID', inplace=True, drop=True)

    soc_in1 = pd.read_csv(bf_soil1 / 'soc.csv')
    soc_in2 = pd.read_csv(bf_soil2 / 'soc.csv')
    if hab != 'S6':
        soc_in3 = pd.read_csv(bf_soil3 / 'soc.csv')
        soc_in = pd.concat([soc_in1, soc_in2, soc_in3])
    else:
        soc_in = pd.concat([soc_in1, soc_in2])
    soc_in.set_index('PlotID', inplace=True, drop=True)

    cec_in1 = pd.read_csv(bf_soil1 / 'cec.csv')
    cec_in2 = pd.read_csv(bf_soil2 / 'cec.csv')
    if hab != 'S6':
        cec_in3 = pd.read_csv(bf_soil3 / 'cec.csv')
        cec_in = pd.concat([cec_in1, cec_in2, cec_in3])
    else:
        cec_in = pd.concat([cec_in1, cec_in2])
    cec_in.set_index('PlotID', inplace=True, drop=True)

    all_in = pd.concat([file_sr, clm5_in, met_in[['TBOT', 'FSDS', 'PRECTmms', 'FLDS']], cec_in['cec [mmol(c)/kg]'],
                        soc_in['soc [dg/kg]'], phh2o_in['phh2o [pH]'], nit_in['nitrogen [cg/kg]']], axis=1)
    all_in2 = all_in.drop(clm5_in[clm5_in.EFLX_LH_TOT.isna()].index)
    all_in_filtered_new = all_in2[~np.isnan(all_in2.EFLX_LH_TOT)]

    bf_out_fin = bf_out / 'final_df'
    bf_out_fin.mkdir(parents=True, exist_ok=True)

    name_out = bf_out_fin / Path('EVA_CLM5_avg_'+hab+'.csv')
    all_in_filtered_new.to_csv(name_out, index=False)

    # now max
    met_in = pd.read_csv(glob.glob(str(bf_out) + '/MET_EVA_max_daily_*')[0])
    met_in.set_index('Unnamed: 0', inplace=True, drop=True)

    clm5_in = pd.read_csv(glob.glob(str(bf_out) + '/EVA_max_daily_*')[0])
    clm5_in.set_index('Unnamed: 0', inplace=True, drop=True)

    all_in = pd.concat([file_sr, clm5_in, met_in[['TBOT', 'FSDS', 'PRECTmms', 'FLDS']]], axis=1)
    all_in2 = all_in.drop(clm5_in[clm5_in.EFLX_LH_TOT.isna()].index)
    all_in_filtered_new = all_in2[~np.isnan(all_in2.EFLX_LH_TOT)]
    name_out = bf_out_fin / Path('EVA_CLM5_max_'+hab+'.csv')
    all_in_filtered_new.to_csv(name_out, index=False)

    # now min
    met_in = pd.read_csv(glob.glob(str(bf_out) + '/MET_EVA_min_daily_*')[0])
    met_in.set_index('Unnamed: 0', inplace=True, drop=True)

    clm5_in = pd.read_csv(glob.glob(str(bf_out) + '/EVA_min_daily_*')[0])
    clm5_in.set_index('Unnamed: 0', inplace=True, drop=True)

    all_in = pd.concat([file_sr, clm5_in, met_in[['TBOT', 'FSDS', 'PRECTmms', 'FLDS']]], axis=1)
    all_in2 = all_in.drop(clm5_in[clm5_in.EFLX_LH_TOT.isna()].index)
    all_in_filtered_new = all_in2[~np.isnan(all_in2.EFLX_LH_TOT)]
    all_in_filtered_new.to_csv(bf_out / 'EVA_grass_r3_min.csv', index=False)

    name_out = bf_out_fin / Path('EVA_CLM5_min_'+hab+'.csv')
    all_in_filtered_new.to_csv(name_out, index=False)

    # now std
    met_in = pd.read_csv(glob.glob(str(bf_out) + '/MET_EVA_std_daily_*')[0])
    met_in.set_index('Unnamed: 0', inplace=True, drop=True)

    clm5_in = pd.read_csv(glob.glob(str(bf_out) + '/EVA_std_daily_*')[0])
    clm5_in.set_index('Unnamed: 0', inplace=True, drop=True)

    all_in = pd.concat([file_sr, clm5_in, met_in[['TBOT', 'FSDS', 'PRECTmms', 'FLDS']]], axis=1)
    all_in2 = all_in.drop(clm5_in[clm5_in.EFLX_LH_TOT.isna()].index)
    all_in_filtered_new = all_in2[~np.isnan(all_in2.EFLX_LH_TOT)]

    name_out = bf_out_fin / Path('EVA_CLM5_std_'+hab+'.csv')
    all_in_filtered_new.to_csv(name_out, index=False)
