"""
Parsers provided by aiida_bigdft.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
import os
import re

from aiida.common import exceptions
from aiida.engine import ExitCode
import aiida.orm
from aiida.parsers.parser import Parser

from aiida_bigdft.calculations import BigDFTCalculation
from aiida_bigdft.data.BigDFTFile import BigDFTFile, BigDFTLogfile
from aiida_bigdft.utils.MiniLogger import MiniLogger


class BigDFTParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a DiffCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, BigDFTCalculation):
            raise exceptions.ParsingError("Can only parse DiffCalculation")

    def parse_stderr(self, inputfile):
        """Parse the stderr file to get common errors, such as OOM or timeout.

        :param inputfile: stderr file
        :returns: exit code in case of an error, None otherwise
        """
        timeout_messages = {
            "DUE TO TIME LIMIT",  # slurm
            "exceeded hard wallclock time",  # UGE
            "TERM_RUNLIMIT: job killed",  # LFS
            "walltime .* exceeded limit",  # PBS/Torque
        }

        oom_messages = {
            "[oO]ut [oO]f [mM]emory",
            "oom-kill",  # generic OOM messages
            "Exceeded .* memory limit",  # slurm
            "exceeds job hard limit .*mem.* of queue",  # UGE
            "TERM_MEMLIMIT: job killed after reaching LSF memory usage limit",  # LFS
            "mem .* exceeded limit",  # PBS/Torque
        }
        for message in timeout_messages:
            if re.search(message, inputfile):
                return self.exit_codes.ERROR_OUT_OF_WALLTIME
        for message in oom_messages:
            if re.search(message, inputfile):
                return self.exit_codes.ERROR_OUT_OF_MEMORY
        return

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """

        exitcode = ExitCode(0)

        stderr = self.node.get_scheduler_stderr()
        if stderr:
            exitcode = self.parse_stderr(stderr)
            if exitcode:
                self.logger.error("Error in stderr: " + exitcode.message)

        jobname = BigDFTCalculation._defaults["jobname"]

        if "jobname" in self.node.get_options():
            jobname = self.node.get_options()["jobname"]

        metadata = self.node.get_metadata_inputs()["metadata"]
        if "jobname" in metadata.get("options", {}):
            jobname = metadata["options"]["jobname"]

        output_filename = f"log-{jobname}.yaml"
        time_filename = f"time-{jobname}.yaml"

        files_retrieved = self.retrieved.list_object_names()
        files_expected = [output_filename, time_filename]

        files_expected += self.node.inputs.extra_files_recv.get_list()

        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                f"Found files '{files_retrieved}', expected to find '{files_expected}'"
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        logfile = self.parse_file(output_filename, "logfile", exitcode)
        timefile = self.parse_file(time_filename, "timefile", exitcode)

        self.out("logfile", logfile)
        self.out("timefile", timefile)

        energy = 0.0
        if logfile.logfile is not None:
            energy = logfile.logfile.energy

        self.out("energy", aiida.orm.Float(energy))

        ttotal = timefile.content.get("SUMMARY", None)
        if ttotal is not None:
            ttotal = ttotal.get("Total", [-1.0])

            self.out("ttotal", aiida.orm.Float(ttotal[-1]))

        else:
            self.out("ttotal", aiida.orm.Float(-1.0))

        return exitcode

    def parse_file(self, output_filename, name, exitcode):
        """
        Parse a retrieved file into a BigDFTFile object
        """

        # add output file
        self.logger.info(f"Parsing '{output_filename}'")
        try:
            with open(output_filename, "w+", encoding="utf8") as tmp:
                tmp.write(self.retrieved.get_object_content(output_filename))
                if name == "logfile":
                    output = BigDFTLogfile(os.path.join(os.getcwd(), output_filename))
                else:
                    output = BigDFTFile(os.path.join(os.getcwd(), output_filename))

        except ValueError:
            self.logger.error(f"Impossible to parse {name} {output_filename}")
            if (
                not exitcode
            ):  # if we already have OOW or OOM, failure here will be handled later
                return self.exit_codes.ERROR_PARSING_FAILED
        try:
            output.store()
            self.logger.info(f"Successfully parsed {name} '{output_filename}'")
        except exceptions.ValidationError:
            self.logger.info(
                f"Impossible to store {name} - ignoring '{output_filename}'"
            )
            if (
                not exitcode
            ):  # if we already have OOW or OOM, failure here will be handled later
                return self.exit_codes.ERROR_PARSING_FAILED

        return output
