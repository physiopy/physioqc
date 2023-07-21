import os

import matplotlib.pyplot as plt
import pandas as pd

from physioqc.metrics.multimodal import peak_amplitude, peak_distance


def generate_figures(figures, data, outdir):
    """
    Generates all the figure needed to populate the visual report.
    Save the figures in the 'figures' folder

    Parameters
    ----------
    figures : dictionary
        A list of functions to run to generate all the figures.
    data : np.array or peakdet Physio object
        Physiological data
    """
    # Create the output directory if not existing
    os.mkdir(os.path.join(outdir, "figures"), exist_ok=True)

    for figure in figures:
        # Get the plot name from the name of the function that was ran
        plot_name = figure.__name__.split("_")[1:]

        # Run the function to generate the figure
        if figure.__name__ == "plot_histogram":
            # plot histogram takes as input the peak distance or peak height,
            # while the other function take a peakdet Physio object

            # Plot histogram of peak distance
            peak_dist = peak_distance(data)
            fig, _ = figure(peak_dist)

            plot_name = "histogram_peak_distance"
            fig.savefig(os.path.join(outdir, "figures", f"sub-01_desc-{plot_name}.svg"))

            # Plot histogram of peak amplitude
            peak_ampl = peak_amplitude(data)
            fig, _ = figure(peak_ampl)

            plot_name = "histogram_peak_distance"
            fig.savefig(os.path.join(outdir, "figures", f"sub-01_desc-{plot_name}.svg"))

        else:
            fig, _ = figure(data)
            # Save the figure
            fig.savefig(os.path.join(outdir, "figures", f"sub-01_desc-{plot_name}.svg"))


def run_metrics(metrics_dict, data):
    """
    Goes through the list of metrics and calls them

    Parameters
    ----------
    metrics : dictionary
        A dictionary that maps the physiological signal instance
        to the function that needs to be called on it.
    data : np.array or peakdet Physio object
        Physiological data

    Returns
    -------
    Dataframe :obj:`panda.dataframe`
        A dataframe containing the value of each metric
    """
    metrics_df = pd.DataFrame()
    name_list = []
    value_list = []
    for m in metrics_dict.items():
        # Extract the physiological signal instance (signal, peak amplitude ...)
        result = m[0](data)
        for fct in m[1]:
            # Run each metric on the physiological signal instance
            value_list.append(fct(result))
            # Save metric name and value
            name_list.append(m.__name__ + "_" + fct.__name__)

        metrics_df = pd.DataFrame(
            list(zip(name_list, value_list)), columns=["Metric", "Value"]
        )

    return metrics_df


def save_metrics(metrics_df, outdir, to_csv=False):
    """
    Save the metrics in the defined output path

    Parameters
    ----------
    metrics_df : pd.Dataframe
        A dataframe gathering the value of the metrics
    outdir : string
        Physiological data
    to.csv : boolean
        If true save in CSV format otherwise save to JSON

    Returns
    -------
    Dataframe :obj:`panda.dataframe`
        A dataframe containing the value of each metric
    """
    os.mkdir(outdir, exist_ok=True)
    if to_csv:
        metrics_df.to_csv(outdir, index=False)
    else:
        metrics_df.to_json(outdir)
