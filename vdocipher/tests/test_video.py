from typing import List

import pytest

import vdocipher
from vdocipher import Video


class TestVideo:

    def test_video_get_list(self, vdocipher, ):
        videos = vdocipher.Video().get_list()

        assert len(videos) > 0
        [isinstance(video_obj, Video) for video_obj in videos[:5]]
        print(videos)

    def test_video_get_list_pagination(self, vdocipher):
        video_list = [vdocipher.Video(title=f'test {i}').upload('resources/test_file.mp4') for i in range(3)]

        number_page = 1
        page_limit = 2

        videos = vdocipher.Video().get_list(number_page, page_limit)

        assert len(videos) <= page_limit
        [isinstance(video_obj, Video) for video_obj in videos]

        [video.delete() for video in video_list]

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
        video_obj = video.get()

        assert video_obj.id == video.id
        assert video_obj.title == video.title
        assert video_obj.status == 'PRE-Upload'

    def test_video_get_query(self, vdocipher):
        video = vdocipher.Video(title='test-query').upload('resources/test_file.mp4')

        videos_list = video.query(query='test-query')

        assert len(videos_list) > 0

        [isinstance(video_obj, Video) for video_obj in videos_list]

        assert videos_list[0].title == video.title

        video.delete()

    def test_create_otp(self, video):
        otp = video.create_otp()

        assert otp.otp
        assert otp.playback_info

    def test_list_delete(self, vdocipher):
        id_example = 'e831dc3da9774eb984ff398942904489'

        video_list_id = vdocipher.Video().get_list()

        for i in video_list_id:
            if i.id != id_example:
                i.delete()
