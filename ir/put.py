#! /user/bin/evn python
# -*- coding:utf8 -*-

"""

@Author   : Lau James
@Contact  : LauJames2017@whu.edu.cn
@Project  : BERT-TKMRC
@File     : put.py
@Time     : 18-10-17 下午4:54
@Software : PyCharm
@Copyright: "Copyright (c) 2018 Lau James. All Rights Reserved"
"""

from ir.config import Config
from elasticsearch import helpers

import pandas as pd
import json
import jieba
import time

excel_path = '../data/wait_paragraphs.xlsx'


def excel_data_convert(path):
    """
    input: excel files:	问题	段落 all of them are string type
    transform the raw data to json type including title and paragraph
    :return:
    """
    dataframe = pd.read_excel(path,
                              sheet_name='Sheet2',
                              usecols=[0, 1, 2, 3],
                              header=0,
                              dtype={'id': str, 'paragraph_content': str, 'name': str, 'title': str})
    # 删除任何包含nan的行数据
    dataframe.dropna()

    paragraphs = {}
    paragraph_count = 0
    for key, data in dataframe.iterrows():  # 返回key, rows.values()
        if not (data['id'].strip() or data['paragraph_content'].strip() or data['name'].strip() or data['title'].strip()):
            print('Wrong line. Find missing value filed')
            continue
        raw_paragraph = data['paragraph_content'].strip().replace('\n', '')
        segmented_paragraph = ' '.join(token for token in jieba.cut(raw_paragraph))
        raw_title = data['title'].strip().replace('\n', '')
        segmented_tilte = ' '.join(token for token in jieba.cut(raw_title))
        raw_name = data['name'].strip().replace('\n', '')
        segmented_name = ' '.join(token for token in jieba.cut(raw_name))
        pid = data['id']
        paragraphs[pid] = {'title': segmented_tilte, 'paragraph': segmented_paragraph, 'name': segmented_name}
        paragraph_count += 1

    print(str(paragraph_count) + 'paragraphs items loaded!')

    return paragraphs


def put2es(paras, bulk_size, config):
    """
    Put paras into es
    :param paras:
    :param bulk_size:
    :param config:
    :return:
    """
    count = 1
    actions = []
    for para_id, para in paras.items():
        action = {
            "_index": config.index_name,
            "_type": config.doc_type,
            "_id": para_id,
            "_source": para
        }

        actions.append(action)
        count += 1

        if len(actions) % bulk_size == 0:
            helpers.bulk(config.es, actions)
            print("bulk index:" + str(count))
            actions = []

    if len(actions) > 0:
        helpers.bulk(config.es, actions)
        print("bulk index:" + str(count))


if __name__ == '__main__':

    config = Config()

    # excel2json()
    paras = excel_data_convert(excel_path)
    # for idx, title_para in title_paras.items():
    #     print(idx)
    #     print(title_para)

    put2es(paras, bulk_size=10000, config=config)
