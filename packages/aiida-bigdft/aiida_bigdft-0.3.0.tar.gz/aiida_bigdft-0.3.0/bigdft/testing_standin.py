#!/usr/bin/env python
"""
Testing class to mimic bigdft.py within the CI. Any validation is to be performed here.

"""
import os

import click
import yaml


@click.command()
@click.option("--structure", help="path to structure json file")
@click.option("--parameters", help="yaml dumped dft parameters")
@click.option("--submission", help="extra submission parameters")
def run(
    structure: str = None,  # pylint: disable=unused-argument
    parameters: str = None,  # pylint: disable=unused-argument
    submission: str = None,
) -> dict:
    """
    Run the calculation. Requires three file path inputs:

    Args:
        structure (str):
            path to the serialised ASE json file
        parameters (str):
            path to the serialised BigDFTParameters yaml file
        submission (str):
            path to the serialised submission yaml file

    Returns:
        BigDFT.Logfile
    """
    ########################
    ### submission param ###
    ########################
    params_sub = {}
    if submission is not None:
        with open(submission, encoding="utf8") as o:
            params_sub = yaml.safe_load(o)

    jobname = params_sub["jobname"]

    with open(f"log-{jobname}.yaml", "w+", encoding="utf8") as o:
        yaml.dump({}, o)

    os.makedirs(f"data-{jobname}")
    with open(f"data-{jobname}/time-{jobname}.yaml", "w+", encoding="utf8") as o:
        yaml.dump({}, o)

    payload = {"pass": True}

    with open("testing_info.yaml", "w+", encoding="utf8") as o:
        yaml.dump(payload, o)


if __name__ == "__main__":
    run()
