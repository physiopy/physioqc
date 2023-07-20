"""These functions compute various non-modality dependent signal processing metrics."""
import numpy as np
import peakdet as pk

from .utils import physio_or_numpy


def std(signal):
    """
    Calculate standard deviation across input channels of signal.

    Parameters
    ----------
    signal : np.array
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Standard deviation of signal.
    """
    signal = physio_or_numpy(signal)
    std_val = np.std(signal, axis=0)
    return std_val


def mean(signal: np.array):
    """
    Calculate mean across input channels of signal.

    Parameters
    ----------
    signal : np.array
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Mean of signal.
    """
    signal = physio_or_numpy(signal)
    mean_val = np.mean(signal, axis=0)
    return mean_val


def tSNR(signal):
    """
    Calculate temporal signal to noise ratio of signal.

    Parameters
    ----------
    signal : np.array
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Temporal signal to noise ratio of signal.
    """
    signal = physio_or_numpy(signal)
    tSNR_val = np.mean(signal, axis=0) / np.std(signal, axis=0)
    return tSNR_val


def CoV(signal):
    """
    Calculate coefficient of variation of signal.

    Parameters
    ----------
    signal : np.array
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Temporal signal to noise ratio of signal.
    """
    signal = physio_or_numpy(signal)
    tSNR_val = np.std(signal, axis=0) / np.mean(signal, axis=0)
    return tSNR_val


def min(signal: np.array):
    """
    Calculate min across input channels of signal.

    Parameters
    ----------
    signal : np.array
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        min of signal.
    """
    signal = physio_or_numpy(signal)
    min_val = np.min(signal, axis=0)
    return min_val


def max(signal: np.array):
    """
    Calculate max across input channels of signal.

    Parameters
    ----------
    signal : np.array
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        max of signal.
    """
    signal = physio_or_numpy(signal)
    max_val = np.max(signal, axis=0)
    return max_val


def iqr(signal: np.array, q_high: float = 75, q_low: float = 25):
    """Calculate the Inter Quantile Range (IQR) over the input signal.

    Parameters
    ----------
    signal : np.array
        Physiological data
    q_high : float, optional
        higher percentile for IQR, by default 75
    q_low : float, optional
        lower percentile for IQR, by default 25

    Returns
    -------
    np.array
        iqr of the signal
    """
    signal = physio_or_numpy(signal)
    p_high, p_low = np.percentile(signal, [q_high, q_low], axis=0)
    iqr_val = p_high - p_low

    return iqr_val


def percentile(signal: np.array, perc: float = 2):
    """Calculate the percentile perc over the signal.

    Parameters
    ----------
    signal : np.array
        Physiological data
    perc : float, optional
        percentile for data, by default 2

    Returns
    -------
    np.array
        percentile of the signal
    """
    signal = physio_or_numpy(signal)
    perc_val = np.percentile(signal, axis=0, q=perc)

    return perc_val


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


def peak_distance(ph: pk.Physio):
    """Calculate the time between peaks (first derivative of onsets).

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
    """Return the amplitude for each peak in the ph.Physio object (peak - trough).

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
