"""Denoising metrics for chest belt recordings."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from peakdet import operations
from scipy.signal import resample, welch
from scipy.stats import pearsonr

from .. import references
from ..due import due
from .utils import butterbpfiltfilt, butterlpfiltfilt, hamming, physio_or_numpy


def respirationprefilter(
    rawresp, Fs, lowerpass=0.01, upperpass=2.0, order=1, debug=False
):
    if debug:
        print(
            f"respirationprefilter: Fs={Fs} order={order}, lowerpass={lowerpass}, upperpass={upperpass}"
        )
    return butterbpfiltfilt(Fs, lowerpass, upperpass, rawresp, order, debug=debug)
    # return operations.filter_physio(rawresp, cutoffs=[lowerpass, upperpass], method='bandpass')


def respenvelopefilter(squarevals, Fs, upperpass=0.05, order=8, debug=False):
    if debug:
        print(f"respenvelopefilter: Fs={Fs} order={order}, upperpass={upperpass}")
    return butterlpfiltfilt(Fs, upperpass, squarevals, order, debug=debug)


@due.dcite(references.ROMANO_2023)
def respiratorysqi(
    rawresp, Fs, envelopelpffreq=0.05, slidingfilterpctwidth=10.0, debug=False
):
    """Implementation of Romano's method from A Signal Quality Index for Improving the Estimation of
    Breath-by-Breath Respiratory Rate During Sport and Exercise,
    IEEE SENSORS JOURNAL, VOL. 23, NO. 24, 15 DECEMBER 2023

    NB: In part A, Romano does not specify the upper pass frequency for the respiratory envelope filter.
        0.05Hz looks pretty good.
        In part B, the width of the sliding window bandpass filter is not specified.  We use a range of +/- 5% of the
        center frequency.
    """

    # rawresp = physio_or_numpy(rawresp)

    # get the sample frequency down to around 25 Hz for respiratory waveforms
    targetfreq = 25.0
    if Fs > targetfreq:
        dsfac = int(Fs / targetfreq)
        print(f"downsampling by a factor of {dsfac}")
        rawresp = rawresp[::dsfac] + 0.0
        Fs /= dsfac

    # A. Signal Preprocessing
    # Apply first order Butterworth bandpass, 0.01-2Hz
    prefiltered = respirationprefilter(rawresp, Fs, debug=debug)
    if debug:
        plt.plot(rawresp)
        plt.plot(prefiltered)
        plt.title("Raw and prefiltered respiratory signal")
        plt.legend(["Raw", "Prefiltered"])
        plt.show()
    if debug:
        print("prefiltered: ", prefiltered)

    # calculate the derivative
    derivative = np.gradient(prefiltered, 1.0 / Fs)

    # normalize the derivative to the range of ~-1 to 1
    derivmax = np.max(derivative)
    derivmin = np.min(derivative)
    derivrange = derivmax - derivmin
    if debug:
        print(f"{derivmax=}, {derivmin=}, {derivrange=}")
    normderiv = 2.0 * (derivative - derivmin) / derivrange - 1.0
    if debug:
        plt.plot(normderiv)
        plt.title("Normalized derivative of respiratory signal")
        plt.legend(["Normalized derivative"])
        plt.show()

    # amplitude correct by flattening the envelope function
    esuperior = 2.0 * respenvelopefilter(
        np.square(np.where(normderiv > 0.0, normderiv, 0.0)),
        Fs,
        upperpass=envelopelpffreq,
    )
    esuperior = np.sqrt(np.where(esuperior > 0.0, esuperior, 0.0))
    einferior = 2.0 * respenvelopefilter(
        np.square(np.where(normderiv < 0.0, normderiv, 0.0)),
        Fs,
        upperpass=envelopelpffreq,
    )
    einferior = -np.sqrt(np.where(einferior > 0.0, einferior, 0.0))
    if debug:
        plt.plot(normderiv)
        plt.plot(esuperior)
        plt.plot(einferior)
        plt.legend(["Normalized derivative", "esuperior", "einferior"])
        plt.show()
    rmsnormderiv = (normderiv - einferior) / (esuperior - einferior)
    if debug:
        plt.plot(rmsnormderiv)
        plt.title(
            "Normalized derivative of respiratory signal after envelope correction"
        )
        plt.show()

    # B. Detection of breaths in sliding window
    seglength = 12.0
    segsamples = int(seglength * Fs)
    segstep = 2.0
    stepsamples = int(segstep * Fs)
    totaltclength = len(rawresp)
    numsegs = int((totaltclength - segsamples) // stepsamples)
    if (totaltclength - segsamples) % segsamples != 0:
        numsegs += 1
    peakfreqs = np.zeros((numsegs), dtype=np.float64)
    respfilteredderivs = rmsnormderiv * 0.0
    respfilteredweights = rmsnormderiv * 0.0
    for i in range(numsegs):
        if i < numsegs - 1:
            segstart = i * stepsamples
            segend = segstart + segsamples
        else:
            segstart = len(rawresp) - segsamples
            segend = segstart + segsamples
        segment = rmsnormderiv[segstart:segend] + 0.0
        segment *= hamming(segsamples)
        segment -= np.mean(segment)
        thex, they = welch(segment, Fs, nfft=4096)
        peakfreqs[i] = thex[np.argmax(they)]
        respfilterorder = 1
        lowerfac = 1.0 - slidingfilterpctwidth / 200.0
        upperfac = 1.0 + slidingfilterpctwidth / 200.0
        lowerpass = peakfreqs[i] * lowerfac
        upperpass = peakfreqs[i] * upperfac
        if debug:
            print(peakfreqs[i], lowerfac, lowerpass, upperfac, upperpass)
        filteredsegment = butterlpfiltfilt(
            Fs, upperpass, segment, respfilterorder, debug=False
        )
        filteredsegment -= np.mean(filteredsegment)
        if i < numsegs - 1:
            respfilteredderivs[
                i * stepsamples : (i * stepsamples) + segsamples
            ] += filteredsegment
            respfilteredweights[i * stepsamples : (i * stepsamples) + segsamples] += 1.0
        else:
            respfilteredderivs[-segsamples:] += filteredsegment
            respfilteredweights[-segsamples:] += 1.0
    respfilteredderivs /= respfilteredweights
    respfilteredderivs /= np.std(respfilteredderivs)
    if debug:
        print(peakfreqs)
        plt.plot(rmsnormderiv)
        plt.plot(respfilteredderivs)
        plt.title("Normalized derivative before and after targeted bandpass filtering")
        plt.legend(["Normalized derivative", "Filtered normalized derivative"])
        plt.show()

    # C. Breaths segmentation
    # The fastest credible breathing rate is 20 breaths/min -> 3 seconds/breath, so set the dist to be 50%
    # of that in points
    thedist = int((3.0 * Fs) / 2.0)
    peakinfo = operations.peakfind_physio(respfilteredderivs, thresh=0.05, dist=thedist)
    if debug:
        ax = operations.plot_physio(peakinfo)
        plt.show()
    thepeaks = peakinfo.peaks

    # D. Similarity Analysis and Exclusion of Unreliable Breaths
    numbreaths = len(thepeaks) - 1
    scaledpeaklength = 100
    thescaledbreaths = np.zeros((numbreaths, scaledpeaklength), dtype=np.float64)
    thebreathlocs = np.zeros((numbreaths), dtype=np.float64)
    thebreathcorrs = np.zeros((numbreaths), dtype=np.float64)
    breathlist = []
    for thisbreath in range(numbreaths):
        breathinfo = {}
        startpt = thepeaks[thisbreath]
        endpt = thepeaks[thisbreath + 1]
        thebreathlocs[thisbreath] = (endpt + startpt) / (Fs * 2.0)
        breathinfo["starttime"] = startpt / Fs
        breathinfo["endtime"] = endpt / Fs
        breathinfo["centertime"] = thebreathlocs[thisbreath]
        thescaledbreaths[thisbreath, :] = resample(
            respfilteredderivs[startpt:endpt], scaledpeaklength
        )
        thescaledbreaths[thisbreath, :] -= np.min(thescaledbreaths[thisbreath, :])
        thescaledbreaths[thisbreath, :] /= np.max(thescaledbreaths[thisbreath, :])
        breathlist.append(breathinfo)
        if debug:
            plt.plot(thescaledbreaths[thisbreath, :], lw=0.1, color="#888888")
    averagebreath = np.mean(thescaledbreaths, axis=0)
    if debug:
        plt.plot(averagebreath, lw=2, color="black")
        plt.show()
    for thisbreath in range(numbreaths):
        thebreathcorrs[thisbreath] = pearsonr(
            averagebreath, thescaledbreaths[thisbreath, :]
        ).statistic
        breathlist[thisbreath]["correlation"] = thebreathcorrs[thisbreath]
    return breathlist


def plotbreathqualities(breathlist, totaltime=None):
    # set up the color codes
    color_0p9 = "#888888"
    color_0p8 = "#aa6666"
    color_0p7 = "#cc4444"
    color_bad = "#ff0000"

    if totaltime is None:
        totaltime = breathlist[-1]["endtime"]

    # unpack the breath information
    numbreaths = len(breathlist)
    thebreathlocs = np.zeros((numbreaths), dtype=np.float64)
    thebreathcorrs = np.zeros((numbreaths), dtype=np.float64)
    for thisbreath in range(numbreaths):
        thebreathlocs[thisbreath] = breathlist[thisbreath]["centertime"]
        thebreathcorrs[thisbreath] = breathlist[thisbreath]["correlation"]

    # plot the breath correlations, with lines indicating thresholds
    plt.plot(thebreathlocs, thebreathcorrs, ls="-", marker="o")
    plt.hlines(
        [0.9, 0.8, 0.7, 0.6],
        0.0,
        totaltime,
        colors=[color_0p9, color_0p8, color_0p7, color_bad],
        linestyles="solid",
        label=["th=0.9", "th=0.8", "th=0.7", "th=0.6"],
    )
    plt.title("Quality evaluation for each breath")
    plt.xlabel("Time in seconds")
    plt.ylabel("Correlation with average breath")
    plt.xlim([0, totaltime])
    plt.ylim([0, 1.05])
    plt.show()


def plotbreathwaveformwithquality(waveform, breathlist, Fs, plottype="rectangle"):
    # now plot the respiratory waveform, color coded for quality

    # set up the color codes
    color_0p9 = "#ff000000"
    color_0p8 = "#ff000044"
    color_0p7 = "#ff000088"
    color_bad = "#ff0000aa"

    # unpack the breath information
    numbreaths = len(breathlist)
    thebreathlocs = np.zeros((numbreaths), dtype=np.float64)
    thebreathcorrs = np.zeros((numbreaths), dtype=np.float64)
    for thisbreath in range(numbreaths):
        thebreathlocs[thisbreath] = breathlist[thisbreath]["centertime"]
        thebreathcorrs[thisbreath] = breathlist[thisbreath]["correlation"]

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
    for thisbreath in range(numbreaths):
        if thebreathcorrs[thisbreath] > 0.9:
            thecolor = color_0p9
        elif thebreathcorrs[thisbreath] > 0.8:
            thecolor = color_0p8
        elif thebreathcorrs[thisbreath] > 0.7:
            thecolor = color_0p7
        else:
            thecolor = color_bad
        startpt = int(breathlist[thisbreath]["starttime"] * Fs)
        endpt = int(breathlist[thisbreath]["endtime"] * Fs)
        if plottype == "rectangle":
            therectangle = Polygon(
                (
                    (breathlist[thisbreath]["starttime"], ymin),
                    (breathlist[thisbreath]["starttime"], ymax),
                    (breathlist[thisbreath]["endtime"], ymax),
                    (breathlist[thisbreath]["endtime"], ymin),
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
    plt.title("Respiratory waveform, color coded by quantifiability")
    plt.xlabel("Time in seconds")
    plt.ylabel("Amplitude (arbitrary units)")
    plt.xlim([0.0, len(waveform) / Fs])
    plt.show()


def summarizebreaths(breathlist):
    numbreaths = len(breathlist)
    for thisbreath in range(numbreaths):
        thebreathinfo = breathlist[thisbreath]
        print(
            f"{thisbreath},{thebreathinfo['starttime']},{thebreathinfo['endtime']},{thebreathinfo['centertime']},{thebreathinfo['correlation']}"
        )
