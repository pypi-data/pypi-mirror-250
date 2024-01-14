# External imports
from typing import Generic, Tuple, TypeVar, get_args

# Local imports
from .common import IBaseStage

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type
N = TypeVar("N", bound=IBaseStage)  # Next stage reference


class IForwardStage(IBaseStage[I, O], Generic[I, O, N]):
    """Interface for the forward stage, defines an input datatype,
    an output datatype and a dependency for the next stage. Which
    will be returened as an instance with the stage output in the
    `get_output` method.

    Examples
    --------
    >>> from pypipeline.stages import IForwardStage

    This will define a new stage with an input, ouput schema and a ref.

    >>> class ForwardStage(IForwardStage[InputSchema, OutputSchema, NextStage]): ...
    """

    def __init_subclass__(cls) -> None:
        cls._types = get_args(cls.__orig_bases__[0])

    def discover(self) -> N:
        """Returns a class object for the next stage in linked
        from this stage.

        Returns
        -------
        N
            Class reference to next stage
        """
        return self._types[-1]

    def get_output(self) -> Tuple[N, O]:
        pass

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
