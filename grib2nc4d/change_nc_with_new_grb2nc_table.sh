!/bin/sh

year=2022
month=06
day=28
hour=00

fyr=2022
for fmon in 07 08 09
do
# calc last days in a month
if [ $fmon -eq "04" ] || [ $fmon -eq "06" ] || [ $fmon -eq "09" ] || [ $fmon -eq "11
" ]
then
   lday=30
else
   lday=31
fi
if [ $fmon -eq "02" ]
then
   lday=28
   if [ $((year%4)) -eq 0 ] && [ $((year%100)) -ne 0 ]
   then
      lday=29
   fi
   if [ $((year%400)) -eq 0 ]
   then
      lday=29
   fi
fi
for fday in 01 02 03 04 05 06 07 08 09 $(eval echo "{10..$lday}")
do
for fhr in 00 06 12 18
do
# grb2 to netcdf
wgrib2 ./grb2/ocnf$fyr$fmon$fday$fhr.01.$year$month$day$hour.grb2 -nc_table ./ocnf.grb2nc.table -append -netcdf ./JAS_20220628/ocnf.${fyr}.${fmon}_$year$month$day$hour.nc
done
done
done
