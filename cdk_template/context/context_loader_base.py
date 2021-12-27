import re

import copy
from typing import Dict, List
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

@dataclass(frozen=True)
class ContextBase(metaclass=ABCMeta):
    aws_account_id: str
    aws_region: str
    app_name: str
    vpc_id: str
    subnet_ids: List[str]
    http_proxy: str
    https_proxy: str
    no_proxy: List[str]
    termination_protection: bool
    tags: Dict[str, str]

    @abstractmethod
    def get_resource_name(self, name: str) -> str:
        raise NotImplementedError
        
    def get_resource_id(self, name: str) -> str:
        resource_name = self.get_resource_name(name)
        return "".join(
            map(
                lambda e: e.capitalize(),
                re.split("[-_]", resource_name)
            )
        )


@dataclass(frozen=True)
class StageContextBase(ContextBase, metaclass=ABCMeta):
    stage: str

    def get_resource_name(self, name: str) -> str:
        return f"{self.app_name}-{name}-{self.stage}"

@dataclass(frozen=True)
class LineContextBase(ContextBase, metaclass=ABCMeta):
    stage: str
    line: str

    def get_resource_name(self, name: str) -> str:
        return f"{self.app_name}-{name}-{self.stage}-{self.line}"


class ContextLoaderBase(metaclass=ABCMeta):
    KEY_CONTEXT_AWS_ACCOUNT_ID = "aws_account_id"
    KEY_CONTEXT_AWS_REGION = "aws_region"
    KEY_CONTEXT_APP_NAME = "app_name"
    KEY_CONTEXT_VPC_ID = "vpc_id"
    KEY_CONTEXT_SUBNET_IDS = "subnet_ids"
    KEY_CONTEXT_HTTP_PROXY = "http_proxy"
    KEY_CONTEXT_HTTPS_PROXY = "https_proxy"
    KEY_CONTEXT_NO_PROXY = "no_proxy"
    KEY_CONTEXT_TERMINATION_PROTECTION = "termination_protection"
    KEY_CONTEXT_TAGS = "tags"

    @abstractmethod
    def load(self) -> ContextBase:
        raise NotImplementedError

    @staticmethod
    def _overwrite_context(context: dict, overwrite_context: dict) -> dict:
        copy_context = copy.deepcopy(context)
        ContextLoaderBase._overwrite_context_inner(copy_context, overwrite_context)
        return copy_context

    @staticmethod
    def _overwrite_context_inner(context: dict, overwrite_context: dict):
        """contextをoverwrite_contextで再帰的に上書きする
        Args:
            context (dict): 更新対象のdict
            overwrite_context (dict): 上書き用のdict
        """
        for k, v in overwrite_context.items():
            if k in context:
                if type(v) == dict:
                    ContextLoaderBase._overwrite_context(
                        context[k],
                        overwrite_context[k]
                    )
                else:
                    context[k] = v

class StageContextLoader(ContextLoaderBase, metaclass=ABCMeta):
    def __init__(self, default_context: dict, overwrite_context: dict, stage: str):
        self.stage = stage
        self.context_src = self._overwrite_context(
            default_context,
            overwrite_context.get(stage, {})
        )

    @abstractmethod
    def load(self) -> StageContextBase:
        raise NotImplementedError

class LineContextLoaderBase(ContextLoaderBase, metaclass=ABCMeta):
    def __init__(self, default_context: dict, overwrite_context: dict, stage: str, line: str):
        self.stage = stage
        self.line = line
        stage_context_src = self._overwrite_context(
            default_context,
            overwrite_context.get(stage, {})
        )
        self.context_src = self._overwrite_context(
            stage_context_src,
            overwrite_context.get(stage, {}).get(line, {})
        )

    @abstractmethod
    def load(self) -> LineContextBase:
        raise NotImplementedError