from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
from cdk_template.context.sample_stage_context import SampleStageContext
from cdk_template.stack.stack_base import (
    StageStackBase
)

class SampleStageStack(StageStackBase):
    STACK_NAME = "sample"
    context: SampleStageContext

    def _resources(self):
        topic = sns.Topic(
            self, self.get_resource_id("sampleTopic"),
            topic_name=self.get_resource_name("sampleTopic")
        )

        topic.add_subscription(subs.EmailSubscription(
            self.context.email_address
        ))
