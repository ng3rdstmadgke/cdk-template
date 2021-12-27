from dataclasses import dataclass
from aws_cdk import (
        core,
        assertions
    )

from cdk_template.context.context_loader_base import (
    StageContextLoader,
    StageContextBase,
    LineContextLoaderBase,
    LineContextBase,
)

KEY_CONTEXT_DEFAULT = "default"
KEY_CONTEXT_OVERWRITE = "overwrite"
ARG_KEY_CONTEXT_STAGE = "stage"
ARG_KEY_CONTEXT_LINE = "line"

@dataclass(frozen=True)
class TestStageContext(StageContextBase):
    STACK_NAME = "testStage"
    test_stage: str

@dataclass(frozen=True)
class TestLineContext(LineContextBase):
    STACK_NAME = "testLine"
    test_line: str

class TestStageContextLoader(StageContextLoader):
    KEY_CONTEXT_TEST_STAGE = "test_stage"

    def load(self) -> TestStageContext:
        return TestStageContext(
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
            # 
            test_stage=self.context_src[self.KEY_CONTEXT_TEST_STAGE]
        )

class TestLineContextLoader(LineContextLoaderBase):
    KEY_CONTEXT_TEST_LINE = "test_line"

    def load(self) -> TestLineContext:
        return TestLineContext(
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
            line=self.line,
            test_line=self.context_src[self.KEY_CONTEXT_TEST_LINE]
        )

def test_load_stage_context():
    """Stageレイヤのコンテキストの上書きのテスト"""
    stage = "dev"
    default_context = {
        "test_01": "0",
        "test_02": "0",
        "test_03": "0",
        "test_04": "0",
    }
    overwrite_context = {
        "dev": { "test_01": "1", "test_10": "1"},
        "stg": {"test_02": "1", "test_20": "1"},
        "prd": {"test_03": "1", "test_30": "1"},
    }

    expect = {
        "test_01": "1",
        "test_02": "0",
        "test_03": "0",
        "test_04": "0",
    }

    result = TestStageContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    )

    assert result.context_src == expect

def test_load_line_context():
    """Lineレイヤのコンテキストの上書きのテスト"""
    stage = "dev"
    line = "line1"
    default_context = {
        "test_01": "0",
        "test_02": "0",
        "test_03": "0",
        "test_04": "0",
    }
    overwrite_context = {
        "dev": {
            "test_01": "1",
            "line1": {"test_02": "1", "test_20": "1"},
            "line2": {"test_03": "1", "test_20": "1"}
        },
    }

    expect = {
        "test_01": "1",
        "test_02": "1",
        "test_03": "0",
        "test_04": "0",
    }

    result = TestLineContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage,
        line=line
    )

    assert result.context_src == expect

def test_create_stage_context():
    default_context = {
      "aws_account_id": "xxxxxxxxxxxxxx",
      "aws_region": "ap-northeast-1",
      "app_name": "mido",
      "vpc_id": "vpc-xxxxxxxxxxxxxxxxx",
      "subnet_ids": [ ],
      "http_proxy": "",
      "https_proxy": "",
      "no_proxy": [],
      "termination_protection": False,
      "tags": {
        "Billing Destination": "SAMPLE",
        "SYS_STACK_APP": "SAMPLE"
      },
      "sns_email_address": "sample@example.com",
      "test_stage": "test"
    }

    stage = "dev"
    context = TestStageContextLoader(default_context=default_context, overwrite_context={}, stage=stage).load()

    assert context.get_resource_name("hogeHoge") == "mido-hogeHoge-dev"
    assert context.get_resource_id("hogeHoge") == "MidoHogehogeDev"
    assert context.aws_account_id == default_context["aws_account_id"]
    assert context.aws_region == default_context["aws_region"]
    assert context.app_name == default_context["app_name"]
    assert context.vpc_id == default_context["vpc_id"]
    assert context.subnet_ids == default_context["subnet_ids"]
    assert context.http_proxy == default_context["http_proxy"]
    assert context.https_proxy == default_context["https_proxy"]
    assert context.no_proxy == default_context["no_proxy"]
    assert context.termination_protection == default_context["termination_protection"]
    assert context.tags == default_context["tags"]
    assert context.stage == stage

def test_create_line_context():
    default_context = {
      "aws_account_id": "xxxxxxxxxxxxxx",
      "aws_region": "ap-northeast-1",
      "app_name": "mido",
      "vpc_id": "vpc-xxxxxxxxxxxxxxxxx",
      "subnet_ids": [ ],
      "http_proxy": "",
      "https_proxy": "",
      "no_proxy": [],
      "termination_protection": False,
      "tags": {
        "Billing Destination": "SAMPLE",
        "SYS_STACK_APP": "SAMPLE"
      },
      "sns_email_address": "sample@example.com",
      "test_line": "test"
    }

    stage = "dev"
    line = "line1"
    context = TestLineContextLoader(default_context=default_context, overwrite_context={}, stage=stage, line=line).load()

    assert context.get_resource_name("hogeHoge") == "mido-hogeHoge-dev-line1"
    assert context.get_resource_id("hogeHoge") == "MidoHogehogeDevLine1"
    assert context.stage == stage
    assert context.line == line