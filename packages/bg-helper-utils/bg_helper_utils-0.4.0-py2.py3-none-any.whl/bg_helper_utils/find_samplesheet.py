#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import click
import pathlib
import logging
import pathlib
import yaml

from rich.console import Console
from datetime import datetime
from typing import Any, Dict

from .console_helper import print_red, print_yellow, print_green
from .file_utils import check_indir_status, check_infile_status, calculate_md5, get_file_size, get_file_creation_date, get_line_count
from .helper import get_analyis_type, get_batch_id

DEFAULT_PROJECT = "bg-helper-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime("%Y-%m-%d-%H%M%S"))

DEFAULT_OUTDIR = os.path.join(
    "/tmp/",
    os.getenv("USER"),
    DEFAULT_PROJECT,
    os.path.basename(__file__),
    DEFAULT_TIMESTAMP,
)


DEFAULT_CONFIG_FILE = os.path.join(
    os.getcwd(),
    'conf',
    'config.yaml'
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def find_samplesheet(config_file: str, config: Dict[str, Any]) -> None:
    """Find the samplesheet.

    Args:
        config_file (str): the configuration file path
        config (Dict[str, Any]): The configuration
    """
    if "base_samplesheet_dir" not in config:
        raise Exception(f"Could not find 'base_samplesheet_dir' in config file '{config_file}'")

    base_samplesheet_dir = config["base_samplesheet_dir"]
    check_indir_status(base_samplesheet_dir)

    analysis_type = get_analyis_type()
    batch_id = get_batch_id()

    if "samplesheet" not in config:
        raise Exception(f"Could not find 'samplesheet' in config file '{config_file}'")

    if "analysis_file_type_mapping" not in config["samplesheet"]:
        raise Exception(f"Could not find 'analysis_file_type_mapping' in 'samplesheet' section in config file '{config_file}'")

    if analysis_type not in config["samplesheet"]["analysis_file_type_mapping"]:
        raise Exception(f"Could not find '{analysis_type}' in 'analysis_file_type_mapping' in 'samplesheet' section in config file '{config_file}'")

    analysis_file_type = config["samplesheet"]["analysis_file_type_mapping"][analysis_type]

    samplesheet = os.path.join(
        base_samplesheet_dir,
        batch_id,
        f"{batch_id}_{analysis_file_type}_samplesheet.csv"
    )

    if os.path.exists(samplesheet):

        console.print(f"\n[bold green]Found samplesheet[/] '{samplesheet}'")
        md5sum = calculate_md5(samplesheet)
        filesize = get_file_size(samplesheet)
        date_created = get_file_creation_date(samplesheet)
        line_count = get_line_count(samplesheet)

        console.print(f"[yellow]md5sum[/]: {md5sum}")
        console.print(f"[yellow]filesize[/]: {filesize}")
        console.print(f"[yellow]date_created[/]: {date_created}")
        console.print(f"[yellow]line_count[/]: {line_count}")
    else:
        print_red(f"Could not find samplesheet '{samplesheet}'")



def validate_verbose(ctx, param, value):
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--logfile', help="The log file")
@click.option('--outdir', help="The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="The output final report file")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: str, logfile: str, outdir: str, outfile: str, verbose: bool):
    """Find the samplesheet."""
    error_ctr = 0

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    check_infile_status(config_file, "yaml")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        print_yellow(f"--logfile was not specified and therefore was set to '{logfile}'")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    if verbose:
        logging.info(f"Will load contents of config file '{config_file}'")
        console.print(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(pathlib.Path(config_file).read_text())

    find_samplesheet(config_file, config)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
