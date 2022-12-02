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
        Calculate standard deviation across input channels
    args : signal
        ND array with signal of some human biometric data, hopefully from a living human.
        
    Returns
    -------
    std_val : N-sized array
        Standard deviation of signal.

    """

     std_val = np.std(signal, axis = 0)
    return std_val