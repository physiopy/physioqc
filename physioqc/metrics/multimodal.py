"""These functions compute various non-modality dependent signal processing metrics."""

import warnings

import numpy as np
import peakdet as pk
from scipy import signal

from .utils import has_peakfind_physio, physio_or_numpy


@physio_or_numpy
def signal_fct(signal):
    """
    Wrapper that turns the object into a function for loop

    Parameters
    ----------
    signal : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    signal : np.array or peakdet Physio object
        Physiological data
    """
    return signal


@physio_or_numpy
def std(signal):
    """
    Calculate standard deviation across input channels of signal.

    Parameters
    ----------
    signal : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Standard deviation of signal.
    """
    std_val = np.std(signal, axis=0)
    return std_val


@physio_or_numpy
def mean(signal: np.array):
    """
    Calculate mean across input channels of signal.

    Parameters
    ----------
    signal : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Mean of signal.
    """
    mean_val = np.mean(signal, axis=0)
    return mean_val


@physio_or_numpy
def tSNR(signal):
    """
    Calculate temporal signal to noise ratio of signal.

    Parameters
    ----------
    signal : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Temporal signal to noise ratio of signal.
    """
    tSNR_val = np.mean(signal, axis=0) / np.std(signal, axis=0)
    return tSNR_val


@physio_or_numpy
def CoV(signal):
    """
    Calculate coefficient of variation of signal.

    Parameters
    ----------
    signal : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        Temporal signal to noise ratio of signal.
    """
    cov_val = np.std(signal, axis=0) / np.mean(signal, axis=0)
    return cov_val


@physio_or_numpy
def min(signal: np.array):
    """
    Calculate min across input channels of signal.

    Parameters
    ----------
    signal : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        min of signal.
    """
    min_val = np.min(signal, axis=0)
    return min_val


@physio_or_numpy
def max(signal: np.array):
    """
    Calculate max across input channels of signal.

    Parameters
    ----------
    signal : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    N-sized array :obj:`numpy.ndarray`
        max of signal.
    """
    max_val = np.max(signal, axis=0)
    return max_val


@physio_or_numpy
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
    p_high, p_low = np.percentile(signal, [q_high, q_low], axis=0)
    iqr_val = p_high - p_low

    return iqr_val


@physio_or_numpy
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
    perc_val = np.percentile(signal, axis=0, q=perc)

    return perc_val


def peak_detection(
    data: pk.Physio,
    peak_threshold: float = 0.1,
    peak_dist: float = 60.0,
):
    """
    Perform peak detection for further metric extraction and plotting.

    Parameters
    ----------
    data : pk.Physio
        A peakdet Physio object
    peak_threshold : float, optional
        Threshold for peak detection, by default 0.1
    peak_dist : float, optional
        Distance for peak detection, by default 60.0

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
    if not has_peakfind_physio(ph):
        warnings.warn("Peaks not estimated, estimating")
        ph = peak_detection(ph)

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
    if not has_peakfind_physio(ph):
        warnings.warn("Peaks not estimated, estimating")
        ph = peak_detection(ph)
    # Assuming that peaks and troughs are aligned. Last peak has no trough.
    peak_amp = ph.data[ph.peaks[:-1]]
    trough_amp = ph.data[ph.troughs]
    peak_amplitude = peak_amp - trough_amp

    return peak_amplitude


def power_spectrum(data):
    """
    Compute the power spectrum of the signal.

    Parameters
    ----------
    args : data
        a peakdet Physio object

    Returns
    -------
    tuple :obj: tuple
        A tuple containing as the first element the frequencies and the second element
        the power spectrum
    """
    freqs, psd = signal.welch(data.data, data.fs)

    return freqs, psd


def energy(data, lowf=None, highf=None):
    """
    Calculate the energy in a certain frequency band.

    Parameters
    ----------
    args : data
        a peakdet Physio object
    args : lowf
        float that corresponds to the lower frequency band limit
    args : highf
        float that corresponds to the higher frequency band limit

    Returns
    -------
    Float :obj:`numpy.ndarray`
        Energy in the defined frequency band
    """
    freqs, psd = power_spectrum(data)

    # Energy is defined as the square of the power spectral density
    energy_density = np.square(psd)

    if lowf is None or highf is None:
        # If frequencies are not defined, compute the total power
        idx_band = np.ones(psd.shape).astype(bool)
    else:
        # Define frequency band
        idx_band = np.logical_and(freqs >= lowf, freqs <= highf)

    energy = np.sum(energy_density[idx_band])

    return energy


def fALFF(data, lowf=0, highf=0.5):
    """
    Calculate the fractional amplitude of low-frequency fluctuations (fALFF).

    fALLF corresponds to the ratio of the energy in a frequency band over the
    total energy.

    Parameters
    ----------
    args : data
        a peakdet Physio object
    args : lowf
        float that corresponds to the lower frequency band limit
    args : highf
        float that corresponds to the higher frequency band limit

    Returns
    -------
    Float :obj:`numpy.ndarray`
        fALFF

    Note
    -------
    The default value of lowf and highf were set randomly. Please update them with more meaningful value
    """
    # Extract energy in the frequency band
    band_energy = energy(data, lowf=lowf, highf=highf)

    # Extract total energy
    total_energy = energy(data)

    # Compute the relative energy
    rel_energy = band_energy / total_energy

    return rel_energy


def freq_energy(data, thr=0.5):
    """
    Compute the minimum frequency with energy higher than the threshold.

    Parameters
    ----------
    args : data
        a peakdet Physio object
    args : thr
        Power threshold

    Returns
    -------
    Float :obj:`numpy.ndarray`
        Minimum frequency with power higher than the threshold

    Note
    ----
    The value of the threshold has been selected randomly for now. Please update it with a more meaningful value.
    """
    energy_nd = energy(data)
    freq = np.argmax(energy_nd > thr)

    return freq
