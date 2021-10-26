from pytube import YouTube, Playlist
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import requests
import shutil
import re
import string
import os

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



def get_download_path():
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def get_path_to_folder(name):
        download_path = get_download_path()
        return download_path + "/" + name


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
        
        
def add_details(song, filename, playlistname):
  current = EasyID3(filename=filename)
  current["artist"] = u"" + song.artist
  current["album"] = u"" + playlistname
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

def cleanup(name):
        cmd = "cd {} && rm *.mp4".format(get_path_to_folder(name=name))
        os.system(cmd)

def main():
 #define the download path
 DOWNLOAD_PATH = get_download_path()

 #get playlist url from user – then use pytube to find the playlist
 playlist_url = input("Enter your playlist's URL: ")
 playlist = Playlist(url=playlist_url)
 playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
 
 #create a list to store the songs in 
 songs = []

 #sanitize the name of the playlist 
 PLAYLIST_NAME = sanitize_name(str(playlist.title))

 # create a "song" object for each video in the playlist
 for video in playlist.videos:
  song_title = sanitize_name(video.title)
  the_song = Song(video_url=video.watch_url, title=song_title, image_url=video.thumbnail_url, artist=video.author)
  songs.append(the_song)
  
 #download the songs
 for song in songs:
  download_audio(song, get_path_to_folder(PLAYLIST_NAME))
 
 #convert the songs to mp3
 for song in songs:
  name = str(sanitize_name(song.title))
  mp4 = str(get_path_to_folder(PLAYLIST_NAME) + "/" + str(name) + ".mp4")
  mp3 = str(get_path_to_folder(PLAYLIST_NAME) + "/" + str(name) + ".mp3")
  convert_audio(song, mp4, mp3)

 #remove the mp4 files
 cleanup(PLAYLIST_NAME)
 

 #add metadata details to the songs 
 for song in songs:
  print("ADDING DETAILS")
  name = str(sanitize_name(str(song.title))) + ".mp3"
  path = get_path_to_folder(PLAYLIST_NAME) + "/" + name
  add_details(song, path, PLAYLIST_NAME)


if(__name__ == "__main__"):
        main()