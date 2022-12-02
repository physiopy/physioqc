"""These functions compute RETROICOR regressors (Glover et al. 2000)."""
# import file
import numpy as np

from .. import references
from ..due import due


def std(signal):  
    """
    Calculate standard deviation across input channels of signal.
    
    Parameters
    ----------
    std : function
        Calculate standard deviation across input channels.
    args : signal (X, n) :obj:`numpy.ndarray`
        ND array with signal of some human biometric data, hopefully from a living human.
        signal, of shape (n_channels, )
        
    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Standard deviation of signal.
    """
    std_val = np.std(signal, axis=0)
    return std_val


def tSNR(signal):  
    """
    Calculate standard deviation across input channels of signal.
    
    Parameters
    ----------
    tSNR : function
        Calculate temporal signal to noise ration
    args : signal
        ND array with signal of some human biometric data, hopefully from a living human.
        
    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Temporal signal to noise ratio of signal.
    """
    me = np.mean(signal, axis=0)
    std = np.std(signal, axis=0)
    tSNR_val = me / std
    return tSNR_val
    