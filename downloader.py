from mutagen import id3
from pytube import YouTube, Playlist
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import requests
import shutil
import re
import string
import os

   
class song:
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


# on_progress_callback takes 4 parameters.
def progress_function(self,stream, chunk,file_handle, bytes_remaining):
    size = stream.filesize
    p = 0
    while p <= 100:
        progress = p
        print(str(p)+'%')
        p = percent(bytes_remaining, size)


def percent(tem, total):
        perc = (float(tem) / float(total)) * float(100)
        return perc

def get_download_path():
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def sanitize_name(name):
 s = str(name)
 s = s.replace("$", "S")
 valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
 sanitized = ''.join(c for c in s if c in valid_chars)
 return sanitized.replace(' ', '_')

def download_audio(song, path_to_folder):
 name = sanitize_name(str(song.title)) + ".mp4"
 print("Downloading " + name + "...", end="")
 YouTube(song.video_url).streams.get_by_itag('140').download(output_path=path_to_folder, filename=name)
 print(" [COMPLETED]")
 

def convert_audio(song, mp4name, mp3name):
        cmd = "ffmpeg -i {} -vn {}".format(mp4name, mp3name)
        os.system(cmd)
        
        
def add_details(song, filename):
  current = EasyID3(filename=filename)
  current["artist"] = u"" + song.artist
  current["album"] = u"" + PLAYLIST_NAME
  current.save()

  response = requests.get(song.image_url, stream=True)
  with open("img.jpg", 'wb') as output:
    shutil.copyfileobj(response.raw, output)
  del response

  current = ID3(filename=filename)
  with open('img.jpg', 'rb') as albumart:  
    current['APIC'] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3 , 
            desc=u'Cover',
            data=albumart.read()
    )
    current.save()

def cleanup():
        cmd = "cd {} && rm *.mp4".format(PATH_TO_FOLDER)
        os.system(cmd)

if (__name__ == "__main__"):
 DOWNLOAD_PATH = get_download_path()
 playlistURL = input("Enter your playlist's URL: ")
 playlist = Playlist(url=playlistURL)
 playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
 songs = []
 PLAYLIST_NAME = sanitize_name(str(playlist.title))
 PATH_TO_FOLDER = DOWNLOAD_PATH + "/" + PLAYLIST_NAME

 print(PATH_TO_FOLDER)
 for video in playlist.videos:
  songTitle = sanitize_name(video.title)
  songs.append(song(video_url=video.watch_url, title=songTitle, image_url=video.thumbnail_url, artist=video.author))
  
 for song in songs:
  download_audio(song, PATH_TO_FOLDER)
 
 for song in songs:
  name = str(sanitize_name(song.title))
  mp4 = str(PATH_TO_FOLDER + "/" + str(name) + ".mp4")
  mp3 = str(PATH_TO_FOLDER + "/" + str(name) + ".mp3")
  convert_audio(song, mp4, mp3)

 cleanup()
 
 for song in songs:
  print("ADDING DETAILS")
  name = str(sanitize_name(str(song.title))) + ".mp3"
  path = PATH_TO_FOLDER + "/" + name
  add_details(song, path)

