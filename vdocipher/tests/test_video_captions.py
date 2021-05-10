from vdocipher import Video
from vdocipher.resources.video import Subtitle
from vdocipher.tests.conftest import BaseTest


class TestVideoSubtitle(BaseTest):

    def test_video_upload(self, video: Video):

        with open('resources/test_caption.vtt', 'rb') as subtitle_file:
            subtitle: Subtitle = video.upload_subtitle(subtitle_file, language='en')

            assert subtitle.id
            assert subtitle.size
            assert subtitle.time
            assert subtitle.lang

