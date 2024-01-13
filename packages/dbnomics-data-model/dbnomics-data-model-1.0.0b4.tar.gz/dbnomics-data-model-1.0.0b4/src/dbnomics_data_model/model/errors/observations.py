from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.observations import Observation


class ObservationError(DataModelError):
    def __init__(self, *, msg: str, observation: Observation) -> None:
        super().__init__(msg=msg)
        self.observation = observation
