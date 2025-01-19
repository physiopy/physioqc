"""Miscellaneous utility functions for metric calculation."""

import json
import os
import functools
import logging

import numpy as np
import pandas as pd

from peakdet.physio import Physio

LGR = logging.getLogger(__name__)
LGR.setLevel(logging.INFO)

from scipy import signal

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


# - butterworth filters
# @conditionaljit()
def butterlpfiltfilt(Fs, upperpass, inputdata, order, debug=False):
    r"""Performs a bidirectional (zero phase) Butterworth lowpass filter on an input vector
    and returns the result.  Ends are padded to reduce transients.

    Parameters
    ----------
    Fs : float
        Sample rate in Hz
        :param Fs:

    upperpass : float
        Upper end of passband in Hz
        :param upperpass:

    inputdata : 1D numpy array
        Input data to be filtered
        :param inputdata:

    order : int
        Order of Butterworth filter.
        :param order:

    debug : boolean, optional
        When True, internal states of the function will be printed to help debugging.
        :param debug:

    Returns
    -------
    filtereddata : 1D float array
        The filtered data

    """
    if upperpass > Fs / 2.0:
        upperpass = Fs / 2.0
    if debug:
        print(
            "butterlpfiltfilt - Fs, upperpass, len(inputdata), order:",
            Fs,
            upperpass,
            len(inputdata),
            order,
        )
    sos = signal.butter(order, 2.0 * upperpass, btype="lowpass", output="sos", fs=Fs)
    return signal.sosfiltfilt(sos, inputdata).real


# @conditionaljit()
def butterhpfiltfilt(Fs, lowerpass, inputdata, order, debug=False):
    r"""Performs a bidirectional (zero phase) Butterworth highpass filter on an input vector
    and returns the result.  Ends are padded to reduce transients.

    Parameters
    ----------
    Fs : float
        Sample rate in Hz
        :param Fs:

    lowerpass : float
        Lower end of passband in Hz
        :param lowerpass:

    inputdata : 1D numpy array
        Input data to be filtered
        :param inputdata:

    order : int
        Order of Butterworth filter.
        :param order:

    debug : boolean, optional
        When True, internal states of the function will be printed to help debugging.
        :param debug:

    Returns
    -------
    filtereddata : 1D float array
        The filtered data
    """
    if lowerpass < 0.0:
        lowerpass = 0.0
    if debug:
        print(
            "butterhpfiltfilt - Fs, lowerpass, len(inputdata), order:",
            Fs,
            lowerpass,
            len(inputdata),
            order,
        )
    sos = signal.butter(order, 2.0 * lowerpass, btype="highpass", output="sos", fs=Fs)
    return signal.sosfiltfilt(sos, inputdata).real


# @conditionaljit()
def butterbpfiltfilt(Fs, lowerpass, upperpass, inputdata, order, debug=False):
    r"""Performs a bidirectional (zero phase) Butterworth bandpass filter on an input vector
    and returns the result.  Ends are padded to reduce transients.

    Parameters
    ----------
    Fs : float
        Sample rate in Hz
        :param Fs:

    lowerpass : float
        Lower end of passband in Hz
        :param lowerpass:

    upperpass : float
        Upper end of passband in Hz
        :param upperpass:

    inputdata : 1D numpy array
        Input data to be filtered
        :param inputdata:

    order : int
        Order of Butterworth filter.
        :param order:

    debug : boolean, optional
        When True, internal states of the function will be printed to help debugging.
        :param debug:

    Returns
    -------
    filtereddata : 1D float array
        The filtered data
    """
    if upperpass > Fs / 2.0:
        upperpass = Fs / 2.0
    if lowerpass < 0.0:
        lowerpass = 0.0
    if debug:
        print(
            f"butterbpfiltfilt - {Fs=}, {lowerpass=}, {upperpass=}, {len(inputdata)=}, {order=}"
        )
    sos = signal.butter(
        order, [2.0 * lowerpass, 2.0 * upperpass], btype="bandpass", output="sos", fs=Fs
    )
    if debug:
        print(sos)
    return signal.sosfiltfilt(sos, inputdata).real


