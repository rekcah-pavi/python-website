from flask import *
import os

song = None


try:
 from youtube_dl import YoutubeDL
except:
 os.system('python3 -m pip install --user youtube_dl')
 from youtube_dl import YoutubeDL


try:
 from youtubesearchpython import Search
except:
 os.system('python3 -m pip install --user youtube-search-python')
 from youtubesearchpython import Search

app = Flask(__name__)





@app.route('/')
def home():
    return '''
    <center>
    <h2>Enter Any Song name or youtube url to download it</h2>
    <h4>
    <form action="/get" method="post">
	<input type="text" name="song_name">
    <p></p>
    <input type="submit" name="get_audio" value="Get Audio">
    <input type="submit" name="get_video" value="Get Video">
    <p>A Simple Python Website for Download Songs</p>
    <p>How to make This Website  Video guide : Rkpavi youtube</p>
    </h4>
    </center>
'''



@app.route('/get', methods=['post'])
def track():
    if request.method == 'POST':
     try:
        song = str(request.form['song_name'])
        if not song:
           return "Please Enter Song Name"
        if 'get_audio' in request.form:
          ty = "mp3"
          opts = {'format':'bestaudio','addmetadata':True,'key':'FFmpegMetadata','writethumbnail':True,'prefer_ffmpeg':True,'geo_bypass':True,'nocheckcertificate':True,'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}],'outtmpl':'%(id)s.mp3','quiet':True,'logtostderr':False}
        elif 'get_video' in request.form:
          ty = "mp4"
          opts = {'format':'best','addmetadata':True,'key':'FFmpegMetadata','writethumbnail':True,'prefer_ffmpeg':True,'geo_bypass':True,'nocheckcertificate':True,'postprocessors': [{'key': 'FFmpegVideoConvertor','preferedformat': 'mp4'}],'outtmpl':'%(id)s.mp4','logtostderr':False,'quiet':True}
        else:
            return "Select audio/video Type"
        test = os.listdir()
        if len(test) > 20:
         for item in test:
          if item.endswith(".mp3") or item.endswith(".webp") or item.endswith(".jpg") or item.endswith(".png") or item.endswith(".mp4"):
             os.remove(item)
        if "http" in song:
           url = song
        else:
          songa = Search(f'{song} song', limit = 1)
          songa = songa.result()['result']
          if not songa:
            return "Error Failed to find this song"
          url = songa[0]['link']
        try:
         with YoutubeDL(opts) as rip:
           rip_data = rip.extract_info(url)
        except Exception as e:
           return str(e)
        if ty == "mp3":
           ty2 = f"{rip_data['id']}.mp3"
        else:
           ty2 = f"{rip_data['id']}"
        if os.path.isfile(f"{ty2}.webp"):
            im = f"/static/{ty2}.webp"
        elif os.path.isfile(f"{ty2}.jpg"):
            im = f"/static/{ty2}.jpg"
        else:
            im = f"/static/{ty2}.png"
        return f'''
        <center>
        <img src="{im}" alt="Song" width="600" height="200">
        <p> </p>
        <h2>{rip_data['title']}</h2>
        <p> </p>
        <h3>
        <video width="320" height="240" controls>
        <source src="/static/{rip_data['id']}.{ty}" type="video/ogg">
        Your browser does not support the video tag.
        </video>
        <p></p>
        <a href="/static/{rip_data['id']}.{ty}" download="{rip_data['title']}.{ty}">Click Here To Download</a>
        </audio.
        </h3>
        <center>
        '''
     except Exception as e:
         return str(e)

@app.route('/find')
def help():
    if not 'song_name' in request.form:
           return "Please Enter Song Name"
    return "ok"

