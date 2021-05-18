# from vdocipher import VideoBandwidth, Video
# from vdocipher.tests.conftest import BaseTest
# from datetime import date
#
#
# class TestVideoBandwidth(BaseTest):
#
#     def test_get(self):
#         date_filter = date(year=2021, month=5, day=13)
#         bandwidth = self.vdocipher.VideoBandwidth()
#         list_video_bandwidth = bandwidth.get(date_filter=date_filter)
#
#         assert len(list_video_bandwidth) > 0
#
#         [isinstance(_, VideoBandwidth) for _ in list_video_bandwidth]
#
#     def test_get_video_id(self):
#         date_filter = date(year=2021, month=5, day=13)
#         video_id = 'bf9ae268cb5601e4cf5d1640c44f92d7'
#         bandwidth = self.vdocipher.VideoBandwidth()
#         video_bandwidth = bandwidth.get_by_video_id(video_id=video_id, date_filter=date_filter)
#
#         assert isinstance(video_bandwidth, VideoBandwidth)
#
#         assert video_bandwidth.video_id == video_id
#
#     def test_get_video(self):
#         date_filter = date(year=2021, month=5, day=13)
#         bandwidth = self.vdocipher.VideoBandwidth()
#         video_bandwidth = bandwidth.get(date_filter)[0]
#         video = video_bandwidth.video
#
#         assert isinstance(video, Video)
#         assert video.id == video_bandwidth.video_id
#         assert video.bandwidth == video_bandwidth.bandwidth
