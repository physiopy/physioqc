# -*- coding: utf-8 -*-
"""Parser for physioqc."""


import argparse

from physioqc import __version__


def _get_parser():
    """
    Parse command line inputs for this function.

    Returns
    -------
    parser.parse_args() : argparse dict

    Notes
    -----
    Default values must be updated in __call__ method from MetricsArgDict class.
    # Argument parser follow template provided by RalphyZ.
    # https://stackoverflow.com/a/43456577
    """

    parser = argparse.ArgumentParser(
        description=(
            "%(prog)s, a tool perform quality control on physiological signal "
            "It generates a visual report and some metrics \n"
            f"Version {__version__}"
        ),
        add_help=False,
    )
    # Required arguments
    required = parser.add_argument_group("Required Argument")
    required.add_argument(
        "-in",
        "--input-file",
        dest="filename",
        type=str,
        help="Full path and name of the file containing "
        "physiological data, with or without extension.",
        required=True,
    )

    # Important optional arguments
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "-outdir",
        "--output-dir",
        dest="outdir",
        type=str,
        help="Folder where output should be placed. Default is current folder.",
        default=".",
    )
    optional.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )

    return parser


if __name__ == "__main__":
    raise RuntimeError(
        "physioqc/cli/run.py should not be run directly;\n"
        "Please `pip install` physioqc and use the "
        "`physioqc` command"
    )
