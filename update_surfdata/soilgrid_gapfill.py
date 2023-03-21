# -*- coding: utf-8 -*-
"""
Desc: gapfill the soilgrid files so we don't have problems with nans...
Created on 19.01.23 16:07
@author: malle
"""

import rasterio
from rasterio.fill import fillnodata
from pathlib import Path

bf = Path('/home/lud11/malle/PTCLM5/soil_grids_tiles_europe/larger_extent')
bf_out = Path('/home/lud11/malle/PTCLM5/soil_grids_tiles_filled')

files_all = list(bf.iterdir())

for file_in in files_all:
    file_out = bf_out / Path(str(file_in).split('/')[-1][:-4]+'_filled.tif')

    with rasterio.open(file_in) as src:
        profile = src.profile
        arr = src.read(1)
        arr_filled = fillnodata(arr, mask=src.read_masks(1), max_search_distance=10, smoothing_iterations=0)

    with rasterio.open(file_out, 'w', **profile) as dest:
        dest.write_band(1, arr_filled)
