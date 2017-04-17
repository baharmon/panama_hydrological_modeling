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
    n='10:47:10N',
    s='5:37:20N',
    e='75:37:32.973365W',
    w='82:27:58.600174W',
    save='region',
    overwrite=overwrite)

# set path
landcover_path = os.path.join(gisdbase, 'esa_landcover')

landcover_files = []
for (dirpath, dirnames, filenames) in os.walk(landcover_path):
    landcover_files.extend(sorted(filenames))
    break

for index, year in enumerate(range(1998,2015)):

    # set path
    landcover_filepath = os.path.join(landcover_path, landcover_files[index])
    print landcover_filepath

    # import
    gscript.run_command('r.import',
        extent='region',
        input=landcover_filepath,
        output='landcover_'+str(year),
        overwrite=overwrite)
