#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: geospatial analysis for study of riverine geochemistry in panama

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

#import os
import sys
import csv
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError
# import matplotlib.pyplot as plt

# set graphics driver
driver = "cairo"

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

# create lists of river names
rivers = ['Rio Trinidad',
    'Rio Cano Quebrado',
    'Rio Gatun',
    'Rio Boqueron',
    'Rio Pequini',
    'Upper Rio Chagres',
    'Rio Indio Este']
river_mapnames = ['rio_trinidad',
    'rio_canoquebrado',
    'rio_gatun',
    'rio_boqueron',
    'rio_pequini',
    'rio_chagres',
    'rio_indioeste']

# set global variables
n = 1072000
s = 952000
e = 694000
w = 574000
res = 30
memory = 12000 # adjust based on your system's RAM
elevation = 'elevation'
conditioned_elevation = 'conditioned_elevation'
srtm = 'panama_90m_dem@PERMANENT'
alos_gdsm = 'panama_30m_dem@PERMANENT'
relief = 'relief'
zscale = 3
shaded_relief = 'shaded_relief'
brighten = 20
skyview = 'skyview'
colorized_skyview = 'colorized_skyview'
accumulation = 'accumulation'
reference_stations = 'stations@PERMANENT'
stations = 'stations'
snapped_stations = 'snapped_stations'
threshold = 1000
streams = 'streams'
direction = 'direction'
basins = 'basins'
step = 50

def main():

    # dependencies()

    # topographic_analysis()

    # hydrological_modeling()

    # extract_basins()

    basin_analysis()

    atexit.register(cleanup)
    sys.exit(0)

def topographic_analysis():
    """compute hydrologically conditioned elevation and and shaded relief"""

    # set region
    gscript.run_command('g.region',
        n=n,
        s=s,
        e=e,
        w=w,
        res=res)

    # patch holes in higher resolution digital surface model
    gscript.run_command('r.mapcalc',
        expression='{composite} = if(isnull({dem_1}), {dem_2}, {dem_1})'.format(composite=elevation,
            dem_1=alos_gdsm,
            dem_2=srtm),
        overwrite=overwrite)

    # hydrologically condition digital surface model
    gscript.run_command('r.hydrodem',
        input=elevation,
        output=conditioned_elevation,
        memory=memory,
        overwrite=overwrite)

    # compute shaded relief
    gscript.run_command('r.relief',
        input=elevation,
        output=relief,
        zscale=zscale,
        overwrite=overwrite)

    gscript.run_command('r.shade',
        shade=relief,
        color=elevation,
        output=shaded_relief,
        brighten=brighten,
        overwrite=overwrite)

    # gscript.run_command('r.skyview',
    #     input=elevation,
    #     output=skyview,
    #     colorized_output=colorized_skyview,
    #     overwrite=overwrite)

def hydrological_modeling():
    """compute stream network and basins"""

    # set region
    gscript.run_command('g.region',
        n=n,
        s=s,
        e=e,
        w=w,
        res=res)

    try:
        gscript.run_command('g.copy',
            vector=[reference_stations,stations])
    except CalledModuleError:
        pass

    # compute flow accumulation
    gscript.run_command('r.watershed',
        elevation=conditioned_elevation,
        accumulation=accumulation,
        flags='b',
        overwrite=overwrite)

    # extract stream network
    gscript.run_command('r.stream.extract',
        elevation=elevation,
        accumulation=accumulation,
        threshold=threshold,
        memory=memory,
        stream_raster=streams,
        stream_vector=streams,
        direction=direction,
        overwrite=overwrite)

    # snap stream gage stations to raster stream network
    gscript.run_command('r.stream.snap',
        input=stations,
        output=snapped_stations,
        stream_rast=streams,
        accumulation=accumulation,
        memory=memory,
        overwrite=overwrite)

    # compute basins with outlets at stream gages
    gscript.run_command('r.stream.basins',
        direction=direction,
        points=snapped_stations,
        basins=basins,
        memory=memory,
        flags='l',
        overwrite=overwrite)

    # convert basins from raster to vector
    gscript.run_command('r.to.vect',
        input=basins,
        output=basins,
        type='area',
        flags='s',
        overwrite=overwrite)

