import os
import cdsapi
import calendar
from subprocess import call

def idm_era5(idm_engine, variable, dst_dir, **kwargs):
    retrieve_type = kwargs.get('retrieve_type', 'reanalysis-era5-land-monthly-means')
    product_type = kwargs.get('product_type','monthly_averaged_reanalysis')
    year = kwargs.get('year', [str(year) for year in range(1980, 2024)])
    month = kwargs.get('month', [str(mon).zfill(2) for mon in range(1, 13)])
    time = kwargs.get('time', '00:00')
    format = kwargs.get('format', 'netcdf.zip')
    file_name = kwargs.get('file_name', f'{variable}.zip')
    
    c = cdsapi.Client()
    dic = {
        'product_type': product_type,
        'variable': variable,
        'year': year,
        'month': month,
        'time': time,
        'format': format
    }

    file_path = os.path.join(dst_dir, file_name)
    
    if not os.path.exists(file_path):
        r = c.retrieve(retrieve_type, dic)
        task_url = r.location
        print('正在下载%s'%task_url)
        call([idm_engine, '/d', task_url, '/p', dst_dir, '/f', file_name, '/a'])
        call([idm_engine, '/s'])
        
    else:
        print(file_path, "存在同名文件")
        
        
def idm_era5_daily(idm_engine, variable, dst_dir, **kwargs):
    retrieve_type = kwargs.get('retrieve_type','reanalysis-era5-land')
    year = kwargs.get('year', '2023')
    month = kwargs.get('month', '01')
    day = kwargs.get('day', [str(day).zfill(2) for day in range(1, calendar.monthrange(year, month)[1] + 1)])
    time = kwargs.get('time', [f"{str(hour).zfill(2)}:00" for hour in range(24)])
    format = kwargs.get('format', 'netcdf.zip')
    file_name = kwargs.get('file_name', f'{variable}.zip')
    
    c = cdsapi.Client()
    dic = {
        'variable': variable,
        'year': year,
        'month': month,
        'day': day,
        'time': time,
        'format': format
    }

    file_path = os.path.join(dst_dir, file_name)
    
    if not os.path.exists(file_path):
        r = c.retrieve(retrieve_type, dic)
        task_url = r.location
        print('正在下载%s'%task_url)
        call([idm_engine, '/d', task_url, '/p', dst_dir, '/f', file_name, '/a'])
        call([idm_engine, '/s'])
        
    else:
        print(file_path, "存在同名文件")