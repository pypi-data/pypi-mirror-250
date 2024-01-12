"""Validate a SLURM shell script."""
import click
import logging
import os
import pathlib
import re
import sys
import yaml

from typing import Any, Dict, List
from datetime import datetime
from rich.console import Console

from .console_helper import print_red, print_yellow, print_green
from .file_utils import check_infile_status


DEFAULT_PROJECT = "slurm-utils"

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
    'config.yaml'
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


error_console = Console(stderr=True, style="bold red")

console = Console()


def is_output_valid(line: str) -> bool:
    """Verify whether the output directive is valid.

    Args:
        line (str): The SBATCH output directive.

    Raises:
        Exception: if output directive could not be derived from the line

    Returns:
        bool: True if valid, False if invalid
    """
    if line.startswith("#SBATCH --output="):
        output = line.split("=")[1]
        # output = line.lstrip("#SBATCH --output=").strip()
    elif line.startswith("#SBATCH -o="):
        output = line.split("=")[1]
        # output = line.lstrip("#SBATCH -o=").strip()
    else:
        raise Exception(f"Line '{line}' does not contain '--output=' or '-o='")

    dirname = os.path.dirname(output)

    if not os.path.exists(dirname):
        print_red(f"output directory '{dirname}' does not exist")
        return False

    logging.info(f"output: '{output}' is valid")
    return True


def is_error_valid(line: str) -> bool:
    """Verify whether the error directive is valid.

    Args:
        line (str): The SBATCH error directive.

    Raises:
        Exception: if error directive could not be derived from the line

    Returns:
        bool: True if valid, False if invalid
    """
    if line.startswith("#SBATCH --error="):
        error = line.split("=")[1]
        # error = line.lstrip("#SBATCH --error=").strip()
    elif line.startswith("#SBATCH -e="):
        error = line.split("=")[1]
        # error = line.lstrip("#SBATCH -e=").strip()
    else:
        raise Exception(f"Line '{line}' does not contain '--error=' or '-e='")
    dirname = os.path.dirname(error)

    if not os.path.exists(dirname):
        print_red(f"error directory '{dirname}' does not exist")
        return False

    logging.info(f"error: '{error}' is valid")
    return True


def is_qos_valid(line: str, config: Dict[str, Any], config_file: str) -> bool:
    """Verify whether the qos directive is valid.

    Args:
        line (str): The SBATCH qos directive.

    Raises:
        Exception: if qos directive could not be derived from the line

    Returns:
        bool: True if valid, False if invalid
    """
    if line.startswith("#SBATCH --qos="):
        qos = line.split("=")[1]
    elif line.startswith("#SBATCH -q="):
        qos = line.split("=")[1]
    else:
        raise Exception(f"Line '{line}' does not contain '--qos=' or '-q='")

    if "qualified_qos_list" not in config:
        raise Exception(f"qualified_qos_list not found in config file '{config_file}'")

    qualified_qos_list = config["qualified_qos_list"]
    if qos not in qualified_qos_list:
        print_red(f"qos '{qos}' is not in the qualified_qos_list")
        return False

    logging.info(f"qos: '{qos}' is valid")
    return True


def is_gres_valid(line: str, config: Dict[str, Any], config_file: str) -> bool:
    """Verify whether the gres directive is valid.

    Args:
        line (str): The SBATCH gres directive.

    Raises:
        Exception: if gres directive could not be derived from the line

    Returns:
        bool: True if valid, False if invalid
    """
    if line.startswith("#SBATCH --gres="):
        gres = line.split("=")[1]
    else:
        raise Exception(f"Line '{line}' does not contain '--gres='")

    if "qualified_gres_list" not in config:
        raise Exception(f"qualified_gres_list not found in config file '{config_file}'")

    qualified_gres_list = config["qualified_gres_list"]
    if gres not in qualified_gres_list:
        print_red(f"gres '{gres}' is not in the qualified_gres_list")
        return False

    logging.info(f"gres: '{gres}' is valid")
    return True


