# External import
from dataclasses import Field, field

# Local imports
from ror.utils._const import FIELD_PERSISTANCE


def field_perishable(**kwargs) -> Field:
    """Field type for fields in the BaseSchema to mark fields as perishable
    which will be a part of the ArtifactSchema produced for this BaseSchema.

    Returns
    -------
    Field
        Dataclass field with the `FIELD_PERSISTANCE` flag set to False.
    """
    return field(metadata={FIELD_PERSISTANCE: False}, **kwargs)
