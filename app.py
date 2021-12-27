#!/usr/bin/env python3

from aws_cdk import core

from cdk_template.cdk_template_stack import CdkTemplateStack

from cdk_template.context.sample_stage_context import SampleStageContextLoader
from cdk_template.stack.sample_stage_stack import SampleStageStack

KEY_CONTEXT_DEFAULT = "default"
KEY_CONTEXT_OVERWRITE = "overwrite"
ARG_KEY_CONTEXT_STAGE = "stage"
ARG_KEY_CONTEXT_LINE = "line"

app = core.App()
default_context = app.node.try_get_context(KEY_CONTEXT_DEFAULT)
overwrite_context = app.node.try_get_context(KEY_CONTEXT_OVERWRITE)

stage = app.node.try_get_context(ARG_KEY_CONTEXT_STAGE)
if stage:
    sample_stage_context = SampleStageContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    ).load()
    SampleStageStack(app, sample_stage_context)


    line = app.node.try_get_context(ARG_KEY_CONTEXT_STAGE)
    if line:
        pass

#CdkTemplateStack(app, "cdk-template")

app.synth()
