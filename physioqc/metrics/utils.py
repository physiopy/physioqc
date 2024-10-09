"""Miscellaneous utility functions for metric calculation."""

import functools
import logging

from peakdet.physio import Physio

LGR = logging.getLogger(__name__)
LGR.setLevel(logging.INFO)


def print_metric_call(metric, args):
    """
    Log a message to describe how a metric is being called.

    Parameters
    ----------
    metric : function
        Metric function that is being called
    args : dict
        Dictionary containing all arguments that are used to parametrise metric

    Notes
    -----
    Outcome
        An info-level message for the logger.
    """
    msg = f"The {metric} regressor will be computed using the following parameters:"

    for arg in args:
        msg = f"{msg}\n    {arg} = {args[arg]}"

    msg = f"{msg}\n"

    LGR.info(msg)


def physio_or_numpy(func):
    """
    Check if the function input is a Physio object or a np.ndarray-like object.

    The "signal" argument must always be the first one.

    Parameters
    ----------
    func: function to run the wrapper around

    Returns
    -------
    function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # signal/data must always be args[0]
        if hasattr(args[0], "history"):
            args = (args[0].data,) + args[1:]
        return func(*args, **kwargs)

    return wrapper


def has_peaks(signal: Physio) -> bool:
    """Check if the signal is a Physio object and has (at least 2) peaks.

    Parameters
    ----------
    signal : peakdet.physio.Physio
        Physio object.

    Returns
    -------
    bool
        Boolean if peakfind_physio is in history.

    Raises
    ------
    AttributeError
        Raises error if object does not have a history attribute.
    """
    if not hasattr(signal, "history"):
        raise AttributeError("Signal has to be a peakdet Physio object!")

    if signal._metadata["peaks"].size == 1:
        LGR.warn("Signal has only one peak! Better to rerun peak detection.")

    return signal._metadata["peaks"].size > 1
