import re

from rope.base.project import File, Project
from rope.refactor.move import MoveGlobal


class GlobalNotFoundError(Exception):
    pass


def find_global_name_offset(src_module: File, name: str) -> int:
    file_content = src_module.read()
    if match_object := re.match(f"^def {name}\\(", file_content):
        return match_object.start() + len("def ")
    elif match_object := re.match(f"^class {name}\\W", file_content):
        return match_object.start() + len("class ")
    elif match_object := re.match(f"^{name}\\W", file_content):
        return match_object.start()
    else:
        raise GlobalNotFoundError((src_module.path, name))


def move_global(project: Project, src: str, dst: str):
    module, name = src.rsplit(".", 1)
    dst_module = project.find_module(dst)
    src_module = project.find_module(module)

    assert src_module
    assert dst_module

    offset = find_global_name_offset(src_module, name)

    return MoveGlobal(project, src_module, offset).get_changes(dst_module)
