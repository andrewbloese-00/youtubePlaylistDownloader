import os
import re
from tkinter import Tk;
from pytube import YouTube
from pytube import Playlist
import pytube
import subprocess
import string
    

def get_download_path():
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def progress_function(self,stream, chunk,file_handle, bytes_remaining):

    size = stream.filesize
    p = 0
    while p <= 100:
        progress = p
        print (str(p)+'%')
        p = percent(bytes_remaining, size)

def percent(self, tem, total):
        perc = (float(tem) / float(total)) * float(100)
        return perc

def splitVids(list,length):
    vids = []
    for i in range(length):
        vids.append(list[i])
    print("Spliting into " + str(len(vids)))
    return vids

def format_filename(s):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename


if(__name__ == "__main__"):

    DOWNLOAD_PATH = str(get_download_path())
    playlistURL = input("Enter the URL to the playlist: ")
    playlist = Playlist(url=playlistURL)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    if(len(playlist.video_urls) < 1): 
        print("Cannot Download an Empty Playlist. Try another URL!")
    
    else:
      qualified_name = str(format_filename(playlist.title))
      path_to_folder = os.path.join(DOWNLOAD_PATH, qualified_name)
      subprocess.call(['mkdir', path_to_folder])
      
   

      files = []
      for video in playlist.videos:
          _filename = format_filename(video.title)+'.mp4'
          files.append(_filename)
          print('Downloading ' + _filename + "...", end="")
          audioStream = video.streams.get_by_itag('140')
          audioStream.download(output_path=path_to_folder, filename=_filename)
          print("[COMPLETED]") 
      for _filename in files:
           print('Converting ' + _filename + "...", end="")
           mp4 = path_to_folder +"/" + _filename 
           mp3 = path_to_folder +"/" + str(_filename).replace('.mp4', '.mp3')
        
           cmd = "ffmpeg -i {} -vn {}".format(mp4, mp3)
           os.system(cmd)
           print(" [COMPLETED]")
            
        
    print("download complete! " + str(len(playlist.video_urls)) + " files downloaded.")


