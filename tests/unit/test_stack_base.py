from dataclasses import dataclass
from aws_cdk import (
        core,
        assertions
    )

from cdk_template.context.context_loader_base import (
    StageContextBase,
    LineContextLoaderBase,
    LineContextBase,
)

from cdk_template.stack.stack_base import (
    StageStackBase
)

class TestContext(StageContextBase):
    pass

class TestStack(StageStackBase):
    STACK_NAME = "test"
    def _resources(self):
        pass

def test_stack_base():
    app = core.App()
    context = TestContext(
        aws_account_id="669567641293",
        aws_region="ap-northeast-1",
        app_name="mido",
        vpc_id="vpc-0aa084a693ff324f4",
        subnet_ids=[],
        http_proxy="",
        https_proxy="",
        no_proxy=[],
        termination_protection=False,
        tags={},
        stage="test"
    )

    stack = TestStack(app, context)

def test_stack_base_get_vpc():
    app = core.App()
    context = TestContext(
        aws_account_id="669567641293",
        aws_region="ap-northeast-1",
        app_name="mido",
        vpc_id="vpc-0aa084a693ff324f4",
        subnet_ids=[],
        http_proxy="",
        https_proxy="",
        no_proxy=[],
        termination_protection=False,
        tags={},
        stage="test"
    )

    stack = TestStack(app, context)
    stack._get_vpc()
    stack._get_vpc()

def test_stack_base_get_subnet():
    app = core.App()
    context = TestContext(
        aws_account_id="669567641293",
        aws_region="ap-northeast-1",
        app_name="mido",
        vpc_id="vpc-0aa084a693ff324f4",
        subnet_ids=[],
        http_proxy="",
        https_proxy="",
        no_proxy=[],
        termination_protection=False,
        tags={},
        stage="dev"
    )

    stack = TestStack(app, context)
    stack._get_subnet("subnet-xxxxxxxxxxxxxxxxx")
    stack._get_subnet("subnet-xxxxxxxxxxxxxxxxx")

def test_stack_base_get_role():
    app = core.App()
    context = TestContext(
        aws_account_id="669567641293",
        aws_region="ap-northeast-1",
        app_name="mido",
        vpc_id="vpc-0aa084a693ff324f4",
        subnet_ids=[],
        http_proxy="",
        https_proxy="",
        no_proxy=[],
        termination_protection=False,
        tags={},
        stage="dev"
    )

    stack = TestStack(app, context)
    stack._get_subnet("some_role")
    stack._get_subnet("some_role")