def is_export_valid(line: str, config: Dict[str, Any], config_file: str) -> bool:
    """Verify whether the export directive is valid.

    Args:
        line (str): The SBATCH export directive.

    Raises:
        Exception: if export directive could not be derived from the line

    Returns:
        bool: True if valid, False if invalid
    """
    if line.startswith("#SBATCH --export="):
        export = line.split("=")[1]
    else:
        raise Exception(f"Line '{line}' does not contain '--export='")

    if "qualified_export_list" not in config:
        raise Exception(f"qualified_export_list not found in config file '{config_file}'")

    qualified_export_list = config["qualified_export_list"]
    if export not in qualified_export_list:
        print_red(f"export '{export}' is not in the qualified_export_list")
        return False

    logging.info(f"export: '{export}' is valid")
    return True


def is_propagate_valid(line: str, config: Dict[str, Any], config_file: str) -> bool:
    """Verify whether the propagate directive is valid.

    Args:
        line (str): The SBATCH propagate directive.

    Raises:
        Exception: if propagate directive could not be derived from the line

    Returns:
        bool: True if valid, False if invalid
    """
    if line.startswith("#SBATCH --propagate="):
        propagate = line.split("=")[1]
    else:
        raise Exception(f"Line '{line}' does not contain '--propagate='")

    if "qualified_propagate_list" not in config:
        raise Exception(f"qualified_propagate_list not found in config file '{config_file}'")

    qualified_propagate_list = config["qualified_propagate_list"]
    if propagate not in qualified_propagate_list:
        print_red(f"propagate '{propagate}' is not in the qualified_propagate_list")
        return False

    logging.info(f"propagate: '{propagate}' is valid")
    return True


def is_partition_valid(line: str, config: Dict[str, Any], config_file: str) -> bool:
    # print(f"{line}")
    partition = None
    if line.startswith("#SBATCH --partition="):
        partition = line.split("=")[1]
        # partition = line.lstrip("#SBATCH --partition=").strip()
    elif line.startswith("#SBATCH -p="):
        partition = line.split("=")[1]
        # partition = line.lstrip("#SBATCH -p=").strip()

    else:
        raise Exception(f"Line '{line}' does not contain '--partition=' or '-p='")

    if "qualified_partition_list" not in config:
        raise Exception(f"qualified_partition_list not found in config file '{config_file}'")

    qualified_partition_list = config["qualified_partition_list"]
    if partition not in qualified_partition_list:
        print_red(f"partition '{partition}' is not in the qualified_partition_list")
        return False

    logging.info(f"partition: '{partition}' is valid")
    return True


def is_job_name_valid(line: str) -> bool:
    # print(f"{line}")
    if line.startswith("#SBATCH --job-name="):
        job_name = line.split("=")[1]
        # job_name = line.lstrip("#SBATCH --job-name=").strip()
    elif line.startswith("#SBATCH -J="):
        job_name = line.split("=")[1]
        # job_name = line.lstrip("#SBATCH -J=").strip()
    else:
        raise Exception(f"Line '{line}' does not contain '--job-name=' or '-J='")

    logging.info(f"job_name: '{job_name}' is valid")

    return True


def is_ntasks_per_node_valid(line: str) -> bool:
    logging.info("NOT YET IMPLEMENTED")
    return True


def is_cpus_per_task_valid(line: str) -> bool:
    logging.info("NOT YET IMPLEMENTED")
    return True


def is_mail_type_valid(line: str, config: Dict[str, Any], config_file: str) -> bool:
    """Verify whether the mail-type directive is valid.

    Args:
        line (str): The SBATCH mail-type directive.
        config (Dict[str, Any]): The configuration loaded in a dictionary.
        config_file (str): The configuration file path.

    Raises:
        Exception: If qualified_mail_type_list is not found in the config file.
        Exception: If mail-type could not be found in the qualified mail type list.

    Returns:
        bool: True if valid, False if invalid.
    """
    if line.startswith("#SBATCH --mail-type="):
        mail_type = line.split("=")[1]
        # mail_type = line.lstrip("#SBATCH --mail-type=").strip()
    else:
        raise Exception(f"Line '{line}' does not contain '--mail-type='")

    if "qualified_mail_type_list" not in config:
        raise Exception(f"qualified_mail_type_list not found in config file '{config_file}'")

    qualified_mail_type_list = config["qualified_mail_type_list"]
    if mail_type not in qualified_mail_type_list:
        print_red(f"mail-type '{mail_type}' is not in the qualified_mail_type_list")
        return False

    logging.info(f"mail-type: '{mail_type}' is valid")
    return True


