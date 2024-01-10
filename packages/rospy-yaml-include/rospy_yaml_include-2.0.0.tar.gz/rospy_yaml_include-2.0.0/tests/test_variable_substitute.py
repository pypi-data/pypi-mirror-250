import pytest
import sys
from rospy_yaml_include.yaml_include import RospyYamlInclude
import yaml
import os

class TestVariableSubstitute:
    """
    Class containing unit tests for dynamic include
    """

    def test_variable_substitute(self):
        """
        Unit test for dynamic relative include
        """
        os.environ['TEST_SUBSTITUTE_VARIABLE'] = 'test'

        cwd = os.getcwd()

        yml = """
            value: 
            - 10
            fields: !variable_substitute ${TEST_SUBSTITUTE_VARIABLE}
            """

        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            yaml.load(yml, Loader=constructor.add_constructor())
        except Exception as error:
            pytest.fail(f"{error}")
        finally:
            del os.environ['TEST_SUBSTITUTE_VARIABLE']
if __name__ == "__main__":
    sys.exit(pytest.main(["--capture=no", __file__]))
