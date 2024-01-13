from collections.abc import Sequence

from dbnomics_data_model.cli.renderables.dataclass_table import DataclassTable
from dbnomics_data_model.model.provider_metadata import ProviderMetadata


class ProviderMetadataTable(DataclassTable[ProviderMetadata]):
    @property
    def column_names(self) -> Sequence[str] | None:
        return ["code", "name", "region", "description", "website"]
