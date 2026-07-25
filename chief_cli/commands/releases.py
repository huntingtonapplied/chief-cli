"""chief releases — manage application releases."""

import click
from chief_cli.api import ChiefClient, AuthError, APIError
from chief_cli.output import get_console, is_json, print_json
from chief_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def releases(ctx):
    """Manage application releases."""
    pass


@releases.command("latest")
@click.option("--platform", default=None, help="Platform to check (macos, windows, linux)")
@click.pass_context
def releases_latest(ctx, platform):
    """Get latest release info."""
    json_mode = is_json(ctx)

    try:
        client = ChiefClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    try:
        data = client.get_latest_release(platform)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(data)
        return

    console = get_console(ctx)
    console.print(f"[bold]Latest Release[/bold]")
    console.print(f"  Version: {data.get('version', 'N/A')}")
    console.print(f"  Platform: {data.get('platform', 'N/A')}")
    console.print(f"  Released: {data.get('released_at', 'N/A')}")


@releases.command("check-update")
@click.pass_context
def releases_check(ctx):
    """Check if an update is available."""
    json_mode = is_json(ctx)

    try:
        client = ChiefClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    try:
        data = client.check_update()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(data)
        return

    console = get_console(ctx)
    if data.get("update_available"):
        console.print(f"[bold green]Update available![/bold green]")
        console.print(f"  Current: {data.get('current_version')}")
        console.print(f"  Latest: {data.get('latest_version')}")
    else:
        console.print("[dim]You're up to date.[/dim]")
