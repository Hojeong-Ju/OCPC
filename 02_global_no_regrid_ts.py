#%%
import numpy as np
import pandas as pd
import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
from glob import glob
import os

#%% 해빙에 np.nan 혹은 -1.8 입력, lim_time에 원하는 기간 입력
lim_time = ['1991', '2020']
# sea_ice = -1.8
sea_ice = np.nan

#%%
dset = xr.open_dataset(r'D:\02_Forecast\02_workspace\01_SST\01_OISST\data/OISST_monthly_v2.1_1982_2021.nc').sel(time = slice(*lim_time))
ice_mask = dset.sst.where(dset.ice > 0.15)
dset2 = dset.sst.where(ice_mask.isnull(), sea_ice)
yearly_dset = dset2.resample(time = '1ys').mean()

weights = np.cos(np.deg2rad(yearly_dset.lat))
weights.name = 'weights'
weighted_dset = yearly_dset.weighted(weights)

mask_dset = xr.open_dataset(r'D:\01_Monthly_analysis\02_workspace\02_OISST\data/ASkmask.nc')

glob = weighted_dset.mean(['lat', 'lon'])
glob_para = np.polyfit(np.arange(0, len(glob.time.data)), glob.data, deg=1)

num_lst = [0, 3, 1, 2]
seas = ['Asia', 'ES', 'YS', 'ECS']
clr_lst = ['lightseagreen', 'navy', 'orange', 'green']
new_date = pd.to_datetime(glob.time.data)

#%% 
os.makedirs('./figure', exist_ok = True)

fig, axes = plt.subplots(figsize = (20, 12), nrows = 5, ncols = 1, sharex = True)
axes[0].plot(new_date, glob.data, marker = '*', color = 'blue', linewidth = 2, markersize = 8)
axes[0].plot(new_date, glob_para[0]*np.arange(0, len(glob.time.data)) + glob_para[-1], color = 'r', linewidth = 2)
axes[0].plot([new_date[0], new_date[-1]], [glob.mean(), glob.mean()], color = 'black', zorder = -1, linewidth = 2, label = 'Mean = %.1f'%glob.mean())
axes[0].set_title('Global [%s$^\circ$C / 10yr]'%(glob_para[0]*10).round(2), loc = 'right', fontsize = 20, fontweight = 'bold')

axes[0].set_xticks(new_date)
axes[0].set_xticklabels(new_date.strftime("'%y"))
axes[0].set_xlim([new_date[0] - dt.timedelta(days=365), new_date[-1] + dt.timedelta(days=365)])
axes[0].legend(loc = 'upper left', fontsize = 15)
axes[0].grid()

for ax, num, sea, clr in zip(np.arange(1, 5), num_lst, seas, clr_lst):
    print(sea)
    print(num)
    if num == 0:
        sea_dset = yearly_dset.interp(lon = mask_dset.XA, lat = mask_dset.YA, method = 'linear').where(mask_dset.LANDSEA != num)
    else:
        sea_dset = yearly_dset.interp(lon = mask_dset.XA, lat = mask_dset.YA, method = 'linear').where(mask_dset.LANDSEA == num)
    
    weights_sel = weights.interp(lat = mask_dset.YA, method = 'linear')
    weighted_sea_dset = sea_dset.weighted(weights_sel).mean(['XA', 'YA'])
    
    a, b = np.polyfit(np.arange(0, len(weighted_sea_dset.time.data)), weighted_sea_dset.data, deg=1)
    axes[ax].plot(new_date, weighted_sea_dset.data, marker = '*', color = '%s'%clr, linewidth = 2, markersize = 8)
    axes[ax].plot(new_date, a * np.arange(0, len(weighted_sea_dset.time)) + b, color = 'r', linewidth = 2)
    axes[ax].plot([new_date[0], new_date[-1]], [weighted_sea_dset.mean(), weighted_sea_dset.mean()], color = 'black', zorder = -1, linewidth = 2, label = 'Mean = %.1f'%weighted_sea_dset.mean())
    axes[ax].set_title('%s [%s$^\circ$C / 10yr]'%(sea, (10 * a).round(2)), loc = 'right', fontsize = 20, fontweight = 'bold')
    axes[ax].legend(loc = 'upper left', fontsize = 15)
    axes[ax].grid()
    
axes[0].set_yticks(np.arange(17.5, 19.1, 0.5))
axes[1].set_yticks(np.arange(19.5, 21.51, 0.5))
axes[2].set_yticks(np.arange(11.5, 14.51, 0.5))
axes[3].set_yticks(np.arange(13.5, 16.1, 0.5))
axes[4].set_yticks(np.arange(21, 23.51, 0.5))
for ax in np.arange(len(axes)):
    axes[ax].tick_params(axis = 'y', labelsize = 15)
    axes[ax].tick_params(axis = 'x', labelsize = 18)
        
        
plt.suptitle('SST Change (sea ice = %s) [%s - %s]'%(sea_ice, lim_time[0], lim_time[-1]), fontsize = 20, fontweight = 'bold')
plt.tight_layout()
plt.savefig(r'./figure/SST Change (sea ice = %s)[%s - %s] non regird.png'%(sea_ice, lim_time[0], lim_time[-1]), dpi = 200)
plt.close()