#!/usr/bin/env python3

from aws_cdk import core

from cdk_template.stack.ecr_stack import EcrStack, EcrContext
from cdk_template.stack.network_stack import NetworkStack, NetworkContext
from cdk_template.lib.base import ContextLoader

app = core.App()
default_context = app.node.try_get_context("default")
overwrite_context = app.node.try_get_context("overwrite")
stage = app.node.try_get_context("stage")

if not stage:
    raise Exception("-c stage=<STAGE> が指定されていません")

level = len(stage.split("."))
if level >= 1:
    ecr_context = ContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    ).get_context(EcrContext)
    EcrStack(app, ecr_context)

    network_context = ContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    ).get_context(NetworkContext)
    NetworkStack(app, network_context)

if level >= 2:
    pass

#CdkTemplateStack(app, "cdk-template")

app.synth()
