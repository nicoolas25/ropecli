try:
    import click
    import rope
    import trogon
except ModuleNotFoundError as e:
    print(f"Please install {e.name} first, using `pip install` should do.")
    exit(0)


@trogon.tui()
@click.group()
def rope_cli():
    ...


@rope_cli.command()
@click.option(
    "--src",
    help="Source module's fullname you would like to move (eg: foo.bar)",
    required=True,
)
@click.option(
    "--dst",
    help="Destination folder's fullname you would like to move your module to (eg: titi/baz)",
    required=True,
)
def move_module(src: str, dst: str):
    """Move a module, from one source package to another existing package, keeping the same module name."""

    from rope.base import project
    from rope.refactor.move import MoveModule

    project = project.Project(".")
    src_module = project.find_module(src)
    dst_folder = project.get_folder(dst)

    changes = MoveModule(project, src_module).get_changes(dst_folder)
    if click.confirm(
        f"{changes.get_description()}\n\n" "Do you confirm the change?"
    ):
        project.do(changes)
