import pytest
import sys
from rospy_yaml_include.yaml_include import RospyYamlInclude
import yaml
import os
import rospy

class TestRosParamInclude:
    """
    Class containing unit tests for dynamic include
    """

    @classmethod
    def setup_class(self):
        """
        setup function for tests
        """

        try:
            rospy.init_node("ros_param_include_test", log_level=rospy.INFO)
        except rospy.exceptions.ROSException:
            pass

        rospy.set_param("ros_param_include_test_param", "import")
        rospy.set_param("ros_param_include_test_param_circular", "circular_import")

    def test_relative_ros_param_include(self):
        """
        Unit test for ros param relative include
        """
        cwd = os.getcwd()

        yml = """
            value: 
            - 10
            fields: !ros_param_include test_files/${ros_param_include_test_param}.yaml
            """

        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_relative_ros_param_circular_include(self):
        """
        Unit test for circular includes in ros param relative include
        """
        cwd = os.getcwd()
        yml = """
            value: 
            - 10
            fields: !ros_param_include test_files/${ros_param_include_test_param_circular}.yaml
            """
        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"

    def test_absolute_ros_param_path_include(self):
        """
        Unit test for ros param absolute include
        """
        cwd = os.getcwd()

        yml = f"""
            value: 
            - 10
            fields: !ros_param_include {cwd}/test_files/${{ros_param_include_test_param}}.yaml
            """

        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

    def test_absolute_ros_param_path_circular_include(self):
        """
        Unit test for circular includes in ros param absolute include
        """
        cwd = os.getcwd()
        yml = f"""
            value: 
            - 10
            fields: !ros_param_include {cwd}/test_files/${{ros_param_include_test_param_circular}}.yaml
            """
        try:
            constructor = RospyYamlInclude()
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            assert f"RecursionError caught: {error}"

if __name__ == "__main__":
    sys.exit(pytest.main(["--capture=no", __file__]))
