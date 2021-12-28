from dataclasses import dataclass
from typing import List
from cdk_template.context.context_loader_base import (
    StageContextBase,
    StageContextLoader
)

@dataclass(frozen=True)
class EcrContext(StageContextBase):
    ecr_repositories: str
    allow_vpce_list: List[str]
    allow_ip_list: List[str]

class EcrContextLoader(StageContextLoader):
    KEY_CONTEXT_ECR_REPOSITORIES = "ecr_repositories"
    KEY_CONTEXT_ECR_ALLOW_VPCE_API = "ecr_allow_vpce_api"
    KEY_CONTEXT_ECR_ALLOW_VPCE_DKR = "ecr_allow_vpce_dkr"
    KEY_CONTEXT_ECR_ALLOW_IP_LIST = "ecr_allow_ip_list"


    def load(self) -> EcrContext:
        return EcrContext(
            # ContextBase の引数
            aws_account_id=self.context_src[self.KEY_CONTEXT_AWS_ACCOUNT_ID],
            aws_region=self.context_src[self.KEY_CONTEXT_AWS_REGION],
            app_name=self.context_src[self.KEY_CONTEXT_APP_NAME],
            vpc_id=self.context_src[self.KEY_CONTEXT_VPC_ID],
            subnet_ids=self.context_src[self.KEY_CONTEXT_SUBNET_IDS],
            http_proxy=self.context_src[self.KEY_CONTEXT_HTTP_PROXY],
            https_proxy=self.context_src[self.KEY_CONTEXT_HTTPS_PROXY],
            no_proxy=self.context_src[self.KEY_CONTEXT_NO_PROXY],
            termination_protection=self.context_src[self.KEY_CONTEXT_TERMINATION_PROTECTION],
            tags=self.context_src[self.KEY_CONTEXT_TAGS],
            # StageContextBase の引数
            stage=self.stage,
            # SampleStageContextLoader の引数
            ecr_repositories=self.context_src[self.KEY_CONTEXT_ECR_REPOSITORIES],
            allow_vpce_list=self._get_allow_vpce_list(),
            allow_ip_list=self.context_src[self.KEY_CONTEXT_ECR_ALLOW_IP_LIST]
        )

    def _get_allow_vpce_list(self) -> List[str]:
        allow_vpce_list = []
        allow_vpce_api = self.context_src[self.KEY_CONTEXT_ECR_ALLOW_VPCE_API]
        if len(allow_vpce_api) > 0:
            allow_vpce_list.append(allow_vpce_api)

        allow_vpce_dkr = self.context_src[self.KEY_CONTEXT_ECR_ALLOW_VPCE_DKR]
        if len(allow_vpce_dkr) > 0:
            allow_vpce_list.append(allow_vpce_dkr)
        return allow_vpce_list