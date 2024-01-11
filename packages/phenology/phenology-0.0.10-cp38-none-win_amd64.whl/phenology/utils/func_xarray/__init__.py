import xarray as xr

def _swap_longtitude_v1(ds, lon_dim='longitude'):
    '''
    把-180到180度改为0-360度, 该版本仅适用于全球数据
    '''
    ds_lon_first_half  = ds.isel({lon_dim: slice(0, ds.dims[lon_dim] // 2)}) # 获取 lon 的左半部分
    ds_lon_second_half = ds.isel({lon_dim: slice(ds.dims[lon_dim] // 2, ds.dims[lon_dim])}) # 获取 lon 的右半部分
    ds_lon_first_half[lon_dim] = ds_lon_first_half[lon_dim] + 360 # 把-180-0的lon改为180-360
    result = xr.concat([ds_lon_second_half, ds_lon_first_half], dim=lon_dim) # 拼接数据
    return result

def _swap_longtitude_v2(ds, lon_dim='longitude'):
    '''
    把0-360度改为-180到180度, 该版本仅适用于全球数据
    '''
    ds_lon_first_half = ds.isel({lon_dim: slice(0, ds.dims[lon_dim] // 2)})
    ds_lon_second_half = ds.isel({lon_dim: slice(ds.dims[lon_dim] // 2, ds.dims[lon_dim])})
    ds_lon_second_half[lon_dim] = ds_lon_second_half[lon_dim] - 360
    result = xr.concat([ds_lon_second_half, ds_lon_first_half], dim=lon_dim)
    return result



def swap_longtitude(ds, lon_dim='longitude'):
    '''
    Converts longitudes based on the input dataset's longitude range:
    - If the input dataset's longitude range is -180 to 180 degrees, it converts to 0-360 degrees.
    - If the input dataset's longitude range is 0-360 degrees, it converts to -180 to 180 degrees.

    Parameters:
    - ds (xarray.Dataset): Input dataset.
    - lon_dim (str, optional): The dimension representing longitudes. Default is 'longitude'.

    Returns:
    xarray.Dataset: Dataset with longitudes converted based on the specified conditions and sorted by latitude and longitude.
    '''
    if max(ds[lon_dim].values) > 300:
        return _swap_longtitude_v2(ds, lon_dim).sortby(lon_dim)
    else:
        return _swap_longtitude_v1(ds, lon_dim).sortby(lon_dim)