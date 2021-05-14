import json
from typing import List, IO
import pathlib
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from requests_toolbelt import MultipartEncoder

from vdocipher.resources.ip_geo_rule import IPGeoRule
from vdocipher.resources.otp import OTP
from vdocipher.resources.request import get, put, post, delete
from vdocipher.resources.routes.base import VIDEOS, BASE_URL


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
class VideoFiles:
    is_downloadable: bool = field(metadata=config(field_name="isDownloadable"), default=None)
    is_deletable: bool = field(metadata=config(field_name="isDeletable"), default=None)
    id: int = None
    name: str = None
    size: int = None
    time: str = None
    enabled: int = None
    format: str = None
    video_codec: str = None
    audio_codec: str = None
    height: int = None
    width: int = None
    bitrate: str = None
    encryption_type: str = None
    lang: str = None


@dataclass_json
@dataclass
class Video:
    id: str = None
    title: str = None
    description: str = None
    length: int = None
    status: str = None
    public: int = None
    upload_time: int = None
    white_list_href: str = field(metadata=config(field_name="whitelisthref"), default=None)
    ip_geo_rules: List[IPGeoRule] = field(metadata=config(field_name="ipGeoRules"), default=None)
    posters: List = None
    poster: str = None
    total_sinze_bytes: int = field(metadata=config(field_name="totalSinzeBytes"), default=None)
    tags: List = None

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

    def get_all(self):
        page = 1
        limit = 10
        videos: List['Video'] = []
        while True:
            videos_page = self.get_list(page=page, limit=limit)
            videos += videos_page
            page += 1

            if len(videos_page) < limit:
                return videos

    def add_tags(self, tags: List = None):
        payload = {
            "videos": [self.id],
            "tags": tags
        }
        response = post(url=f'{VIDEOS}/tags', data=json.dumps(payload))

        return response.json()

    def add_tag_to_video_ids(self, videos_id: List = None, tags: List = None):
        payload = {
            "videos": videos_id,
            "tags": tags
        }

        response = post(url=f'{VIDEOS}/tags', data=json.dumps(payload))

        return response.json()

    def search_by_tag(self, tag: str = None) -> List['Video']:
        querystring = {"tags": tag}
        response = get(url=VIDEOS, params=querystring)

        videos = [self.from_dict(video) for video in response.json()['rows']]

        return videos

    def list_tags(self):
        response = get(url=f'{VIDEOS}/tags')

        return response.json()['rows']

    def replace_tag(self, tags: List = None):
        payload = {
            "videos": [self.id],
            "tags": tags
        }

        response = put(url=f'{VIDEOS}/tags', data=json.dumps(payload))

        return response.json()

    def replace_tag_to_video_ids(self, videos_id: List = None, tags: List = None):
        payload = {
            "videos": videos_id,
            "tags": tags
        }

        response = put(url=f'{VIDEOS}/tags', data=json.dumps(payload))

        return response.json()

    def delete_tag(self, tag: str):

        tags_video = self.get().tags
        tags_video.remove(tag)

        payload = {
            "videos": [self.id],
            "tags": tags_video
        }

        response = put(url=f'{VIDEOS}/tags', data=json.dumps(payload))

        return response.json()

    def delete_all_tags(self):
        payload = {
            "videos": [self.id],
            "tags": []
        }

        response = put(url=f'{VIDEOS}/tags', data=json.dumps(payload))

        return response.json()

    def delete_all_tag_to_video_ids(self, videos_id: List = None):
        payload = {
            "videos": videos_id,
            "tags": []
        }

        response = put(url=f'{VIDEOS}/tags', data=json.dumps(payload))

        return response.json()

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

    def upload_by_url(self, url: str = None) -> 'Video':

        payload = json.dumps({"url": url})

        response = put(url=f'{VIDEOS}/importUrl', data=payload)

        return self.from_dict(response.json())

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

    def delete_subtitle(self, file_id: str = None):
        response = delete(url=f'{VIDEOS}/{self.id}/files/{file_id}')

        return response.json()

    def delete(self):
        querystring = {'videos': f"{self.id}"}

        response = delete(
            url=VIDEOS,
            params=querystring
        )
        return response

    def list_all_files(self) -> List[VideoFiles]:

        response = get(url=f'{VIDEOS}/{self.id}/files/')
        files = [VideoFiles.from_dict(files) for files in response.json()]
        return files

    def upload_poster(self, file: IO):
        extension = pathlib.Path(file.name).suffix.replace('.', '')
        if not extension in ['png', 'jpeg']:
            raise Exception(f'Invalid image extension={extension}')

        data = MultipartEncoder(fields=[
            ('file', ('filename', file, f'image/{extension}'))
        ])
        response = post(
            url=f'{VIDEOS}/{self.id}/files',
            data=data,
            headers={'Content-Type': data.content_type},
        )

        return response.json()

    def get_url_posters(self) -> List:
        response = get(url=f'{BASE_URL}/meta/{self.id}')

        return response.json()['posters']

    def _delete_all(self):
        list_videos = self.get_all()

        [video.delete() for video in list_videos]

        return 'All videos deleted'
