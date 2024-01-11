"""
Module storing a BigDFT inputfile as an AiiDA Dict
"""

from aiida.orm import Dict


class BigDFTParameters(Dict):  # pylint: disable=too-many-ancestors
    """
    Command line options for a BigDFT calculation.

    This class represents the yaml inputfile which will be passed to the executable.
    """

    # pylint: disable=redefined-builtin
    def __init__(self, dict: dict = None, **kwargs):
        """
        Constructor for the data class
        Usage: ``BigDFTParameters(**parameters)``
        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict: dict):
        """Validate command line options.
        Uses the voluptuous package for validation. Find out about allowed keys using::
            print(DiffParameters).schema.schema
        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        if parameters_dict is None:
            parameters_dict = {}

        return parameters_dict

    def __str__(self):
        """String representation of node.
        Append values of dictionary to usual representation. E.g.::
            uuid: b416cbee-24e8-47a8-8c11-6d668770158b (pk: 590)
            {'ignore-case': True}
        """
        string = super().__str__()
        string += "\n" + str(self.get_dict())
        return string
