
from vdocipher import Video
from vdocipher.tests.conftest import BaseTest


class TestVideo(BaseTest):

    def test_video_get_list(self, video: Video):
        videos = self.vdocipher.Video().get_list()

        assert len(videos) > 0

        [isinstance(video_obj, Video) for video_obj in videos[:5]]

    def test_video_get_list_pagination(self):
        video_list = [self.vdocipher.Video(title=f'test {i}').upload('resources/test_file.mp4') for i in range(3)]

        number_page = 1
        page_limit = 2

        videos = self.vdocipher.Video().get_list(number_page, page_limit)

        assert len(videos) <= page_limit
        [isinstance(video_obj, Video) for video_obj in videos]

        [video.delete() for video in video_list]

    def test_video_get_all_video(self, video: Video):
        videos = self.vdocipher.Video().get_all()

        assert len(videos) > 0

        [isinstance(video_obj, Video) for video_obj in videos[:5]]

    def test_video_upload_credentials(self):
        upload_credentials = self.vdocipher.UploadCredentials().create(title='test')

        assert upload_credentials.video_id
        assert upload_credentials.client_payload.uploadLink
        assert upload_credentials.client_payload.x_amz_signature
        assert upload_credentials.client_payload.x_amz_algorithm
        assert upload_credentials.client_payload.x_amz_date
        assert upload_credentials.client_payload.x_amz_credential
        assert upload_credentials.client_payload.key
        assert upload_credentials.client_payload.policy

        self.vdocipher.Video(id=upload_credentials.video_id).delete()

    def test_video_upload(self, video: Video):
        assert isinstance(video, Video)
        assert video.id

    def test_video_delete(self, video):
        response = video.delete()

        assert response.status_code == 200
        assert "Successfully deleted 1 videos" in response.json()['message']

    def test_video_get(self, video):
        video_obj = video.get()

        assert video_obj.id == video.id
        assert video_obj.title == video.title
        assert video_obj.status == 'PRE-Upload' or video_obj.status == 'Queued'

    def test_video_get_query(self):
        videos_to_test = [self.vdocipher.Video(title=f'test-query-{i}').upload('resources/test_file.mp4') for i in
                          range(3)]

        query_test = 'test-query-2'
        videos_list = self.vdocipher.Video().query(query=query_test)

        assert len(videos_list) > 0

        [isinstance(video_obj, Video) for video_obj in videos_list]

        assert videos_list[0].title == query_test

        [video.delete() for video in videos_to_test]

    def test_add_tag_to_video(self, video: Video):
        tags = ['Ubuntu', 'Blender']
        response = video.add_tags(tags=tags)

        assert response['message'] == 'Done'

        assert set(video.get().tags).intersection(set(tags))

    def test_add_tag_to_video_ids(self):
        video_list_id = [self.vdocipher.Video(title=f'test-tag-{i}').upload('resources/test_file.mp4').id for i in
                         range(2)]
        tag_list = ['Modelagem 3D', 'Games', 'Unity', 'Godot']

        response = self.vdocipher.Video().add_tag_to_video_ids(videos_id=video_list_id, tags=tag_list)

        assert response['message'] == 'Done'

        for video_id in video_list_id:
            tag_video = self.vdocipher.Video(id=video_id).get().tags
            tag_video_set = set(tag_video)
            tag_list_set = set(tag_list)

            assert tag_video_set.intersection(tag_list_set)

        [Video(id=video_id).delete() for video_id in video_list_id]

    def test_get_videos_by_tag(self):
        video_list_id = [self.vdocipher.Video(title=f'test-tag-{i}').upload('resources/test_file.mp4').id for i in
                         range(2)]
        video_list_id_not_tag = [self.vdocipher.Video(title=f'test-tag-{i}').upload('resources/test_file.mp4').id for i
                                 in
                                 range(2)]
        tag_list = ['Modelagem 3D', 'Games', 'Unity']

        self.vdocipher.Video().add_tag_to_video_ids(videos_id=video_list_id, tags=tag_list)

        videos_list = self.vdocipher.Video().search_by_tag(tag='Unity')

        assert len(videos_list) > 0

        assert len(videos_list) == len(video_list_id)

        [isinstance(video_obj, Video) for video_obj in videos_list]

        assert videos_list[0].id in video_list_id

        [Video(id=video_id).delete() for video_id in video_list_id]
        [Video(id=video_id).delete() for video_id in video_list_id_not_tag]

    def test_get_all_tags(self):
        video_list_id = [self.vdocipher.Video(title=f'test-tag-{i}').upload('resources/test_file.mp4').id for i in
                         range(2)]
        tag_list = ['Modelagem 3D', 'Games', 'Unity']

        self.vdocipher.Video().add_tag_to_video_ids(videos_id=video_list_id, tags=tag_list)

        response = self.vdocipher.Video().list_tags()

        assert len(response) > 0

        [Video(id=video_id).delete() for video_id in video_list_id]

    def test_repalce_tag(self, video):
        video_obj = video

        video_tag = ['BLender', '3d', 'Photoshop']
        video_obj.add_tags(video_tag)

        video_tag_replace = ['Capture-one', 'Zbrush']
        response = video_obj.replace_tag(video_tag_replace)

        assert response['message'] == 'Done'

        assert set(video_obj.get().tags).intersection(set(video_tag_replace))

    def test_replace_tag_to_video_ids(self):
        video_list_id = [self.vdocipher.Video(title=f'test-tag-{i}').upload('resources/test_file.mp4').id for i in
                         range(2)]
        tag_list = ['Modelagem 3D', 'Games', 'Unity']

        tag_list_replace = ['Python', 'Rust', 'TypeScript']

        self.vdocipher.Video().add_tag_to_video_ids(videos_id=video_list_id, tags=tag_list)

        response = self.vdocipher.Video().replace_tag_to_video_ids(videos_id=video_list_id, tags=tag_list_replace)

        assert response['message'] == 'Done'

        for video_id in video_list_id:
            tag_video = self.vdocipher.Video(id=video_id).get().tags
            tag_video_set = set(tag_video)
            tag_list_replace_set = set(tag_list_replace)

            assert tag_video_set.intersection(tag_list_replace_set)

        [Video(id=video_id).delete() for video_id in video_list_id]

    def test_delete_tags(self, video):
        video_obj = video

        video_obj.add_tags(['BLender', '3d', 'Photoshop'])

        response = video_obj.delete_tag()

        assert response['message'] == 'Done'
        assert not (set(video_obj.get().tags).intersection(set([])))

    def test_delete_tag_to_video_ids(self):
        video_list_id = [self.vdocipher.Video(title=f'test-tag-{i}').upload('resources/test_file.mp4').id for i in
                         range(2)]
        tag_list = ['Modelagem 3D', 'Games', 'Unity']

        self.vdocipher.Video().add_tag_to_video_ids(videos_id=video_list_id, tags=tag_list)

        response = self.vdocipher.Video().delete_tag_to_video_ids(videos_id=video_list_id)

        assert response['message'] == 'Done'

        for video_id in video_list_id:
            tag_video = self.vdocipher.Video(id=video_id).get().tags
            tag_video_set = set(tag_video)

            assert not tag_video_set.intersection([])

        [Video(id=video_id).delete() for video_id in video_list_id]

    def test_create_otp(self, video):
        otp = video.create_otp()

        assert otp.otp
        assert otp.playback_info
