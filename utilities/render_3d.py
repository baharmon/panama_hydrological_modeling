#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: 3D rendering for study of riverine geochemistry in panama

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

# set input and ouput paths
results = os.path.join(gisdbase, location, 'results')

# set variables
res = 30

# 3D rendering parameters
color_3d = "192:192:192"
res_3d = 1
height_3d = 50000
perspective = 25
position = (0.5, 1)
fringe = ['se', 'sw']
fringe_elevation = -1000
format_3d = "tif"
size_3d = (1000, 1000)
zexag = 1
light_position = (0.5, 1, 0.4)
light_brightness = 90
light_color = (255, 215, 0) #(255, 255, 255) # (255, 215, 0)
vline_width = 2
vline_color = "blue"
# vpoint_size = 4
# vpoint_marker = "x"
# vpoint_color = "black"
# arrow_position = (100, 100)
# arrow_size = 100

render_3d()

sys.exit(0)

def render_3d():
    """render 3D maps of the study area"""

    # set region
    gscript.run_command('g.region',
        vector='rio_chagres',
        res=res)

    # 3D render elevation
    gscript.run_command('m.nviz.image',
        elevation_map='rio_chagres_elevation',
        color_map='rio_chagres_shaded_relief',
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        position=position,
        zexag=zexag,
        light_position=light_position,
        light_brightness=light_brightness,
        light_color=light_color,
        vline='rio_chagres_streams',
        vline_width=vline_width,
        vline_color=vline_color,
        output=os.path.join(results, 'rio_chagres_elevation'),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

if __name__ == "__main__":
    sys.exit(main())