def is_mail_user_valid(line: str, config: Dict[str, Any], config_file: str) -> bool:
    """Verify whether the mail-user directive is valid.

    Args:
        line (str): The SBATCH mail-user directive.
        config (Dict[str, Any]): The configuration loaded in a dictionary.
        config_file (str): The configuration file path.

    Raises:
        Exception: If qualified_email_list is not found in the config file.
        Exception: If mail-user email could not be found in the qualified email list.

    Returns:
        bool: _description_
    """
    if line.startswith("#SBATCH --mail-user="):
        mail_user = line.split("=")[1]
        # mail_user = line.lstrip("#SBATCH --mail-user=").strip()
    else:
        raise Exception(f"Line '{line}' does not contain '--mail-user='")

    if not is_email_address_valid(mail_user):
        print_red(f"mail-user '{mail_user}' is not a valid email address")
        return False

    # TODO: Need to add support for multiple email addresses
    if "qualified_email_list" not in config:
        raise Exception(f"qualified_email_list not found in config file '{config_file}'")

    qualified_email_domain_list = config["qualified_email_list"]
    if mail_user not in qualified_email_domain_list:
        print_red(f"mail-user '{mail_user}' is not in the qualified_email_list")
        return False

    logging.info(f"mail-user: '{mail_user}' is valid")
    return True


def is_nodes_valid(line: str) -> bool:
    """Verify whether the nodes directive is valid.

    Args:
        line (str): The SBATCH nodes directive.

    Returns:
        bool: True if valid, False if invalid.
    """
    nodes = None
    if line.startswith("#SBATCH --nodes="):
        nodes = line.split("=")[1]
        # nodes = line.lstrip("#SBATCH --nodes=").strip()
    elif line.startswith("#SBATCH --nodes "):
        nodes = line.split("=")[1]
        # nodes = line.lstrip("#SBATCH --nodes ").strip()
    elif line.startswith("#SBATCH -N="):
        nodes = line.split("=")[1]
        # nodes = line.lstrip("#SBATCH -N=").strip()
    elif line.startswith("#SBATCH -N "):
        nodes = line.split("=")[1]
        # nodes = line.lstrip("#SBATCH -N ").strip()

    if nodes is None:
        return False
    if nodes.isdigit():
        logging.info(f"nodes: '{nodes}' is valid")
        return True
    return False


def tally_directive(directive_lookup: Dict[str, List[int]], directive: str, line_ctr: int) -> None:
    """Tally the count for each directive.

    Args:
        directive_lookup (Dict[str, List[int]]): Dictionary containing the directive and the line number.
        directive (str): The SBATCH directive.
        line_ctr (int): The line number the directive was found on.
    """
    if directive not in directive_lookup:
        directive_lookup[directive] = []
    directive_lookup[directive].append(line_ctr)


def load_required_directives(config: Dict[str, Any], config_file: str)  -> Dict[str, bool]:
    """Load the required directives from the config file.

    Args:
        config (Dict[str, Any]): The configuration loaded in a dictionary.
        config_file (str): The configuration file path.

    Raises:
        Exception: If required_directives is not found in the config file.

    Returns:
        Dict[str, bool]: A dictionary containing the required directives and whether they are required.
    """
    if "required_directives" not in config:
        raise Exception(f"required_directives not found in config file '{config_file}'")

    required_directives_list = config["required_directives"]
    required_directives_lookup = {}
    ctr = 0
    for required_directive in required_directives_list:
        logging.info(f"Loaded required directive '{required_directive}'")
        required_directives_lookup[required_directive] = False

    logging.info(f"Loaded '{ctr}' required directives into the lookup")
    return required_directives_lookup

