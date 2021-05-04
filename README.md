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

# get a list of videos
videos = vdocipher.Video().get_list()

# upload a new video
new_video = vdocipher.Video(title='title').upload('file')

# get a video
video = vdocipher.Video(id=1).get()

# delete
vdocipher.Video(id=1).delete()
```

Installing dev requirements
--------

```shell script 
$ pip install vdocipher.py[dev]
```   

    
    
    