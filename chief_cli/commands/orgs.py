"""chief orgs — manage organizations."""

import click
from rich.table import Table
from chief_cli.api import ChiefClient, AuthError, APIError
from chief_cli.output import get_console, is_json, print_json
from chief_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def orgs(ctx):
    """Manage organizations."""
    pass


@orgs.command("list")
@click.option("--limit", "-n", default=20, show_default=True, help="Max results to return")
@click.option("--quiet", "-q", is_flag=True, help="Print only org IDs")
@click.pass_context
def orgs_list(ctx, limit, quiet):
    """List organizations."""
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
        org_list = client.list_orgs(params=params)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(org_list)
        return

    if not org_list:
        click.echo("No organizations found.")
        return

    if quiet:
        for o in org_list:
            click.echo(o.get("id", ""))
        return

    console = get_console(ctx)
    table = Table(show_edge=False, pad_edge=False, box=None)
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Status", min_width=12)
    table.add_column("ID", style="dim")

    for o in org_list:
        table.add_row(
            o.get("name", "Unknown")[:36],
            o.get("status", "unknown"),
            o.get("id", "")[:8],
        )

    console.print(table)


@orgs.command("get")
@click.argument("org_id")
@click.pass_context
def orgs_get(ctx, org_id):
    """Get details of a specific organization."""
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
        org = client.get_org(org_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(org)
        return

    console = get_console(ctx)
    console.print(f"[bold]{org.get('name', 'Unknown')}[/bold]")
    console.print(f"  ID: {org.get('id', '')}")
    console.print(f"  Status: {org.get('status', '')}")
