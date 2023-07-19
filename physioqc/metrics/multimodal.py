"""These functions compute RETROICOR regressors (Glover et al. 2000)."""
# import file
import numpy as np
import peakdet as pk

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
    Calculate temporal signal to noise ration of signal.

    Parameters
    ----------
    tSNR : function
        Calculate temporal signal to noise ratio.
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

def peak_detection(data: pk.Physio, target_fs: float = 40.0, filter_cutoff: float = 2.0,
                   filter_method: str = "lowpass", filter_order: int = 7,
                   peak_threshold: float = 0.1, peak_dist: int = 60):
    """
    Perform peak detection for further metric extraction and plotting.

    Parameters
    ----------
    data : pk.Physio
        A peakdet Physio object
    target_fs : float, optional
        Sampling rate for interpolation, by default 40.0
    filter_cutoff : float, optional
        Filter cutoff for filtering step, by default 2.0
    filter_method : str, optional
        Filter for filtering step, by default "lowpass"
    filter_order : int, optional
        Filter order for filtering step, by default 7
    peak_threshold : float, optional
        Threshold for peak detection, by default 0.1
    peak_dist : int, optional
        Distance for peak detection, by default 60

    Returns
    -------
    pk.Physio
        Updated pk.Physio class with peaks etc.
    """
    # Downsample the signal - we don't need more than 40 Hz with our MRI data sampling
    ph = pk.operations.interpolate_physio(data, target_fs, kind="linear")
    # Apply a lowpass filter to remove the extreme high frequencies
    ph = pk.operations.filter_physio(ph, filter_cutoff, method=filter_method, order=filter_order)
    ph = pk.operations.peakfind_physio(ph, thresh=peak_threshold, dist=peak_dist)

    return ph

