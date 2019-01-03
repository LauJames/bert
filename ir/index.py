#! /user/bin/evn python
# -*- coding:utf8 -*-

"""

@Author   : Lau James
@Contact  : LauJames2017@whu.edu.cn
@Project  : BERT-TKMRC
@File     : index.py
@Time     : 18-12-3 下午12:22
@Software : PyCharm
@Copyright: "Copyright (c) 2018 Lau James. All Rights Reserved"
"""

from ir.config import Config
from elasticsearch import helpers
import pandas as pd
import jieba


class Index(object):
    def __init__(self):
        print("Indexing ...")

    @staticmethod
    def data_convert(file_path="../data/阅读理解条款.xlsx"):
        print("convert raw csv file into single doc")
        dataframe = pd.read_excel(file_path,
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

    @staticmethod
    def create_index(config):
        print("creating %s index ..." % config.index_name)
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "similarity": {
                    "LM": {
                        "type": "LMJelinekMercer",
                        "lambda": 0.4
                    }
                }
            },
            "mapping": {
                config.index_name: {
                    "properties": {
                        "title": {
                            "type": "text",
                            "term_vector": "with_positions_offsets_payloads",
                            # 支持参数yes（term存储），
                            # with_positions（term + 位置）,
                            # with_offsets（term + 偏移量），
                            # with_positions_offsets(term + 位置 + 偏移量)
                            # 对快速高亮fast vector highlighter能提升性能，但开启又会加大索引体积，不适合大数据量用
                            "store": True,
                            "analyzer": "standard",
                            "similarity": "LM"
                        },
                        "paragraph": {
                            "type": "text",
                            "term_vector": "with_positions_offsets_payloads",
                            "store": True,
                            "analyzer": "standard",
                            "similarity": "LM"
                        },
                        "name": {
                            "type": "text",
                            "term_vector": "with_positions_offsets_payloads",
                            "store": True,
                            "analyzer": "standard",
                            "similarity": "LM"
                        }
                    }
                }
            }
        }

        config.es.indices.delete(index=config.index_name, ignore=[400, 404])
        res = config.es.indices.create(index=config.index_name, body=request_body)
        print(res)
        print("Indices are created successfully")

    @staticmethod
    def bulk_index(questions, bulk_size, config):
        print("Bulk index for question")
        count = 1
        actions = []
        for question_count, question in questions.items():
            action = {
                "_index": config.index_name,
                "_type": config.doc_type,
                "_id": question_count,
                "_source": question
            }
            actions.append(action)
            count += 1

            if len(actions) % bulk_size == 0:
                helpers.bulk(config.es, actions)
                print("Bulk index: " + str(count))
                actions = []

        if len(actions) > 0:
            helpers.bulk(config.es, actions)
            print("Bulk index: " + str(count))


def main():
    config = Config()
    index = Index()
    questions = index.data_convert(config.doc_path)
    index.create_index(config)
    index.bulk_index(questions, bulk_size=10000, config=config)


if __name__ == '__main__':
    main()
