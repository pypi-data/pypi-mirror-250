import pytest
import sys
from rospy_yaml_include.yaml_include import RospyYamlInclude
import yaml


class TestRospyInclude:
    """
    Class containing unit tests for TestPathInclude
    """

    def test_rospy_include(self):
        """
        Unit test for rospy_include
        """

        yml = """
            value: 
            - 10
            fields: !ros_include 
                    package: rospy_yaml_include_test
                    extension: test_files/import.yaml
            """

        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_rospy_circular_include(self):
        """
        Unit test for circular includes in rospy_include
        """
        yml = """
            value: 
            - 10
            fields: !ros_include 
                    package: rospy_yaml_include_test
                    extension: test_files/circular_import_ros.yaml
            """
        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"


if __name__ == "__main__":
    sys.exit(pytest.main(["--capture=no", __file__]))
