"""These functions compute RETROICOR regressors (Glover et al. 2000)."""
# import file
from typing import List

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


def mean(signal: np.array):
    """
    Calculate mean across input channels of signal.

    Parameters
    ----------
    mean : function
        Calculate mean over input channels.
    args : signal (X, n) :obj:`numpy.ndarray`
        ND array with signal of some human biometric data, hopefully from a living human.
        signal, of shape (n_channels, )

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Mean of signal.
    """
    mean_val = np.mean(signal, axis=0)
    return mean_val


def min(signal: np.array):
    """
    Calculate min across input channels of signal.

    Parameters
    ----------
    min : function
        Calculate min over input channels.
    args : signal (X, n) :obj:`numpy.ndarray`
        ND array with signal of some human biometric data, hopefully from a living human.
        signal, of shape (n_channels, )

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        min of signal.
    """
    min_val = np.min(signal, axis=0)
    return min_val


def max(signal: np.array):
    """
    Calculate max across input channels of signal.

    Parameters
    ----------
    max : function
        Calculate max over input channels.
    args : signal (X, n) :obj:`numpy.ndarray`
        ND array with signal of some human biometric data, hopefully from a living human.
        signal, of shape (n_channels, )

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        max of signal.
    """
    max_val = np.max(signal, axis=0)
    return max_val


def peak_detection(
    data: pk.Physio,
    peak_threshold: float = 0.1,
    peak_dist: int = 60,
):
    """
    Perform peak detection for further metric extraction and plotting.

    Parameters
    ----------
    data : pk.Physio
        A peakdet Physio object
    peak_threshold : float, optional
        Threshold for peak detection, by default 0.1
    peak_dist : int, optional
        Distance for peak detection, by default 60

    Returns
    -------
    pk.Physio
        Updated pk.Physio class with peaks etc.
    """
    ph = pk.operations.peakfind_physio(data, thresh=peak_threshold, dist=peak_dist)

    return ph


def metric_dictionary(signal: np.array, perc: List = [5, 95]):
    """Creates a dictionary which contains statistics for a given signal.
    These include, mean, std, percentiles (in q), min, max.

    Parameters
    ----------
    signal : np.array
        Np.array containing the signal of size [nsamples, ]
    perc : List, optional
        Percentiles to compute from signal, by default [5, 95]

    Returns
    -------
    dict
        Dictionary with the different metrics.
    """

    metric_dict = {}

    metric_dict["mean"] = np.mean(signal, axis=0)

    metric_dict["std"] = np.std(signal, axis=0)

    for ii in perc:
        metric_dict[f"perc_{ii}"] = np.percentile(signal, q=ii, axis=0)

    metric_dict["max"] = np.max(signal, axis=0)
    metric_dict["min"] = np.min(signal, axis=0)

    return metric_dict


def peak_distance(ph: pk.Physio):
    """Calculates the time between peaks (first derivative of onsets).

    Parameters
    ----------
    ph : pk.Physio
        A pk.Physio object, that contains peak information.

    Returns
    -------
    np.array
        np.array of shape [npeaks, ]
    """

    # TODO Check if peaks have been estimated.
    diff_peak = np.diff(ph.peaks, axis=0)

    return diff_peak


def peak_amplitude(ph: pk.Physio):
    """Returns the amplitude for each peak in the ph.Physio object (peak - trough).

    Parameters
    ----------
    ph : pk.Physio
        pk.Physio object with peak and trough information.

    Returns
    -------
    np.array
        np.array of shape [npeaks - 1, ]
    """

    # TODO Check if peaks have been estimated.
    # Assuming that peaks and troughs are aligned. Last peak has no trough.
    peak_amp = ph.data[ph.peaks[:-1]]
    trough_amp = ph.data[ph.troughs]
    peak_amplitude = peak_amp - trough_amp

    return peak_amplitude
