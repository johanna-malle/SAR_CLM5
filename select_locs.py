# -*- coding: utf-8 -*-
"""
Desc: script to perform selection of sites per habitat based on limits in plot size, uncertainty,
and some applied stratification
Created on 02.03.23 17:05
@author: malle
"""

import pandas as pd
import numpy as np
from pathlib import Path

# only select sites which are included in the new EVA request:
bf_eva = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_cleaned/EVA.172/cleaned.eva')
eva_in_new = pd.read_csv(bf_eva / 'hea.csv')
eva_in_new.set_index(eva_in_new.plot_id, inplace=True)

bf_out = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')

# start with T3 forests
# read data which we already have:
data_done = pd.read_csv('/home/storage/malle/SPLOT_dataframes/boreal/EVA_forest_t3_min.csv')

id_uncertainty = np.logical_or(eva_in_new['uncertainty_m'] < 5000, np.isnan(eva_in_new['uncertainty_m']))
id_plot_size = np.logical_and(eva_in_new['plot_size'] <= 1000, eva_in_new['plot_size'] >= 100)
id_all_c = np.logical_and(id_uncertainty, id_plot_size)
id_site_species = eva_in_new.Level_2 == 'T3'
id_all = np.logical_and(id_all_c, id_site_species)

eva_in_sel_prel = eva_in_new[id_all]
id_lat = eva_in_sel_prel['Latitude'].duplicated(keep=False)
id_lon = eva_in_sel_prel['Longitude'].duplicated(keep=False)
id_latlon = np.logical_and(id_lat, id_lon)
eva_in_sel = eva_in_sel_prel[~id_latlon]

eva_in_sel_not_done = eva_in_sel[~eva_in_sel['plot_id'].isin(data_done.plot_id)]

# stratified sampling to get a heterogeneous dataset based on level 3 data
sel_T3 = eva_in_sel_not_done.groupby('Level_3', group_keys=False).apply(lambda x: x.sample(60))
# use disproportionate sampling
sel_T3.to_csv(bf_out / 'sel_T3.csv')

# now T1 forests
# read data which we already have:
data_done = pd.read_csv('/home/storage/malle/SPLOT_dataframes/forest_t1/EVA_forest_t1_min.csv')

id_uncertainty = np.logical_or(eva_in_new['uncertainty_m'] < 5000, np.isnan(eva_in_new['uncertainty_m']))
id_plot_size = np.logical_and(eva_in_new['plot_size'] <= 1000, eva_in_new['plot_size'] >= 100)
id_all_c = np.logical_and(id_uncertainty, id_plot_size)
id_site_species = eva_in_new.Level_2 == 'T1'
id_all = np.logical_and(id_all_c, id_site_species)

eva_in_sel_prel = eva_in_new[id_all]
id_lat = eva_in_sel_prel['Latitude'].duplicated(keep=False)
id_lon = eva_in_sel_prel['Longitude'].duplicated(keep=False)
id_latlon = np.logical_and(id_lat, id_lon)
eva_in_sel = eva_in_sel_prel[~id_latlon]

eva_in_sel_not_done = eva_in_sel[~eva_in_sel['plot_id'].isin(data_done.plot_id)]

# stratified sampling to get a heterogeneous dataset based on level 3 data
sel_T1 = eva_in_sel_not_done.groupby('Level_3', group_keys=False).apply(lambda x: x.sample(60))
# use disproportionate sampling
sel_T1.to_csv(bf_out / 'sel_T1.csv')

# now S2 scrubs
# read data which we already have:
data_done = pd.read_csv('/home/storage/malle/SPLOT_dataframes/scrub_s2/EVA_scrub_s2_min.csv')

id_uncertainty = np.logical_or(eva_in_new['uncertainty_m'] < 5000, np.isnan(eva_in_new['uncertainty_m']))
id_plot_size = np.logical_and(eva_in_new['plot_size'] <= 100, eva_in_new['plot_size'] >= 1)
id_all_c = np.logical_and(id_uncertainty, id_plot_size)
id_site_species = eva_in_new.Level_2 == 'S2'
id_all = np.logical_and(id_all_c, id_site_species)

eva_in_sel_prel = eva_in_new[id_all]
id_lat = eva_in_sel_prel['Latitude'].duplicated(keep=False)
id_lon = eva_in_sel_prel['Longitude'].duplicated(keep=False)
id_latlon = np.logical_and(id_lat, id_lon)
eva_in_sel = eva_in_sel_prel[~id_latlon]

eva_in_sel_not_done = eva_in_sel[~eva_in_sel['plot_id'].isin(data_done.plot_id)]

# stratified sampling to get a heterogeneous dataset based on level 3 data
sel_S2_1 = eva_in_sel_not_done.groupby('Level_3', group_keys=False).apply(lambda x: x.sample(80))
# use disproportionate sampling

eva_in_add = eva_in_sel_not_done[~eva_in_sel_not_done['plot_id'].isin(sel_S2_1.plot_id)]
sel_S2_2 = eva_in_add.groupby('Dataset', group_keys=False).apply(lambda x: x.sample(frac=0.1))
# use proportionate sampling in addition since we don't have enough of each individual

sel_S2 = pd.concat([sel_S2_1, sel_S2_2])
sel_S2.to_csv(bf_out / 'sel_S2.csv')

# now S6 scrubs
# read data which we already have:
data_done = pd.read_csv('/home/storage/malle/SPLOT_dataframes/scrub_s6/EVA_scrub_s6_min.csv')

