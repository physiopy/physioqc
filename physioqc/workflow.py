import datetime
import os
import sys

import numpy as np
import peakdet as pk
from bids import layout
from nireports.assembler.report import Report

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

BOOTSTRAP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

print("BOOTSTRAP path", BOOTSTRAP_PATH)


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

    # Stand in for further BIDS support:
    bids_entities = layout.parse_file_entities(filename=filename)

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
    generate_figures(figures, data, outdir, bids_entities)

    # Save the metrics in the output folder
    save_metrics(metrics_df, outdir, bids_entities)

    metric_dict = metrics_df.to_dict(orient="list")
    metric_dict = {i: j for i, j in zip(metric_dict["Metric"], metric_dict["Value"])}
    metadata = {
        "about-metadata": {
            "Metrics": metric_dict,
            "Version": {"version": "pre functional, Definitely does not work yet ;)"},
        }
    }

    filters = {k: bids_entities[k] for k in ["subject"]}

    sub_folders = []
    for k in ["subject", "session"]:
        if k in bids_entities:
            sub_folders.append("-".join([k[:3], bids_entities[k]]))

    out_folder = os.path.join(outdir, *sub_folders, "figures")

    robj = Report(
        outdir,
        "test",
        reportlets_dir=out_folder,
        bootstrap_file=os.path.join(BOOTSTRAP_PATH, "bootstrap.yml"),
        metadata=metadata,
        plugin_meta={},
        **filters,
    )

    robj.generate_report()


def _main(argv=None):
    options = _get_parser().parse_args(argv)

    save_bash_call(options.outdir)

    physioqc(**vars(options))


if __name__ == "__main__":
    _main(sys.argv[1:])
