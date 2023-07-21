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
