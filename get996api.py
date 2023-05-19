import requests
import random
import json
import datetime
import os

agent_list = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10"
]

main_url = 'http://engine-doc.996m2.com/server/index.php?s=/api/item/info'
main_data = {
    'item_id': '9',
    'default_page_id': '154'
}

item_url = 'http://engine-doc.996m2.com/server/index.php?s=/api/page/info'

headers = {
    'Cookie': 'PHPSESSID=19ca51a5e2a78c352759fb5903d9a48c; PHPSESSID=97f765d63e3ee42e1ca285688fd75bd2; think_language=zh',
    'Origin': 'http://engine-doc.996m2.com',
    'Referer': 'http://engine-doc.996m2.com/web/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

output_path = "D:/810/lua_base_moudle/output/"
API_FILE_NAME = "996apilib.lua"
CLASS_NAME = "_996lib"
FILE_PATH = os.path.join(output_path, API_FILE_NAME)


# D:\810\lua底板\scy_mir2\MirServer-lua\Mir200\Envir\QuestDiary\util

def format_data(ll):
    print(f"ll:{ll}")
    api_tab = {}  # 存放解析后的api
    for ele in ll:
        if ele.startswith('###') and not ele.endswith("全局定时器"):
            api_info = ele[4:]  # api的中文描述

            notice = ""  # 接口的用法和描述
            num = ll.index(ele)  # 当前元素的索引
            # 获取api接口名字 `API_NAME`
            try:
                while not ll[num].strip().startswith('`') and not ll[num].strip().endswith('`'):
                    # print(f"==============:{ll[num]}")
                    if not ll[num].strip().startswith('`') and not ll[num].strip().endswith('`'):
                        notice += ll[num]  # 接口的正常用法描述
                    num += 1
            except:
                pass
                # print(f"ERROR::{ll[num - 1]}，{len(ll)}")
            num = num >= len(ll) and len(ll) - 1 or num
            # num -= 1

            # print(f"ll:{num},{ll[num]}")
            if ll[num] != "":
                api_name_tab = str.split(ll[num], '`')
                # print(f"api_name_tab:{api_name_tab},{ll[num]}")
                api_name = api_name_tab[1]  # api的英文名字
                # api_name = api_name == "" and api_info or api_name
                notice += api_name_tab[len(api_name_tab) - 1]  # 特殊某些说明书写在接口同一行
                # print(f"ll[num]::{ll[num]},{api_name_tab},{api_name_tab[len(api_name_tab) - 1]},{api_name}")
                # print(f"notice:{notice},api_info:{api_info},api_name:{api_name}")
                api_tab[api_name] = {}
                api_tab[api_name].update({'api_info': api_info})

                # 获取接口特殊用法描述
                # num += 1
                while not ll[num].startswith("|参数|类型|空|默认|注释|") and not ll[num].strip().startswith("```"):
                    # print(f"while_this:{ll[num]}")
                    num += 1
                    this_notice = ll[num]
                    if not this_notice.startswith("|参数|类型|空|默认|注释|"):
                        try:
                            this_notice = this_notice[this_notice.index('>') + 1:this_notice.index('</') - 1]  # api特殊用法
                        except:
                            this_notice = this_notice

                        if this_notice != "":
                            notice += f"\n---{this_notice}\\"

                api_tab[api_name].update({'api_notice': notice})

                # 获取参数列表
                num = ll.index(ele)
                while not ll[num].startswith("|参数|类型|空|默认|注释|"):
                    num += 1

                # print(f"ll[num]:{ll[num]},api_name:{api_name}")
                func_param_tab = []  # 当前方法的方法体
                # if not ll[num].startswith("###") and ll[num] != "":

                # print(f"while_format_ll[num]:{ll[num]},{api_name}")
                try:
                    while not ll[num].startswith("###") and ll[num] != "":
                        if not ll[num].startswith("|:") and not ll[num].startswith("|参数"):
                            temp_tab = ll[num].split("|")
                            # print(f"{len(temp_tab)},{ll[num]}")
                            if len(temp_tab) == 7:
                                ele1 = temp_tab[1].strip()
                                ele2 = temp_tab[2].strip()
                                ele3 = temp_tab[5].strip()
                                tt = [ele1, ele2, ele3]
                                func_param_tab.insert(len(func_param_tab), tt)
                            # print(f"{tt}")
                        num += 1
                        num = num >= len(ll) and len(ll) or num
                except:

                    with open(output_path + "/ERROR.txt", mode="a", encoding="UTF-8") as ff:
                        # 先清空在写入
                        ff.seek(0)
                        ff.truncate()
                        ff.write(f"检查接口:{api_name},是否写入正常\n")

                # print(f"notice:{notice},api_info:{api_info},api_name:{api_name},func_param_tab:{func_param_tab}")
                api_tab[api_name].update({'func_param_tab': func_param_tab})

    write_api_util(api_tab)


# 写入lua文档文件
def write_api_util(api_tab):
    """
    写入ua文档文件
    :param api_tab: 解析后的api表
    :return:
    """

    for ele in api_tab:
        print(f"ele:{ele},{api_tab[ele]}")
        api_notice = api_tab[ele]['api_notice']
        api_info = api_tab[ele]['api_info']
        func_param_tab = api_tab[ele]['func_param_tab']
        func_param = ""  # 方法体
        func_result = ""  # 方法返回值
        func_str = ""  # 参
        api_note_str = f"---{api_info}"  # 方法注释
        for notice in func_param_tab:

            # 生成参数列表
            this_notice = notice[0].split("/")[0]  # 部分参数支持多种类型
            this_notice = this_notice == "play" and "player" or this_notice
            this_notice = this_notice == "self" and "player" or this_notice
            this_param_type = notice[1][1:-1] == "int" and "number" or notice[1][1:-1]
            this_param_type = this_param_type == "str" and "string" or this_param_type
            this_param_type = this_param_type == "object" and "any" or this_param_type
            this_param_info = notice[2]

            if this_notice != "return" and this_notice != "result" and this_notice != "无参数" and this_notice != "无" and this_notice != "nil":
                api_note_str += f"\n---@param  {this_notice}\t{this_param_type}\t\t{this_param_info}"
                this_notice = this_notice == "play" and "player" or this_notice
                func_param += this_notice + ","
            elif this_notice != "无参数" and this_notice != "无":
                api_note_str += f"\n---@return  \t{this_param_type}\t\t{this_param_info}"

            # if this_notice != "return" and this_notice != "无参数" and this_notice != "result" and this_notice != "无":
            #     this_notice = this_notice == "play" and "player" or this_notice
            #     func_param += this_notice + ","
            #

            # 生成返回值
            if this_notice == "return" or this_notice == "result":
                func_result = f"return {ele}({func_param[:-1]})"
            else:
                func_result = f"{ele}({func_param[:-1]})"

        with open(FILE_PATH, mode="a", encoding="UTF-8") as ff:
            # if ele == "":
            #     with open(output_path + "/ERROR1.txt", mode="a", encoding="UTF-8") as ff:
            #         ff.write(f"{ele}AA\n\n")

            if ele == "tbl2json":
                api_note_str = "---表格转换成字符串\n---@param tab table 待转换的表格 \n---@return str string 字符串 "
                ff.write(f"{api_note_str}\nfunction {CLASS_NAME}.{ele}(tab) \nreturn tbl2json(tab)\nend \n\n")
            elif ele == "json2tbl":
                api_note_str = "---字符串转换成表格\n---@param str string 待转换的字符串 \n---@return tab table table "
                ff.write(f"{api_note_str}\nfunction {CLASS_NAME}.{ele}(str) \nreturn tbl2json(str)\nend \n\n")
            elif api_info == "sqlite库":
                ff.write(f"---{api_notice} \n\n")
            elif ele == "":
                ff.write(
                    f"--------------------------------------------------------------------------------------- \n\n")
            else:
                ff.write(f"{api_note_str}\nfunction {CLASS_NAME}.{ele}({func_param[:-1]}) \n\t{func_result}\nend \n\n")
        pass


# 获取996api网页数据
def get_996api_page(page_list):
    for page in page_list:
        # print(f"page:{page}")
        # page_id = page
        page_id = page['page_id']
        addtime = datetime.datetime.fromtimestamp(int(page['addtime']))
        page_title = 'page_title'
        page_title = page['page_title']
        item_data = {
            'page_id': page_id
        }
        item_response = requests.post(item_url, data=item_data, headers=headers)
        data = json.loads(item_response.text)
        error_code = data['error_code']
        if error_code == 0:
            data = data['data']
            page_content = data['page_content']
            page_content = str.split(page_content, "\n")
            # print(f"page_content:{page_content}")
            # print(f"page_id:{page_id}")
            # if page_id != '122':
            with open(FILE_PATH, mode="a", encoding="UTF-8") as ff:
                ff.write(
                    f"--======================================{page_title},update_time:{addtime}======================================\n")
                ff.write(
                    f"--======================================{page_title},update_time:{addtime}======================================\n")
                ff.write(
                    f"--======================================{page_title},update_time:{addtime}======================================\n\n")
            # pass
            # try:
            # print(f"page_id解析成功:{page_id}")
            # if page_id != '122' and page_id != '120' and page_id != '121' and page_id != '145':
            if page_id != '122' and page_id != '120' and page_id != '121':
                print(f"page_id:{page_id},{page_title}")
                format_data(page_content)
            # except:
            #     pass
            # print(f"page_id:{page_id},page_title:[{page_title}]接口解析失败")
        else:
            print("数据获取失败")


def main():
    response = requests.post(main_url, data=main_data, headers=headers)
    if response.status_code == 200:
        # 如果请求成功，则打印返回的内容
        # print(response.text)
        data = json.loads(response.text)
        page_id_list = []
        error_code = data['error_code']
        if error_code == 0:
            data = data['data']
            pages = data['menu']['catalogs'][0]['pages']
            for ele in pages:
                page_id_list.insert(len(page_id_list), ele)
        else:
            print("数据获取失败")

        get_996api_page(page_id_list)
        # print(page_id_list)
    else:
        # 如果请求失败，则打印错误信息
        print('请求失败：', response.status_code, response.reason)


with open(FILE_PATH, mode="a", encoding="UTF-8") as ff:
    # 先清空在写入
    ff.seek(0)
    ff.truncate()
    ff.write(f"{CLASS_NAME}={{}}\n\n")
pass
main()
# _ll = [122,142,143,153,120,155,146,119,121,136,137,150,149,147]
# _ll = [145]
# get_996api_page(_ll)
