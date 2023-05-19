import numpy as np
import pandas as pd

# 读取Excel文件
_task = pd.read_excel('./excel/勤能补拙.xlsx', sheet_name="task")  # 任务表
_topReward = pd.read_excel('./excel/勤能补拙.xlsx', sheet_name="topReward")  # 奖励表

# 查看数据
# print(df.head(5))

# 获取"df" 勤能补拙_task  勤能补拙_topReward
# sub_df = df.loc[:, "task"]
# print(sub_df.head())

# print(_task)
# print("------------")
# print(_topReward.keys())
# id	startDay	endDay	key	needScore	itemName1	itemNum1


with open("./excel/outfile.lua", encoding="UTF-8", mode="a") as ff:
    ff.write("local tab = {}\ntab[\"topReward\"] = {")


def getNextKey(this_line):
    try:
        next_key = _topReward.iloc[(this_line + 1), 3]
    except:
        next_key = None

    return next_key


def getThisReward(this_line):
    temp_list = {'itemName': _topReward.iloc[this_line, 5], 'itemNum': _topReward.iloc[this_line, 6],
                 'needScore': _topReward.iloc[this_line, 4]}
    return temp_list


for line, row in _topReward.iterrows():
    # 处理一行数据
    topReward_id = row['topReward_id']
    startDay = row['startDay']
    endDay = row['endDay']
    key = int(row['key'])
    needScore = row['needScore']
    itemName1 = row['itemName1']
    itemNum1 = row['itemNum1']
    # print(
    #     f"ling:{line},topReward_id:{topReward_id},startDay:{startDay},endDay:{endDay},key:{key},needScore:{needScore}")
    with open("./excel/outfile.lua", encoding="UTF-8", mode="a") as ff:
        if not pd.isna(topReward_id):
            topReward_id = int(topReward_id)
            ff.write(f'\n\t\t[{topReward_id}]={{')

        if (not pd.isna(startDay)) and (not pd.isna(endDay)):
            ff.write(f"\nlimit={{ startDay = {startDay}, endDay = {endDay}}},")
            ff.write(f"\nrewardList = {{\n")

        if not pd.isna(key):
            ff.write(f'\n\t\t[{int(key)}]={{')
            _list = getThisReward(line)
            print(_list)
            ff.write(f'itemName="{_list["itemName"]}",itemNum={_list["itemNum"]},needScore={_list["needScore"]}')
            ff.write(f'}},')

        nextKey = getNextKey(line)
        if (pd.isna(nextKey)) or (int(nextKey) < key):
            ff.write(f"\n}},\n}},\n")

with open("./excel/outfile.lua", encoding="UTF-8", mode="a") as ff:
    ff.write("\n}\nreturn tab")
