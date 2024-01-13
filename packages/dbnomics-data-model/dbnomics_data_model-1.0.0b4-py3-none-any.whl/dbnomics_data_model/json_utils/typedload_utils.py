from collections.abc import Callable
from typing import Any, TypeAlias

from typedload.datadumper import Dumper
from typedload.dataloader import Loader
from typedload.exceptions import TypedloadValueError

from dbnomics_data_model.model.identifiers import AttributeCode
from dbnomics_data_model.model.identifiers.dataset_code import DatasetCode
from dbnomics_data_model.model.identifiers.simple_code import SimpleCode
from dbnomics_data_model.model.periods.periods import Period, YearPeriod
from dbnomics_data_model.model.url import PublicUrl, Url

TypedloadHandler: TypeAlias = tuple[Callable[[Any], bool], Callable[[Dumper, Any, type], Any]]


strconstructed: set[type] = {AttributeCode, PublicUrl, SimpleCode, Url}


def add_handler(dumper: Dumper, handler: TypedloadHandler, *, sample_value: Any) -> None:
    try:
        index = dumper.index(sample_value)
    except TypedloadValueError:
        index = len(dumper.handlers)
    dumper.handlers.insert(index, handler)


def create_to_str_handler(type: type) -> TypedloadHandler:
    return (
        lambda x: isinstance(x, type),
        lambda _dumper, value, _value_type: str(value),
    )


def create_toolbox_dumper(*, codes_as_str: bool = False, period_as_str: bool = False) -> Dumper:
    dumper = Dumper(hidedefault=False, isodates=True, strconstructed=strconstructed)

    if codes_as_str:
        add_handler(dumper, create_to_str_handler(DatasetCode), sample_value=DatasetCode.parse("D1"))

    if period_as_str:
        add_handler(dumper, create_to_str_handler(Period), sample_value=YearPeriod(year_num=2000))

    return dumper


def create_toolbox_loader() -> Loader:
    return Loader(strconstructed=strconstructed)
