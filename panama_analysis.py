#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: geospatial analysis for study of riverine geochemistry in panama

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

# set input and ouput paths
landcover_recode = os.path.join(gisdbase, location, 'landcover_recode.txt')
landcover_color = os.path.join(gisdbase, location, 'landcover_color.txt')
landcover_categories = os.path.join(gisdbase, location, 'landcover_categories.txt')
results = os.path.join(gisdbase, location, 'results')

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
zscale = 1.5
shaded_relief = 'shaded_relief'
brighten = 36
skyview = 'skyview'
skyview_brighten = 50
colorized_skyview = 'colorized_skyview'
shaded_skyview = 'shaded_skyview'
accumulation = 'accumulation'
reference_stations = 'stations@PERMANENT'
stations = 'stations'
snapped_stations = 'snapped_stations'
threshold = 1000
streams = 'streams'
direction = 'direction'
basins = 'basins'
step = 50
input_landcover = 'panama_300m_landcover'
landcover = 'landcover'

# rendering parameters
width = 1500
height = 1000
fontsize = 16
legend_coord = (2, 42, 2, 4)

def main():

    # dependencies()

    # topographic_analysis()

    # hydrological_modeling()

    # landcover_analysis()

    # climate_analysis()

    # extract_basins()

    # basin_topographic_analysis()

    # basin_hydrologic_analysis()

    # basin_landcover_analysis()

    # basin_climate_analysis()

    # basin_morphometric_analysis()

    # render()

    # render_basins()

    stats()

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

    # compute relief
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

    # compute skyview factor
    gscript.run_command('r.skyview',
        input=elevation,
        output=skyview,
        colorized_output=colorized_skyview,
        overwrite=overwrite)

    # compute shaded skyview factor
    gscript.run_command('r.shade',
        shade=relief,
        color=colorized_skyview,
        output=shaded_skyview,
        brighten=skyview_brighten,
        overwrite=overwrite)

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

def landcover_analysis():
    """process landcover data"""

    # set region
    gscript.run_command('g.region',
        n=n,
        s=s,
        e=e,
        w=w,
        res=res)

    # recode landcover
    gscript.run_command('r.recode',
        input=input_landcover,
        output=landcover,
        rules=landcover_recode,
        overwrite=overwrite)

    # set color table
    gscript.run_command('r.colors',
        map=landcover,
        rules=landcover_color)

    # define categories
    gscript.run_command('r.category',
        map=landcover,
        separator='pipe',
        rules=landcover_categories)

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

def basin_topographic_analysis():
    """compute topographic parameters for each basin"""

    for river in river_mapnames:

        local_elevation = river + '_elevation'
        local_relief = river + '_relief'
        local_shaded_relief = river + '_shaded_relief'
        local_skyview = river + '_skyview'
        local_colorized_skyview = river + '_colorized_skyview'
        local_shaded_skyview = river + '_shaded_skyview'
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
        gscript.run_command('r.colors',
            map=local_elevation,
            color="elevation")

        # compute local slope and aspect
        gscript.run_command('r.slope.aspect',
            elevation=local_elevation,
            slope=local_slope,
            aspect=local_aspect,
            overwrite=overwrite)

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

        # composite relief and skyview factor
        gscript.run_command('r.shade',
            shade=local_relief,
            color=local_colorized_skyview,
            output=local_shaded_skyview,
            brighten=skyview_brighten,
            overwrite=overwrite)

        try:
            # remove mask
            gscript.run_command('r.mask', raster='MASK', flags='r')
        except CalledModuleError:
            pass

