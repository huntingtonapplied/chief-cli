"""chief login — authenticate and store API key."""

import click
from rich.panel import Panel
from chief_cli.config import save_config, load_config, get_api_url
from chief_cli.api import ChiefClient, APIError
from chief_cli.output import get_console
from chief_cli.exit_codes import EXIT_VALIDATION


@click.command()
@click.option("--key", default=None, help="Your Chief API key (skips wizard)")
@click.option("--url", default=None, help="API URL (default: http://localhost:8002)")
@click.pass_context
def login(ctx, key: str, url: str):
    """Authenticate with the Chief platform.

    \b
    Examples:
        chief login                     # interactive wizard
        chief login --key chief_abc123  # non-interactive
    """
    console = get_console(ctx)
    ci_mode = ctx.obj.get("ci", False) if ctx.obj else False

    if not key and ci_mode:
        click.echo("✗ --key is required in CI mode: chief login --key <key>", err=True)
        raise SystemExit(EXIT_VALIDATION)

    if not key:
        click.echo()
        click.echo("  Welcome to Chief!")
        click.echo()
        click.echo("  To get your API key:")
        click.echo("    1. Go to your Chief instance /account")
        click.echo("    2. Click the Developer tab")
        click.echo("    3. Copy your API key")
        click.echo()
        key = click.prompt("  API Key", hide_input=True)
        if not url:
            use_custom = click.confirm("  Use a custom API URL?", default=False)
            if use_custom:
                url = click.prompt("  API URL", default="http://localhost:8002")

    key = key.strip()
    config = load_config()
    config["api_key"] = key
    if url:
        config["api_url"] = url.strip()
    save_config(config)

    api_url = url or get_api_url()
    click.echo(f"✓ API key saved to ~/.chief/config.yaml")
    click.echo(f"  API URL: {api_url}")

    try:
        client = ChiefClient(api_key=key, api_url=api_url)
        org_list = client.list_orgs()
        console.print(Panel(
            f"✓ Authenticated — {len(org_list)} organization(s) found\n\n"
            "  [dim]chief orgs list[/dim]         list your organizations\n"
            "  [dim]chief applets list[/dim]    list your applets\n"
            "  [dim]chief releases latest[/dim]  check for updates",
            title="Connected",
            border_style="green",
            expand=False,
        ))
    except Exception as e:
        click.echo(f"⚠ Key saved but verification failed: {e}", err=True)
        click.echo("  Check your key and try again: chief login", err=True)