def validate(
        config: Dict[str, Any],
        config_file: str,
        logfile: str,
        outdir: str,
        outfile: str,
        infile: str,
        verbose: bool = DEFAULT_VERBOSE
    ) -> None:
    """Validate the SLURM shell script.

    Args:
        config (Dict[str, Any]): The configuration loaded in a dictionary.
        config_file (str): The file path to the configuration file.
        logfile (str): The log file.
        outdir (str): The output directory.
        outfile (str): The output validation report file.
        infile (str): The file path to the SLURM shell script.
        verbose (bool): If True, will print more info to STDOUT.
    """
    logging.info(f"Will read SLURM script '{infile}'")
    line_ctr = 0
    directive_lookup = {}
    directive_ctr = 0

    required_directives_found_lookup = load_required_directives(config, config_file)

    is_valid = True

    with open(infile, 'r') as f:
        for line in f:
            line_ctr += 1
            line = line.strip()
            if not line.startswith("#SBATCH"):
                continue
            if "=" not in line:
                raise Exception(f"Line '{line}' does not contain '='.  Please insert an equal sign for all SBATCH directives")

            if line.startswith("#SBATCH -o=") or line.startswith("#SBATCH --output="):
                tally_directive(directive_lookup, "#SBATCH --output=", line_ctr)
                directive_ctr += 1
                if "output" in required_directives_found_lookup:
                    required_directives_found_lookup["output"] = True

                if not is_output_valid(line):
                    print_red(f"output directive '{line}' is not valid")
                    logging.error(f"output directive '{line}' is not valid")

            elif line.startswith("#SBATCH -e=") or line.startswith("#SBATCH --error="):
                tally_directive(directive_lookup, "#SBATCH --error=", line_ctr)
                directive_ctr += 1

                if "error" in required_directives_found_lookup:
                    required_directives_found_lookup["error"] = True

                if not is_error_valid(line):
                    print_red(f"error directive '{line}' is not valid")
                    logging.error(f"error directive '{line}' is not valid")

            elif line.startswith("#SBATCH -q=") or line.startswith("#SBATCH --qos="):
                tally_directive(directive_lookup, "#SBATCH --qos=", line_ctr)
                directive_ctr += 1

                if "qos" in required_directives_found_lookup:
                    required_directives_found_lookup["qos"] = True

                if not is_qos_valid(line, config, config_file):
                    print_red(f"qos directive '{line}' is not valid")
                    logging.error(f"qos directive '{line}' is not valid")

            elif line.startswith("#SBATCH --gres="):
                tally_directive(directive_lookup, "#SBATCH --gres=", line_ctr)
                directive_ctr += 1

                if "gres" in required_directives_found_lookup:
                    required_directives_found_lookup["gres"] = True

                if not is_gres_valid(line, config, config_file):
                    print_red(f"gres directive '{line}' is not valid")
                    logging.error(f"gres directive '{line}' is not valid")

            elif line.startswith("#SBATCH --export="):
                tally_directive(directive_lookup, "#SBATCH --export=", line_ctr)
                directive_ctr += 1

                if "export" in required_directives_found_lookup:
                    required_directives_found_lookup["export"] = True

                if not is_export_valid(line, config, config_file):
                    print_red(f"export directive '{line}' is not valid")
                    logging.error(f"export directive '{line}' is not valid")

            elif line.startswith("#SBATCH --propagate="):
                tally_directive(directive_lookup, "#SBATCH --propagate=", line_ctr)
                directive_ctr += 1

                if "propagate" in required_directives_found_lookup:
                    required_directives_found_lookup["propagate"] = True

                if not is_propagate_valid(line, config, config_file):
                    print_red(f"propagate directive '{line}' is not valid")
                    logging.error(f"propagate directive '{line}' is not valid")

            elif line.startswith("#SBATCH -J=") or line.startswith("#SBATCH --job-name="):
                tally_directive(directive_lookup, "#SBATCH --job-name=", line_ctr)
                directive_ctr += 1

                if "job-name" in required_directives_found_lookup:
                    required_directives_found_lookup["job-name"] = True

                if not is_job_name_valid(line):
                    print_red(f"job-name directive '{line}' is not valid")
                    logging.error(f"job-name directive '{line}' is not valid")

            elif line.startswith("#SBATCH -p=") or line.startswith("#SBATCH --partition="):
                tally_directive(directive_lookup, "#SBATCH --partition=", line_ctr)
                directive_ctr += 1

                if "partition" in required_directives_found_lookup:
                    required_directives_found_lookup["partition"] = True

                if not is_partition_valid(line, config, config_file):
                    print_red(f"partition directive '{line}' is not valid")
                    logging.error(f"partition directive '{line}' is not valid")

            elif line.startswith("#SBATCH -N=") or line.startswith("#SBATCH --nodes="):
                tally_directive(directive_lookup, "#SBATCH --nodes=", line_ctr)
                directive_ctr += 1

                if "nodes" in required_directives_found_lookup:
                    required_directives_found_lookup["nodes"] = True

                if not is_nodes_valid(line):
                    print_red(f"nodes directive '{line}' is not valid")
                    logging.error(f"nodes directive '{line}' is not valid")

            elif line.startswith("#SBATCH --ntasks-per-node="):
                tally_directive(directive_lookup, "#SBATCH --ntasks-per-node=", line_ctr)
                directive_ctr += 1

                if "ntasks-per-node" in required_directives_found_lookup:
                    required_directives_found_lookup["ntasks-per-node"] = True

                if not is_ntasks_per_node_valid(line):
                    print_red(f"ntasks-per-node directive '{line}' is not valid")
                    logging.error(f"ntasks-per-node directive '{line}' is not valid")

            elif line.startswith("#SBATCH --cpus-per-task="):
                tally_directive(directive_lookup, "#SBATCH --cpus-per-task=", line_ctr)
                directive_ctr += 1

                if "cpus-per-task" in required_directives_found_lookup:
                    required_directives_found_lookup["cpus-per-task"] = True

                if not is_cpus_per_task_valid(line):
                    print_red(f"cpus-per-task directive '{line}' is not valid")
                    logging.error(f"cpus-per-task directive '{line}' is not valid")

            elif line.startswith("#SBATCH --time="):
                tally_directive(directive_lookup, "#SBATCH --time=", line_ctr)
                directive_ctr += 1

                if "time" in required_directives_found_lookup:
                    required_directives_found_lookup["time"] = True

                if not is_time_valid(line):
                    print_red(f"time directive '{line}' is not valid")
                    logging.error(f"time directive '{line}' is not valid")

            elif line.startswith("#SBATCH --mail-type="):
                tally_directive(directive_lookup, "#SBATCH --mail-type=", line_ctr)
                directive_ctr += 1

                if "mail-type" in required_directives_found_lookup:
                    required_directives_found_lookup["mail-type"] = True

                if not is_mail_type_valid(line, config, config_file):
                    print_red(f"mail-type directive '{line}' is not valid")
                    logging.error(f"mail-type directive '{line}' is not valid")

            elif line.startswith("#SBATCH --mail-user="):
                tally_directive(directive_lookup, "#SBATCH --mail-user=", line_ctr)
                directive_ctr += 1

                if "mail-user" in required_directives_found_lookup:
                    required_directives_found_lookup["mail-user"] = True

                if not is_mail_user_valid(line, config, config_file):
                    print_red(f"mail-user directive '{line}' is not valid")
                    logging.error(f"mail-user directive '{line}' is not valid")
            else:
                print_yellow(f"Line '{line_ctr}' contains unexpected SLURM SBATCH directive: '{line}'")
                logging.warning(f"Line '{line_ctr}' contains unexpected SLURM SBATCH directive: '{line}'")

    if line_ctr > 0:
        logging.info(f"Read '{line_ctr}' lines from file '{infile}'")
    else:
        logging.info(f"Did not read any lines from file '{infile}'")


    if missing_required_directives(required_directives_found_lookup):
        print_red("Required directives are missing")
        is_valid = False

    if directive_ctr > 0:
        if has_duplicated_directives(directive_lookup):
            print_red("There are duplicated directives")
            is_valid = False

    else:
        print_red("No SLURM SBATCH directives were found")
        is_valid = False

    if not is_valid:
        print_red(f"Validation of '{infile}' failed")
        write_validation_report(
            outfile,
            config,
            config_file,
            logfile,
            infile,
            verbose,
        )
        sys.exit(1)
    else:
        print_green(f"Validation of '{infile}' passed")