id_uncertainty = np.logical_or(eva_in_new['uncertainty_m'] < 5000, np.isnan(eva_in_new['uncertainty_m']))
id_plot_size = np.logical_and(eva_in_new['plot_size'] <= 100, eva_in_new['plot_size'] >= 1)
id_all_c = np.logical_and(id_uncertainty, id_plot_size)
id_site_species = eva_in_new.Level_2 == 'S6'
id_all = np.logical_and(id_all_c, id_site_species)

eva_in_sel_prel = eva_in_new[id_all]
id_lat = eva_in_sel_prel['Latitude'].duplicated(keep=False)
id_lon = eva_in_sel_prel['Longitude'].duplicated(keep=False)
id_latlon = np.logical_and(id_lat, id_lon)
eva_in_sel = eva_in_sel_prel[~id_latlon]

eva_in_sel_not_done = eva_in_sel[~eva_in_sel['plot_id'].isin(data_done.plot_id)]

# stratified sampling to get a heterogeneous dataset based on level 3 data
sel_S6_1 = eva_in_sel_not_done.groupby('Level_3', group_keys=False).apply(lambda x: x.sample(30))
# use disproportionate sampling

eva_in_add = eva_in_sel_not_done[~eva_in_sel_not_done['plot_id'].isin(sel_S6_1.plot_id)]
sel_S6_2 = eva_in_add.groupby('Dataset', group_keys=False).apply(lambda x: x.sample(frac=0.7))
# use proportionate sampling in addition since we don't have enough of each individual
sel_S6 = pd.concat([sel_S6_1, sel_S6_2])
sel_S6.to_csv(bf_out / 'sel_S6.csv')

# now R3 grasses
# read data which we already have:
data_done = pd.read_csv('/home/storage/malle/SPLOT_dataframes/grass_r3/EVA_grass_r3_min.csv')

id_uncertainty = np.logical_or(eva_in_new['uncertainty_m'] < 5000, np.isnan(eva_in_new['uncertainty_m']))
id_plot_size = np.logical_and(eva_in_new['plot_size'] <= 100, eva_in_new['plot_size'] >= 1)
id_all_c = np.logical_and(id_uncertainty, id_plot_size)
id_site_species = eva_in_new.Level_2 == 'R3'
id_all = np.logical_and(id_all_c, id_site_species)

eva_in_sel_prel = eva_in_new[id_all]
id_lat = eva_in_sel_prel['Latitude'].duplicated(keep=False)
id_lon = eva_in_sel_prel['Longitude'].duplicated(keep=False)
id_latlon = np.logical_and(id_lat, id_lon)
eva_in_sel = eva_in_sel_prel[~id_latlon]

eva_in_sel_not_done = eva_in_sel[~eva_in_sel['plot_id'].isin(data_done.plot_id)]

# stratified sampling to get a heterogeneous dataset based on level 3 data
sel_R3_1 = eva_in_sel_not_done.groupby('Level_3', group_keys=False).apply(lambda x: x.sample(38))
# use disproportionate sampling

eva_in_add = eva_in_sel_not_done[~eva_in_sel_not_done['plot_id'].isin(sel_R3_1.plot_id)]
sel_R3_2 = eva_in_add.groupby('Dataset', group_keys=False).apply(lambda x: x.sample(frac=0.03))
# use proportionate sampling in addition since we don't have enough of each individual

sel_R3 = pd.concat([sel_R3_1, sel_R3_2])
sel_R3.to_csv(bf_out / 'sel_R3.csv')

# now R4 grasses
# read data which we already have:
data_done = pd.read_csv('/home/storage/malle/SPLOT_dataframes/grassland/EVA_grass_r4_min.csv')

id_uncertainty = np.logical_or(eva_in_new['uncertainty_m'] < 5000, np.isnan(eva_in_new['uncertainty_m']))
id_plot_size = np.logical_and(eva_in_new['plot_size'] <= 100, eva_in_new['plot_size'] >= 1)
id_all_c = np.logical_and(id_uncertainty, id_plot_size)
id_site_species = eva_in_new.Level_2 == 'R4'
id_all = np.logical_and(id_all_c, id_site_species)

eva_in_sel_prel = eva_in_new[id_all]
id_lat = eva_in_sel_prel['Latitude'].duplicated(keep=False)
id_lon = eva_in_sel_prel['Longitude'].duplicated(keep=False)
id_latlon = np.logical_and(id_lat, id_lon)
eva_in_sel = eva_in_sel_prel[~id_latlon]

eva_in_sel_not_done = eva_in_sel[~eva_in_sel['plot_id'].isin(data_done.plot_id)]

# stratified sampling to get a heterogeneous dataset based on level 3 data
sel_R4_1 = eva_in_sel_not_done.groupby('Level_3', group_keys=False).apply(lambda x: x.sample(80))
# use disproportionate sampling

eva_in_add = eva_in_sel_not_done[~eva_in_sel_not_done['plot_id'].isin(sel_R4_1.plot_id)]
sel_R4_2 = eva_in_add.groupby('Dataset', group_keys=False).apply(lambda x: x.sample(frac=0.07))
# use proportionate sampling in addition since we don't have enough of each individual

sel_R4 = pd.concat([sel_R4_1, sel_R4_2])
sel_R4.to_csv(bf_out / 'sel_R4.csv')
