import pandas as pd
import sys
import os
SHEET = "转生"
# 读取Excel文件

abs_path = os.path.dirname(os.path.realpath(sys.executable))

path = os.path.join(abs_path,"excel/module.xlsx")
outfile_path = os.path.join(abs_path,"excel/cfg_rein.lua")

_excel = pd.read_excel(path, sheet_name=SHEET)

with open(outfile_path, encoding="UTF-8", mode="a") as ff:
    ff.write("local config = {")


def getNextKey(this_line, row):
    try:
        next_key = _excel.iloc[(this_line + 1), row]
    except:
        next_key = None
    return next_key


def getCostStr(this_line):
    idx = _excel.iloc[this_line, 2]
    num = _excel.iloc[this_line, 3]
    temp = f'{{idx = {idx}, num = {num}}}'
    return temp


def getAttrLineStr(this_line, _type):
    '''
    获取某行的属性数据
    '''
    row = 5
    idx = _excel.iloc[this_line, row]
    num = _excel.iloc[this_line, row + 1]
    temp = f'{{[1] = {idx}, [2] = {num}}}'
    return temp


rowList = [7, 4]


def getAttrStr(this_line, _type):
    next_key = None
    _str = ""
    model = 0
    if SHEET == "转生":
        model = 1
    row = rowList[model]
    print(row,SHEET)
    try:
        while pd.isna(next_key):
            next_key = getNextKey(this_line, row)
            _str = _str + getAttrLineStr(this_line, _type) + ",\n"
            this_line += 1
    except:
        pass
    return _str


def writeTitle(key, lt):
    with open(outfile_path, encoding="UTF-8", mode="a") as ff:
        ff.write(f'\n\t[{key}] = {{')
        # ff.write(f'\n\t[{lt}] = {{')
        # ff.write(f'\n\t\tinfo = {{')

def main_zhibao():
    for line, row in _excel.iterrows():

        key = row['key']
        lt = row['lt']
        thishuxin = row['thishuxin']
        if isinstance(thishuxin, int):
            attr_str = getAttrStr(line, 0)

        with open(outfile_path, encoding="UTF-8", mode="a") as ff:
            if isinstance(key, int):
                writeTitle(key, lt)

            needItem = getCostStr(line)
            next_key = getNextKey(line, 4)
            try:
                if pd.isna(next_key):
                    needItem = f'\t{needItem},\n\t\t{getCostStr(line + 1)}'
            except:
                pass

            if isinstance(lt, int):
                ff.write(f'\n\t[{lt}] = {{\n'
                         f'\tcost = {{\n'
                         f'\t{needItem}\n'
                         f'\t}},\n'
                         f'\tthishuxin = {{\n'
                         f'{attr_str}'
                         f'\t}},\n'
                         f'\t}},')
            next_key = getNextKey(line, 0)
            if isinstance(next_key, int) and pd.isna(lt):
                # ff.write(f"\n\t}},\n")
                ff.write(f"\n\t}},\n")

    with open(outfile_path, encoding="UTF-8", mode="a") as ff:
        # ff.write(f"\n\t}},\n")
        ff.write(f"\n\t}},\n")
        ff.write("\n}\nreturn config")

main_zhibao()
