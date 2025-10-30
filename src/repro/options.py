import os
from collections.abc import Iterable
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Optional, Union

import attrs
import click
import typed_settings as ts
import typed_settings.types as tst


def click_bad_parameter(fn):
    """Wrap validator to return click.BadParameter."""

    @wraps(fn)
    def wrapper(instance: Any, attribute: attrs.Attribute, value):
        if isinstance(instance, click.core.Context):
            try:
                return fn(instance, attribute, value)
            # TODO: this should catch a custom exception instead
            except ValueError as err:
                raise click.BadParameter(str(err)) from err
        return fn(instance, attribute, value)

    return wrapper


def empty_str_to_none(val: str):
    """Replace empty string with ``None``."""
    if val == "":
        return None
    return val


def loaders(
    appname: str,
    config_files: Iterable[Union[str, Path]] = (),
    *,
    config_file_section: Union[str, None] = None,
) -> list[ts.loaders.Loader]:
    """
    Load config files.

    Wrapper around ts.default_loaders with opinionated settings.

    Args:
        appname: Your application's name - used to derive defaults for the
          remaining args.

        config_files: Load settings from these files. The last one has the
          highest precedence.

        config_file_section: Name of your app's section in the config file.
          By default, use *appname* (in lower case and with "_" replaced by
          "-").

    """
    if config_file_section is None:
        env_prefix = f"{appname}_".upper()
        section = tst.AUTO
    else:
        section = config_file_section
        env_prefix = f"{appname}_{config_file_section}_".upper()

    return ts.default_loaders(
        appname,
        config_files,
        config_file_section=section,
        env_prefix=env_prefix,
    )


@ts.settings
class CLIOptions:
    """Global options for CLI app."""

    sentry_dsn: Optional[str] = ts.option(help="If provided, errors are sent to Sentry.")
    log: bool = ts.option(default=True, help="Print logs.")

@ts.settings
class ExecuteOptions:
    """Options for execute command."""
    output_path: str = ts.option(init=False, help="Dynamically set from the input filename")
    engine_name: str = ts.option(default="", converter=empty_str_to_none,help="engine")
    

    def __attrs_post_init__(self):
        """Here we set properties that have init=False and do not fit as property."""
        self.output_path = os.path.join(self.output_dir, "dummy")
