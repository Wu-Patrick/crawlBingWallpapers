# Get lots of beautiful wallpapers

> 让你拥有大量的漂亮壁纸（使用Python多线程爬取所有的[Bing](https://cn.bing.com/)[壁纸](https://bing.ioliu.cn/)，目前1600+张）。

![bingwallpapers](/images/bingwallpapers.jpg)

----



# 1. 介绍

总为找到漂亮且高清的壁纸而发愁，而每日更新的[Bing搜索](https://cn.bing.com/)的主页背景又让人心旷神怡，所以写了个python脚本爬取下来所有的美图(感谢大佬[收集壁纸的站点](https://bing.ioliu.cn/))，然后用作自己电脑桌面壁纸的自动更换。

整个过程很简单，分为三步（以下以windows为例）。



# 2. 不想操作，拿来就用

如果你不想使用脚本下载，下载编译好的 [crawlBingWallpapers.exe](https://github.com/Wu-Patrick/first/releases/download/v1.0/crawlBingWallpapers.exe) ，双击运行，就可以在分分钟内获得1600+张漂亮的壁纸。

如此，就不用往下看了……



---



# 3. 使用脚本下载

## 1. 准备工作

**1. 安装Python**

访问[Python官网](https://www.python.org/downloads/)，根据自己的操作系统下载安装包，双击安装。

<img src="/images/PythonInstall.jpg" width = 600></img>

**2. 安装依赖包**

打开命令提示符：(<kbd>Win</kbd>+<kbd>R</kbd>) &rArr; 输入“cmd” &rArr; <kbd>Enter</kbd> ，然后输入

~~~cmd
pip install requests
pip install fake_useragent
pip install bs4
~~~



## 2. Coding

新建个脚本文件**crawlBingWallpapers.py**，输入下面的代码。

~~~python
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from concurrent.futures import ThreadPoolExecutor,wait

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
    pool = ThreadPoolExecutor(12)

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
    print('Existing pictures will be skipped.')
    pictureNum = input('How many pages to download? 12 per page. (default: 160): ') or '160'
    num = eval(pictureNum)
    
    downloadMain(num)
    
    print('Over!')
~~~

然后运行该脚本，等待下载完就可以了。脚本中使用了12个线程，速度相当快！

所有的壁纸会保存在脚本所在目录下的**BingWallpapers**文件夹中。



## 3. 享用

下载完成后就可以用起来了。

桌面右键 &rArr; 个性化 &rArr; 背景 &rArr; 幻灯片放映 &rArr; 选择**BingWallpapers**文件夹

![background](/images/background.jpg)

搞定，祝你用的开心~

