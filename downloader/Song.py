class Song:
 def __init__(self, video_url,  title, image_url, artist):
  self.video_url = video_url
  self.title = title
  self.image_url = image_url
  self.artist = artist
 
 def set_video_url(self, url):
  self.video_url = url
 def set_title(self, title):
  self.title = title
 def set_title(self, title):
  self.title = title
 
 def to_string(self):
  return str(self.title) + " | " + str(self.artist) 