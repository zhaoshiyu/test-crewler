# -*- coding: utf-8 -*-

import re
import requests
import time
from collections import deque
from lxml import etree
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient("127.0.0.1", 27017)

db = client.news

def crawler(main_url):
    # 待访问的集合queue
    queue = deque()
    # 访问过的集合visited
    visited = set()
    queue.append(main_url)
    # 已经抓取的页面数count
    count = 0
    # 当待访问页面不为空时，一直循环
    while queue:  #and count <= 500000
        # time.sleep(1)
        url = queue.popleft() # 队首元素出队
        visited |= {url} # 标记为已访问
        print('已经抓取: ' + str(count) + ' / ' + str(len(queue)) + '   正在抓取 :\t' + url)
        #print('已经抓取: ' + str(count) + '   正在抓取 <---  ' + url)
        # 返回url对应的页面内容
        # 用try...处理异常
        try:
            request = requests.get(url)
            data = request.text
            news = news_parse_by_xpath(data)
            if news['title'] != '':
                news['cate'] = '体育'
                news['url'] = url
                db.QQ_News.save(news)
                count = count + 1
        except Exception:
            continue
        
        # 存储页面
        # file_ope.file_ope.file_save(data)

        # 提取影片信息
        # try:
        #     info = get_info(data,url)
        #     if info['name'] is not None and info['name'] != '':
        #         save_book_information(info)
        #         count = count + 1
        #     author = get_author(data)
        #     save_author(author)
        # except Exception:
        #     print('解析或保存错误：' + url)

        # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
        # http://sports.qq.com/a/20170318/029808.htm
        link_regex = re.compile('href="(http://sports\.qq\.com/a/\d+/\d+\.htm)"')
        for link in link_regex.findall(data):
            if link not in visited and link not in queue:
                queue.append(link)
                print('加入队列 --->  ' + link)

def news_parse_by_xpath(data):
    html = etree.HTML(data)
    title_xpath = '//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1//text()'
    second_cate_xpath = '//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[1]/a//text()'
    source_xpath = '//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[2]/a//text()'
    pub_time_xpath = '//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[3]//text()'
    content_xpath = '//*[@id="Cnt-Main-Article-QQ"]/p//text()'
    title = get_news_info_by_xpath(html, title_xpath)
    second_cate = get_news_info_by_xpath(html, second_cate_xpath)
    source = get_news_info_by_xpath(html, source_xpath)
    pub_time = get_news_info_by_xpath(html, pub_time_xpath)
    # content = get_news_info_by_xpath(html, content_xpath)
    title = re.sub('[\r\n\r]+', '', title)
    return {'title': title, 'secondCate': second_cate, 'source': source, 'pubTime': pub_time}
    

def get_news_info_by_xpath(html, xpath):
    contents = html.xpath(xpath)
    if len(contents) > 0:
        return re.sub('\n+', '\n', '\n'.join(contents))
    return ''

if __name__ == '__main__':
    # 入口页面
    url_start = "http://sports.qq.com/"
    crawler(url_start)
    
