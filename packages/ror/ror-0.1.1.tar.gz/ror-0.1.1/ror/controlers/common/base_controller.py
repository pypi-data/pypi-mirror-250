# External imports
import uuid
from collections import defaultdict
from typing import Tuple

from rich.console import Console
from rich.table import Table

# Local imports
from ror.schemas import BaseSchema
from ror.stages import IInitStage, ITerminalStage
from ror.stages.common import IBaseStage


class BaseController:
    """Basic controller, which accepts an InitStage, and some inital data which is the
    input dataclass for the InitStage and performs the iterative process over all the
    linked stages.

    Examples
    --------
    >>> from pypipeline.schemas import BaseSchema
    >>> from pypipeline.schemas.fields import field_perishable, field_persistance
    >>> from pypipeline.stages import IForwardStage, IInitStage, ITerminalStage
    >>> from pypipeline.controlers.common import BaseController

    Let's deine some very basic pipeline of three stages.

    >>> @dataclass
    >>> class InputTest(BaseSchema):
    >>>     A: str = field_persistance()
    >>>     B: str = field_perishable()

    >>> @dataclass
    >>> class OutputTest(BaseSchema):
    >>>     A: str = field_perishable()
    >>>     C: str = field_persistance()

    >>> @dataclass
    >>> class TerminalOutputTest(BaseSchema):
    >>>     C: str = field_persistance()

    Then using these dataclasses we can define the processing stages.

    >>> class TerminalStageTest(ITerminalStage[OutputTest, TerminalOutputTest])
    >>> ...

    >>> class ForwardStageTest(IForwardStage[OutputTest, OutputTest, TerminalStageTest]):
    >>> ...

    >>> class InitStageTest(IInitStage[InputTest, OutputTest, ForwardStageTest]):
    >>> ...

    Then we can instantiate the contrsoller and discover the connections or perform a
    computation over the entire pipeline.

    >>> data = {"A": "A", "B": "B"}
    >>> dataclass = InputTest(**self._data)
    >>> stage = InitStageTest
    >>> controller = BaseController(dataclass, stage)

    >>> controller.discover() # Prints out a table of the connected stages for debugging.
    >>> output = controller.start() # Computes through the pipeline and return terminal data.
    """

    def __init__(self, init_data: BaseSchema, init_stage: IInitStage):
        """Instantiates the controller with a pipeline input and an init stage.

        Parameters
        ----------
        init_data : BaseSchema
            Input dataclass for the InitStage.
        init_stage : IInitStage
            Reference to the InitStage class (reference and not instance).
        """
        self.init_data = init_data
        self.init_stage = init_stage

        self._artifact_cache = defaultdict(dict)

    def _generate_discover_table(self) -> Table:
        """Creates a basic table to preview the connected computaion stages.

        Returns
        -------
        Table
            Returns an instance of the table to be filled at `self.discover()`
        """
        table = Table(title="Discover")

        table.add_column("Stage No.", style="cyan", no_wrap=True)
        table.add_column("Stage Name", justify="center", style="magenta")
        table.add_column("Input Data", justify="center", style="green")
        table.add_column("Output Data", justify="center", style="red")
        table.add_column("Next Stage", justify="right", style="green")

        return table

    def _stage_name(self, stage: IBaseStage) -> str:
        return stage.__class__.__name__

    def discover(self) -> None:
        """Iteratively goes through the entire pipelineand adds rows to the discover
        table with the relationship links between the different stages, usefull for debugging
        a pipeline.
        """
        table = self._generate_discover_table()
        stage = self.init_stage()
        stage_no = 0

        table.add_row(
            str(stage_no),
            self._stage_name(stage),
            str(stage.input_schema()),
            str(stage.output_schema()),
            str(stage.discover()),
        )

        while not isinstance(stage, ITerminalStage):
            stage = stage.discover()
            stage = stage()
            stage_no += 1

            table.add_row(
                str(stage_no),
                self._stage_name(stage),
                str(stage.input_schema()),
                str(stage.output_schema()),
                str(stage.discover()),
            )

        console = Console()
        console.print(table)

    def start(self) -> Tuple[BaseSchema, str]:
        """Performs the iterative computation through the pipeline and returns a tuple
        of the output data and a `run_id` which can be used to access the artifact cache
        produced for the different runs.

        Returns
        -------
        Tuple[BaseSchema, str]
            Tuple of the terminal stage output data and a `run_id`

        Raises
        ------
        ReferenceError
            Check that the `get_output` method of a stage indeed returns an instance of
            the next stage and not a class reference. If class reference the fail.
        """
        run_id = str(uuid.uuid4())

        stage = self.init_stage()
        stage.set_input(self.init_data)

        while not isinstance(stage, ITerminalStage):
            # Cache artifact
            self._artifact_cache[run_id][
                stage.__class__.__name__
            ] = stage.input.get_artifact()

            # Compute and get next output
            stage.compute()
            stage, output = stage.get_output()

            if isinstance(stage, type):
                raise ReferenceError(
                    "The get_object method needs to return an instance!", stage
                )

            stage.set_input(output)

        # Get terminal output and artifact
        stage.compute()
        output = stage.get_output()
        self._artifact_cache[run_id][
            stage.__class__.__name__
        ] = stage.input.get_artifact()
        self._artifact_cache[run_id][stage.__class__.__name__] = output.get_artifact()

        return output, run_id

    def get_artifacts(self, run_id: str) -> dict:
        """For some `run_id` try to access the artifacts which where produced during
        that specific run.

        Parameters
        ----------
        run_id : str
            Run id which to get the corresponding artifacts from.

        Returns
        -------
        dict
            A dictionary where the keys are the stages, and the values are the artifacts
            produced for those stages.
        """
        return self._artifact_cache[run_id]
