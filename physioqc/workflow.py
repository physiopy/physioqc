import datetime
import os
import sys

import numpy as np
import peakdet as pk

from .cli.run import _get_parser
from .interfaces.interfaces import generate_figures, run_metrics, save_metrics
from .interfaces.visualizations import (
    plot_average_peak,
    plot_histogram,
    plot_power_spectrum,
    plot_raw_data,
)
from .metrics.multimodal import (
    fALFF,
    freq_energy,
    max,
    mean,
    min,
    peak_amplitude,
    peak_distance,
    signal_fct,
    std,
)


def save_bash_call(outdir):
    """
    Save the bash call into file `p2d_call.sh`.

    Parameters
    ----------
    metric : function
        Metric function to retrieve arguments for
    metric_args : dict
        Dictionary containing all arguments for all functions requested by the
        user
    """
    arg_str = " ".join(sys.argv[1:])
    call_str = f"physioqc {arg_str}"
    outdir = os.path.abspath(outdir)
    log_path = os.path.join(outdir, "code", "logs")
    os.makedirs(log_path, exist_ok=True)
    isotime = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    f = open(os.path.join(log_path, f"p2d_call_{isotime}.sh"), "a")
    f.write(f"#!bin/bash \n{call_str}")
    f.close()


def physioqc(
    filename,
    outdir=".",
    **kwargs,
):
    """
    Run main workflow of physioqc.

    Runs the parser, computes the quality metrics, generate the figures for quality control
    and compile the metrics and the figure in a visual report.

    Notes
    -----
    The code was greatly copied from phys2bids (copyright the physiopy community)

    """
    # Define which metrics you want to compute on which physiological signal instance
    metrics = {
        signal_fct: [fALFF, freq_energy],
        peak_distance: [min, max, std, mean],
        peak_amplitude: [min, max, std, mean],
    }

    figures = [plot_average_peak, plot_histogram, plot_power_spectrum, plot_raw_data]

    # Load the data
    d = np.genfromtxt(filename)

    # Find index of time 0
    idx_0 = np.argmax(d[:, 0] >= 0)

    # Extract respiration belt signal
    # TO IMPLEMENT : the sampling frequency should be extracted automatically from the file
    data = pk.Physio(d[idx_0:, 1], fs=10000)

    # Compute all the metrics
    metrics_df = run_metrics(metrics, data)

    # Generate figures
    generate_figures(figures, data, outdir)

    # Save the metrics in the output folder
    save_metrics(metrics_df, outdir)


def _main(argv=None):
    options = _get_parser().parse_args(argv)

    save_bash_call(options.outdir)

    physioqc(**vars(options))


if __name__ == "__main__":
    _main(sys.argv[1:])
