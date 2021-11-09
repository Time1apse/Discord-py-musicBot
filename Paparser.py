import requests
from bs4 import BeautifulSoup as bs
import re
from pytube import Playlist
import pafy

def music(name: str):
    name = name.replace(' ', '+')
    if name == "":
       return None
    url = f'https://www.youtube.com/results?search_query={name}'
    print(url)
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    soup = str(soup)
    result = re.search(r'"videoId":"(\w+)"', soup).group(0)
    result = result.replace('"', "")
    result = result.replace("videoId:", "")
    print(result)
    return(str(result))

def playlist(url: str, x=0):
   playlist = Playlist(url)
<<<<<<< HEAD
   playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
   ids = ""
   for url in playlist.video_urls:
      id = url
      ids += id+" "
   ids = ids.split( )
   print(ids)
   return(ids)
   
=======
   if(x==1):
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        ids = ""
        for url in playlist.video_urls:
            id = url
            ids += id+" "
        ids = ids.split( )
        return(ids)
>>>>>>> 34aa7979e1021849b4164e7f2beee565c3404d20

if __name__ == "__main__":
   playlist("https://www.youtube.com/playlist?list=PLADmR6fAuPwfZK6Su-O4p3Qyfm-dliwW1", 1)
   
