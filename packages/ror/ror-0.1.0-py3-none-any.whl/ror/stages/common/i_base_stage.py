# External imports
from typing import Generic, TypeVar

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type


class IBaseStage(Generic[I, O]):
    """Interface extended by all the additional stages which exclicitly
    defines that all stages should expect the `set_input`, `compute`and
    `get_output` as public methods which is essential for the controllers.

    Parameters
    ----------
    Generic : Generic
        Typing generic used to explicitly define the input dataclass of
        the stage and the output dataclass in the stage.
    """

    def __str__(self) -> str:
        return f"hello"

    def __repr__(self):
        pass

    def set_input(self, input: I) -> None:
        """Given an input from the last stage or init dataclass, set the
        local state for this stage -> data used in `compute`.

        Parameters
        ----------
        input : I
            Input dataclass of the define input dataclass I.
        """
        self.input = input

    def compute(self) -> None:
        pass

    def get_output(self) -> O:
        """Returns the output dataclass as type O defined in the
        construction.

        Returns
        -------
        O
            Output dataclass defined for this stage.
        """
        pass
