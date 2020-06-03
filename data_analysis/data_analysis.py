"""
Simple data analysis routine for science.

This is a module/file level docstring.
"""

import requests
import numpy as np
import warnings

def download_data(location):
    '''downloads temperature data anomaly from Berkeley Earth for a given location
    
    Parameters
    ----------
    location: str
        name of the region
    
    Returns
    -------
    
    data: 2D numpy float array
        data table
    '''
    
    url = f'http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/{location.lower()}-TAVG-Trend.txt'
    
    # Download the content of the URL
    response = requests.get(url)
    data = np.loadtxt(response.iter_lines(), comments="%")
    
    return data


def moving_avg(data,width):
    '''calculates moving average of temperature anomaly data
    
    Parameters
    ----------
    data: 1D numpy float array
        temperature data
    width: int
        half-width of the moving window used for averaging
    
    Returns
    -------
    moving_avg: 1D numy float array
        averaged data
    '''
    
    moving_avg = np.full(data.size, np.nan)
    for i in range(width, moving_avg.size - width):
        moving_avg[i] = np.mean(data[i - width:i + width])
   
    if len(np.where(np.isnan(moving_avg) == True)) > 0:
        warnings.warn('NAN alert!!!')
    return moving_avg

def extract_monthly_anomaly(data):
    """
    Extract the monthly anomaly from the data array and calculate a decimal
    year.
    
    Parameters
    ----------
    
    data: 1D numpy float array
    
    Returns
    -------
    
    decimal_year: float
    anomaly: 1D numpy float array
    
    """
    decimal_year = data[:, 0] + 1/12*(data[:, 1] - 1)
    anomaly = data[:, 2]
    return decimal_year, anomaly

    