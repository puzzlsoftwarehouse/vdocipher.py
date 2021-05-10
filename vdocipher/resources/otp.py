import json
from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json, config

from vdocipher.resources.annotate import Annotate
from vdocipher.resources.ip_geo_rule import IPGeoRule
from vdocipher.resources.license_rules import LicenseRules
from vdocipher.resources.request import post
from vdocipher.resources.routes.base import VIDEOS


@dataclass_json
@dataclass
class OTP:
    otp: str = None
    playback_info: str = field(metadata=config(field_name="playbackInfo"), default=None)
    annotations: List[Annotate] = None
    license_rules: LicenseRules = None
    ip_geo_rules: List[IPGeoRule] = None
    white_list_href: str = None

    def create(self, video_id: str, ttl: int = 300) -> 'OTP':
        data = {'ttl': ttl}

        if self.annotations:
            data['annotate'] = json.dumps([annotate.to_dict() for annotate in self.annotations])

        if self.license_rules:
            data['licenseRules'] = json.dumps(self.license_rules.to_dict())

        if self.white_list_href:
            data['whitelisthref'] = json.dumps(self.white_list_href)

        if self.ip_geo_rules:
            data['ipGeoRules'] = json.dumps([ip_rule.to_dict() for ip_rule in self.ip_geo_rules])

        response = post(url=f'{VIDEOS}/{video_id}/otp', data=json.dumps(data))

        return self.from_dict(response.json())
