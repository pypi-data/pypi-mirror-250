import pytest
import sys
from rospy_yaml_include.yaml_include import RospyYamlInclude
import yaml
import os


class TestDynamicInclude:
    """
    Class containing unit tests for dynamic include
    """

    def test_relative_dynamic_include(self):
        """
        Unit test for dynamic relative include
        """
        cwd = os.getcwd()

        yml = """
            value: 
            - 10
            fields: !include test_files/import.yaml
            """

        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_relative_dynamic_circular_include(self):
        """
        Unit test for circular includes in dynamic relative include
        """
        cwd = os.getcwd()
        yml = """
            value: 
            - 10
            fields: !include test_files/circular_import.yaml
            """
        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"

    def test_dynamic_path_include(self):
        """
        Unit test for dynamic absolute include
        """
        cwd = os.getcwd()

        yml = f"""
            value: 
            - 10
            fields: !include {cwd}/test_files/import.yaml
            """

        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_dynamic_path_circular_include(self):
        """
        Unit test for circular includes in dynamic absolute include
        """
        cwd = os.getcwd()
        yml = f"""
            value: 
            - 10
            fields: !include {cwd}/test_files/circular_import.yaml
            """
        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"


if __name__ == "__main__":
    sys.exit(pytest.main(["--capture=no", __file__]))
