from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Annotate:
    annotation_type: str = field(metadata=config(field_name="type"), default='text')
    text: str = None
    alpha: str = None
    color: str = None
    x: str = None
    y: str = None
    size: str = None
    interval: str = None
    skip: str = None
