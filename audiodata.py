import requests
import os,time
from uuid import uuid4
from setting import MUSIC_PATH,IMAGE_PATH,MONGO_DB

# 路径
base_url ='http://audio.xmcdn.com/'
url = 'http://m.ximalaya.com/m-revision/page/track/queryTrackPage/%s'
content_list = ["/ertong/424529/7713660","/ertong/424529/7713675",
                "/ertong/424529/7713577","/ertong/424529/7713571",
                "/ertong/424529/7713546","/ertong/424529/7713539"]

#数据采集
def xiaopapa(clist):
    my_content=[]

    for i in clist:
        audio_id = i.rsplit('/',1)[-1]
        print(audio_id)
        res = requests.get(url%(audio_id))
        res_dict = res.json().get('data').get('trackDetailInfo').get('trackInfo')

        cover_url = base_url+res_dict.get('cover')  #图片路径
        audio_url = res_dict.get('playPath')   #音乐路径
        cover = requests.get(cover_url)
        audio = requests.get(audio_url)

        #采集数据图片、音乐保存到本地
        filename = uuid4()
        image = os.path.join(IMAGE_PATH,f'{filename}.jpg')
        music = os.path.join(MUSIC_PATH,f'{filename}.mp3')

        with open(music,'wb')as f:
            f.write(audio.content)

        with open(image,'wb')as cf:
            cf.write(cover.content)

        #需要把这些数据放入数据库中
        music_info = {
            'title':res_dict.get('title'),
            'intro':res_dict.get('intro'),
            'cover':f'{filename}.jpg',
            'audio':f'{filename}.mp3'
        }

        my_content.append(music_info)
        time.sleep(1)

    MONGO_DB.content.insert_many(my_content)


xiaopapa(content_list)