from vdocipher.resources.annotate import Annotate
from vdocipher.resources.ip_geo_rule import IPGeoRule
from vdocipher.resources.license_rules import LicenseRules
from vdocipher.resources.otp import OTP
from vdocipher.tests.conftest import BaseTest


class TestOTP(BaseTest):

    def test_create_otp(self, video):
        otp = self.vdocipher.OTP().create(video_id=video.id)

        assert isinstance(otp, OTP)

    def test_create_otp_with_annotate(self, video):
        annotate = Annotate(
            annotation_type='rtext',
            text='name',
            alpha='0.60',
            x='10',
            y='10',
            color='0xFF0000',
            size='15',
            interval='5000',
            skip='200'
        )
        annotate_list = [annotate]
        otp = self.vdocipher.OTP(annotations=annotate_list).create(video_id=video.id)

        assert isinstance(otp, OTP)
        assert otp.otp
        assert otp.playback_info

    def test_create_otp_with_license_rules(self, video):

        duration = 15 * 24 * 3600
        rule = LicenseRules(
            can_persist=True,
            rental_duration=duration
        )
        otp = self.vdocipher.OTP(license_rules=rule).create(video_id=video.id)

        assert isinstance(otp, OTP)
        assert otp.otp
        assert otp.playback_info

    def test_create_opt_with_white_list_href(self, video):
        otp = self.vdocipher.OTP(white_list_href="vdocipher.com").create(video_id=video.id)

        assert isinstance(otp, OTP)
        assert otp.otp
        assert otp.playback_info

    def test_create_opt_with_ip_geo_rules(self, video):
        geo_rules = IPGeoRule(
            actions=True,
            ip_set=[],
            country_set=["IN", "GB"]
        )
        geo_rules_list = [geo_rules]
        otp = self.vdocipher.OTP(ip_geo_rules=geo_rules_list).create(video_id=video.id)

        assert isinstance(otp, OTP)
        assert otp.otp
        assert otp.playback_info
