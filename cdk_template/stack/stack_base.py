from abc import abstractmethod
from typing import Dict, Optional, List
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from cdk_template.context.context_loader_base import ContextBase, LineContextBase, StageContextBase

class StackBase(core.Stack):
    """レイヤ共通で利用するメソッドやメンバが定義されたStackのベースクラス

    core.Stack: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stack.html
    """

    STACK_NAME: str
    context: ContextBase
    vpc_ref: Optional[ec2.IVpc] = None
    subnet_refs: Dict[str, ec2.ISubnet] = {}
    role_refs: Dict[str, iam.IRole] = {}

    def __init__(self, scope: core.Construct, context: ContextBase):
        self.context = context
        super().__init__(
            scope,
            self._get_resource_name(self.STACK_NAME),
            env=core.Environment( # スタックがデプロイされるaccountとregionを指定する
                account=self.context.aws_account_id,
                region=self.context.aws_region
            ),
            termination_protection=context.termination_protection,
        )
        self._add_default_tag()
        self._resources()

    # AWS Resourceについてをデプロイするメソッド
    @abstractmethod
    def _resources(self):
        raise NotImplementedError

    def _get_resource_name(self, name: str) -> str:
        """CFnのスタック名やリソース名を生成するメソッド。ケバブケース"""
        return self.context.get_resource_name(name)
        
    def _get_resource_id(self, name: str) -> str:
        """CFnのリソースidを生成するメソッド。パスカルケース"""
        return self.context.get_resource_id(name)

    def _add_default_tag(self):
        for k, v in self.context.tags.items():
            core.Tags.of(self).add(k, v)

    def _get_vpc(self) -> ec2.IVpc:
        """cdk.jsonのvpc_idに指定されているVPCの参照を取得"""
        if self.vpc_ref is None:
            self.vpc_ref = ec2.Vpc.from_lookup(
                self, self._get_resource_id("defaultVpcRef"),
                vpc_id=self.context.vpc_id,
            )
        return self.vpc_ref

    def _get_subnet(self, subnet_id: str) -> ec2.ISubnet:
        """指定されたsubnet_idからsubnetの参照を取得"""
        if subnet_id not in self.subnet_refs:
            self.subnet_refs[subnet_id] = ec2.Subnet.from_subnet_id(
                self, self._get_resource_id(f"{subnet_id}Ref"),
                subnet_id=subnet_id,
            )
        return self.subnet_refs[subnet_id]

    def _get_subnet_selection(self, subnet_ids: List[str]) -> ec2.SubnetSelection:
        subnets = [self._get_subnet(subnet_id) for subnet_id in subnet_ids]
        return ec2.SubnetSelection(subnets=subnets)

    def _get_role(self, role_name: str) -> iam.IRole:
        """指定されたIAM Role名からRoleの参照を取得"""
        if role_name not in self.role_refs:
            self.role_refs[role_name] = iam.Role.from_role_arn(
                self, self._get_resource_id(f"{role_name}Ref"),
                role_arn=f"arn:aws:iam::{self.context.aws_account_id}:user/{role_name}",
            )
        return self.role_refs[role_name]

class StageStackBase(StackBase):
    """stageレイヤのStackが継承するべきクラス"""
    context: StageContextBase

class LineStackBase(StackBase):
    """lineレイヤのStackが継承するべきクラス"""
    context: LineContextBase