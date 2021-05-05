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

# removing a video
vdocipher.Video(id=1).delete()

# obtaining OTP

otp = OTP().create(videoid='your_video_id')

# or
otp = Video(title='test video').upload('file').create_otp()
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



    
    
    