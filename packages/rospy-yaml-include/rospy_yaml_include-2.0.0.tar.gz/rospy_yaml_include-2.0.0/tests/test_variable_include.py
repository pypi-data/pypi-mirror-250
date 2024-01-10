import pytest
import sys
from rospy_yaml_include.yaml_include import RospyYamlInclude
import yaml
import os


class TestVariableInclude:
    """
    Class containing unit tests for dynamic include
    """

    @classmethod
    def setup_class(self):
        """
        setup function for tests
        """
        os.environ['TEST_INCLUDE_VARIABLE'] = 'import'
        os.environ['TEST_INCLUDE_VARIABLE_CIRCULAR'] = 'circular_import'

    def test_relative_variable_include(self):
        """
        Unit test for variable relative include
        """
        cwd = os.getcwd()

        yml = """
            value: 
            - 10
            fields: !variable_include test_files/${TEST_INCLUDE_VARIABLE}.yaml
            """

        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_relative_variable_circular_include(self):
        """
        Unit test for circular includes in variable relative include
        """
        cwd = os.getcwd()
        yml = """
            value: 
            - 10
            fields: !variable_include test_files/${TEST_INCLUDE_VARIABLE_CIRCULAR}.yaml
            """
        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"

    def test_absolute_variable_path_include(self):
        """
        Unit test for variable absolute include
        """
        cwd = os.getcwd()

        yml = f"""
            value: 
            - 10
            fields: !variable_include {cwd}/test_files/${{TEST_INCLUDE_VARIABLE}}.yaml
            """

        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_absolute_variable_path_circular_include(self):
        """
        Unit test for circular includes in variable absolute include
        """
        cwd = os.getcwd()
        yml = f"""
            value: 
            - 10
            fields: !variable_include {cwd}/test_files/${{TEST_INCLUDE_VARIABLE_CIRCULAR}}.yaml
            """
        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"

    @classmethod
    def teardown_class(self):
        """
        teardown function for tests
        """

        del os.environ['TEST_INCLUDE_VARIABLE']

if __name__ == "__main__":
    sys.exit(pytest.main(["--capture=no", __file__]))