def basin_landcover_analysis():
    """compute landcover parameters for each basin"""

    for river in river_mapnames:

        local_landcover = river + '_landcover'
        local_shaded_skyview = river + '_shaded_skyview'
        local_shaded_landcover = river + '_shaded_landcover'

        # set region
        gscript.run_command('g.region',
            vector=river,
            res=res)

        # set mask
        gscript.run_command('r.mask',
            vector=river)

        # clip local landcover
        gscript.run_command('r.mapcalc',
            expression='{local_landcover} = {landcover}'.format(local_landcover=local_landcover,
                landcover=landcover),
            overwrite=overwrite)

        # set color table
        gscript.run_command('r.colors',
            map=local_landcover,
            rules=landcover_color)

        # define categories
        gscript.run_command('r.category',
            map=local_landcover,
            separator='pipe',
            rules=landcover_categories)

        # landcover with shaded relief
        gscript.run_command('r.shade',
            shade=local_shaded_skyview,
            color=local_landcover,
            output=local_shaded_landcover,
            brighten=skyview_brighten,
            overwrite=overwrite)

        try:
            # remove mask
            gscript.run_command('r.mask', raster='MASK', flags='r')
        except CalledModuleError:
            pass


def basin_climate_analysis():
    """compute climatic parameters for each basin"""

    for river in river_mapnames:

        # set region
        gscript.run_command('g.region',
            vector=river,
            res=res)

        # set mask
        gscript.run_command('r.mask',
            vector=river)

        # clip climate data

        try:
            # remove mask
            gscript.run_command('r.mask', raster='MASK', flags='r')
        except CalledModuleError:
            pass


def basin_hydrologic_analysis():
    """compute hydrologic parameters for each basin"""

    for river in river_mapnames:

        local_elevation = river + '_elevation'
        local_streams = river + '_streams'
        local_direction = river + '_direction'
        local_accumulation = river + '_accumulation'
        local_distance = river + '_distance'
        local_direction = river + '_direction'
        local_difference = river + '_difference'
        local_attributes = river + '_attributes'
        local_order = river + '_order'
        local_stats = os.path.join(results, river + '_stats.csv')

        # set region
        gscript.run_command('g.region',
            vector=river,
            res=res)

        # set mask
        gscript.run_command('r.mask',
            vector=river)

        # clip local flow accumulation
        gscript.run_command('r.mapcalc',
            expression='{local_accumulation} = {accumulation}'.format(local_accumulation=local_accumulation,
                accumulation=accumulation),
            overwrite=overwrite)

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
        gscript.run_command('r.stream.distance',
            stream_rast=local_streams,
            direction=local_direction,
            elevation=local_elevation,
            distance=local_distance,
            difference=local_difference,
            memory=memory,
            overwrite=overwrite)

        # compute stream order
        gscript.run_command('r.stream.order',
            stream_rast=local_streams,
            direction=local_direction,
            elevation=local_elevation,
            accumulation=local_accumulation,
            stream_vect=local_attributes,
            strahler=local_order,
            memory=memory,
            overwrite=overwrite)

        # set color table
        gscript.run_command('r.colors',
            map=local_order,
            color='water')

        # compute stream stats
        gscript.run_command('r.stream.stats',
            stream_rast=local_streams,
            direction=local_direction,
            elevation=local_elevation,
            output=local_stats,
            memory=memory,
            overwrite=overwrite)

        try:
            # remove mask
            gscript.run_command('r.mask', raster='MASK', flags='r')
        except CalledModuleError:
            pass

def basin_morphometric_analysis():
    """compute morphometric parameters for each basin"""

    # try to install dependencies
    try:
        gscript.run_command('g.extension',
            extension='r.width.funct',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.hypso',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.basin',
            operation='add')
    except CalledModuleError:
        pass

    for index, river in enumerate(river_mapnames):
        local_elevation = river + '_elevation'

        # set region
        gscript.run_command('g.region',
            vector=river,
            res=res)

        # set mask
        gscript.run_command('r.mask',
            vector=river)

        # find stream gage station coordinates
        coor = gscript.read_command('v.out.ascii',
            input=stations,
            format='point',
            separator='comma',
            flags='r')
        coor_list = coor.split(',')

        # morphometric characterization
        gscript.run_command('r.basin',
            map=local_elevation,
            prefix=river,
            coordinates=[coor_list[0], coor_list[1]],
            dir=results,
            threshold=threshold)

        try:
            # remove mask
            gscript.run_command('r.mask', raster='MASK', flags='r')
        except CalledModuleError:
            pass


