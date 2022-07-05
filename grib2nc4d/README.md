How to use nc_table for CFSv2 grib2 file change into netCDF with wgrib2

wgrib2 a.grb2 -nc_table ocnf.grb2nc.table -append -netcdf a.nc

pgbf도 마찬가지

flxf의 경우는 별도의 nc_table이 필요 없어 보임

Reference https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/netcdf.html
