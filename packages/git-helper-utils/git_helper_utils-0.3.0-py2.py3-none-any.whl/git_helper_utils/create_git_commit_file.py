"""Create a git commit file."""
import datetime
import os
import sys
import click
import pathlib
import logging
import subprocess

from datetime import datetime

from rich.console import Console

# https://www.conventionalcommits.org/en/v1.0.0/
commit_type_lookup = {
    "feat": "A new feature for the user.",
    "fix": "A bug fix.",
    "chore": "Routine tasks, maintenance, and other non-user-facing changes.",
    "docs": "Documentation changes.",
    "style": "Code style changes (formatting, indentation).",
    "refactor": "Code refactoring.",
    "test": "Adding or modifying tests.",
    "ci": "Changes to the project's CI/CD configuration."
}

DEFAULT_COMMIT_TYPES = [commit_type for commit_type in commit_type_lookup.keys()]

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


def get_desc_from_user() -> str:
    desc = input("Please provide a description for the commit (type 'done' when finished)\n")
    return desc


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
@click.option('--comment', help="Optional: A one line comment.")
@click.option('--issue_id', help="Optional: The issue identifier.")
@click.option('--logfile', help="Optional: The log file.")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'.")
@click.option('--outfile', help="Optional: The output commit comment file.")
@click.option('--scope', help="Optional: Describes the module, component, or section of the project that is affected by the commit.")
@click.option('--commit_type', type=click.Choice(DEFAULT_COMMIT_TYPES), help="Optional: Describes the purpose of the commit.")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(comment: str, issue_id: str, logfile: str, outdir: str, outfile: str, scope: str, commit_type: str, verbose: bool):
    """Create a git commit file."""
    error_ctr = 0

    if error_ctr > 0:
        sys.exit(1)

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

    if outfile is None:
        outfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.txt'
        )
        console.print(f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]")

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        console.print(f"[yellow]--verbose was not specified and therefore was set to '{verbose}'[/]")


    while commit_type is None or commit_type == "" or commit_type.lower().strip() not in DEFAULT_COMMIT_TYPES:
        print("\n")
        for commit_type in DEFAULT_COMMIT_TYPES:
            console.print(f"[bold blue]{commit_type}[/] - {commit_type_lookup[commit_type]}")
        commit_type = click.prompt("Please enter the type of commit", type=str)

    if scope is None or scope == "":
        scope = input("Please enter the scope of the commit [just press Enter if none]: ")
        if scope is None or scope == "":
            scope = None

    while comment is None or comment == "":
        comment = click.prompt("Please enter a one-line comment", type=str)

    if issue_id is None or issue_id == "":
        issue_id = click.prompt("Please enter the issue identifier [Enter if none]", type=str)
        if issue_id is None or issue_id == "":
            issue_id = None
        else:
            issue_id = issue_id.strip()
    else:
        issue_id = issue_id.strip()

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    ans = input("Do you want to provide more details? [Y/n]:")
    desc = None
    if ans is None or ans == "" or ans.lower() == "y":
        desc = get_desc_from_user()

    outline = None
    if scope is not None:
        outline = f"{commit_type}({scope}): {comment}"
    else:
        outline = f"{commit_type}: {comment}"

    with open(outfile, 'w') as of:

        of.write(f"{outline}\n\n")
        if desc is not None and desc != "":
            of.write(f"{desc}\n\n")
        if issue_id is not None and issue_id != "":
            of.write(f"{issue_id}\n")

    logging.info(f"Wrote commit comment file '{outfile}'")
    print(f"\nWrote commit comment file '{outfile}'")


    print(f"\nThe log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")
    sys.exit(0)

if __name__ == "__main__":
    main()

