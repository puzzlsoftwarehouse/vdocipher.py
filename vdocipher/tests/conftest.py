from datetime import datetime

import pytest as pytest
import os
import vdocipher as vdocipher_lib
from vdocipher import Video


class BaseTest:

    vdocipher = vdocipher_lib
    vdocipher.authenticate(os.getenv('VDOCIPHER_API_SECRET', default=''))

    @pytest.yield_fixture
    def video(self) -> Video:

        with open('resources/test_file.mp4', 'rb') as file:
            video_name = f'test - {datetime.now()}'

            video_obj = self.vdocipher.Video(title=video_name).upload(file)

            assert isinstance(video_obj, Video)
            assert video_obj.id

            yield video_obj

            video_obj.delete()

