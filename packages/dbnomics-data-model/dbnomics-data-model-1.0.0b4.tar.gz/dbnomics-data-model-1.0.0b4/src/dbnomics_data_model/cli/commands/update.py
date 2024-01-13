from typing import Annotated

from typer import Abort, Argument, Context, Option

from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.storage.storage_updater import StorageUpdater
from dbnomics_data_model.storage.types import UpdateStrategy

__all__ = ["update"]


def update(
    *,
    ctx: Context,
    category_tree_update_strategy: Annotated[
        UpdateStrategy, Option(envvar="CATEGORY_TREE_UPDATE_STRATEGY")
    ] = UpdateStrategy.MERGE.value,  # type: ignore[assignment]
    dataset_update_strategy: Annotated[
        UpdateStrategy, Option(envvar="DATASET_UPDATE_STRATEGY")
    ] = UpdateStrategy.REPLACE.value,  # type: ignore[assignment]
    target_storage_uri_or_dir: Annotated[
        str, Argument(envvar="TARGET_STORAGE_URI", help="Update this storage with data from the main storage")
    ],
) -> None:
    """Update a DBnomics storage with data from another one."""
    root_ctx_params = ctx.find_root().params
    source_storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    if source_storage_uri_or_dir == target_storage_uri_or_dir:
        console.print(
            f"Source storage URI {source_storage_uri_or_dir!r} must be different than the target one {target_storage_uri_or_dir!r}"  # noqa: E501
        )
        raise Abort

    source_storage = open_storage(source_storage_uri_or_dir)
    target_storage = open_storage(target_storage_uri_or_dir)

    storage_updater = StorageUpdater(
        source_storage=source_storage,
        target_storage=target_storage,
    )
    storage_updater.update(
        category_tree_update_strategy=category_tree_update_strategy,
        dataset_update_strategy=dataset_update_strategy,
    )
