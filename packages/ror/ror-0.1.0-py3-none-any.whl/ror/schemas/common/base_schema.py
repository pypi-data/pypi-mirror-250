# External imports
from dataclasses import dataclass, fields, make_dataclass
from typing import List, Set

# Local imports
from ror.utils._const import FIELD_PERSISTANCE

from .artifact_schema import ArtifactSchema


@dataclass
class BaseSchema:
    """BaseSchema is extended for any Input our Output dataclass for each stage,
    which implements a set of functions to get artifacts of the current stage
    (all fields which are `perishable`), and to get the carry over to some Output
    dataclass (fields marked as `persistant`).

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from pypipeline.schemas import BaseSchema
    >>> from pypipeline.schemas.fields import field_perishable, field_persistance

    Which will enable you to define input or output dataclasses for your stage

    >>> @dataclass
    >>> class InputTest(BaseSchema):
    >>>     A: str = field_persistance()
    >>>     B: str = field_perishable()

    >>> @dataclass
    >>> class OutputTest(BaseSchema):
    >>>     A: str = field_persistance()

    Where Output does not contain field B as it is marked perishable in the input,
    and thus this data is only used in the computation for this stage and not
    propagated further from the output data of this stage.
    """

    def _del_fields(self, fields: List[str]) -> dict:
        """Given a list of field key names in the dataclass, remove these from
        the dataclass instance.

        Parameters
        ----------
        fields : List[str]
            List of dataclass key names.

        Returns
        -------
        dict
            Dictionary representation of the new data which will be in the
            dataclass after removal.
        """
        _temp = self.__dict__.copy()

        for field in fields:
            _temp.pop(field)

        return _temp

    def _get_fields(self, schema: dataclass) -> List[str]:
        """Gets all the key names as a list of strings present in the current
        instance if the dataclass.

        Parameters
        ----------
        schema : dataclass
            Dataclass to extract key names from.

        Returns
        -------
        List[str]
            List of strings representing the key/field names in dataclass.
        """
        return [v.name for v in fields(schema)]

    def _get_perishables(self, schema: dataclass) -> List[str]:
        """Similar to `self._get_fields` but extracts only the list of key/field
        names which are marked as perishable.

        Parameters
        ----------
        schema : dataclass
            Dataclass instance to extract perishable field/key names from.

        Returns
        -------
        List[str]
            List of strings representing the perishable key/field names.
        """
        return [v.name for v in fields(schema) if not v.metadata[FIELD_PERSISTANCE]]

    def _validate_retire(self, fields: Set[str]) -> None:
        """Given a set of unique field names to retire/drop from the dataclass
        verify that the field names are indeed present in the instance of this
        dataclass.

        Parameters
        ----------
        fields : Set[str]
            Set of unique field/key names to possibly retire.

        Raises
        ------
        Exception
            Raises an exception if the set of fields contain a field which is not
            present in the instance of this dataclass.
        """
        _fields = set(self._get_fields(schema=self))
        _shared_fields = fields.intersection(_fields)

        if len(_shared_fields) != len(fields):
            _diff = set(fields) - _fields
            raise Exception(
                f"""
                  Fields to retire not present:
                    - {_diff}
                  Out of:
                    - {_fields}
                """
            )

    def _get_field_types(self, schema: dataclass) -> dict:
        """Constructs a dict, where for some key name we get the type of the field,
        thus returning a dict.

        Parameters
        ----------
        schema : dataclass
            A dataclass instance to extract the field types from.

        Returns
        -------
        dict
            Dictionary with keys names and their repsective types.
        """
        return {v.name: v.type for v in fields(schema)}

    def get_artifact(self) -> ArtifactSchema:
        """Constructs an ArtfifactSchema instance with the data which was marked
        as perishable from the instance of this dataclass, and implicitly deletes
        the perishable fields from this instance.

        Returns
        -------
        ArtifactSchema
            Dataclass containing the perishable data and additional meta-data.
        """
        _perishables = self._get_perishables(schema=self)
        _base_fields = self._get_fields(schema=self)

        artifact_fields = set(_base_fields) - set(_perishables)
        _fields = [
            (n, t)
            for n, t in self._get_field_types(schema=self).items()
            if n in _perishables
        ]
        _values = self._del_fields(artifact_fields)

        return make_dataclass("Artifact", fields=_fields, bases=(ArtifactSchema,))(
            **_values, source_schema=self.__class__
        )

    def get_carry(self) -> dict:
        """Returns a dictionary instance of this dataclass where all the perishable
        fields are removed from the dictionary.

        Returns
        -------
        dict
            Carry over dictionary without the perishable fields.
        """
        _perishables = self._get_perishables(schema=self)

        return self._del_fields(_perishables)
