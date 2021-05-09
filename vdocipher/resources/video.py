from datetime import datetime
from typing import List, IO

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from requests_toolbelt import MultipartEncoder

from vdocipher.resources.otp import OTP
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
class Subtitle:
    id: str
    time: str
    size: str
    lang: str


@dataclass_json
@dataclass
class Video:
    id: str = None
    title: str = None
    description: str = None
    length: int = None
    status: str = None
    public: int = None

    def get_list(self, page: int = 1, limit: int = 10) -> List['Video']:
        response = get(url=f'{VIDEOS}?page={page}&limit={limit}')

        videos = [self.from_dict(video) for video in response.json()['rows']]

        return videos

    def get(self) -> 'Video':
        response = get(url=f'{VIDEOS}/{self.id}')

        return self.from_dict(response.json())

    def query(self, query: str = None) -> List['Video']:
        querystring = {"q": query}

        response = get(url=VIDEOS, params=querystring)
        videos = [self.from_dict(video) for video in response.json()['rows']]

        return videos

    def create_upload_credentials(self) -> UploadCredentials:
        response = UploadCredentials().create(self.title)

        return response

    def create_otp(self, ttl: int = 300) -> OTP:
        otp = OTP().create(self.id, ttl)

        return otp

    def upload(self, file: IO) -> 'Video':

        credentials = self.create_upload_credentials()

        data = MultipartEncoder(fields=[
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
            data=data,
            headers={'Content-Type': data.content_type},
            use_api_secret=False
        )

        if response.status_code == 201:
            self.id = credentials.video_id

            return self

    def upload_subtitle(self,
                        subtitle_file: IO,
                        language: str = 'en') -> Subtitle:

        querystring = {'language': language}

        data = MultipartEncoder(fields=[
            (f'file', (subtitle_file.name, subtitle_file, 'text/vtt'))
        ])

        response = post(url=f'{VIDEOS}/{self.id}/files',
                        params=querystring,
                        headers={'Content-Type': data.content_type},
                        data=data)

        return Subtitle.from_dict(response.json())

    def delete(self):
        querystring = {'videos': f"{self.id}"}

        response = delete(
            url=VIDEOS,
            params=querystring
        )
        return response
