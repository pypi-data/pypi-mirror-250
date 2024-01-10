import ast
import enum
import os
from typing import List, Tuple, Generator


class AnnotationErrorCodes(enum.Enum):
    ARGUMENT_ANNOTATION_MISSING = "ETA001"
    RETURN_TYPE_ANNOTATION_MISSING = "ETA002"


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, current_module: str, current_filename: str, errors: List[Tuple[int, int, str]]) -> None:
        self.current_module = current_module
        self.current_filename = current_filename
        self.errors = errors

    def is_function_arg_annotation_present(self, arg: ast.arg) -> bool:
        args_to_skip = ['self', 'cls']
        if arg.arg not in args_to_skip and arg.annotation is None:
            return False
        return True

    def is_function_return_annotation_present(self, node: ast.FunctionDef) -> bool:
        is_special_function = node.name.startswith("__") and node.name.endswith("__")
        if is_special_function is False and node.returns is None:
            return False
        return True

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        for arg in node.args.args:
            if self.is_function_arg_annotation_present(arg) is False:
                self.errors.append((arg.lineno, arg.col_offset, f"{AnnotationErrorCodes.ARGUMENT_ANNOTATION_MISSING.value} Argument `{arg.arg}` missing type annotation in function `{node.name}`"))

        if self.is_function_return_annotation_present(node) is False:
            self.errors.append((node.lineno, node.col_offset, f"{AnnotationErrorCodes.RETURN_TYPE_ANNOTATION_MISSING.value} Function `{node.name}` missing return type annotation"))
        return node


class Plugin:
    name = "enforce_type_annotations"
    version = "0.1.1"

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self.tree = tree
        self.current_filename = filename
        path = os.path.splitext(filename)[0]
        mod_path = []
        while path:
            if os.path.exists(os.path.join(path, '.flake8')):
                break
            dir, name = os.path.split(path)
            mod_path.insert(0, name)
            path = dir
        self.current_module = '.'.join(mod_path)

    def run(self) -> Generator:
        errors: List[Tuple[int, int, str]] = []
        visitor = FunctionVisitor(current_module=self.current_module, current_filename=self.current_filename, errors=errors)
        visitor.visit(self.tree)
        for lineno, colno, msg in errors:
            yield lineno, colno, msg, type(self)
