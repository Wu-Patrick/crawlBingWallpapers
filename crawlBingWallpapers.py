import os
os.system('pip install bs4')
os.system('pip install fake_useragent')
os.system('pip install requests')

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from concurrent.futures import ThreadPoolExecutor,wait

# savePath = r'D:\Media\Picture\BingWallpapers'
savePath = r'BingWallpapers'
if not os.path.exists(savePath):
    os.mkdir(savePath)

def download(img_url):
    print(img_url)

    imgFile = savePath + '/' + img_url.rsplit('/', maxsplit=1)[-1].split('?')[0]
    if os.path.exists(imgFile):
        return

    img_ret = requests.get(img_url, headers={'User-Agent': UserAgent().random})

    with open(imgFile, 'wb+')as f:
        f.write(img_ret.content)

def downloadMain(num):
    pool = ThreadPoolExecutor(8)

    all_task = []
    for i in range(num):
        print('Crawling images on page %s' % (i + 1))
        ret = requests.get('https://bing.ioliu.cn/?p=%d' % (i + 1), headers={'User-Agent': UserAgent().random})

        bs = BeautifulSoup(ret.text, 'html.parser')
        img_list = bs.find_all(name='img')

        for img in img_list:
            img_url = img.get('src').replace('640x480', '1920x1080')

            all_task.append(pool.submit(download, img_url))
    wait(all_task)
                
if __name__ == '__main__':
    print('Crawl Bing Wallpapers')    
    print('website: wuzhipeng.cn')
    print('    by Zhipeng Wu    ')
    print('---------------------')
    print()
    print('Existing pictures will be skipped.')
    pictureNum = input('How many pages to download? 12 per page. (default: 160): ') or '160'
    num = eval(pictureNum)
    downloadMain(num)

    print()
    print('Over!')
    input("Press <enter> to quit")