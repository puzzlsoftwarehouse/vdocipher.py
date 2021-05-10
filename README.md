# vdocipher.py
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

# uploading a video
new_video = vdocipher.Video(title='title').upload('file')

# obtaining a video
video = vdocipher.Video(id=1).get()

# search for videos
videos = vdocipher.Video().query('some_text')

# removing a video
vdocipher.Video(id=1).delete()

# adding a video subtitle
subtitle = vdocipher.Video(id=1).upload_subtitle('file')

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
 
 geo_rules = IPGeoRules(
     actions=True,
     ip_set=["122.0.0.0/16", "49.323.23.56"],
     country_set=["IN", "GB"]
    )
 geo_rules_list = [geo_rules]
 otp = vdocipher.OTP(ip_geo_rules=geo_rules_list).create(videoid='your_video_id')
 
 

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



    
    
    