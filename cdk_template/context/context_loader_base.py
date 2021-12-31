import re

import copy
from typing import Any, Dict, List, Type, Optional
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from pydantic import BaseModel

class ContextBase(BaseModel):
    """レイヤ共通で利用するメソッドやメンバが定義されたContextのベースクラス"""
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
        """CFnのスタック名やリソース名を生成するメソッド。ケバブケース"""
        raise NotImplementedError
        
    def get_resource_id(self, name: str) -> str:
        """CFnのリソースidを生成するメソッド。パスカルケース"""
        resource_name = self.get_resource_name(name)
        return "".join(
            map(
                lambda e: e.capitalize(),
                re.split("[-_]", resource_name)
            )
        )


class StageContextBase(ContextBase):
    """stageレイヤのContextが継承するべきクラス"""
    stage: str

    def get_resource_name(self, name: str) -> str:
        return f"{self.app_name}-{name}-{self.stage}"


class LineContextBase(ContextBase):
    """lineレイヤのContextが継承するべきクラス"""
    stage: str
    line: str

    def get_resource_name(self, name: str) -> str:
        return f"{self.app_name}-{name}-{self.stage}-{self.line}"

    def get_context(self, model: Type["BaseModel"]) -> BaseModel:
        raise NotImplementedError


class ContextLoaderBase(metaclass=ABCMeta):
    context_src: dict

    """レイヤ共通で利用するメソッドやメンバが定義されたContextLoaderのベースクラス"""
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
    
    def get_context(self, model: Type["BaseModel"]) -> Any:
        return model.parse_obj(self.context_src)

class StageContextLoader(ContextLoaderBase):
    """stageレイヤのContextオブジェクトを生成するクラス"""

    def __init__(self, default_context: dict, overwrite_context: dict, stage: str):
        context_src = ContextLoaderBase._overwrite_context(
            default_context,
            overwrite_context.get(stage, {})
        )
        context_src["stage"] = stage
        self.context_src = context_src

class LineContextLoader(ContextLoaderBase):
    """lineレイヤのContextオブジェクトを生成するクラス"""

    def __init__(self, default_context: dict, overwrite_context: dict, stage: str, line: str):
        stage_context_src = ContextLoaderBase._overwrite_context(
            default_context,
            overwrite_context.get(stage, {})
        )
        context_src = ContextLoaderBase._overwrite_context(
            stage_context_src,
            overwrite_context.get(stage, {}).get(line, {})
        )
        context_src["stage"] = stage
        context_src["line"] = line
        self.context_src = context_src
