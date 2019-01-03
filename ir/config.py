#! /user/bin/evn python
# -*- coding:utf8 -*-

"""

@Author   : Lau James
@Contact  : LauJames2017@whu.edu.cn
@Project  : BERT-TKMRC
@File     : config.py
@Time     : 18-12-3 下午12:13
@Software : PyCharm
@Copyright: "Copyright (c) 2018 Lau James. All Rights Reserved"
"""

from elasticsearch import Elasticsearch


class Config(object):
    def __init__(self):
        print("config...")
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.index_name = "tkmrc2"
        self.doc_type = "paragraph"

        file_path = '../data/阅读理解条款.xlsx'
        self.doc_path = file_path


def main():
    Config()


if __name__ == '__main__':
    main()
