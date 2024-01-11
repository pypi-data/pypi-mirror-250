# !/usr/bin/env python
"""Run a test calculation on localhost.
Usage: ./example_01.py
"""
import os
import click

from aiida import cmdline
from aiida.engine import submit
from aiida.orm import StructureData

from aiida_bigdft import helpers
from aiida_bigdft.calculations import BigDFTCalculation
from aiida_bigdft.data import BigDFTParameters


def test_run(code):
    """Run a calculation on the localhost computer.
    Uses test helpers to create AiiDA Code on the fly.
    """
    if not code:
        # get code
        computer = helpers.get_computer()
        code = helpers.get_code(entry_point="bigdft", computer=computer)

    testfile = os.path.join(os.getcwd(), "test.txt")

    with open(testfile, "w+", encoding="utf8") as o:
        # use `verdi calcjob outputcat <pk> test.txt` to verify the existence of this file
        o.write("I am a test\n")

    cell = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
    s = StructureData(cell=cell)
    s.append_atom(position=(0, 0, 0), symbols="C")

    print(f"running code {code}")
    inputs = {
        "code": code,
        "structure": s,
        "extra_files_send": [testfile],
        "metadata": {
            "options": {
                "jobname": "Mono_Carbon",
                "max_wallclock_seconds": 3600,
                "withmpi": False,
            }
        },
    }

    bigdft_parameters = {}
    bigdft_parameters["dft"] = {"ixc": "LDA", "itermax": "5"}
    bigdft_parameters["output"] = {"orbitals": "binary"}

    inputs["parameters"] = BigDFTParameters(bigdft_parameters)

    result = submit(BigDFTCalculation, **inputs)

    return result


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.
    Example usage: $ ./example_01.py --code diff@localhost
    Alternative (creates diff@localhost-test code): $ ./example_01.py
    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
