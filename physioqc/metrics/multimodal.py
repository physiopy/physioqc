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


def peak_distance(ph: pk.Physio, perc: List = [5, 95]):
    """Calculates the timing between peaks and returns a dictionary containing
    diferent metrics.

    Parameters
    ----------
    ph : pk.Physio
        A pk.Physio object, that contains peak information.
    perc : List, optional
        Percentiles to calculate, by default [5, 95]

    Returns
    -------
    Dict
        A metric_dictionarys
    """

    # TODO Check if peaks have been estimated.
    diff_peak = np.diff(ph.peaks, axis=0)

    metric_dict = metric_dictionary(diff_peak, perc=perc)

    return metric_dict


def peak_amplitude(ph: pk.Physio, perc: List = [5, 95]):
    """Calculates different metrics for the amplitude of peaks (peak - trough).

    Parameters
    ----------
    ph : pk.Physio
        pk.Physio object with peak and trough information.
    perc : List, optional
        Percentiles to calculate, by default [5, 95]

    Returns
    -------
    Dict
        A metric dictionary
    """

    # TODO Check if peaks have been estimated.
    # Assuming that peaks and troughs are aligned. Last peak has no trough.
    peak_amp = ph.data[ph.peaks[:-1]]
    trough_amp = ph.data[ph.troughs]
    peak_amplitude = peak_amp - trough_amp

    metric_dict = metric_dictionary(peak_amplitude, perc=perc)

    return metric_dict
