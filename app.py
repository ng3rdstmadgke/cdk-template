#!/usr/bin/env python3

from aws_cdk import core

from cdk_template.context.context_loader_base import (
    StageContextLoader,
    LineContextLoader,
)
from cdk_template.context.sample_stage_context import SampleStageContext
from cdk_template.stack.sample_stage_stack import SampleStageStack
from cdk_template.context.sample_line_context import SampleLineContext
from cdk_template.stack.sample_line_stack import SampleLineStack
from cdk_template.context.ecr_context import EcrContext
from cdk_template.stack.ecr_stack import EcrStack
from cdk_template.context.network_context import NetworkContext
from cdk_template.stack.network_stack import NetworkStack


KEY_CONTEXT_DEFAULT = "default"
KEY_CONTEXT_OVERWRITE = "overwrite"
ARG_KEY_CONTEXT_STAGE = "stage"
ARG_KEY_CONTEXT_LINE = "line"

app = core.App()
default_context = app.node.try_get_context(KEY_CONTEXT_DEFAULT)
overwrite_context = app.node.try_get_context(KEY_CONTEXT_OVERWRITE)

stage = app.node.try_get_context(ARG_KEY_CONTEXT_STAGE)
if stage:
    sample_stage_context = StageContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    ).get_context(SampleStageContext)
    SampleStageStack(app, sample_stage_context)

    ecr_context = StageContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    ).get_context(EcrContext)
    EcrStack(app, ecr_context)

    network_context = StageContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    ).get_context(NetworkContext)
    NetworkStack(app, network_context)


    line = app.node.try_get_context(ARG_KEY_CONTEXT_LINE)
    if line:
        sample_line_context = LineContextLoader(
            default_context=default_context,
            overwrite_context=overwrite_context,
            stage=stage,
            line=line
        ).get_context(SampleLineContext)
        SampleLineStack(app, sample_line_context)

#CdkTemplateStack(app, "cdk-template")

app.synth()
