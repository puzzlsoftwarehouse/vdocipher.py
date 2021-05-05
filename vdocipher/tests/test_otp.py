from vdocipher.resources.otp import OTP


class TestOTP:

    def test_video_get_list(self, vdocipher, video):

        otp = vdocipher.OTP().create(video_id=video.id)

        assert isinstance(otp, OTP)
