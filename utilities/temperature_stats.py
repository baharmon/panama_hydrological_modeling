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
temperature = os.path.join(gisdbase, 'climate_data','precip.mon.mean.nc')

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
    res=0.3)

# create list
mean_temperature = []

# csv filepath
temperature_stats = os.path.join(gisdbase, 'temperature_stats.csv')

# write statistics to csv file
with open(temperature_stats, 'wb') as csvfile:
    stats_writer = csv.writer(csvfile,
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL)

    # write headers
    stats_writer.writerow(['Time',
        'Temperature(degC)'])

    # process temperature rasters
    i = 0
    for year in range(start_year, end_year, 1):
        for month in range(start_month, end_month, 1):
            try:

                # set map name variables
                old = 'temperature_{year}_{month}@{mapset}'.format(year=time.year,
                    month=time.strftime('%m'),
                    mapset='temperature')
                new = 'temperature_{year}_{month}'.format(year=time.year,
                    month=time.strftime('%m'),
                    mapset=mapset)

                # import to mapset, crop map to region, and divide by ten
                # since integer versions of temperature grids
                # are stored in tenths of degrees C
                gscript.run_command('r.mapcalc',
                    expression='{new} = {old}*0.1'.format(old=old,
                        new=new),
                    overwrite=overwrite)

                # compute statistics
                univar = gscript.parse_command('r.univar',
                    map=new,
                    separator='newline',
                    flags='g')
                mean_temperature.append(univar['mean'])

                # write data
                stats_writer.writerow([time,
                    mean_temperature[i]])

                # advance
                i = i + 1
                time = time + relativedelta(months=+1)

            except:
                pass
