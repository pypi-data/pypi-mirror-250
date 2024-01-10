import ast

import pytest
from enforce_kwargs.checker import Plugin


class TestPlugin:
    file_name: str = "mock_filename"

    def test_when_kwargs_present_in_function(self):
        code = """def test_function(*, mock_arg):pass"""
        tree = ast.parse(code)
        plugin = Plugin(tree=tree, filename=self.file_name)
        plugin_run = plugin.run()
        with pytest.raises(StopIteration):
            next(plugin_run)

    def test_when_kwargs_not_present_in_function(self):
        code = """def test_function(mock_arg):pass"""
        tree = ast.parse(code)
        plugin = Plugin(tree=tree, filename=self.file_name)
        for lineno, col_offset, error_message, instance in plugin.run():
            assert error_message == "EKW001 Function `test_function` should only accept keyword arguments."

    def test_when_kwargs_not_present_in_class_method(self):
        code = """class TestClass:
                    def test_function(self, mock_arg):pass
        """
        tree = ast.parse(code)
        plugin = Plugin(tree=tree, filename=self.file_name)
        for lineno, col_offset, error_message, instance in plugin.run():
            assert error_message == "EKW002 Class method `test_function` should only accept keyword arguments."

        code = """class TestClass:
                    @classmethod
                    def test_function(cls, mock_arg):pass
        """
        tree = ast.parse(code)
        plugin = Plugin(tree=tree, filename=self.file_name)
        for lineno, col_offset, error_message, instance in plugin.run():
            assert error_message == "EKW002 Class method `test_function` should only accept keyword arguments."
