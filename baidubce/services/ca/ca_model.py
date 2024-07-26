"""
This module provides a model class for CA.
"""

class Instance(dict):
    """
    This class defines the Tag object.
    """

    def __init__(self, instance_id):
        """
        :param instance_id: Instance Id
        :type instance_id: str
        """
        super(Instance, self).__init__()
        self["instanceId"] = instance_id


class Command(dict):
    """
    This class defines the Command object.
    """

    def __init__(self, type, content, scope, enable_parameter, parameters, user, work_dir):
        """
        :param type: Command type
        :type type: str
        :param content: Command content
        :type content: str
        :param scope: Command scope
        :type scope: str
        :param enable_parameter: Enable parameter flag
        :type enable_parameter: bool
        :param user: User
        :type user: str
        :param work_dir: Working directory
        :type work_dir: str
        """
        super(Command, self).__init__()
        self["type"] = type
        self["content"] = content
        self["scope"] = scope
        self["enableParameter"] = enable_parameter
        self["parameters"] = parameters
        self["user"] = user
        self["workDir"] = work_dir


class Action(dict):
    """
    This class defines the Action object.
    """

    def __init__(self, ref=None, id=None, type=None, name=None, timeout_second=None, command=None):
        """
        :param ref: Action ref
        :ref type: str
        :param ref: Action id
        :id type: str
        :param type: Action type
        :type type: str
        :param name: Action name
        :type name: str
        :param timeout_second: Timeout in seconds
        :type timeout_second: int
        :param command: Command object
        :type command: Command
        """
        super(Action, self).__init__()
        self["ref"] = ref
        self["id"] = id
        self["type"] = type
        self["name"] = name
        self["timeoutSecond"] = timeout_second
        self["command"] = command


class Target(dict):
    """
    This class defines the Target object.
    """

    def __init__(self, instance_type, instance_id):
        """
        :param instance_type: Instance type
        :type instance_type: str
        :param instance_id: Instance Id
        :type instance_id: str
        """
        super(Target, self).__init__()
        self["instanceType"] = instance_type
        self["instanceId"] = instance_id


class TargetSelector(dict):
    """
    This class defines the Target object.
    """

    def __init__(self, instance_type, tags):
        """
        :param instance_type: Instance type
        :type instance_type: str
        :param tags: tags
        :type tags: list
        """
        super(TargetSelector, self).__init__()
        self["instanceType"] = instance_type
        self["tags"] = tags


class Execution(dict):
    """
    This class defines the Execution object.
    """

    def __init__(self, execution, action, targets):
        """
        :param execution: Execution type
        :type execution: str
        :param action: Action object
        :type action: Action
        :param targets: List of Target objects
        :type targets: list
        """
        super(Execution, self).__init__()
        self["execution"] = execution
        self["action"] = action
        self["targets"] = targets
