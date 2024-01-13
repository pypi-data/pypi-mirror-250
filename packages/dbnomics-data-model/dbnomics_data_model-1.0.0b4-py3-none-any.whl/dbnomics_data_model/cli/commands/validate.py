from typing import TYPE_CHECKING, Annotated, Optional

from more_itertools import peekable
from typer import Abort, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.validation.errors.validation_error_chain import build_error_chain
from dbnomics_data_model.validation.storage_validator import StorageValidator

if TYPE_CHECKING:
    from dbnomics_data_model.validation.errors.validation_error_code import ValidationErrorCode

__all__ = ["validate"]


def validate(
    *,
    ctx: Context,
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Validate storage at this revision")
    ] = None,
    series_per_dataset_limit: Annotated[
        Optional[int],
        Option(
            envvar="SERIES_PER_DATASET_LIMIT",
            help="Maximum number of series to validate per dataset. If not set, validate all series.",
        ),
    ] = None,
) -> None:
    """Validate data of a DBnomics storage."""
    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]
    disabled_validation_error_codes: set[ValidationErrorCode] = root_ctx_params["disabled_validation_error_codes"]

    if series_per_dataset_limit is not None and series_per_dataset_limit <= 0:
        console.print(f"series limit must be strictly positive, got {series_per_dataset_limit!r}")
        raise Abort

    storage = open_storage(storage_uri_or_dir)

    validator = StorageValidator(
        revision_id=revision_id, series_per_dataset_limit=series_per_dataset_limit, storage=storage
    )
    storage_validator_errors = peekable(validator.iter_errors())

    had_any_error = False

    for error in storage_validator_errors:
        error_root_node = build_error_chain(error)
        if error_root_node.data is not None and error_root_node.data.code in disabled_validation_error_codes:
            continue

        error_json = error_root_node.to_json()
        console.print_json(data=error_json)
        had_any_error = True

    if had_any_error:
        raise Abort
