#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: Reproject global temperature data for Panama

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
res=1000, #50000

# set region
gscript.run_command('g.region',
    raster='panama_30m_dem',
    res=res,
    overwrite=overwrite)

# reproject temperature rasters
for year in range(1998,2016):
    for month in range(01,13):
        try:
            # import
            gscript.run_command('r.proj',
                location='worldlocation',
                mapset='temperature',
                input='temperature_'+str(year)+'_'+str(month),
                output='temperature_'+str(year)+'_'+str(month),
                method='bilinear',
                memory='9000',
                resolution=res,
                overwrite=overwrite)
        except:
            pass
