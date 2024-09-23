"""Miscellaneous utility functions for metric calculation."""

import functools
import logging

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
        # signal must always be args[0]
        if hasattr(args[0], "history"):
            args[0] = args[0].data
        return func(*args, **kwargs)

    return wrapper


def has_peakfind_physio(signal) -> bool:
    """Check if "peakfind_physio" is in signal's history.

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
        raise AttributeError("Signal has to be a Physio object!")

    has_peakfind = any(["peakfind_physio" in i for i in signal.history])

    return has_peakfind
