import csv
import json
from dataclasses import dataclass
from typing import List
from datetime import date
from vdocipher.resources.request import post
from vdocipher.resources.routes.base import BASE_URL


@dataclass
class VideoBandwidth:
    data: str = None
    video_id: str = None
    video_title: str = None
    bandwidth: str = None

    @staticmethod
    def _from_csv(content: str) -> List['VideoBandwidth']:
        csv_content = csv.reader(content.split('\r\n'))

        return [VideoBandwidth(*row) for row in csv_content]

    def get(self, date_filter: date):
        data = json.dumps({
            "date": date_filter.strftime('%Y-%m-%d')
        })

        response = post(url=f'{BASE_URL}/account/video-usage', data=data)

        return self._from_csv(response.text)

    def get_by_video_id(self, video_id: str, date_filter: date) -> 'VideoBandwidth':
        bandwith_list = self.get(date_filter)

        return next((_ for _ in bandwith_list if _.video_id == video_id), None)
