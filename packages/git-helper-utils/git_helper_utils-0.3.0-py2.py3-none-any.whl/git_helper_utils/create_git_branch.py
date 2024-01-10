"""Create a git branch."""
import datetime
import os
import sys
import click
import pathlib
import logging
import subprocess

from datetime import datetime

from rich.console import Console

DEFAULT_VALID_TYPES = ["feature", "bugfix", "hotfix", "custom"]

DEFAULT_SOURCE_BRANCH = "development"

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    "git-utils",
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False

error_console = Console(stderr=True, style="bold red")

console = Console()

def _execute_cmd(
    cmd: str,
    outdir: str = None,
    stdout_file: str = None,
    stderr_file: str = None,
    verbose: bool = DEFAULT_VERBOSE,
):
    """Execute a command via system call using the subprocess module
    :param cmd: {str} - the executable to be invoked
    :param outdir: {str} - the output directory where STDOUT, STDERR and the shell script should be written to
    :param stdout_file: {str} - the file to which STDOUT will be captured in
    :param stderr_file: {str} - the file to which STDERR will be captured in
    """
    if cmd is None:
        raise Exception("cmd was not specified")

    cmd = cmd.strip()

    logging.info(f"Will attempt to execute '{cmd}'")
    if verbose:
        print(f"Will attempt to execute '{cmd}'")

    if outdir is None:
        outdir = "/tmp"
        logging.info(
            f"outdir was not defined and therefore was set to default '{outdir}'"
        )

    if stdout_file is None:
        primary = cmd.split(" ")[0]
        basename = os.path.basename(primary)
        stdout_file = os.path.join(outdir, basename + ".stdout")
        logging.info(
            f"stdout_file was not specified and therefore was set to '{stdout_file}'"
        )

    if stderr_file is None:
        primary = cmd.split(" ")[0]
        basename = os.path.basename(primary)
        stderr_file = os.path.join(outdir, basename + ".stderr")
        logging.info(
            f"stderr_file was not specified and therefore was set to '{stderr_file}'"
        )

    if os.path.exists(stdout_file):
        logging.info(
            f"STDOUT file '{stdout_file}' already exists so will delete it now"
        )
        os.remove(stdout_file)

    if os.path.exists(stderr_file):
        logging.info(
            f"STDERR file '{stderr_file}' already exists so will delete it now"
        )
        os.remove(stderr_file)

    consolidated_cmd = cmd
    p = subprocess.Popen(consolidated_cmd, shell=True)

    (stdout, stderr) = p.communicate()

    pid = p.pid

    logging.info(f"The child process ID is '{pid}'")
    if verbose:
        print(f"The child process ID is '{pid}'")

    p_status = p.wait()

    p_returncode = p.returncode

    if p_returncode is not None:
        logging.info(f"The return code was '{p_returncode}'")
    else:
        logging.info("There was no return code")

    if p_status == 0:
        logging.info(f"Execution of cmd '{cmd}' has completed")
    else:
        raise Exception(f"Received status '{p_status}'")

    if stdout is not None:
        logging.info("stdout is: " + stdout_file)

    if stderr is not None:
        logging.info("stderr is: " + stderr_file)

    return stdout_file


def validate_verbose(ctx, param, value):
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--desc', help="Required: A description to apply during the creation of the branch")
@click.option('--jira_id', help="Optional: The Jira ticket identifier")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--source_branch', help=f"Optional: The source branch to establish the new branch from - default is '{DEFAULT_SOURCE_BRANCH}'")
@click.option('--type', type=click.Choice(DEFAULT_VALID_TYPES), help="Required: The type of branch to establish")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'", callback=validate_verbose)
def main(desc: str, jira_id: str, logfile: str, outdir: str, source_branch: str, type: str, verbose: bool):
    """Create a git branch."""
    error_ctr = 0

    if desc is None:
        desc = click.prompt("Please enter a description for the branch", type=str)
        if desc is None or desc == "":
            error_console.print("[bold red]--desc was not specified[/]")
            error_ctr += 1

    while type is None or type not in DEFAULT_VALID_TYPES:
        type = click.prompt(f"Please enter the type of branch to establish (valid options: {DEFAULT_VALID_TYPES})", type=str)

    if error_ctr > 0:
        sys.exit(1)

    if source_branch is None:
        source_branch = input(f"Please provide the source branch (default is '{DEFAULT_SOURCE_BRANCH}'): ")
        if source_branch is None or source_branch == "":
            source_branch = DEFAULT_SOURCE_BRANCH
        source_branch = source_branch.strip()

    if jira_id is None:
        jira_id = input("Please enter the Jira ticket identifier or press ENTER to skip: ")
        if jira_id is None or jira_id == "":
            jira_id = None
        else:
            jira_id = jira_id.strip()

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        console.print(f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]")

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        console.print(f"[yellow]--verbose was not specified and therefore was set to '{verbose}'[/]")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    timestamp = datetime.today().strftime('%Y-%m-%d-%H%M%S')

    new_branch = None

    if jira_id is None:
        new_branch = f"{type}/from-{source_branch}-on-{timestamp}-for-{desc.lower().replace(' ', '-')}"
    else:
        new_branch = f"{type}/{jira_id}-from-{source_branch}-on-{timestamp}-for-{desc.lower().replace(' ', '-')}"

    print(f"New branch: {new_branch}")

    _execute_cmd(f"git checkout -b {new_branch}")

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")
    sys.exit(0)

if __name__ == "__main__":
    main()

