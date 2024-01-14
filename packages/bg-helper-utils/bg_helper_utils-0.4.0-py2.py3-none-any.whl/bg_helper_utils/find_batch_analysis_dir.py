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
from rich.progress import Progress
from datetime import datetime
from typing import Any, Dict

from .console_helper import print_red, print_yellow, print_green
from .file_utils import check_indir_status, check_infile_status, calculate_md5, get_file_size, get_file_creation_date, get_file_list_from_directory
from .helper import get_analyis_type, get_batch_id

console = Console()

DEFAULT_PROJECT = "bg-helper-utils"


# If set to True, will profile each of the files nest in the
# batch analysis directory. This means the following attributes
# will be derived and printed to the report file:
# - file size
# - md5sum
# - date created
DEFAULT_PROFILE_DIR_FILES = False

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


def find_batch_analysis_dir(
        config_file: str,
        config: Dict[str, Any],
        logfile: str,
        outdir: str,
        outfile: str,
        profile: bool = DEFAULT_PROFILE_DIR_FILES) -> None:
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

    if profile:
        console.print(f"[bold green]Profiling batch analysis directory[/] '{analysis_dir}'")
        profile_dir_files(analysis_dir, outfile, logfile, config_file)
    else:
        console.print(f"[bold green]Found batch analysis directory[/] '{analysis_dir}'")


def profile_dir_files(analysis_dir: str, outfile: str, logfile: str, config_file: str)  -> None:
    file_list = get_file_list_from_directory(analysis_dir)
    if len(file_list) == 0:
        print_red(f"Could not find any files in directory '{analysis_dir}'")
        sys.exit(0)

    lookup = {}

    count = len(file_list)

    with Progress() as progress:
        task = progress.add_task(f"[cyan]Profiling {count} files", total=count)

        for f in file_list:
            md5sum = calculate_md5(f)
            filesize = get_file_size(f)
            date_created = get_file_creation_date(f)
            lookup[f] = {
                "md5sum": md5sum,
                "filesize": filesize,
                "date_created": date_created,
            }
            progress.update(task, advance=1)


    generate_report(lookup, analysis_dir, outfile, logfile, config_file, count)


def generate_report(lookup: Dict[str, Dict[str, str]], analysis_dir: str, outfile: str, logfile: str, config_file: str, count: int) -> None:

    with open(outfile, 'w') as of:
        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## batch-analysis-dir: {analysis_dir}\n")
        of.write(f"## config-file: {config_file}\n")
        of.write(f"## logfile: {logfile}\n")

        with Progress() as progress:
            task = progress.add_task(f"[cyan]Generating report for {count} files", total=count)

            for f in lookup:
                md5sum = lookup[f]["md5sum"]
                filesize = lookup[f]["filesize"]
                date_created = lookup[f]["date_created"]
                line = f"{f}\nmd5sum: {md5sum}\nbytesize: {filesize}\ndate created: {date_created}"

                of.write(f"{line}\n\n")

                progress.update(task, advance=1)

    logging.info(f"Wrote report file '{outfile}'")
    print(f"Wrote report file '{outfile}'")


def validate_profile(ctx, param, value):
    if value is None:
        click.secho("--profile was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_PROFILE_DIR_FILES
    return value

def validate_verbose(ctx, param, value):
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"Optional: The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output report file containing profile metadata")
@click.option('--profile', is_flag=True, help=f"Optional: If set to True, will profile all files in the batch analysis directory - default is '{DEFAULT_PROFILE_DIR_FILES}'.", callback=validate_profile)
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: str, logfile: str, outdir: str, outfile: str, profile: bool, verbose: bool):
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

    if outfile is None:
        outfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.report.txt'
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")

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


    find_batch_analysis_dir(
        config_file,
        config,
        logfile,
        outdir,
        outfile,
        profile
    )

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
