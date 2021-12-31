from dataclasses import dataclass
from typing import List, Optional
from cdk_template.context.context_loader_base import StageContextBase

class EcrContext(StageContextBase):
    ecr_repositories: List[str]
    ecr_allow_vpce_api: Optional[str]
    ecr_allow_vpce_dkr: Optional[str]
    ecr_allow_ip_list: List[str]

    def get_allow_vpce_list(self) -> List[str]:
        allow_vpce_list = []
        if self.ecr_allow_vpce_api:
            allow_vpce_list.append(self.ecr_allow_vpce_api)
        if self.ecr_allow_vpce_dkr:
            allow_vpce_list.append(self.ecr_allow_vpce_dkr)
        return allow_vpce_list