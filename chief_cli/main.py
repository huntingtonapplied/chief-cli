"""Chief CLI — Application management from your terminal."""

import os
import signal
import sys

import click
from chief_cli import __version__
from chief_cli.log import setup_logging, logger
from chief_cli.exit_codes import EXIT_GENERAL, EXIT_SIGINT, EXIT_SIGTERM
from chief_cli.config import load_config, validate_config
from chief_cli.update_check import UpdateChecker
from chief_cli.commands.login import login
from chief_cli.commands.orgs import orgs
from chief_cli.commands.applets import applets
from chief_cli.commands.releases import releases
from chief_cli.commands.metrics import metrics
from chief_cli.commands.status import status
from chief_cli.commands.doctor import doctor
from chief_cli.commands.completion import completion


@click.group()
@click.version_option(version=__version__, prog_name="chief")
@click.option("--output", "-o", type=click.Choice(["table", "json", "yaml"]), default="table",
              help="Output format (default: table)")
@click.option("--no-color", is_flag=True, default=False, envvar="NO_COLOR",
              help="Disable colored output")
@click.option("--verbose", "-v", is_flag=True, default=False,
              help="Show informational messages (INFO level)")
@click.option("--debug", is_flag=True, default=False,
              help="Show debug messages including HTTP requests")
@click.option("--ci", is_flag=True, default=False,
              help="CI mode: no color, no spinners, no interactive prompts")
@click.pass_context
def cli(ctx, output, no_color, verbose, debug, ci):
    """Chief CLI — Application management from your terminal."""
    if not ci and (os.getenv("CI") or os.getenv("GITHUB_ACTIONS") or os.getenv("GITLAB_CI")):
        ci = True

    if ci:
        no_color = True

    ctx.ensure_object(dict)
    ctx.obj["output"] = output
    ctx.obj["no_color"] = no_color
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    ctx.obj["ci"] = ci
    setup_logging(verbose=verbose, debug=debug)

    config = load_config()
    if config:
        warnings = validate_config(config)
        for w in warnings:
            click.echo(f"Warning: {w}", err=True)


cli.add_command(login)
cli.add_command(orgs)
cli.add_command(applets)
cli.add_command(releases)
cli.add_command(metrics)
cli.add_command(status)
cli.add_command(doctor)
cli.add_command(completion)


_update_checker = UpdateChecker()


def main():
    """Entry point with top-level signal and exception handling."""
    signal.signal(signal.SIGTERM, lambda sig, frame: sys.exit(EXIT_SIGTERM))
    _update_checker.start()
    try:
        cli(standalone_mode=False)
    except click.exceptions.Exit as e:
        raise SystemExit(e.exit_code)
    except (KeyboardInterrupt, click.Abort):
        raise SystemExit(EXIT_SIGINT)
    except SystemExit:
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise SystemExit(EXIT_GENERAL)
    finally:
        _update_checker.notify_if_outdated()


if __name__ == "__main__":
    main()