def extract_basins():
    """extract each basin by name"""

    # join stream gage station names with basin vector attributes
    gscript.run_command('v.db.join',
        map=basins,
        column='value',
        other_table=stations,
        other_column='cat',
        subset_columns='str_1')

    # extract basins
    for index, river in enumerate(rivers):
        gscript.run_command('v.extract',
            input=basins,
            type='area',
            where='str_1 = "{river}"'.format(river=river),
            output=river_mapnames[index],
            overwrite=overwrite)

def basin_analysis():
    """compute topographic, hydrologic, and landcover parameters
    for each basin"""

    for river in river_mapnames:

        local_streams = river + '_streams'
        local_elevation = river + '_elevation'
        local_direction = river + '_direction'
        local_accumulation = river + '_accumulation'
        local_relief = river + '_relief'
        local_shaded_relief = river + '_shaded_relief'
        local_skyview = river + '_skyview'
        local_colorized_skyview = river + '_colorized_skyview'
        local_slope = river + '_slope'
        local_aspect = river + '_aspect'
        local_contours = river + '_contours'

        # set region
        gscript.run_command('g.region',
            vector=river,
            res=res)

        # set mask
        gscript.run_command('r.mask',
            vector=river)

        # clip local elevation
        gscript.run_command('r.mapcalc',
            expression='{local_elevation} = {elevation}'.format(local_elevation=local_elevation,
                elevation=elevation),
            overwrite=overwrite)

        # clip local flow accumulation
        gscript.run_command('r.mapcalc',
            expression='{local_accumulation} = {accumulation}'.format(local_accumulation=local_accumulation,
                accumulation=accumulation),
            overwrite=overwrite)

        # compute local slope and aspect
        gscript.run_command('r.slope.aspect',
            elevation=local_elevation,
            slope=local_slope,
            aspect=local_aspect
            overwrite=True)

        # compute local contours
        gscript.run_command('r.contour',
            input=local_elevation,
            output=local_contours,
            step=step,
            overwrite=overwrite)

        # compute local shaded relief
        gscript.run_command('r.relief',
            input=local_elevation,
            output=local_relief,
            zscale=zscale,
            overwrite=overwrite)
        gscript.run_command('r.shade',
            shade=local_relief,
            color=local_elevation,
            output=local_shaded_relief,
            brighten=brighten,
            overwrite=overwrite)

        # compute local skyview factor
        gscript.run_command('r.skyview',
            input=local_elevation,
            output=local_skyview,
            colorized_output=local_colorized_skyview,
            overwrite=overwrite)






        # clip local landcover

        # clip climate data

        # extract stream network
        gscript.run_command('r.stream.extract',
            elevation=local_elevation,
            accumulation=accumulation,
            threshold=threshold,
            memory=memory,
            stream_raster=local_streams,
            stream_vector=local_streams,
            direction=local_direction,
            overwrite=overwrite)

        # compute stream distance

        # compute stream order

        # compute stream stats



        #gscript.run_command('',)

        # clip topography, landcover, and climate data to basins
        # compute stream parameters
        # compute statistics for each watershed
            # compute stats
                # elevation
                # landcover
                #
            # export statistics
            # render 2d maps
            # render 3d maps


        try:
            # remove mask
            gscript.run_command('r.mask', raster='MASK', flags='r')
        except CalledModuleError:
            pass


def dependencies():
    """try to install required add-ons"""

    try:
        gscript.run_command('g.extension',
            extension='r.skyview',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.hydrodem',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.stream.snap',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.stream.basins',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.stream.distance',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.stream.order',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.stream.stats',
            operation='add')
    except CalledModuleError:
        pass

def cleanup():

    try:
        # remove temporary maps
        gscript.run_command('g.remove',
            type='raster',
            name=['temp',
                'a',
                'b'],
            flags='f')
    except CalledModuleError:
        pass

    try:
        # remove mask
        gscript.run_command('r.mask', raster='MASK', flags='r')
    except CalledModuleError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
