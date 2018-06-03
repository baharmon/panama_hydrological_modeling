# [WorldClim Version2](http://worldclim.org/version2)
WorldClim version 2 has average monthly climate data for minimum, mean, and maximum temperature and for precipitation for 1970-2000 at 1 sq km resolution.

## Data
http://worldclim.org/version2

## References
Fick, S.E. and R.J. Hijmans, 2017. Worldclim 2: New 1-km spatial resolution climate surfaces for global land areas. International Journal of Climatology.

## Processing in GRASS GIS
r.in.gdal input=/home/baharmon/Downloads/wc2.0_30s_prec/wc2.0_30s_prec_01.tif output=precipitation_01

r.proj location=worldlocation mapset=wc_precipitation input=precipitation_01 method=bilinear memory=9000 resolution=1000
