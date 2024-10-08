"""These functions compute various non-modality dependent signal processing metrics."""

import warnings

import numpy as np
from peakdet import Physio
from peakdet.operations import peakfind_physio
from scipy import signal

from .utils import has_peaks, physio_or_numpy


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
    return np.std(signal, axis=0)


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
    return np.mean(signal, axis=0)


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
    return np.mean(signal, axis=0) / np.std(signal, axis=0)


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
    return np.std(signal, axis=0) / np.mean(signal, axis=0)


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
    return np.min(signal, axis=0)


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
    return np.max(signal, axis=0)


@physio_or_numpy
def max_amplitude(signal: np.array):
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
    return np.max(signal, axis=0) - np.min(signal, axis=0)


@physio_or_numpy
def IQR(signal: np.array, q_high: float = 75, q_low: float = 25):
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

    return p_high - p_low


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
    return np.percentile(signal, q=perc, axis=0)


def peak_detection(
    data: Physio,
    peak_threshold: float = 0.1,
    peak_dist: float = 60.0,
):
    """
    Perform peak detection for further metric extraction and plotting.

    Parameters
    ----------
    data : Physio
        A peakdet Physio object
    peak_threshold : float, optional
        Threshold for peak detection, by default 0.1
    peak_dist : float, optional
        Distance for peak detection, by default 60.0

    Returns
    -------
    Physio
        Updated Physio class with peaks etc.
    """
    return peakfind_physio(data, thresh=peak_threshold, dist=peak_dist)


def peak_distance(
    ph: Physio,
    peak_threshold: float = 0.1,
    peak_dist: float = 60.0,
):
    """Calculate the time (in seconds) between peaks (first derivative of onsets).

    Parameters
    ----------
    ph : Physio
        A Physio object, that contains peak information.

    Returns
    -------
    np.array
        np.array of shape [npeaks, ]
    """
    if not has_peaks(ph):
        warnings.warn("Peaks not estimated, estimating")
        ph = peakfind_physio(ph, thresh=peak_threshold, dist=peak_dist)

    return np.diff(ph.peaks, axis=0) / ph.fs


def peak_amplitude(
    ph: Physio,
    peak_threshold: float = 0.1,
    peak_dist: float = 60.0,
):
    """Return the amplitude for each peak in the ph.Physio object (peak - trough).

    Parameters
    ----------
    ph : Physio
        Physio object with peak and trough information.

    Returns
    -------
    np.array
        np.array of shape [npeaks - 1, ]
    """
    if not has_peaks(ph):
        warnings.warn("Peaks not estimated, estimating")
        ph = peakfind_physio(ph, thresh=peak_threshold, dist=peak_dist)
    # Assuming that peaks and troughs are aligned. Last peak has no trough.
    peak_amp = ph.data[ph.peaks[:-1]]
    trough_amp = ph.data[ph.troughs]
    return peak_amp - trough_amp


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

    return np.sum(energy_density[idx_band])


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
    return band_energy / total_energy


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
    return np.argmax(energy_nd > thr)
