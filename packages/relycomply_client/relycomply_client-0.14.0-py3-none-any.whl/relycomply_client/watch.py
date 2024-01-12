from pathlib import Path
from typing import Optional
import typer
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
from relycomply_client.cli import RelyComplyCLI
from relycomply_client.sync import RelySync, sync
from watchfiles import watch
from watchfiles import Change, DefaultFilter, watch


class TomlFilter(DefaultFilter):
    allowed_extensions = ".toml"

    def __call__(self, change: Change, path: str) -> bool:
        return super().__call__(change, path) and path.endswith(self.allowed_extensions)


def watch_new(
    location: Optional[Path] = typer.Argument(Path(".")),
    recursive: bool = typer.Option(False),
    interactive: bool = typer.Option(False),
):
    cli = RelyComplyCLI()

    abs_location = location.absolute()
    wait_message = f"Waiting for changes at path: {abs_location} {'(recursive)' if recursive else ''}\n"

    print(wait_message)

    for changes in watch(
        location, recursive=recursive, debounce=300, watch_filter=TomlFilter()
    ):
        print("Detected changes in:")
        for change in changes:
            print(f"  - {change[1]}")
        print()
        changed_locations = [change[1] for change in changes]
        rely_sync = RelySync(changed_locations, recursive, interactive, cli=cli)
        rely_sync.run_cli()
        print()
        print(wait_message)


def main():
    typer.run(watch_new)


if __name__ == "__main__":
    main()
