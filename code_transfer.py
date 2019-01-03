#! /user/bin/evn python
# -*- coding:utf8 -*-

"""

@Author   : Lau James
@Contact  : LauJames2017@whu.edu.cn
@Project  : bert 
@File     : code_transfer.py
@Time     : 18-12-26 下午1:11
@Software : PyCharm
@Copyright: "Copyright (c) 2018 Lau James. All Rights Reserved"
"""

import json

unicode_file = './result/predictions.json'
utf8_file = './result/utf8.predictions.json'


def encode_transfer(input_file, output_file):
    """
    Transform the unicode encoding file to utf-8 for Chinese.
    :param input_file: Unicode encoding
    :param output_file:  UTF-8 encoding
    :return:
    """
    lines = []
    with open(input_file, 'r') as fin:
        for line in fin.readlines():
            lines.append(line.replace(' ', ''))
    one_line = ''.join(lines)
    json_predictions = json.loads(one_line)
    with open(output_file, 'w', encoding='utf-8') as fout:
        fout.write(json.dumps(json_predictions, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    encode_transfer(unicode_file, utf8_file)
