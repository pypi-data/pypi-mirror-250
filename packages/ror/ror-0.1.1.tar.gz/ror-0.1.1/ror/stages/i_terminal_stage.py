# External imports
from typing import TypeVar, get_args

# Local imports
from .common import IBaseStage

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type


class ITerminalStage(IBaseStage[I, O]):
    """Interface for the ITerminal stage, defines an input datatype,
    an output datatype. There is no next stage ref since this is the
    final stage of any pipeline.

    Examples
    --------
    >>> from pypipeline.stages import ITerminalStage

    This will define a new stage with an input, ouput schema and a ref.

    >>> class TerminalStage(ITerminalStage[InputSchema, OutputSchema]): ...
    """

    def __init_subclass__(cls) -> None:
        cls._types = get_args(cls.__orig_bases__[0])

    def discover(self) -> None:
        """As this is the final stage then it will return None
        to indicate that this is the final stage.

        Returns
        -------
        None
            Class reference to next stage
        """
        return None

    def input_schema(self) -> I:
        """Returns the input schema defined for this stage

        Returns
        -------
        I
            Reference to dataclass schema
        """
        return self._types[0]

    def output_schema(self) -> O:
        """Returns the output schema defined for this stage

        Returns
        -------
        O
            Reference to dataclass schema
        """
        return self._types[-1]
