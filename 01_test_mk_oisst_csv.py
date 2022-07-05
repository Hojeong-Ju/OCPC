#%% 리눅스 경로
# 1982 ~ 2019 v2.0
# /data/public/OCPC/raw/sst_daily/v2.0/ 연도
# 2020 ~ 2021 v2.1
# /data/public/OCPC/raw/sst_daily/v2.1/preliminary_data/ 연도
# mask 경로
# /data/public/OCPC/ASKmask.nc

#%% 
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import datetime as dt
from glob import glob
from dask.diagnostics import ProgressBar

#%% 추가
# #%% v2.0, v2.1 차원 같음
# test_2019 = xr.open_dataset(r'D:\01_Monthly_analysis\02_workspace\02_OISST\data/2019/20190101120000-NCEI-L4_GHRSST-SSTblend-AVHRR_OI-GLOB-v02.0-fv02.0.nc')
# test_2020 = xr.open_dataset(r'D:\01_Monthly_analysis\02_workspace\02_OISST\data/2020/20200101120000-NCEI-L4_GHRSST-SSTblend-AVHRR_OI-GLOB-v02.0-fv02.1.nc')

#%% 로컬 경로 사용

f_lst = glob(r'D:\01_Monthly_analysis\02_workspace\02_OISST\data/**/*.nc', recursive=True)

with ProgressBar():
    dset = xr.open_mfdataset(f_lst, combine = 'by_coords', concat_dim = 'time', coords = 'minimal',
                            data_vars='minimal', compat='override', parallel=True) - 273.15

mask_dset = xr.open_dataset(r'./data/ASKmask.nc')
monthly_dset = dset.resample(time = '1M').mean()

ys_mean = monthly_dset.analysed_sst.sel(lon = mask_dset.XA, lat = mask_dset.YA, method = 'nearest').where(mask_dset.LANDSEA == 1).mean(['YA', 'XA'])
ys_clima = ys_mean.groupby('time.month').mean()
ys_clima_anomaly = ys_mean.groupby('time.month') - ys_clima

repeat_ys_clima = np.array([])
for yr in np.arange(0, len(np.unique(monthly_dset.time.dt.year))):
    repeat_ys_clima = np.concatenate([repeat_ys_clima, ys_clima])

ecs_mean = monthly_dset.analysed_sst.sel(lon = mask_dset.XA, lat = mask_dset.YA, method = 'nearest').where(mask_dset.LANDSEA == 2).mean(['YA', 'XA'])
ecs_clima = ecs_mean.groupby('time.month').mean()
ecs_clima_anomaly = ecs_mean.groupby('time.month') - ecs_clima

repeat_ecs_clima = np.array([])
for yr in np.arange(0, len(np.unique(monthly_dset.time.dt.year))):
    repeat_ecs_clima = np.concatenate([repeat_ecs_clima, ecs_clima])

es_mean = monthly_dset.analysed_sst.sel(lon = mask_dset.XA, lat = mask_dset.YA, method = 'nearest').where(mask_dset.LANDSEA == 3).mean(['YA', 'XA'])
es_clima = es_mean.groupby('time.month').mean()
es_clima_anomaly = es_mean.groupby('time.month') - es_clima

repeat_es_clima = np.array([])
for yr in np.arange(0, len(np.unique(monthly_dset.time.dt.year))):
    repeat_es_clima = np.concatenate([repeat_es_clima, es_clima])

ask_mean = monthly_dset.analysed_sst.sel(lon = mask_dset.XA, lat = mask_dset.YA, method = 'nearest').where(mask_dset.LANDSEA == 4).mean(['YA', 'XA'])
ask_clima = ask_mean.groupby('time.month').mean()
ask_clima_anomaly = ask_mean.groupby('time.month') - ask_clima


repeat_ask_clima = np.array([])
for yr in np.arange(0, len(np.unique(monthly_dset.time.dt.year))):
    repeat_ask_clima = np.concatenate([repeat_ask_clima, ask_clima])
    
glob_mean = monthly_dset.analysed_sst.mean(['lon', 'lat'])
glob_clima = glob_mean.groupby('time.month').mean()
glob_clima_anomaly = glob_mean.groupby('time.month') - glob_clima


repeat_glob_clima = np.array([])
for yr in np.arange(0, len(np.unique(monthly_dset.time.dt.year))):
    repeat_glob_clima = np.concatenate([repeat_glob_clima, glob_clima])
    
yr = monthly_dset.time.dt.year.data
mon = monthly_dset.time.dt.month.data

df2 = pd.DataFrame([yr, mon, ys_mean.data, repeat_ys_clima, ys_clima_anomaly.data, ecs_mean.data, repeat_ecs_clima, ecs_clima_anomaly.data, es_mean.data, repeat_es_clima, 
                    es_clima_anomaly.data, ask_mean.data, repeat_ask_clima, ask_clima_anomaly.data, glob_mean.data, repeat_glob_clima, glob_clima_anomaly.data]).T
df3 = df2.astype({0:int, 1:int})
df3.columns = ['Year', 'Month', 'YS_Mean', 'Climatology', 'Anomaly', 'ECS_Mean', 'Climatology', 'Anomaly', 'ES_Mean',
               'Climatology', 'Anomaly', 'ASK_Mean', 'Climatology', 'Anomaly', 'GLOB_Mean', 'Climatology', 'Anomaly']

df3.to_csv(r'./SST_analysis_depanding_on_seas.csv', index = False)