from typing import List, TypedDict
from typing_extensions import Required


class _FunctionItem(TypedDict, total=False):
    fingerprint: "_Uint"
    function: str
    in_app: bool
    package: str
    self_times_ns: List["_Uint"]


class _Root(TypedDict, total=False):
    functions: Required[List["_FunctionItem"]]
    """ Required property """

    environment: str
    profile_id: Required[str]
    """ Required property """

    platform: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    received: Required[int]
    """ Required property """

    release: str
    retention_days: Required[int]
    """ Required property """

    timestamp: Required[int]
    """ Required property """

    transaction_name: Required[str]
    """ Required property """



_Uint = int
""" minimum: 0 """

