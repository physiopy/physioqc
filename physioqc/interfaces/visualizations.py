from __future__ import annotations

from typing import List, Literal, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import peakdet as pk

from ..metrics import multimodal


def check_create_figure(
    ax: plt.axes = None, figsize=(10, 5)
) -> Tuple[plt.figure, plt.axes]:
    """Helper function to check if a new figure should be created or to further
    plot on axes.

    Parameters
    ----------
    ax : plt.axes, optional
        Check if axes object is present, if not creates new figure, by default None
    figsize : tuple, optional
        Size of the new figure (if created), by default (10, 5)

    Returns
    -------
    Tuple[plt.figure, plt.axes]
        Figure and axes objects of the plot.
    """

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
    else:
        fig = None

    return fig, ax


def plot_raw_data(phys: pk.Physio, ax: plt.axes = None) -> Tuple[plt.figure, plt.axes]:
    """Plots the raw data using peakdet.
    Parameters
    ----------
    phys : pk.Physio
        The data object, used for plotting.
    ax : plt.axes, optional
        axes object to use for plotting, by default None

    Returns
    -------
    Tuple[plt.figure, plt.axes]
        Figure and axes objects of the plot.
    """
    fig, ax = check_create_figure(ax, figsize=(7, 5))

    ax = pk.plot_physio(phys, ax=ax)

    return fig, ax


def plot_average_peak(
    phys: pk.Physio,
    window: List = [-3, 3],
    target_fs: float = 1000.0,
    peak_dist: float = 1.0,
    peak_thr: float = 0.1,
    plot_mode: Literal["traces", "ci", "auto"] = "auto",
    ax: plt.axes = None,
) -> Tuple[plt.figure, plt.axes]:
    """Plots peaks and their surroundings (defined by the window size). Depending
    on the setting, plotting traces or the confidence interval (1 SD) around the
    mean signal.

    Parameters
    ----------
    phys : pk.Physio
        data object, used for plotting.
    window : List, optional
        window size around the peak in s, by default [-3, 3]
    target_fs : float, optional
        sampling rate for plotting and peak detection, by default 1000.0, only
        applied if signal sampling rate is larger than target sampling rate.
    peak_dist : float, optional
        distance for peak detection, by default 1.0
    peak_thr : float, optional
        threshold for peak detection, by default 0.1
    plot_mode : Literal["traces", "ci", "auto"], optional
        to plot traces or standard deviation around signal, if left on "auto",
        traces are plotted when there are less than 2_500 detected peaks,
        otherwise uses the CI, y default 'auto'
    ax : plt.axes, optional
        axes object to use for plotting, by default None


    Returns
    -------
    Tuple[plt.figure, plt.axes]
        Figure and axes objects of the plot.

    Raises
    ------
    ValueError
        If an inappropriate plot type is chosen.
    """
    if plot_mode not in ["traces", "ci", "auto"]:
        raise ValueError('Plot mode has to be in ["traces", "ci", "auto"]')

    if phys.fs > target_fs:
        #  This should probably go to the logs, or warning
        print(
            f"Fs = {phys.fs} Hz is higher than target_fs ({target_fs} Hz), resampling to {target_fs} Hz"
        )
        phys = pk.operations.interpolate_physio(phys, target_fs, kind="linear")

    phys = multimodal.peak_detection(phys, peak_dist=peak_dist, peak_threshold=peak_thr)

    window = np.array(window) * phys.fs
    window = window.astype(int)

    window_range = np.arange(window[0], window[1] + 1)
    t = window_range / phys.fs

    # Excluding peaks at the very end and beginning, to avoid indexing errors,
    # i.e. only including peaks where we can extract a full window around it:
    peaks = list(
        filter(
            lambda ps: ((ps + window[0]) >= 0)
            and ((ps + window[1] + 1) < phys.data.shape[0]),
            phys.peaks,
        )
    )
    peak_array = np.zeros((len(peaks), t.shape[0]))

    for n, ps in enumerate(peaks):
        peak_array[n, :] = phys.data[ps + window[0] : ps + window[1] + 1]

    fig, ax = check_create_figure(ax, figsize=(7, 5))

    if plot_mode == "auto":
        if len(peaks) > 2_500:
            plot_mode = "ci"
        else:
            plot_mode = "traces"

    pmean = np.mean(peak_array, axis=0)
    ax.plot(t, pmean)
    if plot_mode == "ci":
        pstd = np.std(peak_array, axis=0)
        ax.fill_between(t, pmean - pstd, pmean + pstd, alpha=0.5)
    elif plot_mode == "traces":
        ax.plot(t, peak_array.T, color=[0.25, 0.25, 0.25], alpha=0.01, zorder=-1)

    ax.scatter(0, pmean[t == 0], zorder=2)  # Adding a point for the peak.
    ax.set(xlabel="t in s", ylabel="Peak height")

    return fig, ax


def plot_power_spectrum(
    phys: pk.Physio, ax: plt.axes = None
) -> Tuple[plt.figure, plt.axes]:
    """Plots the power spectrum of pk.Physio data.

    Parameters
    ----------
    phys : pk.Physio
        The data object, used for plotting.
    ax : plt.axes, optional
        axes object to use for plotting, by default None

    Returns
    -------
    Tuple[plt.figure, plt.axes]
        Figure and axes objects of the plot.
    """

    fig, ax = check_create_figure(ax, figsize=(7, 5))

    freqs, psd = multimodal.power_spectrum(phys)

    ax.plot(freqs, psd)
    ax.set(xlabel="Frequencies", ylabel="a.u.")
    return fig, ax


def plot_histogram(
    signal: np.array,
    ax: plt.axes = None,
    bins: int | Sequence[float] | str | None = 10,
) -> Tuple[plt.figure, plt.axes]:
    """
    Wrapper around matplotlibs histogram function.

    Parameters
    ----------
    signal : np.array
        Numpy array for histogram.
    ax : plt.axes, optional
        axes object to use for plotting, by default 10
    bins : int | Sequence[float] | str | None, optional
        If bins is an integer, defines the number of bins, if a Sequence defines
        the bin edges. See the matplotlib.pyplot.hist documentation for more details,
        by default 10

    Returns
    -------
    Tuple[plt.figure, plt.axes]
        Figure and axes objects of the plot.
    """

    fig, ax = check_create_figure(ax, figsize=(7, 5))

    ax.hist(signal, bins=bins)

    return fig, ax
