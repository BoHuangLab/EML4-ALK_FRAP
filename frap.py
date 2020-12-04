import numpy as np
import pandas as pd

from scipy import optimize

def six_column(df):
    
    assert (df.columns == ['Frame', 'Mean(Focus)','Mean(Spot)', 'Mean(Bgd)',
       'Mean(Control_Focus)', 'Mean(Control_Spot)',
       'Protein', 'File', 'Filename', 'Experiment', 'Bleach Frame']).all()
    
    six_columns = df.iloc[:,0:6]
    
    return six_columns


def four_column(df):
    
    assert (df.columns == ['Frame', 'Mean(Focus)','Mean(Spot)', 'Mean(Bgd)',
       'Mean(Control_Focus)', 'Mean(Control_Spot)',
       'Protein', 'File', 'Filename', 'Experiment', 'Bleach Frame']).all()
    
    four_columns = df.iloc[:,0:4]
    
    return four_columns


def prebleach(df):
    
    pre = df.iloc[0:6,1:].mean()
    pre = pd.DataFrame(pre).T
    
    return pre


def subtract_background(df: pd.DataFrame):
    ''''''
    
    sub = df.subtract(df['Mean(Bgd)'], axis=0)
    sub.Frame = df.Frame
    sub.drop(columns='Mean(Bgd)', inplace=True)
    return sub


def normalise(sub: pd.DataFrame):
    ''''''
    
    pre = prebleach(sub)
    
    norm = pd.DataFrame()

    for key, value in pre.to_dict(orient='index')[0].items():
    #     print(key, value)

        norm[str(key)] = sub.loc[:, key].divide(value)

    norm['Frame'] = sub['Frame']
    
    return norm


def get_FRAP(norm: pd.DataFrame, t0: int):
    '''
    Parameters
    ----
    norm: pd.DataFrame
    To calculate fluorescence recovery get_FRAP uses a normalised input
    
    t0: int 
    The first postbleach frame. This is used to set the 'Time' column
    
    Returns
    ----
    FRAP: pd.DataFrame
    '''
    
    FRAP = norm.copy() #Here FRAP is NOT cropped
    FRAP['Time'] = (FRAP['Frame']-t0)
    
    return FRAP


def exp_curve(x, A, c, h):
    
    y = h - A*(np.exp(-x/c))
    
    return y


def fit_exp(x, y0, p0, bounds):
    
    #ensure array-like structure
#     x = np.array(x)
#     y = np.array(y0)

    p , e = optimize.curve_fit(f = exp_curve, xdata=x, ydata=y0, p0=p0, bounds=bounds)

    A, c, h = p

    fit = exp_curve(x, A, c, h)

    return fit, p, e


def exp_inv(y, A, c, h):
    
    #numpy.log   is the natural log. 
    #numpy.log10 is log10
    
#     y = h - A*(np.exp(-x/c))
#     y + A*(np.exp(-x/c)) =           h
#         A*(np.exp(-x/c)) =           h - y
#             np.exp(-x/c) =          (h - y)/A
#             np.exp(-x/c) =          (h - y)/A
#                    -x/c  =    np.ln((h - y)/A)
#                    -x    =  c*np.ln((h - y)/A)
    x1    = -c*np.log((h - y)/A)                
    
    return x1


def get_mobile_from_fit(y1):
    
    v  = y1.max()
    F0 = y1.min()
    M  = (v - F0)/(1-F0)
    
    return M
