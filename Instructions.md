# 索引需要进行阅读理解的条款(存放在： ./data/阅读理解条款.xlsx)
- cd ir
- python3 index.py
- 若有新的数据，可以利用  puy.py  将新数据放入es

# 根据产品问题(这里选择的是  康护一生注释问题.xlsx), 检索适合的段落, 构造问题、段落等阅读理解json数据
- cd data
- python3 para4question.py
## 得到  wait_answer.json

# 修改 run_dureader.py 中predict文件路径, 然后执行：
- python3 run_dureader.py --do_predict=True

# result文件夹下的  predictions.json  即为预测结果