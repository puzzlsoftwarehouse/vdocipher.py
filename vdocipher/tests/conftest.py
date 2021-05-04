from datetime import datetime

import pytest as pytest
import os
import vdocipher as vdocipher_lib
from vdocipher import Video


@pytest.fixture
def vdocipher():

    vdocipher_lib.authenticate(os.getenv('VDOCIPHER_API_SECRET'))

    return vdocipher_lib


@pytest.yield_fixture
def video(vdocipher) -> Video:

    video_name = f'test - {datetime.now()}'

    video_obj = vdocipher.Video(title=video_name).upload('resources/test_file.mp4')

    yield video_obj

    video_obj.delete()

