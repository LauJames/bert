#! /user/bin/evn python
# -*- coding:utf8 -*-

"""

@Author   : Lau James
@Contact  : LauJames2017@whu.edu.cn
@Project  : BERT-TKMRC
@File     : para4question.py
@Time     : 18-12-27 下午3:37
@Software : PyCharm
@Copyright: "Copyright (c) 2018 Lau James. All Rights Reserved"
"""


import pandas as pd
import json
import jieba
import uuid
from ir.config import Config
from ir.search import Search
import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curdir))

config = Config()
search = Search()

question_path = './康护一生注释问题.xlsx'
output_path = 'wait_answer.json'


def cut2tokens(text):
    """
    use jieba.cut do word segmentation, and return one line
    :param text:
    :return: tokens
    """
    cuted = []
    for cut_line in jieba.cut(text):
        if cut_line not in ['', '\n', ' ', '\t']:
            cuted.append(cut_line)
            # print(cut_line)
    # print(cuted)
    return cuted


def get_questions(q_path):
    """
    Read questions waiting for find answer from excel file
    :param q_path: str
    :return: questions: List(str)
    """
    dataframe = pd.read_excel(q_path,
                              sheet_name='Sheet1',
                              usecols=[0],
                              header=0,
                              dtype={'问题': str})
    dataframe.dropna()

    questions = []

    for key, data in dataframe.iterrows():
        questions.append(data['问题'])

    return questions


def search_para4question(questions, output_path):
    """
    Searching related paragraph for question using elasticsearch
    :param questions: List(str)
    :return:
    """
    # questions = ['保险事故如何鉴定的？', '请问这款产品有犹豫期吗？', '犹豫期多少天？']
    data_list = []
    for question in questions:
        result = search.search_by_question(question, 1, config)
        for data in result:
            pqID = str(uuid.uuid1())
            title = data[0]
            para = data[1]
            name = data[2]

            paras_and_seg_json = [{"paragraphs": [para.replace(' ', '').replace('\n', '').replace('\t', '')],
                                   "segmented_paragraphs": [cut2tokens(para.replace(' ', '').replace('\n', '').replace('\t', ''))],
                                   "title": title.replace(' ', '').replace('\n', '').replace('\t', ''),
                                   "segmented_title": cut2tokens(title.replace(' ', '').replace('\n', '').replace('\t', '')),
                                   "name": name.replace(' ', '').replace('\n', '').replace('\t', ''),
                                   "is_selected": True,
                                   "most_related_para": 0}]
            print(paras_and_seg_json)

            item_json = {"question": question,
                         "question_id": pqID,
                         "segmented_question": cut2tokens(question.replace(' ', '').replace('\n', '').replace('\t', '')),
                         "documents": paras_and_seg_json,
                         "answer_docs": [0]}
            data_list.append(item_json)

    with open(output_path, 'w', encoding='utf-8') as fout:
        for json_line in data_list:
            data_json = json.dumps(json_line, ensure_ascii=False)
            fout.write(str(data_json))
            fout.write('\n')


if __name__ == '__main__':
    questions = get_questions(question_path)
    search_para4question(questions, output_path)
