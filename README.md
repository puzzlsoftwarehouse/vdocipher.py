# vdocipher.py  v0.5.1
Just a VdoCipher api wrapper for python.

Installing
--------

```shell script 
$ pip install vdocipher.py
```    
 
Using
--------

```python 
import vdocipher 

# First, we need to authenticate our api
vdocipher.authenticate('VDOCIPHER_API_SECRET')

# Examples:

# obtaining a list of videos
videos = vdocipher.Video().get_list()

# obtaining a list of all videos
videos = vdocipher.Video().get_all()

# uploading a video
new_video = vdocipher.Video(title='title').upload('file')

# uploading a video from HTTP(s)/FTP urls
new_video = .vdocipher.Video().upload_by_url('url_video')

# obtaining a video
video = vdocipher.Video(id=1).get()

# search for videos
videos = vdocipher.Video().query('some_text')

# removing a video
vdocipher.Video(id=1).delete()

# adding a video subtitle
subtitle = vdocipher.Video(id=1).upload_subtitle('file')

# removing a video subtitle
subtitle = vdocipher.Video(id=1).delete_subtitle(subtitle.id)

# adding a video tag
video = vdocipher.Video(id=1).add_tags(['Ubuntu', 'Blender'])

# adding tag in multiple videos
vidos_id = ['xdv23rosj940fj49jfd9ajl','29fjue98lsd934hfg9']

tag_list = ['Vdocipher', 'Games', 'Unity']

response = self.vdocipher.Video().add_tags(videos_id=videos_id, tags=tag_list)

# searching videos with tag
video_list = vdocipher.Video().search_tag(tag='Unity')

# obtaining all tags
tag_list = vdocipher.Video().list_tags()

# changing video tags
video = elf.vdocipher.Video().replace_tag(['Capture-one', 'Zbrush'])

# changing tag in multiple videos
vidos_id = ['xdv23rosj940fj49jfd9ajl','29fjue98lsd934hfg9']

tag_list_replace = ['Python', 'Rust', 'TypeScript']

replace = vdocipher.Video().replace_tag(videos_id=video_list_id, tags=tag_list_replace)

# deleting video tag
video = vdocipher.Video(id=1).delete_tag('JavaScript')

# deleting all video tags
video = vdocipher.Video(id=1).delete_all_tags()

# deleting a tags in multiple videos
vidos_id = ['xdv23rosj940fj49jfd9ajl','29fjue98lsd934hfg9']
vdocipher.Video().delete_tag_by_video_ids(videos_ids=vidos_id, tag='PythonJS')

# deleting all tags in multiple videos
video = vdocipher.Video().delete_tag_to_video_ids(videos_id=video_list_id)

# List all files of a video including captions and posters
video = vdocipher.Video().list_all_files()

# adding a video poster
poster = vdocipher.Video(id=1).upload_poster('file')

# obtaining post url
poster_url = vdocipher.Video(id=1).get_url_posters()

# obtaining OTP
otp = OTP().create(videoid='your_video_id')

# or
otp = Video(title='test video').upload('file').create_otp()

# opt with anotations
 annotate = Annotate(
            annotation_type='text' # Set type parameter as "rtext" for Dynamic watermark
            text='Name: {name}, email: {email}, IP: {ip}', # You can add user identifiable information
            alpha='0.60',
            x='10',
            y='10',
            color='0xFF0000',
            size='15',
            interval='5000',
            skip='200'
        )
 annotate_list = [annotate]
 otp = vdocipher.OTP(annotations=annotate_list).create(videoid='your_video_id')
 
 # generating OTP for offline use

 duration = 15 * 24 * 3600 
 rule = LicenseRules(
     can_persist=True,
     rental_duration=duration
 )
 otp = vdocipher.OTP(license_rules=rule).create(videoid='your_video_id')
 
 # opt with url whitelist
 
 url = "vdocipher.com"
 otp = vdocipher.OTP(white_list_href=url).create(videoid='your_video_id')
 
 # otp with IP and GeoRules
 
 geo_rules = IPGeoRule(
     actions=True,
     ip_set=["122.0.0.0/16", "49.323.23.56"],
     country_set=["IN", "GB"]
    )
 geo_rule_list = [geo_rule]
 otp = vdocipher.OTP(ip_geo_rule=geo_rules_list).create(videoid='your_video_id')
 
 # obtaining video bandwidth
 video_obj = vdocipher.Video(id='12rew').get()
 date_filter = date(year=2021, month=5, day=13)
 video_bandwidth = video_obj.bandwidth(date_filter)
 
 # obtaining all video bandwidth
 date_filter = date(year=2021, month=5, day=13)
 bandwidth = vdocipher.VideoBandwidth()
 list_video_bandwidth = bandwidth.get(date_filter=date_filter)
 
 # obtaining video from bandwidth
 bandwidth = vdocipher.VideoBandwidth()
 video_bandwidth = bandwidth.get(date_filter)[0]
 video = video_bandwidth.video
 

```

Installing dev requirements
--------

```shell script 
$ git clone https://github.com/puzzlsoftwarehouse/vdocipher.py.git
$ cd vdocipher.py
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .[dev]
```

build and publish

```shell script
$ python setup.py sdist bdist_wheel
$ twine upload -r pypi dist/*
```



    
    
    