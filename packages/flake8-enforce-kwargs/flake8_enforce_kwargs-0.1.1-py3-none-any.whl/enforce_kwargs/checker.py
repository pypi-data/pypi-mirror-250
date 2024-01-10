import ast
import enum
import os

from typing import List, Tuple, Generator


class KwargsErrorCodes(enum.Enum):
    FUNCTION_KWARG_ONLY = "EKW001"
    CLASS_METHOD_KWARG_ONLY = "EKW002"


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, current_module: str, current_filename: str, errors: List[Tuple[int, int, str]]) -> None:
        self.current_module = current_module
        self.current_filename = current_filename
        self.errors = errors

    @staticmethod
    def is_positional_arg_present_in_function(*, node: ast.FunctionDef) -> bool:
        is_special_function = node.name.startswith("__") and node.name.endswith("__")
        has_positional_or_default_arguments = bool(node.args.args or node.args.defaults)
        return is_special_function is False and has_positional_or_default_arguments is True

    def __check_function_def(self, *, node: ast.FunctionDef, errors: List[Tuple[int, int, str]]) -> None:
        first_arg = None
        if len(node.args.args) > 0:
            first_arg = node.args.args[0].arg

        valid_class_method_first_args = ['self', 'cls']
        is_class_method = first_arg in valid_class_method_first_args

        is_positional_arg_present_in_function = self.is_positional_arg_present_in_function(node=node)

        if is_class_method is False:
            # The function is either a normal funtion or a static method
            if is_positional_arg_present_in_function is True:
                errors.append(
                    (
                        node.lineno,
                        node.col_offset,
                        f"{KwargsErrorCodes.FUNCTION_KWARG_ONLY.value} Function `{node.name}` should only accept keyword arguments."
                    )
                )
        else:
            if is_positional_arg_present_in_function is True and len(node.args.args) > 1:
                self.errors.append(
                    (
                        node.lineno,
                        node.col_offset,
                        f"{KwargsErrorCodes.CLASS_METHOD_KWARG_ONLY.value} Class method `{node.name}` should only accept keyword arguments."
                    )
                )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.__check_function_def(node=node, errors=self.errors)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.__check_function_def(node=item, errors=self.errors)
        return node


class Plugin:
    name = "enforce_kwargs"
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
