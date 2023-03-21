# -*- coding: utf-8 -*-
"""
Desc: output needed for domain calculations..
Created on 13.03.23 13:40
@author: malle
"""

from pathlib import Path
import pandas as pd
import numpy as np

bf_hea_all = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')

hab_in = ['R3', 'R4', 'S2', 'S6', 'T1', 'T3']

lat_all_all = []
lon_all_all = []
name_all_all = []
lon_all_all_neg = []

for hab in hab_in:
    eva_in = pd.read_csv(bf_hea_all / Path('sel_' + hab + '.csv'))
    coords_splot_int = list(zip(eva_in['Latitude'], eva_in['Longitude'], eva_in['plot_id']))

    lat_all = [str(item[0]) for item in coords_splot_int]
    lon_all = [str(item[1]) for item in coords_splot_int]
    name_all = [str(item[2]) for item in coords_splot_int]

    lon_all_num = [(item[1]) for item in coords_splot_int]  # for esmf I need neg. long sub. from 360
    a1=np.array(lon_all_num)
    lon_all_no_neg = np.where(a1<0,a1+360,a1)
    lon_all_num_no_neg = [str(item) for item in lon_all_no_neg]

    lat_all_all.extend(lat_all)
    lon_all_all.extend(lon_all_num_no_neg)
    name_all_all.extend(name_all)
    lon_all_all_neg.extend(lon_all)

print(*lat_all_all, sep='" "')
print(*lon_all_all, sep='" "')
print(*name_all_all, sep='" "')

lat_min = np.min([float(i) for i in lat_all_all])
lat_max = np.max([float(i) for i in lat_all_all])
print(lat_min,lat_max)

lon_min = np.min([float(i) for i in lon_all_all_neg])
lon_max = np.max([float(i) for i in lon_all_all_neg])

print(lon_min,lon_max)
