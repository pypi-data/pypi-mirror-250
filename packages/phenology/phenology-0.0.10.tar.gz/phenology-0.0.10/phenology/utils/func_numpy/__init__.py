import numpy as np
from .api_resample import resample_2D_mean

def aggregate(x, exc_shape, ignore_nodata=None):
    """
    x: 2D array
    exc_shape: tuple of (rows, cols)
    return: 2D array
    """
    cur_rows, cur_cols = x.shape
    exc_rows, exc_cols = exc_shape
    rw = cur_rows / exc_rows
    cw = cur_cols / exc_cols
    
    x = np.pad(x, ((0, int(rw+1)), (0, int(cw+1))), 'constant', constant_values=np.nan)
    x[np.isinf(x)] = np.nan
    
    if ignore_nodata is not None:
        x[x==ignore_nodata] = np.nan
    
    x_min = np.nanmin(x)-1
    x = x - x_min # x >= 1

    x[np.isnan(x)] = 0 # 0 is the missing value
    x = x.astype(np.float64)
    y = np.full(exc_shape, np.nan).astype(np.float64)
    y = resample_2D_mean(x, y, rw, cw, exc_rows, exc_cols, 0) # 0 is the missing value
    y = np.asarray(y) + x_min
    
    return y