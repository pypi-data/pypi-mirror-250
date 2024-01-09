import datetime
import typing

import kubernetes.client

class V1alpha1ServiceCIDRSpec:
    cidrs: typing.Optional[list[str]]
    
    def __init__(self, *, cidrs: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ServiceCIDRSpecDict:
        ...
class V1alpha1ServiceCIDRSpecDict(typing.TypedDict, total=False):
    cidrs: typing.Optional[list[str]]
