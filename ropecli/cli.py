from dataclasses import dataclass

import click
import trogon
from rope.base import project


@dataclass
class ContextObj:
    project: project.Project


class Context(click.Context):
    obj: ContextObj


def run_cli():
    rope_cli(
        obj=ContextObj(
            project=project.Project(
                ".",
                prefer_module_from_imports=True,
            )
        )
    )


@trogon.tui()
@click.group()
def rope_cli():
    pass


@rope_cli.command()
@click.pass_context
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
def move_function(ctx: Context, src: str, dst: str):
    """Move a function, from one source module to a destination module, keeping the same function name."""

    from ropecli.utils import move_global

    changes = move_global(ctx.obj.project, src, dst)
    details = changes.get_description()

    if click.confirm(f"{details}\n\n" "Do you confirm the change?"):
        ctx.obj.project.do(changes)


@rope_cli.command()
@click.pass_context
@click.option(
    "--src",
    help="Source constant's qualified name you would like to move (eg: foo.bar.const)",
    required=True,
)
@click.option(
    "--dst",
    help="Destination module's qualified name you would like to move your constant to (eg: foo.baz)",
    required=True,
)
def move_constant(ctx: Context, src: str, dst: str):
    """Move a constant, from one source module to a destination module, keeping the same constant name."""

    from ropecli.utils import move_global

    changes = move_global(ctx.obj.project, src, dst)
    details = changes.get_description()

    if click.confirm(f"{details}\n\n" "Do you confirm the change?"):
        ctx.obj.project.do(changes)


@rope_cli.command()
@click.pass_context
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
def move_module(ctx: Context, src: str, dst: str):
    """
    Move a module, from one source package to another existing package, keeping the same module name.

    Works with nested modules as well, in that case, moves all its submodules as well.
    """

    from rope.refactor.move import MoveModule

    src_module = ctx.obj.project.find_module(src)
    dst_folder = ctx.obj.project.get_folder(dst)

    changes = MoveModule(ctx.obj.project, src_module).get_changes(dst_folder)
    if click.confirm(f"{changes.get_description()}\n\n" "Do you confirm the change?"):
        ctx.obj.project.do(changes)
