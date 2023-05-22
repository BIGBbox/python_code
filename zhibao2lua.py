import pandas as pd
import sys
import os

SHEET = "至宝"
# 读取Excel文件
abs_path = os.path.dirname(os.path.realpath(sys.executable))

path = os.path.join(abs_path, "excel/module.xlsx")
outfile_path = os.path.join(abs_path, "excel/cfg_zhibao.lua")

_excel = pd.read_excel(path, sheet_name=SHEET)

with open(outfile_path, encoding="UTF-8", mode="a") as ff:
    ff.write("local config = {")


def getNextKey(this_line, row):
    try:
        next_key = _excel.iloc[(this_line + 1), row]
    except:
        next_key = None
    return next_key


def getThisReward(this_line):
    temp_list = {'itemName': _excel.iloc[this_line, 5], 'itemNum': _excel.iloc[this_line, 6],
                 'needScore': _excel.iloc[this_line, 4]}
    return temp_list


def getCostStr(this_line):
    idx = _excel.iloc[this_line, 5]
    num = _excel.iloc[this_line, 6]
    temp = f'{{idx = {idx}, num = {num}}}'
    return temp


def getAttrLineStr(this_line, _type):
    '''
    获取某行的属性数据
    '''
    row = _type == 0 and 8 or 10
    idx = _excel.iloc[this_line, row]
    num = _excel.iloc[this_line, row + 1]
    temp = f'{{[1] = {idx}, [2] = {num}}}'
    return temp


rowList = [7, 5]


def getAttrStr(this_line, _type):
    next_key = None
    _str = ""
    model = 0
    if SHEET == "转生":
        model = 1
    row = rowList[model]
    try:
        while pd.isna(next_key):
            next_key = getNextKey(this_line, row)
            _str = _str + getAttrLineStr(this_line, _type) + ",\n"
            this_line += 1
    except:
        pass
    return _str


def writeTitle(key, pos):
    with open(outfile_path, encoding="UTF-8", mode="a") as ff:
        ff.write(f'\n\t[{key}] = {{')
        ff.write(f'\n\t\tpos = {pos},')
        ff.write(f'\n\t\tinfo = {{')


def main_zhibao():
    for line, row in _excel.iterrows():

        key = row['key']
        pos = row['pos']
        this_idx = row['thisIdx']
        level = row['level']
        nexteqidx = row['nexteqidx']
        thishuxin = row['thishuxin']
        if isinstance(thishuxin, int):
            attr_str = getAttrStr(line, 0)
            next_attr_str = getAttrStr(line, 1)

        with open(outfile_path, encoding="UTF-8", mode="a") as ff:
            if isinstance(key, int):
                writeTitle(key, pos)

            needItem = getCostStr(line)
            next_key = getNextKey(line, 4)
            try:
                if pd.isna(next_key):
                    needItem = f'\t{needItem},\n\t\t{getCostStr(line + 1)}'
            except:
                pass

            if isinstance(this_idx, int):
                ff.write(f'\n\t["{this_idx}"] = {{\n'
                         f'\tlevel = "{level}",\n'
                         f'\tnexteqidx = "{nexteqidx}",\n'
                         f'\tcost = {{\n'
                         f'\t{needItem}\n'
                         f'\t}},\n'
                         f'\tthishuxin = {{\n'
                         f'{attr_str}'
                         f'\t}},\n'
                         f'\tnextshuxin = {{\n'
                         f'{next_attr_str}'
                         f'\t}},\n'
                         f'\t}},')
            next_key = getNextKey(line, 0)
            if isinstance(next_key, int) and pd.isna(this_idx):
                ff.write(f"\n\t}},\n")
                ff.write(f"\n\t}},\n")

    with open(outfile_path, encoding="UTF-8", mode="a") as ff:
        ff.write(f"\n\t}},\n")
        ff.write(f"\n\t}},\n")
        ff.write("\n}\nreturn config")


main_zhibao()
