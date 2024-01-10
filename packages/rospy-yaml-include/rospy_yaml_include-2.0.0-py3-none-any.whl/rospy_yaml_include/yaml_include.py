"""
rospy_yaml_include
------------------

This module provides a way to include yaml files in other yaml files.
"""
from ast import literal_eval
import os
import re
from typing import Any, Union, Dict, List, Tuple

import rospkg
import rospy
import yaml


def convert_to_type(default_value: str) -> Any:
    """
    Converts a <str> input to its literal <type> output
    """
    try:  # to convert str to Dict, List, int, float, bool
        return literal_eval(default_value)
    except (ValueError, SyntaxError):
        return default_value


def extract_arguments(input_string: str,
                      pattern: str = r'\$\{([^}]+)\}') \
        -> List[Tuple[str, str]]:
    matches = re.findall(pattern, input_string)
    params = []
    for match in matches:
        match = match.split(';')
        param = match[0].strip()
        try:
            default = match[1].strip()
        except IndexError:
            default = None
        params.append((param, default))
    return params


class RospyYamlInclude:
    """
    RospyYamlInclude class
    """

    def __init__(
        self, loader: type = yaml.SafeLoader, base_directory: str = None, import_limit: int = 150
    ) -> None:
        self.import_limit = import_limit
        self.import_count = 0

        self.loader = loader
        self.base_directory = base_directory

    class _RosInclude:
        """
        Mappping for !ros_include constructor
        """

        def __init__(self, package, extension) -> None:
            self.package = package
            self.extension = extension

    def _ros_include_constructor(
        self, loader: type, node: yaml.nodes.MappingNode
    ) -> dict:
        """
        _ros_include_constructor function handles !ros_include tag
        """
        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        rospack = rospkg.RosPack()

        file = self._RosInclude(**loader.construct_mapping(node))

        include_file = os.path.join(
            rospack.get_path(file.package),
            file.extension,
        )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _path_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _path_include_constructor function handles !path_include tag

        """
        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)

        with open(file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _relative_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _path_include_constructor function handles !relative_include tag

        this can be used to import a yaml relative to a base directory provided in the class init
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        if self.base_directory is None:
            raise ValueError(
                "base_directory must be provided in class init to use !relative_include"
            )

        file = loader.construct_scalar(node)

        include_file = os.path.join(
            self.base_directory,
            file,
        )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _dynamic_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _dynamic_include_constructor function handles !include tag

        this constructor attempts to infer the type of include based on the file extension
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)

        if file.startswith("/"):
            include_file = file
        else:
            if self.base_directory is None:
                raise ValueError(
                    "base_directory must be provided in class init to use relative include"
                )

            include_file = os.path.join(
                self.base_directory,
                file,
            )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())

    def _variable_subsitute_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _variable_subsitute_constructor function handles !variable_substitute tag

        this can be used to substitute a variable in a yaml file
        """

        param_string = loader.construct_scalar(node)
        variables = re.findall(r"\${(.*?)}", param_string)
        for variable in variables:
            fill_param = os.getenv(variable, None)
            if fill_param is not None:
                param_string = param_string.replace(f"${{{variable}}}", str(fill_param))
            else:
                raise ValueError(f"env {variable} not found")

        return param_string

    def _variable_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _variable_include_constructor function handles !variable_include tag

        this can be used to import a yaml while substituting a env variable
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)
        variables = re.findall(r"\${(.*?)}", file)
        for variable in variables:
            fill_param = os.getenv(variable, None)
            if fill_param is not None:
                file = file.replace(f"${{{variable}}}", str(fill_param))
            else:
                raise ValueError(f"env {variable} not found")

        if file.startswith("/"):
            include_file = file
        else:
            if self.base_directory is None:
                raise ValueError(
                    "base_directory must be provided in class init to use relative include"
                )

            include_file = os.path.join(
                self.base_directory,
                file,
            )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())
        
    def _ros_param_substitute_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> Union[None, Dict, List, bool, int, float, str]:
        """
        _ros_param_substitute_constructor function handles !ros_param_substitute tag

        this can be used to import a yaml substitute a rosparam

        includes option for "; <default value>" to provide a default value if rosparam is not found
            MUST be separated by semicolon ';' to allow for dict, list as default values
        """
        param_string = loader.construct_scalar(node)
        rospy.logdebug(f'ROS_PARAM_SUBSTITUTE STR: {param_string}')

        # pattern = r'\$\{([^}]+)\}'  # finds ${<ros_param_substitute>; <default>}
        # the pattern below is a modified version of the above pattern,
        # allowing for nested {} in the default value e.g.:
        # https://regex101.com/r/wPCbj8/1
        pattern = r'\$\{([^{}]*(?:{[^{}]*}[^{}]*)*)\}'  # finds ${<ros_param_substitute>; <{default}>}

        params = extract_arguments(param_string, pattern=pattern)
        rospy.logdebug(f'PARAMS [(param, default),]: {params}')

        clean_param_string = [f'${{{param}}}' for param, default in params]

        # Join the matches to re-form the resultant param_string (with defaults stripped)
        param_string = ' '.join(clean_param_string)
        rospy.logdebug(f'ROS_PARAM_SUBSTITUTE STR (CLEAN): {param_string}')

        for param, default in params:
            # if param is not found, use default value (if provided, else None)
            fill_param = rospy.get_param(param, default)

            # immediately throw error if param is not found AND default is not provided
            if fill_param is None:
                rospy.logerr(f"ERROR: tag= {node.tag} value='{node.value}'")
                raise ValueError(f"rosparam '{param}' not found; no default provided "
                                 f"[tag= {node.tag} value='{node.value}']")

            # TODO: determine if we want this capability?
            # check if default value is a rosparam substitution
            if isinstance(fill_param, str) and fill_param.startswith('${'):
                default_param_sub = re.findall(r"\${(.*?)}", fill_param)[0]
                fill_param = rospy.get_param(default_param_sub, None)

            rospy.logdebug(f'FILL_PARAM: {type(fill_param)} {fill_param}')

            param_string = param_string.replace(f"${{{param}}}", str(fill_param))
            rospy.logdebug(f"PARAM_STRING: '{param_string}'")

        # param_string Union[None, Dict, List, bool, int, float, str]
        return convert_to_type(param_string)

    def _ros_param_include_constructor(
        self, loader: type, node: yaml.nodes.ScalarNode
    ) -> dict:
        """
        _ros_param_include_constructor function handles !ros_param_include tag

        this can be used to import a yaml with a rosparam substitution
        """

        self.import_count += 1
        if self.import_count > self.import_limit:
            raise RecursionError(
                "Maximum import limit reached, check for circular references or increase import limit"
            )

        file = loader.construct_scalar(node)
        params = re.findall(r"\${(.*?)}", file)
        for param in params:
            fill_param = rospy.get_param(param, None)
            if fill_param is not None:
                file = file.replace(f"${{{param}}}", str(fill_param))
            else:
                raise ValueError(f"rosparam {param} not found")

        if file.startswith("/"):
            include_file = file
        else:
            if self.base_directory is None:
                raise ValueError(
                    "base_directory must be provided in class init to use relative include"
                )

            include_file = os.path.join(
                self.base_directory,
                file,
            )

        with open(include_file, encoding="utf-8") as yaml_file:
            return yaml.load(yaml_file, Loader=self.add_constructor())
        
    def add_constructor(self) -> type:
        """
        add constructor to yaml
        """

        loader = self.loader
        loader.add_constructor("!ros_include", self._ros_include_constructor)
        loader.add_constructor("!path_include", self._path_include_constructor)
        loader.add_constructor("!relative_include", self._relative_include_constructor)
        loader.add_constructor("!include", self._dynamic_include_constructor)
        loader.add_constructor("!variable_substitute", self._variable_subsitute_constructor)
        loader.add_constructor("!variable_include", self._variable_include_constructor)
        loader.add_constructor("!ros_param_substitute", self._ros_param_substitute_constructor)
        loader.add_constructor("!ros_param_include", self._ros_param_include_constructor)

        return loader
