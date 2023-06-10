import click
import trogon

config = {
    "prefer_module_from_imports": True,
}

@trogon.tui()
@click.group()
def rope_cli():
    ...


@rope_cli.command()
@click.option(
    "--src",
    help="Source function's qualified name you would like to move (eg: foo.bar.fn)",
    required=True,
)
@click.option(
    "--dst",
    help="Destination module's qualified name you would like to move your function to (eg: foo.baz)",
    required=True,
)
def move_function(src: str, dst: str):
    """Move a module, from one source package to another existing package, keeping the same module name."""

    from rope.base import project
    from rope.refactor.move import MoveGlobal

    from ropecli.utils import find_global_function_name_offset

    project = project.Project(".", **config)

    [root_module, *sub_modules, function_name] = src.split(".")
    src_module = project.find_module(".".join([root_module, *sub_modules]))
    dst_module = project.find_module(dst)

    assert src_module

    offset = find_global_function_name_offset(src_module, function_name)

    changes = MoveGlobal(project, src_module, offset).get_changes(dst_module)

    if click.confirm(f"{changes.get_description()}\n\n" "Do you confirm the change?"):
        project.do(changes)


@rope_cli.command()
@click.option(
    "--src",
    help="Source module's qualified name you would like to move (eg: foo.bar)",
    required=True,
)
@click.option(
    "--dst",
    help="Destination folder's path you would like to move your module to (eg: titi/baz)",
    required=True,
)
def move_module(src: str, dst: str):
    """
    Move a module, from one source package to another existing package, keeping the same module name.

    Works with nested modules as well, in that case, moves all its submodules as well.
    """

    from rope.base import project
    from rope.refactor.move import MoveModule

    project = project.Project(".", **config)
    src_module = project.find_module(src)
    dst_folder = project.get_folder(dst)

    changes = MoveModule(project, src_module).get_changes(dst_folder)
    if click.confirm(f"{changes.get_description()}\n\n" "Do you confirm the change?"):
        project.do(changes)
