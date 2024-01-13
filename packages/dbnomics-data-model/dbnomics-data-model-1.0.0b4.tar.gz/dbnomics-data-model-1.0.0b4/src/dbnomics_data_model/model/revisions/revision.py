from dataclasses import dataclass, field
from datetime import datetime
from textwrap import indent
from typing import Final

from rich.console import Console, ConsoleOptions, RenderResult

from dbnomics_data_model.model.revisions.types import RevisionId, RevisionMetadata

AUTHOR_KEY: Final = "Author"
DATE_KEY: Final = "Date"


@dataclass(frozen=True, kw_only=True)
class Revision:
    author_email: str | None
    author_name: str
    created_at: datetime
    id: RevisionId
    message: str = field(repr=False)

    metadata: RevisionMetadata = field(default_factory=dict)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        def format_key(key: str) -> str:
            key1 = f"{key}:"
            return f"{key1:{padding + 2}}"

        yield f"[orange3]revision {self.id}[/]"

        padding = max(len(key) for key in [AUTHOR_KEY, DATE_KEY, *self.metadata.keys()])

        yield f"{format_key(AUTHOR_KEY)}{self.formatted_author}"
        yield f"{format_key(DATE_KEY)}{self.formatted_created_at}"
        yield from (f"{format_key(k.capitalize())}{v}" for k, v in sorted(self.metadata.items()))
        yield ""
        yield indent(self.message, 4 * " ")

    def __str__(self) -> str:
        return self.id

    @property
    def formatted_author(self) -> str:
        if self.author_email is None:
            return self.author_name

        return f"{self.author_name} <{self.author_email}>"

    @property
    def formatted_created_at(self) -> str:
        return self.created_at.strftime("%a %b %d %H:%M:%S %Y %z")
