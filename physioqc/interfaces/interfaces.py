import os

import matplotlib.pyplot as plt
import pandas as pd
from bids import layout

from physioqc.metrics.multimodal import peak_amplitude, peak_detection, peak_distance

# Save pattern as global
pattern = (
    "sub-{subject}[_ses-{session}]_task-{task}[_acq-{acquisition}]"
    + "[_rec-{reconstruction}][_run-{run}][_echo-{echo}]"
    + "[_desc-{description}]_{suffix}.{extension}"
)


def generate_figures(figures, data, outdir, entities):
    """
    Generates all the figure needed to populate the visual report.
    Save the figures in the 'figures' folder

    Parameters
    ----------
    figures : dictionary
        A list of functions to run to generate all the figures.
    data : np.array or peakdet Physio object
        Physiological data
    outdir: str
        The path to the output directory.
    entities: dictionary
        A dictionary of bids entities used to write out the files.
    """
    # Create the output directory if not existing
    sub_folders = []
    for k in ["subject", "session"]:
        if k in entities:
            sub_folders.append("-".join([k[:3], entities[k]]))

    out_folder = os.path.join(outdir, *sub_folders, "figures")
    os.makedirs(out_folder, exist_ok=True)

    out_entities = {k: v for k, v in entities.items()}
    out_entities.update({"description": "", "extension": ".svg"})

    for figure in figures:
        # Get the plot name from the name of the function that was ran
        plot_name = "_".join(figure.__name__.split("_")[1:])

        # Run the function to generate the figure
        if figure.__name__ == "plot_histogram":
            # plot histogram takes as input the peak distance or peak height,
            # while the other function take a peakdet Physio object

            data = peak_detection(data)
            # Plot histogram of peak distance
            peak_dist = peak_distance(data)
            fig, _ = figure(peak_dist)

            out_entities["description"] = "histpeakdist"
            # TO IMPLEMENT the subject name should be automatically read when the data are loaded
            fig.savefig(
                os.path.join(
                    out_folder, layout.writing.build_path(out_entities, pattern)
                )
            )

            # Plot histogram of peak amplitude
            peak_ampl = peak_amplitude(data)
            fig, _ = figure(peak_ampl)

            out_entities["description"] = "histpeakamp"
            # TO IMPLEMENT the subject name should be automatically read when the data are loaded
            fig.savefig(
                os.path.join(
                    out_folder, layout.writing.build_path(out_entities, pattern)
                )
            )
        else:
            fig, _ = figure(data)
            # Save the figure
            out_entities["description"] = plot_name
            # TO IMPLEMENT the subject name should be automatically read when the data are loaded
            fig.savefig(
                os.path.join(
                    out_folder, layout.writing.build_path(out_entities, pattern)
                )
            )


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
        # TO IMPLEMENT : if the function m is peak_amplitude or peak_distance, you should first
        # run peak_detection and then pass the output of peak_detection to the latter.
        result = m[0](data)
        for fct in m[1]:
            # Run each metric on the physiological signal instance
            value_list.append(fct(result))
            # Save metric name and value
            name_list.append(m[0].__name__ + "_" + fct.__name__)

        metrics_df = pd.DataFrame(
            list(zip(name_list, value_list)), columns=["Metric", "Value"]
        )

    return metrics_df


def save_metrics(metrics_df, outdir, entities, to_csv=False):
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
    # TO IMPLEMENT : there may be a bug associated to the next line IsDirectoryError
    sub_folders = []
    for k in ["subject", "session"]:
        if k in entities:
            sub_folders.append("-".join([k[:3], entities[k]]))

    out_folder = os.path.join(outdir, *sub_folders)
    os.makedirs(out_folder, exist_ok=True)

    out_entities = {k: v for k, v in entities.items()}

    if to_csv:
        out_entities.update({"description": "metrics", "extension": ".csv"})
        metrics_df.to_csv(
            os.path.join(out_folder, layout.writing.build_path(out_entities, pattern)),
            index=False,
        )
    else:
        out_entities.update({"description": "metrics", "extension": ".json"})
        metrics_df.to_json(
            os.path.join(out_folder, layout.writing.build_path(out_entities, pattern))
        )
