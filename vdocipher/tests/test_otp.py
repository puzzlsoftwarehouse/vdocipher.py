from vdocipher.resources.annotate import Annotate
from vdocipher.resources.otp import OTP


class TestOTP:

    def test_create_otp(self, vdocipher, video):
        otp = vdocipher.OTP().create(video_id=video.id)

        assert isinstance(otp, OTP)

    def test_create_otp_with_annotate(self, vdocipher, video):
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
        annotate_list = [annotate for _ in range(4)]
        otp = vdocipher.OTP(annotations=annotate_list).create(video_id=video.id)

        assert isinstance(otp, OTP)
        assert otp.otp
        assert otp.playback_info
