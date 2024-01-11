# !/usr/bin/env python
"""Run a test calculation on localhost.
Usage: ./example_01.py
"""
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

    alat = 4  # angstrom
    cell = [
        [
            alat,
            0,
            0,
        ],
        [
            0,
            alat,
            0,
        ],
        [
            0,
            0,
            alat,
        ],
    ]

    s = StructureData(cell=cell)
    s.append_atom(position=(alat / 2, alat / 2, alat / 2), symbols="Ti")
    s.append_atom(position=(alat / 2, alat / 2, 0), symbols="O")
    s.append_atom(position=(alat / 2, 0, alat / 2), symbols="O")

    print(f"running code {code}")
    inputs = {
        "code": code,
        "structure": s,
        "metadata": {
            "options": {
                "jobname": "TiO2",
                "max_wallclock_seconds": 3600,
                "queue_name": "short",
                "resources": {
                    # "num_cores_per_machine": 16,
                    "num_cores_per_mpiproc": 1,
                    "num_mpiprocs_per_machine": 1,
                    "num_machines": 1,
                },
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
