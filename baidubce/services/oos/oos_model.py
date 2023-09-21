
class OperatorModel(dict):
    """
    This class define operator.
    """
    def __init__(self, name, operator, properties, retries=0, retry_interval=60000, timeout=3600000, description=""):
        """
        :param name:
            Operator name.
        :type name: string

        :param operator:
            Operator type.
        :type operator: string

        :param properties:
            Operator execute parameters.
        :type properties: dict

        :param retries:
            Operator retry count.
        :type retries: int

        :param retry_interval:
            Operator retry interval.
        :type retries: int

        :param timeout:
            Operator execute timeout.
        :type timeout: int

        :param description:
            Operator description.
        :type description: string
        """
        super(OperatorModel, self).__init__()
        self["name"] = name
        self["operator"] = operator
        self["properties"] = properties
        self["retries"] = retries
        self["retryInterval"] = retry_interval
        self["timeout"] = timeout
        self["description"] = description


class TemplateModel(dict):
    """
    This class define template.
    """
    def __init__(self, name, operators=[], linear=True, ref=""):
        """
        :param name:
            Template name.
        :type name: string

        :param operators:
            Include template operators to execute.
        :type operators: OperatorModel array

        :param linear:
            Operator execute linearly.
        :type linear: bool

        :param ref:
            template id.
        :type ref: string
        """
        super(TemplateModel, self).__init__()
        self["name"] = name
        self["ref"] = ref
        self["operators"] = operators
        self["linear"] = linear


class TagModel(dict):
    """
    This class define tag.
    """
    def __init__(self, key, value):
        """
        :param key:
            Tag key.
        :type key: string

        :param value:
            Tag value.
        :type value: string
        """
        super(TagModel, self).__init__()
        self["tagKey"] = key
        self["tagValue"] = value
