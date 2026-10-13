"""chief status — show system status."""

import click
from rich.panel import Panel
from chief_cli.api import ChiefClient, AuthError, APIError
from chief_cli.output import get_console, is_json, print_json
from chief_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.command()
@click.pass_context
def status(ctx):
    """Show Chief system status and recent activity."""
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
        orgs = client.list_orgs(params={"limit": 5})
        applets = client.list_applets(params={"limit": 5})
        metrics = client.get_portfolio_metrics()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json({
            "organizations": orgs[:5] if orgs else [],
            "applets": applets[:5] if applets else [],
            "metrics": metrics,
        })
        return

    console = get_console(ctx)

    if orgs:
        click.echo(f"\nOrganizations ({len(orgs)} recent):")
        for org in orgs[:5]:
            click.echo(f"  • {org.get('name', 'Unknown')} — {org.get('status', 'unknown')}")

    if applets:
        click.echo(f"\nApplets ({len(applets)} recent):")
        for a in applets[:5]:
            click.echo(f"  • {a.get('name', 'Unknown')} — {a.get('status', 'unknown')}")

    if metrics:
        click.echo(f"\nPortfolio Metrics:")
        click.echo(f"  Total Organizations: {metrics.get('total_organizations', 'N/A')}")
        click.echo(f"  Active Applets: {metrics.get('active_applets', 'N/A')}")
