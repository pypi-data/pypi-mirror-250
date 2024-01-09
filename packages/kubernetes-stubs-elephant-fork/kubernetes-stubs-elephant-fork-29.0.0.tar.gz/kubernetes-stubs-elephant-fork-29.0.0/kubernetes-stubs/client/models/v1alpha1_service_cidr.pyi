import datetime
import typing

import kubernetes.client

class V1alpha1ServiceCIDR:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1alpha1ServiceCIDRSpec]
    status: typing.Optional[kubernetes.client.V1alpha1ServiceCIDRStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1alpha1ServiceCIDRSpec] = ..., status: typing.Optional[kubernetes.client.V1alpha1ServiceCIDRStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ServiceCIDRDict:
        ...
class V1alpha1ServiceCIDRDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1alpha1ServiceCIDRSpecDict]
    status: typing.Optional[kubernetes.client.V1alpha1ServiceCIDRStatusDict]