def render():
    """render maps of the study area"""

    # set region
    gscript.run_command('g.region',
        n=n,
        s=s,
        e=e,
        w=w,
        res=res)

    # render shaded relief with streams
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(results, shaded_relief+".png"),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map=shaded_relief)
    gscript.run_command('d.vect',
        map=streams,
        display='shape',
        width=2,
        #icon='basic/circle',
        size=0,
        color='blue')
    gscript.run_command('d.legend',
        raster=elevation,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

def render_basins():
    """render maps for each basin"""

    for river in river_mapnames:

        local_elevation = river + '_elevation'
        local_relief = river + '_relief'
        local_shaded_relief = river + '_shaded_relief'
        local_skyview = river + '_skyview'
        local_colorized_skyview = river + '_colorized_skyview'
        local_shaded_skyview = river + '_shaded_skyview'
        local_streams = river + '_streams'
        local_accumulation = river + '_accumulation'
        local_order = river + '_order'
        local_landcover = river + '_landcover'
        local_shaded_landcover = river + '_shaded_landcover'

        # set region
        gscript.run_command('g.region',
            vector=river,
            res=res)

        # render shaded relief with streams
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(results, local_streams+".png"),
            overwrite=overwrite)
        gscript.run_command('d.rast',
            map=local_shaded_skyview)
        gscript.run_command('d.rast',
            map=local_order)
        gscript.run_command('d.vect',
            map=snapped_stations,
            display='shape',
            icon='basic/circle',
            size=2,
            color='blue')
        gscript.run_command('d.legend',
            raster=local_elevation,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # render landcover with streams
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(results, local_landcover+".png"),
            overwrite=overwrite)
        gscript.run_command('d.rast',
            map=local_shaded_landcover)
        gscript.run_command('d.rast',
            map=local_order)
        gscript.run_command('d.vect',
            map=snapped_stations,
            display='shape',
            icon='basic/circle',
            size=2,
            color='blue')
        gscript.run_command('d.legend',
            raster=local_landcover,
            fontsize=fontsize,
            range=(1,9),
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

def stats():
    "write stats for each basin as csv file"

    # create lists
    mean_elevation = []
    min_elevation = []
    max_elevation = []
    mean_slope = []
    min_slope = []
    max_slope = []

    # csv filepath
    topographic_stats = os.path.join(results, 'topograhic_stats.csv')

    # write statistics to csv file
    with open(topographic_stats, 'wb') as csvfile:
        stats_writer = csv.writer(csvfile,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL)

        # write headers
        stats_writer.writerow(['River',
            'Mean elevation',
            'Min elevation',
            'Max elevation',
            'Mean slope',
            'Max slope',
            'Min slope'])

        # loop through rivers
        for index, river in enumerate(river_mapnames):

            # set local variables
            local_elevation = river + '_elevation'
            local_slope = river + '_slope'
            local_landcover = river + '_landcover'

            # set region
            gscript.run_command('g.region',
                vector=river,
                res=res)

            # compute elevation statistics
            univar = gscript.parse_command('r.univar',
                map=local_elevation,
                separator='newline',
                flags='g')
            mean_elevation.append(univar['mean'])
            min_elevation.append(univar['min'])
            max_elevation.append(univar['max'])

            # compute slope statistics
            univar = gscript.parse_command('r.univar',
                map=local_slope,
                separator='newline',
                flags='g')
            mean_slope.append(univar['mean'])
            min_slope.append(univar['min'])
            max_slope.append(univar['max'])

            # compute landcover statistics
            gscript.run_command('r.report',
                map=local_landcover,
                units='me,p',
                flags='n',
                output=os.path.join(results, local_landcover+".txt"),
                overwrite=overwrite)

            # write data
            stats_writer.writerow([rivers[index],
                mean_elevation[index],
                min_elevation[index],
                max_elevation[index],
                mean_slope[index],
                min_slope[index],
                max_slope[index]])


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

    try:
        # stop cairo monitor
        gscript.run_command('d.mon', stop=driver)
    except CalledModuleError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