def write_validation_report(outfile: str, config: Dict[str, Any], config_file: str, logfile: str, infile: str, verbose: bool = DEFAULT_VERBOSE) -> None:
    """Write the validation report.

    Args:
        outfile (str): The output validation report file.
        config (Dict[str, Any]): The configuration loaded in a dictionary.
        config_file (str): The configuration file path.
        logfile (str): The log file.
        infile (str): The file path to the SLURM shell script.
        verbose (bool): If True, will print more info to STDOUT.
    """
    #import logging

    with open(outfile, 'w') as of:
        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## infile: {infile}\n")
        of.write(f"## logfile: {logfile}\n")
        of.write(f"## config_file: {config_file}\n")

        of.write("NOT YET IMPLEMENTED\n")

    logging.info(f"Wrote validation report file '{outfile}'")
    if verbose:
        console.print(f"Wrote validation report file '{outfile}'")



def missing_required_directives(required_directives_found_lookup: Dict[str, bool]) -> bool:
    """Check whether there are missing required directives.

    Args:
        required_directives_found_lookup (Dict[str, bool]): Dictionary containing the required directive and whether it was found.

    Returns:
        bool: True if there are missing required directives, False if there are no missing required directives.
    """
    found_ctr = 0
    missing_ctr = 0
    for required_directive in required_directives_found_lookup:
        if not required_directives_found_lookup[required_directive]:
            logging.error(f"Required directive '{required_directive}' was not found")
            missing_ctr += 1
        else:
            logging.info(f"Required directive '{required_directive}' was found")
            found_ctr += 1

    if missing_ctr > 0:
        logging.error(f"Found '{found_ctr}' required directives and '{missing_ctr}' required directives are missing")
        return True
    elif found_ctr > 0:
        logging.info(f"Found '{found_ctr}' required directives")
        return False
    return False


