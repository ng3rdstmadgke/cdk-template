from abc import abstractmethod
from aws_cdk import core
from cdk_template.context.context_loader_base import ContextBase, LineContextBase, StageContextBase

class StackBase(core.Stack):
    STACK_NAME: str
    context: ContextBase

    def __init__(self, scope: core.Construct, context: ContextBase):
        self.context = context
        super().__init__(
            scope,
            self.get_resource_name(self.STACK_NAME),
            termination_protection=context.termination_protection,
        )
        self._add_default_tag()
        self._resources()

    def get_resource_name(self, name: str) -> str:
        return self.context.get_resource_name(name)
        
    def get_resource_id(self, name: str) -> str:
        return self.context.get_resource_id(name)

    def _add_default_tag(self):
        for k, v in self.context.tags.items():
            core.Tags.of(self).add(k, v)

    # AWS Resourceについてをデプロイするメソッド
    @abstractmethod
    def _resources(self):
        raise NotImplementedError


class StageStackBase(StackBase):
    context: StageContextBase

class LineStackBase(StackBase):
    context: LineContextBase