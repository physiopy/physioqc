"""Denoising metrics for cardio recordings."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from numpy.polynomial import Polynomial
from peakdet import operations
from scipy.signal import resample, welch
from scipy.stats import kurtosis, pearsonr, skew

from .. import references
from ..due import due
from .chest_belt import romanosqi
from .utils import butterbpfiltfilt, butterlpfiltfilt, hamming


def cardiacprefilter(rawcard, Fs, lowerpass=0.1, upperpass=10.0, order=1, debug=False):
    if debug:
        print(
            f"cardiacprefilter: Fs={Fs} order={order}, lowerpass={lowerpass}, upperpass={upperpass}"
        )
    return butterbpfiltfilt(Fs, lowerpass, upperpass, rawcard, order, debug=debug)


def cardenvelopefilter(squarevals, Fs, upperpass=0.25, order=8, debug=False):
    if debug:
        print(f"cardenvelopefilter: Fs={Fs} order={order}, upperpass={upperpass}")
    return butterlpfiltfilt(Fs, upperpass, squarevals, order, debug=debug)


def trendgen(thexvals, thefitcoffs, demean):
    """

    Parameters
    ----------
    thexvals: array-like
        The x-axis value at which to calculate the trend
    thefitcoffs: array-like
        The polynomial coefficients used to calculate the trend
    demean: bool
        Flag to determine if data should be demeaned

    Returns
    -------

    """
    theshape = thefitcoffs.shape
    order = theshape[0] - 1
    thepoly = thexvals
    thefit = 0.0 * thexvals
    if order > 0:
        for i in range(1, order + 1):
            thefit += thefitcoffs[order - i] * thepoly
            thepoly = np.multiply(thepoly, thexvals)
    if demean:
        thefit = thefit + thefitcoffs[order]
    return thefit


def detrend(inputdata, order=1, demean=False):
    """

    Parameters
    ----------
    inputdata: array-like
        The waveform to be corrected
    order: int
        The order of the polynomial
    demean: bool
        Flag to determine if data should be demeaned

    Returns
    -------
    outputdata: array-like
        The input waveform with the polynomial baseline removed

    """
    thetimepoints = np.arange(0.0, len(inputdata), 1.0) - len(inputdata) / 2.0
    try:
        thecoffs = Polynomial.fit(thetimepoints, inputdata, order).convert().coef[::-1]
    except np.lib.polynomial.RankWarning:
        thecoffs = [0.0, 0.0]
    thefittc = trendgen(thetimepoints, thecoffs, demean)
    return inputdata - thefittc


@due.dcite(references.ELGENDI_2016)
def calcplethskeqwness(
    waveform,
    Fs,
    S_windowsecs=5.0,
    detrendorder=8,
    debug=False,
):
    """

    Parameters
    ----------
    waveform: array-like
        The cardiac waveform to be assessed
    Fs: float
        The sample rate of the data
    S_windowsecs: float
        Skewness window duration in seconds.  Defaults to 5.0 (optimal for discrimination of "good" from "acceptable"
        and "unfit" according to Elgendi)
    detrendorder: int
        Order of detrending polynomial to apply to plethysmogram.
    debug: boolean
        Turn on extended output

    Returns
    -------
    S_sqi_mean: float
        The mean value of the quality index over all time
    S_std_mean: float
        The standard deviation of the quality index over all time
    S_waveform: array
        The quality metric over all timepoints


    Calculates the windowed skewness quality metric described in Elgendi, M. in
    "Optimal Signal Quality Index for Photoplethysmogram Signals". Bioengineering 2016, Vol. 3, Page 21 3, 21 (2016).
    """

    # waveform = physio_or_numpy(waveform)

    # detrend the waveform
    dt_waveform = detrend(waveform, order=detrendorder, demean=True)

    # calculate S_sqi and K_sqi over a sliding window.  Window size should be an odd number of points.
    S_windowpts = int(np.round(S_windowsecs * Fs, 0))
    S_windowpts += 1 - S_windowpts % 2
    S_waveform = dt_waveform * 0.0

    if debug:
        print("S_windowsecs, S_windowpts:", S_windowsecs, S_windowpts)
    for i in range(0, len(dt_waveform)):
        startpt = np.max([0, i - S_windowpts // 2])
        endpt = np.min([i + S_windowpts // 2, len(dt_waveform)])
        S_waveform[i] = skew(dt_waveform[startpt : endpt + 1], nan_policy="omit")

    S_sqi_mean = np.mean(S_waveform)
    S_sqi_std = np.std(S_waveform)

    return S_sqi_mean, S_sqi_std, S_waveform


@due.dcite(references.ELGENDI_2016)
def calcplethkurtosis(
    waveform,
    Fs,
    K_windowsecs=60.0,
    detrendorder=8,
    debug=False,
):
    """

    Parameters
    ----------
    waveform: array-like
        The cardiac waveform to be assessed
    Fs: float
        The sample rate of the data
    K_windowsecs: float
        Skewness window duration in seconds.  Defaults to 2.0 (after Selveraj)
    detrendorder: int
        Order of detrending polynomial to apply to plethysmogram.
    debug: boolean
        Turn on extended output

    Returns
    -------
    K_sqi_mean: float
        The mean value of the quality index over all time
    K_std_mean: float
        The standard deviation of the quality index over all time
    K_waveform: array
        The quality metric over all timepoints


    Calculates the windowed kurtosis quality metric described in Elgendi, M. in
    "Optimal Signal Quality Index for Photoplethysmogram Signals". Bioengineering 2016, Vol. 3, Page 21 3, 21 (2016).
    """
    # waveform = physio_or_numpy(waveform)

    # detrend the waveform
    dt_waveform = detrend(waveform, order=detrendorder, demean=True)

    # calculate S_sqi and K_sqi over a sliding window.  Window size should be an odd number of points.
    K_windowpts = int(np.round(K_windowsecs * Fs, 0))
    K_windowpts += 1 - K_windowpts % 2
    K_waveform = dt_waveform * 0.0

    if debug:
        print("K_windowsecs, K_windowpts:", K_windowsecs, K_windowpts)
    for i in range(0, len(dt_waveform)):
        startpt = np.max([0, i - K_windowpts // 2])
        endpt = np.min([i + K_windowpts // 2, len(dt_waveform)])
        K_waveform[i] = kurtosis(dt_waveform[startpt : endpt + 1], fisher=False)

    K_sqi_mean = np.mean(K_waveform)
    K_sqi_std = np.std(K_waveform)

    return K_sqi_mean, K_sqi_std, K_waveform


def approximateentropy(waveform, m, r):
    def _maxdist(x_i, x_j):
        return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

    def _phi(m):
        x = [[waveform[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        C = [
            len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0)
            for x_i in x
        ]
        return (N - m + 1.0) ** (-1) * sum(np.log(C))

    N = len(waveform)

    return abs(_phi(m + 1) - _phi(m))


@due.dcite(references.ELGENDI_2016)
def calcplethentropy(
    waveform,
    Fs,
    E_windowsecs=1.0,
    detrendorder=8,
    debug=False,
):
    """

    Parameters
    ----------
    waveform: array-like
        The cardiac waveform to be assessed
    Fs: float
        The sample rate of the data
    E_windowsecs: float
        Entropy window duration in seconds.  Defaults to 0.5 (after Selveraj)
    detrendorder: int
        Order of detrending polynomial to apply to plethysmogram.
    debug: boolean
        Turn on extended output

    Returns
    -------
    E_sqi_mean: float
        The mean value of the quality index over all time
    E_std_mean: float
        The standard deviation of the quality index over all time
    E_waveform: array
        The quality metric over all timepoints


    Calculates the windowed entropy quality metric described in Elgendi, M. in
    "Optimal Signal Quality Index for Photoplethysmogram Signals". Bioengineering 2016, Vol. 3, Page 21 3, 21 (2016).
    """
    # waveform = physio_or_numpy(waveform)

    # detrend the waveform
    dt_waveform = detrend(waveform, order=detrendorder, demean=True)

    # calculate S_sqi and K_sqi over a sliding window.  Window size should be an odd number of points.
    E_windowpts = int(np.round(E_windowsecs * Fs, 0))
    E_windowpts += 1 - E_windowpts % 2
    E_waveform = dt_waveform * 0.0

    if debug:
        print("E_windowsecs, E_windowpts:", E_windowsecs, E_windowpts)
    for i in range(0, len(dt_waveform)):
        startpt = np.max([0, i - E_windowpts // 2])
        endpt = np.min([i + E_windowpts // 2, len(dt_waveform)])
        r = 0.2 * np.std(dt_waveform[startpt : endpt + 1])
        E_waveform[i] = approximateentropy(dt_waveform[startpt : endpt + 1], 2, r)

    E_sqi_mean = np.mean(E_waveform)
    E_sqi_std = np.std(E_waveform)

    return E_sqi_mean, E_sqi_std, E_waveform


def cardiacsqi(rawresp, debug=False):
    """
    Calculate the breath by breath quality of the respiratory signal
    Parameters
    ----------
    rawresp: physio_like
        The raw respiratory signal
    debug: bool
        Print debug information and plot intermediate results

    Returns
    -------
    breathlist: list
        List of "breathinfo" dictionaries for each detected breath.  Each breathinfo dictionary contains:
            "startime", "centertime", and "endtime" of each detected breath in seconds from the start of the waveform,
            and "correlation" - the Pearson correlation of that breath waveform with the average waveform.

    """
    targetfs = 50.0
    prefilterlimits = [0.01, 5.0]
    seglength = 4.0
    segstep = 0.5
    envelopelpffreq = 0.1
    slidingfilterpctwidth = 10.0
    # The fastest credible cardiac rate is 200 bpm -> 0.3 seconds/heartbeat, so set the dist to be 75%
    # of that in points
    minperiod = 0.3
    distfrac = 0.75

    return romanosqi(
        rawresp,
        targetfs=targetfs,
        prefilterlimits=prefilterlimits,
        envelopelpffreq=envelopelpffreq,
        slidingfilterpctwidth=slidingfilterpctwidth,
        minperiod=minperiod,
        distfrac=distfrac,
        seglength=seglength,
        segstep=segstep,
        label="cardiac",
        debug=debug,
    )


def plotheartbeatqualities(heartbeatlist, totaltime=None):
    # set up the color codes
    color_0p9 = "#888888"
    color_0p8 = "#aa6666"
    color_0p7 = "#cc4444"
    color_bad = "#ff0000"

    if totaltime is None:
        totaltime = heartbeatlist[-1]["endtime"]

    # unpack the heartbeat information
    numheartbeats = len(heartbeatlist)
    theheartbeatlocs = np.zeros((numheartbeats), dtype=np.float64)
    theheartbeatcorrs = np.zeros((numheartbeats), dtype=np.float64)
    for thisheartbeat in range(numheartbeats):
        theheartbeatlocs[thisheartbeat] = heartbeatlist[thisheartbeat]["centertime"]
        theheartbeatcorrs[thisheartbeat] = heartbeatlist[thisheartbeat]["correlation"]

    # plot the heartbeat correlations, with lines indicating thresholds
    plt.plot(theheartbeatlocs, theheartbeatcorrs, ls="-", marker="o")
    plt.hlines(
        [0.9, 0.8, 0.7, 0.6],
        0.0,
        totaltime,
        colors=[color_0p9, color_0p8, color_0p7, color_bad],
        linestyles="solid",
        label=["th=0.9", "th=0.8", "th=0.7", "th=0.6"],
    )
    plt.title("Quality evaluation for each heartbeat")
    plt.xlabel("Time in seconds")
    plt.ylabel("Correlation with average heartbeat")
    plt.xlim([0, totaltime])
    plt.ylim([0, 1.05])
    plt.show()


def plotcardiacwaveformwithquality(waveform, heartbeatlist, Fs, plottype="rectangle"):
    # now plot the cardiac waveform, color coded for quality

    # set up the color codes
    color_0p9 = "#ff000000"
    color_0p8 = "#ff000044"
    color_0p7 = "#ff000088"
    color_bad = "#ff0000aa"

    # unpack the heartbeat information
    numheartbeats = len(heartbeatlist)
    theheartbeatlocs = np.zeros((numheartbeats), dtype=np.float64)
    theheartbeatcorrs = np.zeros((numheartbeats), dtype=np.float64)
    for thisheartbeat in range(numheartbeats):
        theheartbeatlocs[thisheartbeat] = heartbeatlist[thisheartbeat]["centertime"]
        theheartbeatcorrs[thisheartbeat] = heartbeatlist[thisheartbeat]["correlation"]

    # initialize the plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # plot the whole line if we're doing rectangle occlusion
    if plottype == "rectangle":
        xvals = np.linspace(0.0, len(waveform) / Fs, len(waveform), endpoint=False)
        plt.plot(xvals, waveform, color="black")
    yrange = np.max(waveform) - np.min(waveform)
    ymax = np.min(waveform) + yrange * 1.05
    ymin = np.max(waveform) - yrange * 1.05
    for thisheartbeat in range(numheartbeats):
        if theheartbeatcorrs[thisheartbeat] > 0.9:
            thecolor = color_0p9
        elif theheartbeatcorrs[thisheartbeat] > 0.8:
            thecolor = color_0p8
        elif theheartbeatcorrs[thisheartbeat] > 0.7:
            thecolor = color_0p7
        else:
            thecolor = color_bad
        startpt = int(heartbeatlist[thisheartbeat]["starttime"] * Fs)
        endpt = int(heartbeatlist[thisheartbeat]["endtime"] * Fs)
        if plottype == "rectangle":
            therectangle = Polygon(
                (
                    (heartbeatlist[thisheartbeat]["starttime"], ymin),
                    (heartbeatlist[thisheartbeat]["starttime"], ymax),
                    (heartbeatlist[thisheartbeat]["endtime"], ymax),
                    (heartbeatlist[thisheartbeat]["endtime"], ymin),
                ),
                fc=thecolor,
                ec=thecolor,
                lw=0,
            )
            ax.add_patch(therectangle)
            pass
        else:
            if endpt == len(waveform) - 1:
                endpt -= 1
            xvals = np.linspace(
                startpt / Fs, (endpt + 1) / Fs, endpt - startpt + 1, endpoint=False
            )
            yvals = waveform[startpt : endpt + 1]
            plt.plot(xvals, yvals, color=thecolor)
    plt.ylim([ymin, ymax])
    plt.title("Cardiac waveform, color coded by quantifiability")
    plt.xlabel("Time in seconds")
    plt.ylabel("Amplitude (arbitrary units)")
    plt.xlim([0.0, len(waveform) / Fs])
    plt.show()


def summarizeheartbeats(heartbeatlist):
    numheartbeats = len(heartbeatlist)
    for thisheartbeat in range(numheartbeats):
        theheartbeatinfo = heartbeatlist[thisheartbeat]
        print(
            f"{thisheartbeat},{theheartbeatinfo['starttime']},{theheartbeatinfo['endtime']},{theheartbeatinfo['centertime']},{theheartbeatinfo['correlation']}"
        )
