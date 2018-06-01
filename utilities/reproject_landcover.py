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
    raster='panama_30m_dem',
    res=300,
    overwrite=overwrite)

# reproject landcover rasters
for index, year in enumerate(range(1998,2016)):

    # import
    gscript.run_command('r.proj',
        location='ESACCI-LC',
        mapset='PERMANENT',
        input='landcover_'+str(year),
        output='landcover_'+str(year),
        method='nearest',
        memory='9000',
        resolution='300',
        overwrite=overwrite)
