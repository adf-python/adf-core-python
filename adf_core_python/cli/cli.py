import os
import shutil

import click

NAME_PLACEHOLDER = "team_name"


@click.command()
@click.option(
    "--name", prompt="Your agent team name", help="The name of your agent team"
)
def cli(name: str) -> None:
    # load template dir and create a new agent team
    click.echo(f"Creating a new agent team with name: {name}")
    # 自身がいるディレクトリを取得
    template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "template")
    # コマンドラインのカレントディレクトリを取得
    current_dir = os.getcwd()

    _copy_template(
        template_dir,
        current_dir,
        name,
    )


def _copy_template(
    src: str,
    dest: str,
    name: str,
) -> None:
    dest = os.path.join(dest, name)
    shutil.copytree(src, dest)

    # dest以下のファイル内のNAME_PLACEHOLDERをnameに置換
    for root, dirs, files in os.walk(dest):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                if not file_path.endswith((".py", ".yaml")):
                    continue
                content = f.read()
            with open(file_path, "w") as f:
                f.write(content.replace(NAME_PLACEHOLDER, name))

    # ディレクトリ名のNAME_PLACEHOLDERをnameに置換
    for root, dirs, files in os.walk(dest):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            new_dir_path = dir_path.replace(NAME_PLACEHOLDER, name)
            os.rename(dir_path, new_dir_path)


if __name__ == "__main__":
    cli()
