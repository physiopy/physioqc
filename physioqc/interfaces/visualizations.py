from typing import List

import matplotlib.pyplot as plt
import numpy as np
import peakdet as pk


def plot_raw_data(phys: pk.Physio):
    """Plots the raw data using peakdet.
    Parameters
    ----------
    phys : pk.Physio
        The data object, used for plotting.

    Returns
    -------
    typle(fig, axes)
        Returns the fig and axes object of the plot.
    """
    fig, axes = plt.subplots(1, 1, figsize=(10, 5))
    axes = pk.plot_physio(phys, ax=axes)

    return fig, axes


def plot_average_peak(phys: pk.Physio, window: List = [-3, 3]):
    """Plots the average amplitude of the signal around a peak and its
    standard deviation. Area around is given by the window list.

    Parameters
    ----------
    phys : pk.Physio
        The data object, used for plotting.
    window : List, optional
        The window size around the peak in s, by default [-3, 3]

    Returns
    -------
    typle(fig, axes)
        Returns the fig and axes object of the plot.
    """
    window = np.array(window)
    window = window * phys.fs
    window = window.astype(int)

    t = (np.arange(window[0], window[1] + 1)) / phys.fs

    peak_array = list()

    for ps in phys.peaks:
        # Check if the window covers a full peak.
        if (ps - window[0]) < 0 or (ps + window[1] + 1) > len(phys.data):
            pass
        else:
            peak_array.append(phys.data[ps + window[0] : ps + window[1] + 1])

    peak_array = np.array(peak_array)
    pmean = np.mean(peak_array, axis=0)
    pstd = np.std(peak_array)

    fig, axes = plt.subplots(1, 1, figsize=(7, 5))

    axes.plot(t, pmean)
    axes.fill_between(t, pmean - pstd, pmean + pstd, alpha=0.5)
    axes.scatter(0, pmean[t == 0], zorder=2)  # Adding a point for the peak.
    axes.set(xlabel="t in s", ylabel="Mean amplitude")

    return fig, axes
