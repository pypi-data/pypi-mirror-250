import pytest
import sys
from rospy_yaml_include.yaml_include import RospyYamlInclude
import yaml
import os


class TestPathInclude:
    """
    Class containing unit tests for absolute path include
    """

    def test_path_include(self):
        """
        Unit test for path_include
        """
        cwd = os.getcwd()

        yml = f"""
            value: 
            - 10
            fields: !path_include {cwd}/test_files/import.yaml
            """

        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_path_circular_include(self):
        """
        Unit test for circular includes in absolute path include
        """
        cwd = os.getcwd()
        yml = f"""
            value: 
            - 10
            fields: !path_include {cwd}/test_files/circular_import.yaml
            """
        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"


if __name__ == "__main__":
    sys.exit(pytest.main(["--capture=no", __file__]))
