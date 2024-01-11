from aiida.common import AttributeDict
from aiida.engine import (
    BaseRestartWorkChain,
    ProcessHandlerReport,
    process_handler,
    while_,
)

from aiida_bigdft.calculations import BigDFTCalculation


class BigDFTBaseWorkChain(BaseRestartWorkChain):
    """Base workchain for running a BigDFT Calculation"""

    _process_class = BigDFTCalculation
    _workchain_namespace = "BigDFT"

    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.expose_inputs(
            BigDFTCalculation, namespace=BigDFTBaseWorkChain._workchain_namespace
        )
        spec.expose_outputs(BigDFTCalculation)

        spec.outline(
            cls.setup,
            while_(cls.should_run_process)(cls.run_process, cls.inspect_process),
            cls.results,
        )
        spec.exit_code(
            300,
            "ERROR_UNRECOVERABLE_FAILURE",
            message="The calculation encountered an unrecoverable error",
        )

    def setup(self):
        """Call the `setup` of the `BaseRestartWorkChain` and then create the inputs dictionary in `self.ctx.inputs`.

        This `self.ctx.inputs` dictionary will be used by the `BaseRestartWorkChain` to submit the calculations in the
        internal loop.
        """
        super().setup()
        self.ctx.restart_calc = None
        self.ctx.inputs = AttributeDict(
            self.exposed_inputs(
                BigDFTCalculation, BigDFTBaseWorkChain._workchain_namespace
            )
        )

    def report_error_handled(self, calculation, action):
        """Report an action taken for a calculation that has failed.

        This should be called in a registered error handler if its condition is met and an action was taken.

        :param calculation: the failed calculation node
        :param action: a string message with the action taken
        """
        self.report(
            f"{calculation.process_label}<{calculation.pk}> "
            f"failed with exit status {calculation.exit_status}: "
            f"{calculation.exit_message}"
        )
        self.report(f"Action taken: {action}")

    @process_handler(priority=600)
    def handle_unrecoverable_failure(self, node):
        """Handle calculations with an exit status below 400 which are unrecoverable, so abort the work chain."""
        if node.is_failed and node.exit_status < 400:
            self.report_error_handled(node, "unrecoverable error, aborting...")
            return ProcessHandlerReport(
                True, self.exit_codes.ERROR_UNRECOVERABLE_FAILURE
            )
