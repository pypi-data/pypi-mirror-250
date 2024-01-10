import ast

import pytest
from enforce_type_annotations.checker import Plugin


class TestPlugin:
    file_name: str = "mock_filename"

    def test_when_type_annotation_are_present(self):
        code = """def test_function(mock_arg: Any) -> None:pass"""
        tree = ast.parse(code)
        plugin = Plugin(tree=tree, filename=self.file_name)
        with pytest.raises(StopIteration):
            next(plugin.run())

    def test_argument_type_annotation_not_present_in_function(self):
        code = """def test_function(mock_arg) -> None:pass"""
        tree = ast.parse(code)
        plugin = Plugin(tree=tree, filename=self.file_name)
        for lineno, col_offset, error_message, instance in plugin.run():
            assert error_message == "ETA001 Argument `mock_arg` missing type annotation in function `test_function`"

    def test_return_type_annotation_not_present_in_function(self):
        code = """def test_function(mock_arg: Any):pass
        """
        tree = ast.parse(code)
        plugin = Plugin(tree=tree, filename=self.file_name)
        for lineno, col_offset, error_message, instance in plugin.run():
            assert error_message == "ETA002 Function `test_function` missing return type annotation"
