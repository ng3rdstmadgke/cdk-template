import json
from aws_cdk import (
    aws_ecr as ecr
)
from cdk_template.context.ecr_context import EcrContext
from cdk_template.stack.stack_base import StageStackBase

class EcrStack(StageStackBase):
    STACK_NAME = "ecr"
    context: EcrContext

    def _ecr_repositories(self, repository_name: str):
        lifecycle_policy = json.dumps(
            {
                "rules": [
                    {
                        "action": {
                            "type": "expire",
                        },
                        "selection": {
                            "countType": "imageCountMoreThan",
                            "countNumber": 10,
                            "tagStatus": "untagged",
                        },
                        "description": "delete untagged image cycle",
                        "rulePriority": 1,
                    }
                ],
            }
        )

        repository_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Deny",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": ["ecr:*"],
                    "Condition": {
                        "StringNotEquals": {
                            # cloudformationからのアクセスを許可
                            "aws:CalledVia": [ 
                                "cloudformation.amazonaws.com",
                            ],
                            # ECRのVPCエンドポイントからのアクセスを許可
                            "aws:sourceVpce": self.context.allow_vpce_list,
                        },
                        "NotIpAddress": {
                            # 指定のネットワークからのアクセスを許可
                            "aws:SourceIp": self.context.allow_ip_list,
                        },
                    },
                }
            ],
        }

        ecr_repo = ecr.CfnRepository(
            self, self._get_resource_id(f"ecr_{repository_name}"),
            repository_name=self._get_full_repository_name(repository_name),
            image_scanning_configuration=ecr.CfnRepository.ImageScanningConfigurationProperty(
                scan_on_push=True,
            ),
            repository_policy_text=repository_policy,
            lifecycle_policy=ecr.CfnRepository.LifecyclePolicyProperty(
                lifecycle_policy_text=lifecycle_policy,
            ),
        )

    def _get_full_repository_name(self, repository_name: str) -> str:
        return f"{self.context.app_name}-{self.context.stage}/{repository_name}"

    def _resources(self):
        for repository_name in self.context.ecr_repositories:
            self._ecr_repositories(repository_name)
