"""
This module provides models for Route-SDK.
"""


class NextHop(object):
    """
    NextHop
    """

    def __init__(self, next_hop_id, next_hop_type, path_type):
        self.nexthopId = next_hop_id
        self.nexthopType = next_hop_type
        self.pathType = path_type
