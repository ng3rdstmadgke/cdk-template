from dataclasses import dataclass
from cdk_template.context.context_loader_base import (
    StageContextBase,
    StageContextLoader
)

@dataclass(frozen=True)
class SampleStageContext(StageContextBase):
    email_address: str



class SampleStageContextLoader(StageContextLoader):
    KEY_CONTEXT_SNS_EMAIL_ADDRESS = "sns_email_address"


    def load(self) -> SampleStageContext:
        return SampleStageContext(
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
            email_address=self.context_src[self.KEY_CONTEXT_SNS_EMAIL_ADDRESS]
        )