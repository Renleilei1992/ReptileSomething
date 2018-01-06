# 抓取图虫站点的私房图

import urllib.request
import os
import ssl
import urllib.error
from bs4 import BeautifulSoup
import json

tags = urllib.request.quote("私房")  # 中文编码,可按需修改成自己喜欢的分类
base_url = "https://tuchong.com/rest/tags/" + tags + "/posts?"
max_page = 100
count = 20
pic_save_path = "output/Picture/TuChong/"


# 下载图片
def download_pic(url, dir_name):
    print(url)
    correct_url = url
    if not url.startswith('http'):
        correct_url = 'http://' + url
    req = urllib.request.Request(correct_url)
    try:
        resp = urllib.request.urlopen(req)
        pic = resp.read()
        pic_name = correct_url.split("/")[-1]
        with open(dir_name + pic_name, "wb+") as f:
            f.write(pic)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


# 获取Json
def fetch_json(url):
    resp = urllib.request.urlopen(url)
    data = str(resp.read().decode('utf-8'))
    data = json.loads(data)
    result_list = data['postList']
    for result in result_list:
        save_path = pic_save_path + result['post_id'] + '/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        pic_list = get_pic_url_list(result['url'])
        for pic in pic_list:
            download_pic(pic, save_path)


# 抓取图片列表
def get_pic_url_list(url):
    print("开始解析：" + url)
    url_list = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    div = soup.find('article', attrs={'class': 'post-content'})
    imgs = div.findAll('img')
    for img in imgs:
        url_list.append(img['src'])
    return url_list


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    for page in range(1, max_page + 1):
        url = base_url + 'page=' + str(page) + '&count=20&order=weekly'
        print("开始抓取第%d页 === %s" % (page, url))
        fetch_json(url)
