from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
from cdk_template.context.sample_line_context import SampleLineContext
from cdk_template.stack.stack_base import LineStackBase

class SampleLineStack(LineStackBase):
    STACK_NAME = "sampleLine"
    context: SampleLineContext

    def _resources(self):
        topic = sns.Topic(
            self, self._get_resource_id("sampleTopic"),
            topic_name=self._get_resource_name("sampleTopic")
        )

        topic.add_subscription(subs.EmailSubscription(
            self.context.sample_line_param
        ))
