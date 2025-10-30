from pathlib import Path

import click
import typed_settings as ts


from .options import (
    CLIOptions,
    ExecuteOptions,
    loaders,
)

HERE = Path(__file__).parent
CONFIG_FILES = [ts.find("settings.toml"), ts.find(".secrets.toml")]
APPNAME = "repro"

@click.group()
@ts.click_options(
    CLIOptions,
    loaders=loaders(
        appname=APPNAME,
        config_files=CONFIG_FILES,
    ),
    argname="opts",
)
def app(
    opts: CLIOptions,
):
    print("main cli runs")
    pass

@click.command()
@ts.click_options(
    ExecuteOptions,
    loaders=loaders(
        appname=APPNAME,
        config_files=CONFIG_FILES,
        config_file_section="execute",
    ),
)
def execute(opts: ExecuteOptions):
    print("this should run", opts.engine_name)


app.add_command(execute)


if __name__ == "__main__":
    app()
