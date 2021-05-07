from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class LicenseRules:
    can_persist: bool = field(metadata=config(field_name="canPersist"), default=None)
    rental_duration: float = field(metadata=config(field_name="rentalDuration"), default=None)
