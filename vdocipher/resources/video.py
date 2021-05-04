from typing import List

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from requests_toolbelt import MultipartEncoder

from vdocipher.resources.request import get, put, post, delete
from vdocipher.resources.routes.base import VIDEOS


@dataclass_json
@dataclass
class ClientPayload:
    policy: str = None
    key: str = None

    x_amz_signature: str = field(metadata=config(field_name="x-amz-signature"),
                                 default=None)

    x_amz_algorithm: str = field(metadata=config(field_name="x-amz-algorithm"),
                                 default=None)

    x_amz_date: str = field(metadata=config(field_name="x-amz-date"),
                            default=None)

    x_amz_credential: str = field(metadata=config(field_name="x-amz-credential"),
                                  default=None)

    uploadLink: str = None


@dataclass_json
@dataclass
class UploadCredentials:
    video_id: str = field(metadata=config(field_name="videoId"), default=None)
    client_payload: ClientPayload = field(metadata=config(field_name="clientPayload"), default=None)

    def create(self, title: str) -> 'UploadCredentials':
        response = put(url=VIDEOS, params={'title': title})

        return self.from_dict(response.json())


@dataclass_json
@dataclass
class Video:
    id: str = None
    title: str = None
    description: str = None
    length: int = None
    status: str = None
    public: int = None

    def get_list(self) -> List['Video']:
        response = get(url=VIDEOS)

        videos = [self.from_dict(video) for video in response.json()['rows']]

        return videos

    def get_video(self) -> 'Video':
        response = get(url=f'{VIDEOS}/{self.id}')

        return self.from_dict(response.json())

    def get_upload_credentials(self) -> UploadCredentials:
        response = UploadCredentials().create(self.title)

        return response

    def upload(self, file) -> 'Video':
        file = open(file, 'rb')

        credentials = self.get_upload_credentials()

        m = MultipartEncoder(fields=[
            ('x-amz-credential', credentials.client_payload.x_amz_credential),
            ('x-amz-algorithm', credentials.client_payload.x_amz_algorithm),
            ('x-amz-date', credentials.client_payload.x_amz_date),
            ('x-amz-signature', credentials.client_payload.x_amz_signature),
            ('key', credentials.client_payload.key),
            ('policy', credentials.client_payload.policy),
            ('success_action_status', '201'),
            ('success_action_redirect', ''),
            ('file', ('filename', file, 'text/plain'))
        ])

        response = post(
            url=credentials.client_payload.uploadLink,
            data=m,
            headers={'Content-Type': m.content_type}
        )

        if response.status_code == 201:
            self.id = credentials.video_id

            return self

    def delete(self):
        querystring = {'videos': f"{self.id}"}

        response = delete(
            url=VIDEOS,
            params=querystring
        )
        return response
