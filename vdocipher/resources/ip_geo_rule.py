from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class IPGeoRule:
    actions: bool = None
    ip_set: List = field(metadata=config(field_name="ipSet"), default=None)
    country_set: List = field(metadata=config(field_name="countrySet"), default=None)



