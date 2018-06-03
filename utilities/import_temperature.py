#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: Import netcdf temperature data in GRASS GIS

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import sys
import csv
import atexit
import datetime
from dateutil.relativedelta import relativedelta
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

# set path
temperature = os.path.join(gisdbase, 'climate_data','air.mon.mean.nc')

# set temporal parameters
start_year = 1948
start_month = 1
end_year = 2018
end_month = 4
time = datetime.date(start_year, start_month, 1)

# print number of bands
bands = gscript.read_command('r.in.gdal',
    input=temperature,
    output='temperature',
    memory=6000,
    flags='p')

# import temperature data
for band in enumerate(range(int(bands)), 1):
    gscript.run_command('r.in.gdal',
        input=temperature,
        output='temperature_{year}_{month}'.format(year=time.year, month=time.strftime('%m')),
        band=band[0],
        memory=6000,
        flags='o',
        overwrite=overwrite)

    # advance time
    time = time + relativedelta(months=+1)
