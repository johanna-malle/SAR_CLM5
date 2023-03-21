# -*- coding: utf-8 -*-
"""
Desc: make overview plot of selected EVA sites where we performed CLM5 simulations for SAR analysis
Created on 20.03.23 09:24
@author: malle
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx
import palettable as pc

bf_sel = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected')
bf_add_on = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected_add_on')
bf_prev = Path('/home/malle/slfhome/Postdoc3/SAR_biodiv/EVA_request/EVA_selected_previous')

hab_in = ['T1', 'T3', 'R3', 'R4', 'S2', 'S6']

crs = {'init': 'epsg:4326'}

bf = Path('/home/malle/slfhome/Postdoc3/SPLOT/')
path_lb = bf / "NUTS_RG_60M_2021_4326.json"
gdf_lb = gpd.read_file(path_lb)
gdf_countrya = gdf_lb[gdf_lb.LEVL_CODE == 0]
gdf_countrya.crs = "EPSG:25832"

col_all = pc.colorbrewer.qualitative.Set2_6.hex_colors

fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(111)
for num_in in range(len(hab_in)):
    print(num_in)
    hab = hab_in[num_in]
    print(hab)

    eva_in_sel = pd.read_csv(bf_sel / Path('sel_' + hab + '.csv'))
    coords_splot_sel = list(zip(eva_in_sel['Longitude'], eva_in_sel['Latitude']))

    eva_in_prev = pd.read_csv(bf_prev / Path('sel_' + hab + '.csv'))
    coords_splot_pre = list(zip(eva_in_prev['Longitude'], eva_in_prev['Latitude']))

    if hab != 'S6':
        eva_in_add = pd.read_csv(bf_add_on / Path('sel_' + hab + '.csv'))
        coords_splot_add = list(zip(eva_in_add['Longitude'], eva_in_add['Latitude']))
        geom_add = [Point(xy) for xy in coords_splot_add]
        geodata_add = gpd.GeoDataFrame(eva_in_add, crs=crs, geometry=geom_add)
        geodata_add_p = geodata_add.to_crs(epsg=3035)
        geodata_add_p.plot(color=col_all[num_in], ax=ax1, edgecolor='gray', linewidth=0.15, markersize=25, alpha=0.7)
        # ,marker="o",markersize=15)

    geom_sel = [Point(xy) for xy in coords_splot_sel]
    geodata_sel = gpd.GeoDataFrame(eva_in_sel, crs=crs, geometry=geom_sel)
    geodata_sel_p = geodata_sel.to_crs(epsg=3035)

    geom_prev = [Point(xy) for xy in coords_splot_pre]
    geodata_prev = gpd.GeoDataFrame(eva_in_prev, crs=crs, geometry=geom_prev)
    geodata_prev_p = geodata_prev.to_crs(epsg=3035)

    ax2 = geodata_sel_p.plot(color=col_all[num_in], ax=ax1, edgecolor='gray', linewidth=0.15, markersize=25,
                             label=hab, alpha=0.7)  # ,marker="o",markersize=15)
    geodata_prev_p.plot(color=col_all[num_in], ax=ax1, edgecolor='gray', linewidth=0.15, markersize=25,
                        alpha=0.7)  # ,marker="o",markersize=15)

ctx.add_basemap(ax2, crs="EPSG:3035", source=ctx.providers.Stamen.TonerLite, alpha=0.8)
ax1.legend()
ax1.ticklabel_format(style='plain')
ax1.xaxis.set_ticks_position('none')
ax1.yaxis.set_ticks_position('none')
plt.xticks(color='w')
plt.yticks(color='w')

plt.show()
fig_comp1 = bf_sel / Path("overview_locs.png")
fig.savefig(fig_comp1, dpi=250, bbox_inches='tight')
plt.close()
