# -*- coding: utf-8 -*-

import re
import pymongo
import pandas as pd

client = pymongo.MongoClient("127.0.0.1", 27017)

db = client.news
collection = db.QQ_News
data = []
max_length = 0
len_dict = {}
for d in collection.find({}):
    data.append([d['cate'], d['title']])
    sent_len = len(d['title'])
    if sent_len > max_length:
        max_length = sent_len
    if sent_len in len_dict:
        len_dict[sent_len] = len_dict[sent_len] + 1
    else:
        len_dict[sent_len] = 1

print(len_dict)
print(max_length)
# df = pd.DataFrame(data, columns=['label', 'text'])
# df.to_csv('./train.csv', encoding='utf-8')