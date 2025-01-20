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
from .utils import butterbpfiltfilt, butterlpfiltfilt, hamming, physio_or_numpy


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


@due.dcite(references.ROMANO_2023)
def cardiacsqi(rawcard, Fs, debug=False):
    """Implementation of Romano's method from A Signal Quality Index for Improving the Estimation of
    Breath-by-Breath cardiac Rate During Sport and Exercise,
    IEEE SENSORS JOURNAL, VOL. 23, NO. 24, 15 DECEMBER 2023"""

    # rawcard = physio_or_numpy(rawcard)

    # get the sample frequency down to around 25 Hz for cardiac waveforms
    targetfreq = 50.0
    if Fs > targetfreq:
        dsfac = int(Fs / targetfreq)
        print(f"downsampling by a factor of {dsfac}")
        rawcard = rawcard[::dsfac] + 0.0
        Fs /= dsfac
    timeaxis = np.linspace(0, len(rawcard) * Fs, len(rawcard), endpoint=False)

    # A. Signal Preprocessing
    # Apply first order Butterworth bandpass, 0.01-2Hz
    prefiltered = cardiacprefilter(rawcard, Fs, debug=debug)
    if debug:
        plt.plot(timeaxis, rawcard)
        plt.plot(timeaxis, prefiltered)
        plt.title("Raw and prefiltered cardiac signal")
        plt.legend(["Raw", "Prefiltered"])
        plt.show()
    if debug:
        print("prefiltered: ", prefiltered)

    # normalize the derivative to the range of ~-1 to 1
    prefiltmax = np.max(prefiltered)
    prefiltmin = np.min(prefiltered)
    prefiltrange = prefiltmax - prefiltmin
    if debug:
        print(f"{prefiltmax=}, {prefiltmin=}, {prefiltrange=}")
    normderiv = 2.0 * (prefiltered - prefiltmin) / prefiltrange - 1.0
    if debug:
        plt.plot(timeaxis, normderiv)
        plt.title("Normalized cardiac signal")
        plt.legend(["Normalized cardiac signal"])
        plt.show()

    # amplitude correct by flattening the envelope function
    esuperior = 2.0 * cardenvelopefilter(
        np.square(np.where(normderiv > 0.0, normderiv, 0.0)), Fs
    )
    esuperior = np.sqrt(np.where(esuperior > 0.0, esuperior, 0.0))
    einferior = 2.0 * cardenvelopefilter(
        np.square(np.where(normderiv < 0.0, normderiv, 0.0)), Fs
    )
    einferior = np.sqrt(np.where(einferior > 0.0, einferior, 0.0))
    if debug:
        plt.plot(timeaxis, normderiv)
        plt.plot(timeaxis, esuperior)
        plt.plot(timeaxis, -einferior)
        plt.title("Normalized cardiac signal, upper and lower envelope")
        plt.legend(["Normalized derivative", "Envelope top", "Envelope bottom"])
        plt.show()
    rmsnormderiv = normderiv / (esuperior + einferior)
    if debug:
        plt.plot(timeaxis, rmsnormderiv)
        plt.title("RMSnormed cardiac signal")
        plt.show()

    # B. Detection of heartbeats in sliding window
    seglength = 5.0
    segsamples = int(seglength * Fs)
    segstep = 1.5
    stepsamples = int(segstep * Fs)
    totaltclength = len(rawcard)
    numsegs = int((totaltclength - segsamples) // stepsamples)
    if (totaltclength - segsamples) % segsamples != 0:
        numsegs += 1
    peakfreqs = np.zeros((numsegs), dtype=np.float64)
    cardfilteredderivs = rmsnormderiv * 0.0
    cardfilteredweights = rmsnormderiv * 0.0
    for i in range(numsegs):
        if i < numsegs - 1:
            segstart = i * stepsamples
            segend = segstart + segsamples
        else:
            segstart = len(rawcard) - segsamples
            segend = segstart + segsamples
        segment = rmsnormderiv[segstart:segend] + 0.0
        segment *= hamming(segsamples)
        segment -= np.mean(segment)
        if False:
            thex, they = welch(segment, Fs, nperseg=2048)
        else:
            thex, they = welch(segment, Fs, nfft=4096)
        peakfreqs[i] = thex[np.argmax(they)]
        cardfilterpctwidth = 10.0
        cardfilterorder = 1
        lowerfac = 1.0 - cardfilterpctwidth / 200.0
        upperfac = 1.0 + cardfilterpctwidth / 200.0
        lowerpass = peakfreqs[i] * lowerfac
        upperpass = peakfreqs[i] * upperfac
        if debug:
            print(peakfreqs[i], lowerfac, lowerpass, upperfac, upperpass)
        filteredsegment = butterlpfiltfilt(
            Fs, upperpass, segment, cardfilterorder, debug=False
        )
        filteredsegment -= np.mean(filteredsegment)
        if i < numsegs - 1:
            cardfilteredderivs[
                i * stepsamples : (i * stepsamples) + segsamples
            ] += filteredsegment
            cardfilteredweights[i * stepsamples : (i * stepsamples) + segsamples] += 1.0
        else:
            cardfilteredderivs[-segsamples:] += filteredsegment
            cardfilteredweights[-segsamples:] += 1.0
    cardfilteredderivs /= cardfilteredweights
    cardfilteredderivs /= np.std(cardfilteredderivs)
    if debug:
        print(peakfreqs)
        plt.plot(rmsnormderiv)
        plt.plot(cardfilteredderivs)
        plt.title("Cardiac signal with peaks")
        plt.show()

    # C. heartbeats segmentation
    # The fastest credible cardiac rate is 200 bpm -> 0.3 seconds/heartbeat, so set the dist to be 75%
    # of that in points
    thedist = int(0.75 * (0.3 * Fs))
    peakinfo = operations.peakfind_physio(cardfilteredderivs, thresh=0.1, dist=thedist)
    if debug:
        ax = operations.plot_physio(peakinfo)
        plt.show()
    thetroughs = peakinfo.troughs

    # D. Similarity Analysis and Exclusion of Unreliable heartbeats
    numheartbeats = len(thetroughs) - 1
    scaledpeaklength = 100
    thescaledheartbeats = np.zeros((numheartbeats, scaledpeaklength), dtype=np.float64)
    theheartbeatlocs = np.zeros((numheartbeats), dtype=np.float64)
    theheartbeatcorrs = np.zeros((numheartbeats), dtype=np.float64)
    heartbeatlist = []
    for thisheartbeat in range(numheartbeats):
        heartbeatinfo = {}
        startpt = thetroughs[thisheartbeat]
        endpt = thetroughs[thisheartbeat + 1]
        theheartbeatlocs[thisheartbeat] = (endpt + startpt) / (Fs * 2.0)
        heartbeatinfo["starttime"] = startpt / Fs
        heartbeatinfo["endtime"] = endpt / Fs
        heartbeatinfo["centertime"] = theheartbeatlocs[thisheartbeat]
        thescaledheartbeats[thisheartbeat, :] = resample(
            cardfilteredderivs[startpt:endpt], scaledpeaklength
        )
        thescaledheartbeats[thisheartbeat, :] -= np.min(
            thescaledheartbeats[thisheartbeat, :]
        )
        thescaledheartbeats[thisheartbeat, :] /= np.max(
            thescaledheartbeats[thisheartbeat, :]
        )
        heartbeatlist.append(heartbeatinfo)
        if debug:
            plt.plot(thescaledheartbeats[thisheartbeat, :], lw=0.1, color="#888888")
    averageheartbeat = np.mean(thescaledheartbeats, axis=0)
    if debug:
        plt.plot(averageheartbeat, lw=2, color="black")
        plt.show()
    for thisheartbeat in range(numheartbeats):
        theheartbeatcorrs[thisheartbeat] = pearsonr(
            averageheartbeat, thescaledheartbeats[thisheartbeat, :]
        ).statistic
        heartbeatlist[thisheartbeat]["correlation"] = theheartbeatcorrs[thisheartbeat]

    return heartbeatlist


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
