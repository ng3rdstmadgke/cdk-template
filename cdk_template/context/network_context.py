from typing import Dict, List, Optional
from cdk_template.context.context_loader_base import StageContextBase
from pydantic import BaseModel

class NetworkPublicSubnets(BaseModel):
    cidr: str
    az: str

class NetworkPrivateSubnets(BaseModel):
    cidr: str
    az: str
    ngw_idx: int

class NetworkContext(StageContextBase):
    network_vpc_cidr: str
    network_public_subnets: List[NetworkPublicSubnets]
    network_private_subnets: List[NetworkPrivateSubnets]