def readbidstsv(inputfilename, colspec=None, warn=True, debug=False):
    r"""Read time series out of a BIDS tsv file

    Parameters
    ----------
    inputfilename : str
        The root name of the tsv and accompanying json file (no extension)
    colspec: list
        A comma separated list of column names to return
    debug : bool
        Output additional debugging information

    Returns
    -------
        samplerate : float
            Sample rate in Hz
        starttime : float
            Time of first point, in seconds
        columns : str array
            Names of the timecourses contained in the file
        data : 2D numpy array
            Timecourses from the file

    NOTE:  If file does not exist or is not valid, all return values are None

    """
    thefileroot, theext = os.path.splitext(inputfilename)
    if theext == ".gz":
        thefileroot, thenextext = os.path.splitext(thefileroot)
        if thenextext is not None:
            theext = thenextext + theext

    if debug:
        print("thefileroot:", thefileroot)
        print("theext:", theext)
    if os.path.exists(thefileroot + ".json") and (
        os.path.exists(thefileroot + ".tsv.gz") or os.path.exists(thefileroot + ".tsv")
    ):
        with open(thefileroot + ".json", "r") as json_data:
            d = json.load(json_data)
            try:
                samplerate = float(d["SamplingFrequency"])
            except:
                print("no samplerate found in json, setting to 1.0")
                samplerate = 1.0
                if warn:
                    print(
                        "Warning - SamplingFrequency not found in "
                        + thefileroot
                        + ".json.  This is not BIDS compliant."
                    )
            try:
                starttime = float(d["StartTime"])
            except:
                print("no starttime found in json, setting to 0.0")
                starttime = 0.0
                if warn:
                    print(
                        "Warning - StartTime not found in "
                        + thefileroot
                        + ".json.  This is not BIDS compliant."
                    )
            try:
                columns = d["Columns"]
            except:
                if debug:
                    print(
                        "no columns found in json, will take labels from the tsv file"
                    )
                columns = None
                if warn:
                    print(
                        "Warning - Columns not found in "
                        + thefileroot
                        + ".json.  This is not BIDS compliant."
                    )
            else:
                columnsource = "json"
        if os.path.exists(thefileroot + ".tsv.gz"):
            compression = "gzip"
            theextension = ".tsv.gz"
        else:
            compression = None
            theextension = ".tsv"
            if warn:
                print(
                    "Warning - "
                    + thefileroot
                    + ".tsv is uncompressed.  This is not BIDS compliant."
                )

        df = pd.read_csv(
            thefileroot + theextension,
            compression=compression,
            names=columns,
            header=None,
            sep="\t",
            quotechar='"',
        )

        # check for header line
        if any(df.iloc[0].apply(lambda x: isinstance(x, str))):
            headerlinefound = True
            # reread the data, skipping the first row
            df = pd.read_csv(
                thefileroot + theextension,
                compression=compression,
                names=columns,
                header=0,
                sep="\t",
                quotechar='"',
            )
            if warn:
                print(
                    "Warning - Column header line found in "
                    + thefileroot
                    + ".tsv.  This is not BIDS compliant."
                )
        else:
            headerlinefound = False

        if columns is None:
            columns = list(df.columns.values)
            columnsource = "tsv"
        if debug:
            print(
                samplerate,
                starttime,
                columns,
                np.transpose(df.to_numpy()).shape,
                (compression == "gzip"),
                warn,
                headerlinefound,
            )

        # select a subset of columns if they were specified
        if colspec is None:
            return (
                samplerate,
                starttime,
                columns,
                np.transpose(df.to_numpy()),
                (compression == "gzip"),
                columnsource,
            )
        else:
            collist = colspec.split(",")
            try:
                selectedcols = df[collist]
            except KeyError:
                print("specified column list cannot be found in", inputfilename)
                return [None, None, None, None, None, None]
            columns = list(selectedcols.columns.values)
            return (
                samplerate,
                starttime,
                columns,
                np.transpose(selectedcols.to_numpy()),
                (compression == "gzip"),
                columnsource,
            )
    else:
        print("file pair does not exist")
        return [None, None, None, None, None, None]


hammingwindows = {}


def hamming(length, debug=False):
    #   return 0.54 - 0.46 * np.cos((np.arange(0.0, float(length), 1.0) / float(length)) * 2.0 * np.pi)
    r"""Returns a Hamming window function of the specified length.  Once calculated, windows
    are cached for speed.

    Parameters
    ----------
    length : int
        The length of the window function
        :param length:

    debug : boolean, optional
        When True, internal states of the function will be printed to help debugging.
        :param debug:

    Returns
    -------
    windowfunc : 1D float array
        The window function
    """
    try:
        return hammingwindows[str(length)]
    except KeyError:
        hammingwindows[str(length)] = 0.54 - 0.46 * np.cos(
            (np.arange(0.0, float(length), 1.0) / float(length)) * 2.0 * np.pi
        )
        if debug:
            print("initialized hamming window for length", length)
        return hammingwindows[str(length)]
