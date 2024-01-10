# External import
from dataclasses import dataclass


@dataclass
class ArtifactSchema:
    """A simple dataclass schema which is supposed to only contain the perishable
    fields which where dropped from some source BaseSchema.
    """

    source_schema: dataclass

    def get_standard_fields(self):
        return ["source_schema"]
