"""chief applets — manage applets."""

import click
from rich.table import Table
from chief_cli.api import ChiefClient, AuthError, APIError
from chief_cli.output import get_console, is_json, print_json
from chief_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def applets(ctx):
    """Manage applets."""
    pass


@applets.command("list")
@click.option("--limit", "-n", default=20, show_default=True, help="Max results to return")
@click.option("--quiet", "-q", is_flag=True, help="Print only applet IDs")
@click.pass_context
def applets_list(ctx, limit, quiet):
    """List applets."""
    json_mode = is_json(ctx)

    try:
        client = ChiefClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    params = {"limit": limit} if limit != 20 else {}

    try:
        applet_list = client.list_applets(params=params)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(applet_list)
        return

    if not applet_list:
        click.echo("No applets found.")
        return

    if quiet:
        for a in applet_list:
            click.echo(a.get("id", ""))
        return

    console = get_console(ctx)
    table = Table(show_edge=False, pad_edge=False, box=None)
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Status", min_width=12)
    table.add_column("ID", style="dim")

    for a in applet_list:
        table.add_row(
            a.get("name", "Unknown")[:36],
            a.get("status", "unknown"),
            a.get("id", "")[:8],
        )

    console.print(table)


@applets.command("get")
@click.argument("applet_id")
@click.pass_context
def applets_get(ctx, applet_id):
    """Get details of a specific applet."""
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
        applet = client.get_applet(applet_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(applet)
        return

    console = get_console(ctx)
    console.print(f"[bold]{applet.get('name', 'Unknown')}[/bold]")
    console.print(f"  ID: {applet.get('id', '')}")
    console.print(f"  Status: {applet.get('status', '')}")
