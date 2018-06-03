# [GHCN CAMS global monthly land surface temperature analysis for 1948-2018](https://www.esrl.noaa.gov/psd/data/gridded/data.ghcncams.html)

Global Historical Climatology Network (GHCN) and
Climate Anomaly Monitoring System (CAMS)
global monthly land surface temperature data
from January 1948 to April 2018
gridded at 0.5 x 0.5 degree resolution.

## Data
[air.mon.mean.nc](ftp://ftp.cdc.noaa.gov/Datasets/ghcncams/air.mon.mean.nc)

## References
Fan, Y., and H. van den Dool (2008), A global monthly land surface air temperature analysis for 1948-present, J. Geophys. Res., 113, D01103, doi:10.1029/2007JD008470.

## Acknowledgements
GHCN Gridded V2 data provided by the NOAA/OAR/ESRL PSD, Boulder, Colorado, USA, from their Web site at https://www.esrl.noaa.gov/psd

## Processing in GRASS GIS
import_temperature.py
temperature_stats.py
g.list -e type=raster pattern=temperature_(199[8-9]|200[0-9]|201[0-5]) separator=comma
t.create output=temperature temporaltype=absolute semantictype=mean title=temperature description=temperature
t.register input=temperature maps=... start=1998-01 increment="1 months"
g.gui.animation strds=temperature


# [CPC Merged Analysis of Precipitation](https://www.esrl.noaa.gov/psd/data/gridded/data.cmap.html)

Climate Prediction Centers (CPC) Merged Analysis of Precipitation (CMAP)
global monthly precipitation data
from January 1979 to April 2018
gridded at 2.5 x 2.5 degree resolution.

## Data
[precip.mon.mean.nc](ftp://ftp.cdc.noaa.gov/Datasets/cmap/enh/precip.mon.mean.nc)

## References
Xie, P., and P.A. Arkin, 1997: Global precipitation: A 17-year monthly analysis based on gauge observations, satellite estimates, and numerical model outputs. Bull. Amer. Meteor. Soc., 78, 2539 - 2558.

## Acknowledgements
CMAP Precipitation data provided by the NOAA/OAR/ESRL PSD, Boulder, Colorado, USA, from their Web site at https://www.esrl.noaa.gov/psd/

## Processing in GRASS GIS
import_precipitation.py
precipitation_stats.py
g.list -e type=raster pattern=precipitation_(199[8-9]|200[0-9]|201[0-5]) separator=comma
t.create output=precipitation temporaltype=absolute semantictype=mean title=precipitation description=precipitation
t.register input=precipitation maps=... start=1998-01 increment="1 months"
g.gui.animation strds=precipitation
