from typing import List

import pytest

import vdocipher
from vdocipher import Video


class TestVideo:

    def test_video_get_list(self, vdocipher, video):
        videos = vdocipher.Video().get_list()

        assert len(videos) > 0
        [isinstance(video_obj, Video) for video_obj in videos[:5]]

    def test_video_upload_credentials(self, vdocipher):
        upload_credentials = vdocipher.UploadCredentials().create(title='test')

        assert upload_credentials.video_id
        assert upload_credentials.client_payload.uploadLink
        assert upload_credentials.client_payload.x_amz_signature
        assert upload_credentials.client_payload.x_amz_algorithm
        assert upload_credentials.client_payload.x_amz_date
        assert upload_credentials.client_payload.x_amz_credential
        assert upload_credentials.client_payload.key
        assert upload_credentials.client_payload.policy

        vdocipher.Video(id=upload_credentials.video_id).delete()

    def test_video_upload(self, video: Video):

        assert isinstance(video, Video)
        assert video.id

    def test_video_delete(self, video):
        response = video.delete()

        assert response.status_code == 200
        assert "Successfully deleted 1 videos" in response.json()['message']

    def test_video_get(self, video):
        video_obj = video.get_video()

        assert video_obj.id == video.id
        assert video_obj.title == video.title
        assert video_obj.status == 'PRE-Upload'

