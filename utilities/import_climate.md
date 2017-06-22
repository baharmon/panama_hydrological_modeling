scp /Users/baharmon/Downloads/precip.mon.mean.nc baharmon@fatra.cnr.ncsu.edu:precip.mon.mean.nc

ssh -Y baharmon@fatra.cnr.ncsu.edu

grass-trunk

gdalinfo precip.mon.mean.nc

r.in.gdal input=NETCDF:"precip.mon.mean.nc":precip output=precip_mon_mean

zip -r NLCC.zip grassdata/NLCC

scp baharmon@fatra.cnr.ncsu.edu:NLCC.zip /Users/baharmon/Downloads/NLCC.zip
