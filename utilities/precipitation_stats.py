#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: Import netcdf precipitation data in GRASS GIS

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
precipitation = os.path.join(gisdbase, 'climate_data','precip.mon.mean.nc')

# set temporal parameters
start_year = 1998
start_month = 1
end_year = 2016
end_month = 13
time = datetime.date(start_year, start_month, 1)

# set region
gscript.run_command('g.region',
    n=10,
    s=8,
    e=-78,
    w=-80,
    res=2)

# create list
mean_precipitation = []

# csv filepath
precipitation_stats = os.path.join(gisdbase, 'precipitation_stats.csv')

# write statistics to csv file
with open(precipitation_stats, 'wb') as csvfile:
    stats_writer = csv.writer(csvfile,
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL)

    # write headers
    stats_writer.writerow(['Time',
        'Precipitation(mm/day)'])

    # process precipitation rasters
    i = 0
    for year in range(start_year, end_year, 1):
        for month in range(start_month, end_month, 1):
            try:

                # set map name variables
                old = 'precipitation_{year}_{month}@{mapset}'.format(year=time.year,
                    month=time.strftime('%m'),
                    mapset='precipitation')
                new = 'precipitation_{year}_{month}'.format(year=time.year,
                    month=time.strftime('%m'),
                    mapset=mapset)

                # import to mapset and crop map to region
                gscript.run_command('r.mapcalc',
                    expression='{new} = {old}'.format(old=old,
                        new=new),
                    overwrite=overwrite)

                # compute statistics
                univar = gscript.parse_command('r.univar',
                    map=new,
                    separator='newline',
                    flags='g')
                mean_precipitation.append(univar['mean'])

                # write data
                stats_writer.writerow([time,
                    mean_precipitation[i]])

                # advance
                i = i + 1
                time = time + relativedelta(months=+1)

            except:
                pass
