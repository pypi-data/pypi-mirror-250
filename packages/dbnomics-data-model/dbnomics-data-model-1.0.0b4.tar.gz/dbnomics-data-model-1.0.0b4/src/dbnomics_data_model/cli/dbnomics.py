#! /usr/bin/env python3

import logging
from typing import TYPE_CHECKING, Annotated, Final, Optional

import daiquiri
from click import BadParameter
from typer import Context, Option, Typer

from dbnomics_data_model.cli.parsers import parse_csv_str, parse_validation_error_codes
from dbnomics_data_model.validation.validation_settings import current_validation_settings_var

from .commands.dataset.app import dataset_app
from .commands.provider.app import provider_app
from .commands.series.app import series_app
from .commands.update import update
from .commands.validate import validate

if TYPE_CHECKING:
    from dbnomics_data_model.validation.errors.validation_error_code import ValidationErrorCode

DEFAULT_LOG_LEVELS: Final = "dbnomics_data_model.cli=INFO"
DISABLE_VALIDATION_ERROR_CODES_OPTION_NAME: Final = "--disable-validation-error-codes"
LOG_LEVELS_OPTION_NAME: Final = "--log-levels"

logger = daiquiri.getLogger(__name__)


app = Typer(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)
app.add_typer(dataset_app)
app.add_typer(provider_app)
app.add_typer(series_app)
app.command(name="update")(update)
app.command(name="validate")(validate)


@app.callback()
def app_callback(
    *,
    ctx: Context,
    debug: Annotated[bool, Option(help="Display debug messages logged by dbnomics_data_model")] = False,
    fail_fast: Annotated[bool, Option(envvar="FAIL_FAST", help="Stop at the first exception")] = False,  # noqa: ARG001
    disabled_validation_error_codes_str: Annotated[
        Optional[str],
        Option(
            DISABLE_VALIDATION_ERROR_CODES_OPTION_NAME,
            envvar="DISABLE_VALIDATION_ERROR_CODES",
            help="Disable those validation error codes",
        ),
    ] = None,
    log_levels_str: Annotated[
        str,
        Option(
            LOG_LEVELS_OPTION_NAME,
            envvar="LOG_LEVELS",
            help="Logging levels: logger_name1=log_level1,logger_name2=log_level2[,...]",
        ),
    ] = DEFAULT_LOG_LEVELS,
    storage_uri_or_dir: Annotated[str, Option(envvar="STORAGE_URI")],  # noqa: ARG001
    verbose: Annotated[
        bool, Option("-v", "--verbose", help="Display debug messages logged by dbnomics_data_model")
    ] = False,
) -> None:
    """DBnomics CLI tool."""
    disabled_validation_error_codes: set[ValidationErrorCode] = set()
    if disabled_validation_error_codes_str is not None:
        try:
            disabled_validation_error_codes = parse_validation_error_codes(disabled_validation_error_codes_str)
        except Exception as exc:
            raise BadParameter(str(exc), param_hint=DISABLE_VALIDATION_ERROR_CODES_OPTION_NAME) from exc
    root_ctx_params = ctx.find_root().params
    root_ctx_params["disabled_validation_error_codes"] = disabled_validation_error_codes

    try:
        log_levels = parse_csv_str(log_levels_str)
    except Exception as exc:
        raise BadParameter(str(exc), param_hint=LOG_LEVELS_OPTION_NAME) from exc

    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)]
    )
    daiquiri.parse_and_set_default_log_levels(log_levels)

    validation_settings = current_validation_settings_var.get()
    if disabled_validation_error_codes is not None:
        new_validation_settings = validation_settings.disable(disabled_validation_error_codes)
        current_validation_settings_var.set(new_validation_settings)


if __name__ == "__main__":
    app()
