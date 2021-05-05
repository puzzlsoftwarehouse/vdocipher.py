import json
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config

from vdocipher.resources.request import post
from vdocipher.resources.routes.base import VIDEOS


@dataclass_json
@dataclass
class OTP:
    otp: str = None
    playback_info: str = field(metadata=config(field_name="playbackInfo"), default=None)

    def create(self, video_id: str, ttl: int = 300) -> 'OTP':
        data = {'ttl': ttl}

        response = post(url=f'{VIDEOS}/{video_id}/otp', data=json.dumps(data))

        return self.from_dict(response.json())
