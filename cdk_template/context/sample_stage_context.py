from dataclasses import dataclass
from cdk_template.context.context_loader_base import StageContextBase

class SampleStageContext(StageContextBase):
    sample_stage_param: str