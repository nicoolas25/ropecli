import re

from rope.base.project import File


class GlobalFunctionNotFoundError(Exception):
    pass


def find_global_function_name_offset(src_module: File, function_name: str) -> int:
    file_content = src_module.read()
    global_function_re = f"^def {function_name}\\("
    match_object = re.match(global_function_re, file_content)
    if match_object:
        return match_object.start() + len("def ")
    else:
        raise GlobalFunctionNotFoundError((src_module.path, function_name))
