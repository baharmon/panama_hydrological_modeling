#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: Import landcover

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import sys
import csv
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError

# temporary region
gscript.use_temp_region()

# set environment
env = gscript.gisenv()

overwrite = True
env['GRASS_OVERWRITE'] = overwrite
env['GRASS_VERBOSE'] = False
env['GRASS_MESSAGE_FORMAT'] = 'standard'
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']
mapset = env['MAPSET']

# set region
gscript.run_command('g.region',
    n='10.78611111',
    s='5.62222222',
    e='-75.62555556',
    w='-82.95777778',
    save='region',
    overwrite=overwrite)

count = 1

# rename precipitation rasters
for year in range(1979,2018):
    for month in range(1,13):
        try:
            gscript.run_command(
            'g.rename',
            raster="precip_mon_mean.{count},"
            "precipitation_{year}_{month}".format(
                count=str(count),
                year=str(year),
                month=str(month)),
            overwrite=True)
            count = count + 1
        except:
            pass
