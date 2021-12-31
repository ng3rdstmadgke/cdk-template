from dataclasses import dataclass
from cdk_template.context.context_loader_base import LineContextBase

class SampleLineContext(LineContextBase):
    sample_line_param: str