import csv
import json
from typing import List
from datetime import date
from dataclasses import dataclass

from vdocipher.resources.request import post
from vdocipher.resources.routes.base import BASE_URL


@dataclass
class VideoBandwidth:
    date_bandwidth: str = None
    video_id: str = None
    bandwidth: str = None

    @staticmethod
    def _from_csv(content: str) -> List['VideoBandwidth']:
        csv_content = csv.reader(content.split('\r\n'))
        list_bandwidth = [VideoBandwidth(*row[:2], row[3]) for row in csv_content]
        del list_bandwidth[0]
        return list_bandwidth

    def get(self, date_filter: date) -> List['VideoBandwidth']:
        data = json.dumps({
            "date": date_filter.strftime('%Y-%m-%d')
        })

        response = post(url=f'{BASE_URL}/account/video-usage', data=data)

        return self._from_csv(response.text)

    def get_by_video_id(self, video_id: str, date_filter: date) -> 'VideoBandwidth':
        bandwidth_list = self.get(date_filter)

        return next((_ for _ in bandwidth_list if _.video_id == video_id), None)

    @property
    def video(self):
        from vdocipher import Video
        video = Video(id=self.video_id).get()
        video.bandwidth = self.bandwidth
        return video
