import pyperclip as pyperclip
import requests
import json

headers = {
    'Cookie': 'kw_token=19X12B0TSK4',
    'Host': 'www.kuwo.cn',
    'Referer': 'https://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'csrf': '19X12B0TSK4'
}


def main(artist, soname, page=1):
    url = 'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=20'
    thisUrl = url.format(artist, page)

    midUrl = 'https://www.kuwo.cn/api/v1/www/music/playUrl?mid={mid}&type=convert_url'
    response = requests.get(thisUrl, headers=headers)
    jsonData = json.loads(response.text)
    data = jsonData['data']
    list = data['list']
    total = data['total']
    runtimes = 0
    for ele in list:
        rid = ele['rid']
        name = ele['name']
        # print(f'ele:{ele},')
        # print(f'songname:{songname},name:{name}')
        # print(f'name:{name.find(songname)}')
        if name.find(soname) > -1:
            album = ele['album']
            artist = ele['artist']
            midUrl = midUrl.format(mid=rid)
            print(f'专辑:{album},歌曲名字:{name},歌手:{artist}')
            response = requests.get(midUrl)
            data = json.loads(response.text)
            musicUrl = data['data']['url']
            print(f'音乐下载链接已经复制到剪切板了,请前往浏览器打开:{musicUrl}')
            pyperclip.copy(musicUrl)
            return
        runtimes += 1

    if runtimes == 20:
        page += 1
        main(artist, soname, page=page)


artist = input("请输入歌手名字:")
soname = input("请输入需要下载的歌曲:")
main(str(artist), str(soname))
