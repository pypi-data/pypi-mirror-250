# External import
from dataclasses import Field, field

# Local imports
from ror.utils._const import FIELD_PERSISTANCE


def field_persistance(**kwargs) -> Field:
    """Dataclass field type which indeicates that this field will be carried over
    to the output dataclass. Thus, fields with this propoerty will be carried over
    until there is some BaseSchema at a stage which sets it to `perishable`.

    Returns
    -------
    Field
        Dataclass field with the `FIELD_PERSISTANCE` flag set to True.
    """
    return field(metadata={FIELD_PERSISTANCE: True}, **kwargs)