def has_duplicated_directives(directive_lookup: Dict[str, List[int]]) -> bool:
    """Check whether there are duplicated directives.

    Args:
        directive_lookup (Dict[str, List[int]]): Dictionary containing the directive and the line number.

    Returns:
        bool: True if there are duplicated directives, False if there are no duplicated directives.
    """
    for directive in directive_lookup:
        if len(directive_lookup[directive]) > 1:
            print_red(f"Directive '{directive}' was found on lines '{directive_lookup[directive]}'")
            return True
    return False


def is_time_valid(line: str) -> bool:

    if not line.startswith("#SBATCH --time="):
        raise Exception(f"Line '{line}' does not start with '#SBATCH --time='")

    time_value = line.split("=")[1]

    # Define a regular expression pattern for a valid Slurm time value
    pattern = r'^(\d+-)?(\d+:)?\d+:\d+:\d+$'

    # Use re.match to check if the provided time value matches the pattern
    match = re.match(pattern, time_value)

    # If there is a match, the time value is valid; otherwise, it's invalid
    return bool(match)


def original_is_mail_user_valid(mail_user: str, config: Dict[str, Any]) -> bool:
    if mail_user is None or mail_user == "":
        return False
    qualified_email_domain_list = config["qualified_email_domain_list"]
    qualified_domain_found = False
    for qualified_email_domain in qualified_email_domain_list:
        if mail_user.endswith(qualified_email_domain):
            qualified_domain_found = True
            break
    if not qualified_domain_found:
        return False
    if not is_email_address_valid(mail_user):
        return False

    return True


def is_email_address_valid(email: str) -> bool:
    # Define a regular expression pattern for a valid email address
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'

    # Use re.match to check if the provided email matches the pattern
    match = re.match(pattern, email)

    # If there is a match, the email is valid; otherwise, it's invalid
    return bool(match)


def original_is_mail_type_valid(mail_type: str, config: Dict[str, Any]) -> bool:
    qualified_mail_type_list = config["qualified_mail_type_list"]
    if mail_type.upper() in qualified_mail_type_list:
        return True
    return False


def validate_verbose(ctx, param, value):
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=str, help=f"Optional: The YAML configuration file - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help="Optional: The output directory where logfile and default output file will be written - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output validation report file that will be written to'")
@click.option('--slurm_script', help="Required: The SLURM script to be validated")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(config_file: str, logfile: str, outdir: str, outfile: str, slurm_script: str, verbose: bool):
    """Validate a SLURM shell script."""
    error_ctr = 0

    if slurm_script is None:
        print_red("--slurm_script was not specified")
        error_ctr += 1

    if error_ctr > 0:
        print_red("Required command-line arguments were not provided")
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(slurm_script)

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
            os.path.splitext(os.path.basename(__file__))[0] + '.validation-report.txt'
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    # pip install PyYAML
    # echo 'PyYAML' >> requirements.txt

    if verbose:
        console.print(f"Will load contents of config file '{config_file}'")
        logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(pathlib.Path(config_file).read_text())

    validate(
        config,
        config_file,
        logfile,
        outdir,
        outfile,
        slurm_script,
        verbose,
    )

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
