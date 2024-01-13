"""Validate a SLURM shell script."""
import click
import logging
import os
import pathlib
import sys
import yaml

from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from typing import Any, Dict, List

from .console_helper import print_red, print_yellow, print_green
from .file_utils import check_infile_status


DEFAULT_PROJECT = "slurm-helper-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.getenv("USER"),
    DEFAULT_PROJECT,
    os.path.splitext(os.path.basename(__file__))[0],
    DEFAULT_TIMESTAMP
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.getcwd(),
    'conf',
    'config_builder.yaml'
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def create_slurm_script(
    config: Dict[str, Any],
    config_file: str,
    logfile: str,
    outfile: str,
    outdir: str = DEFAULT_OUTDIR
    ) -> None:
    """Prompt the user and then create the SLURM sbatch script.

    Args:
        config (Dict[str, Any]): The dictionary representation of the YAML config file.
        config_file (str): The YAML config file.
        outfile (str): The output SLURM sbatch script.
        outdir (str, optional): The output directory. Defaults to DEFAULT_OUTDIR.
    """
    directive_to_option_lookup = {}

    process_required_directives(
        directive_to_option_lookup,
        config,
        config_file,
    )

    if "optional_directives" in config:

        process_optional_directives(
            directive_to_option_lookup,
            config,
        )

    write_slurm_script(
        config_file,
        logfile,
        outfile,
        directive_to_option_lookup
    )


def write_slurm_script(
    config_file: str,
    logfile: str,
    outfile: str,
    directive_to_option_lookup: Dict[str, str]
    ) -> None:
    """Write the SLURM sbatch script.

    Args:
        outfile (str): The output SLURM sbatch script.
        directive_to_option_lookup (Dict[str, str]): The dictionary lookup for directive to option.
    """
    with open(outfile, 'w') as of:
        of.write("#!/bin/bash\n\n")
        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## config-file: {config_file}\n")
        of.write(f"## logfile: {logfile}\n\n\n")
        for directive, option in directive_to_option_lookup.items():
            of.write(f"#SBATCH --{directive}={option}\n")

    logging.info(f"Wrote SLURM sbatch script '{outfile}'")
    console.print(f"Wrote SLURM sbatch script '{outfile}'")


def process_required_directives(
    directive_to_option_lookup: Dict[str, Any],
    config: Dict[str, Any],
    config_file: str
    ) -> None:
    if "required_directives" not in config:
        print_red(f"The 'required_directives' key was not found in the config file '{config_file}'")
        sys.exit(1)

    directives_lookup = config["required_directives"]
    directives_list = [d for d in directives_lookup]

    console.print(f"There are '{len(directives_list)}' required directives")

    prompt_user(
        directives_list,
        directives_lookup,
        directive_to_option_lookup
    )


def process_optional_directives(
    directive_to_option_lookup: Dict[str, Any],
    config: Dict[str, Any],
    ) -> None:

    directives_lookup = config["optional_directives"]
    directives_list = [d for d in directives_lookup]

    console.print(f"There are '{len(directives_list)}' optional directives")

    prompt_user(
        directives_list,
        directives_lookup,
        directive_to_option_lookup
    )


def prompt_user(
    directives_list: List[str],
    directives_lookup: Dict[str, List[str]],
    directive_to_option_lookup: Dict[str, str]) -> None:
    """Prompt the user for the directives.

    Args:
        directives_list (List[str]): List of directives.
        directives_lookup (Dict[str, List[str]]): Dictionary lookup for directives.
        directive_to_option_lookup (Dict[str, str]): Dictionary lookup for directive to option.
    """
    for i, directive in enumerate(directives_list):

        if "qualified_options" in directives_lookup[directive]:

            options = directives_lookup[directive]["qualified_options"]
            options_str = [str(o) for o in options]

            console.print(f"Please enter the option for directive '[bold yellow]{directive}[/]':")
            console.print(f"options: {options_str}")

            completer = WordCompleter(options_str)
            answer = prompt(f"Enter {directive}: ", completer=completer)
            directive_to_option_lookup[directive] = answer

    logging.info(f"directive_to_option_lookup: {directive_to_option_lookup}")


def validate_verbose(ctx, param, value):
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=str, help=f"Optional: The YAML configuration file - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The output directory where logfile and default output file will be written - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output SLURM sbatch script to be created")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: str, logfile: str, outdir: str, outfile: str, verbose: bool):
    """Validate a SLURM shell script."""
    error_ctr = 0

    if error_ctr > 0:
        print_red("Required command-line arguments were not provided")
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    check_infile_status(config_file)

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
            "slurm_sbatch.sh"
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )


    if verbose:
        console.print(f"Will load contents of config file '{config_file}'")
        logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(pathlib.Path(config_file).read_text())

    create_slurm_script(
        config,
        config_file,
        logfile,
        outfile,
        outdir,
    )

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
