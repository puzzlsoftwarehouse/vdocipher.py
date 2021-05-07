import json
from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json, config

from vdocipher.resources.annotate import Annotate
from vdocipher.resources.request import post
from vdocipher.resources.routes.base import VIDEOS


@dataclass_json
@dataclass
class OTP:
    otp: str = None
    playback_info: str = field(metadata=config(field_name="playbackInfo"), default=None)
    annotations: List[Annotate] = None

    def create(self, video_id: str, ttl: int = 300) -> 'OTP':
        data = {'ttl': ttl}
        if self.annotations:
            data['annotate'] = [annotate.to_dict() for annotate in self.annotations]

        response = post(url=f'{VIDEOS}/{video_id}/otp', data=json.dumps(data))

        return self.from_dict(response.json())
