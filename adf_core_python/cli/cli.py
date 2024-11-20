import os

import click

NAME_PLACEHOLDER = "team_name"


@click.command()
@click.option(
    "--name", prompt="Your agent team name", help="The name of your agent team"
)
def cli(name):
    # load template dir and create a new agent team
    click.echo(f"Creating a new agent team with name: {name}")
    # 自身がいるディレクトリを取得
    template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "template")
    click.echo(f"Current file path: {template_dir}")
    # コマンドラインのカレントディレクトリを取得
    current_dir = os.getcwd()
    click.echo(f"Current directory: {current_dir}")

    _copy_template(
        template_dir,
        current_dir,
        name,
    )


def _copy_template(
    src,
    dest,
    name,
):
    if os.path.isdir(src):
        if not os.path.exists(dest):
            os.makedirs(dest)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(
                dest,
                item.replace(NAME_PLACEHOLDER, name),
            )
            _copy_template(s, d, name)
    else:
        with open(src, "r") as f:
            content = f.read()
        with open(dest, "w") as f:
            f.write(content.replace(NAME_PLACEHOLDER, name))
        new_dest = dest.replace(NAME_PLACEHOLDER, name)
        if new_dest != dest:
            os.rename(dest, new_dest)


if __name__ == "__main__":
    cli()
