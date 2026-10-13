"""Shell completion for Chief CLI."""

import click


@click.command()
@click.argument("shell", required=False, type=click.Choice(["bash", "zsh", "fish"], case_sensitive=False))
@click.pass_context
def completion(ctx, shell):
    """Generate shell completion script.

    \b
    Examples:
        chief completion bash > ~/.bashrc
        chief completion zsh >> ~/.zshrc
        chief completion fish > ~/.config/fish/config.fish
    """
    if shell is None:
        import os
        shell = _detect_shell()

    if shell == "bash":
        click.echo("eval \"$(_CHIEF_COMPLETE=bash_source chief)\"")
    elif shell == "zsh":
        click.echo("eval \"$(_CHIEF_COMPLETE=zsh_source chief)\"")
    elif shell == "fish":
        click.echo("eval (env _CHIEF_COMPLETE=fish_source chief)")


def _detect_shell():
    import os
    shell = os.path.basename(os.getenv("SHELL", ""))
    if "bash" in shell:
        return "bash"
    elif "zsh" in shell:
        return "zsh"
    elif "fish" in shell:
        return "fish"
    return "bash"
