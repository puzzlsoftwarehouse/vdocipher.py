from vdocipher import Video
from vdocipher.resources.video import Subtitle
from vdocipher.tests.conftest import BaseTest


class TestVideoSubtitle(BaseTest):

    def test_video_upload_subtitle(self, video: Video):
        with open('resources/test_caption.vtt', 'rb') as subtitle_file:
            subtitle: Subtitle = video.upload_subtitle(subtitle_file, language='en')

            assert subtitle.id
            assert subtitle.size
            assert subtitle.time
            assert subtitle.lang

    def test_video_delete_subtitle(self):
        video_obj = self.vdocipher.Video(title='test').upload('resources/test_file.mp4')

        with open('resources/test_caption.vtt', 'rb') as subtitle_file:
            subtitle: Subtitle = video_obj.upload_subtitle(subtitle_file, language='en')

            assert subtitle.id
            assert subtitle.size
            assert subtitle.time
            assert subtitle.lang

        response = video_obj.delete_subtitle(subtitle.id)
        assert response['message'] == 'Deleted'

        video_obj.delete()
