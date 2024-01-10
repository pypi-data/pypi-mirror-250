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
from .file_utils import check_indir_status, check_infile_status
from .helper import get_analyis_type, get_batch_id

console = Console()

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

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()


def find_batch_analysis_dir(config_file: str, config: Dict[str, Any]) -> None:
    """Find the samplesheet.

    Args:
        config_file (str): the configuration file path
        config (Dict[str, Any]): The configuration
    """
    if "analysis_base_dir" not in config:
        raise Exception(f"Could not find 'analysis_base_dir' in config file '{config_file}'")

    analysis_base_dir= config["analysis_base_dir"]
    check_indir_status(analysis_base_dir)

    analysis_type = get_analyis_type()
    batch_id = get_batch_id()

    if "batch_analysis" not in config:
        raise Exception(f"Could not find 'batch_analysis' in config file '{config_file}'")

    if "analysis_file_type_mapping" not in config["batch_analysis"]:
        raise Exception(f"Could not find 'analysis_file_type_mapping' in 'batch_analysis' section in config file '{config_file}'")

    if analysis_type not in config["batch_analysis"]["analysis_file_type_mapping"]:
        raise Exception(f"Could not find analysis type '{analysis_type}' in 'analysis_file_type_mapping' in 'batch_analysis' section in config file '{config_file}'")

    analysis_file_type = config["batch_analysis"]["analysis_file_type_mapping"][analysis_type]

    analysis_dir = os.path.join(analysis_base_dir, analysis_file_type, batch_id)

    check_indir_status(analysis_dir)

    console.print(f"[bold green]Found batch analysis directory[/] '{analysis_dir}'")



def validate_verbose(ctx, param, value):
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--logfile', help="The log file")
@click.option('--outdir', help=f"The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: str, logfile: str, outdir: str, verbose: bool):
    """Find the samplesheet."""
    error_ctr = 0

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

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

    check_infile_status(config_file, "yaml")

    if verbose:
        logging.info(f"Will load contents of config file '{config_file}'")
        console.log(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(pathlib.Path(config_file).read_text())


    find_batch_analysis_dir(config_file, config)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
