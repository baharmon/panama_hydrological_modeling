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
    res=32000,
    overwrite=overwrite)

# reproject precipitation rasters
for year in range(1979,2018):
    for month in range(1,13):
        try:
            # import
            gscript.run_command('r.proj',
                location='NLCC',
                mapset='PERMANENT',
                input='precipitation_'+str(year)+'_'+str(month),
                output='precipitation_'+str(year)+'_'+str(month),
                method='bilinear',
                memory='9000',
                resolution='32000',
                overwrite=overwrite)
        except:
            pass
