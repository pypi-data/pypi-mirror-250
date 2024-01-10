import pytest
import sys
from rospy_yaml_include.yaml_include import RospyYamlInclude
import yaml
import os
import rospy

class TestRosParamSubstitute:
    """
    Class containing unit tests for dynamic include
    """

    def test_ros_param_substitute(self):
        """
        Unit test for dynamic relative include
        """

        try:
            rospy.init_node("ros_param_substitute_test", log_level=rospy.INFO)
        except rospy.exceptions.ROSException:
            pass

        rospy.set_param("ros_param_substitute_test_param", 10)

        cwd = os.getcwd()

        yml = """
            value: 
            - 10
            fields: !ros_param_substitute ${ros_param_substitute_test_param}
            """

        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")

if __name__ == "__main__":
    sys.exit(pytest.main(["--capture=no", __file__]))
