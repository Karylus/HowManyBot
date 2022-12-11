import random
import youtube_dl

def save_id(id):
    f = open("./data/ids.txt", 'a')
    f.write(str(id) + "\n")
    f.close()

def get_quote():
    with open('./data/sigmaQuotes.txt', 'r', encoding='utf8') as f:
        read = f.read()
        array = read.split('\n')
        quote = random.choice(array)

    return quote

def get_video():
    try:
        with open('./data/sigmaVideo.txt', 'r', encoding='utf8') as f:
            read = f.read()
            array = read.split('\n')
            video_url = random.choice(array)
        
        print("The video url is: " + video_url)

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'tempVideo.%(ext)s'
        }
    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    
    except:
        get_video()