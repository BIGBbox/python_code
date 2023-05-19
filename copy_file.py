import os
import shutil
import glob
import pyodbc
import time
print("请依次输入m2的路径,pak导出img的路径和保存路径\n")
# M2的路径
# m2_source_path = "D:/810/枭雄三国/MirServer"
m2_source_path = input("请输入请输入m2的路径:")

# 导出的补丁位置
# sour_all_img_path = "D:/810/枭雄三国/导出补丁/pak_out/1"
sour_all_img_path = input("请输入导出后的补丁的目录:")


# 存放整理后的补丁位置
# img_path = "D:/810/枭雄三国/导出补丁/pak_out"
img_path = input("请输入存放整理后的补丁位置路径:")


abspath = os.path.abspath(os.path.dirname(__file__))
output_path = abspath+"/output"  # 创建存放补丁文件夹
isExists = os.path.exists(output_path)  # 判断路径是否存在，存在则返回true
if not isExists:
    os.makedirs(output_path)

npc_dir_path = output_path+"/npc"  # 存放npc序列帧的文件夹


def parse_string_to_list(string, _parsesign):
    '''
        将某个字符串截取成两半,存入一个列表
    '''
    # 获取npc序列帧开始编号
    start_str = str(string).replace("\n", "")
    _tab = start_str.split(_parsesign, 1)
    return _tab


def get_effect_list():
    '''
    将补丁放入列表
    '''
    # effect_image_list = m2_source_path+"/Mir200/Envir/EffectImageList.txt"
    effect_image_list = os.path.join(m2_source_path, "Mir200", "Envir", "EffectImageList.txt")
    try:
       with open(effect_image_list, 'r') as f:
        content = f.readlines()
        return content
    except :
        print(f"请确定路径m2路径:【{m2_source_path}】是否正确")
        # time.sleep(10)
        return []

def format_effect_list():
    '''
    把补丁名字提取出来,方便使用
    '''
    file_list = get_effect_list()
    _list = []
    _list = [os.path.splitext(ele.strip())[0] for ele in file_list]
    # for ele in file_list:
    #     # ele2 = ele[:-6]
    #     # ele2 = ele.split(".", 1)[0]
    #     ele2 = parse_string_to_list(ele, ".")[0]
    #     _list.insert(len(_list), ele2)
    # return _list
    return _list

pull_effect_list = format_effect_list()


def pickup_img(fileindex, imgindex, imgcount, savepath, _type=None):
    '''
    提取序列帧图片
    '''

    dirname = pull_effect_list[fileindex]
    print(f"正在导出:{dirname},{str(imgindex).zfill(6)}+.png")

    file_paths = glob.glob(os.path.join(sour_all_img_path, '*'))

    for ele in pull_effect_list:
        for file_path in file_paths:
            if ele == dirname:
                # 创建保存序列帧坐标的文件夹
                # save_position_path = savepath+"/Placements"
                save_position_path = os.path.join(savepath, "Placements")

                isExists = os.path.exists(save_position_path)
                if not isExists:
                    os.makedirs(save_position_path)

                for i in range(imgcount):  # imgcount张序列帧遍历保存(序列帧id为连续的)
                    imgname = str(i+imgindex).zfill(6)
                    img_path = file_path+"/"+ele+"/"+imgname+".png"  # 序列帧路径
                    source_position_txt = file_path+"/"+ele + \
                        "/Placements/"+imgname+".txt"  # 序列帧坐标文件
                    if os.path.isfile(img_path):
                        # 复制到目标文件夹中
                        shutil.copy(img_path, savepath)
                        shutil.copy(source_position_txt, save_position_path)
                        with open(output_path+"/npc提取日志.txt", mode="a") as ff:
                            ff.write("id:【"+img_path+"】保存到→→→【"+savepath+"】\n")


def pickup_npc_img(m2_source_path):
    '''
    提取npc序列帧图片
    '''
    full_paths = m2_source_path+"/Mir200/Envir/UserData/CustomNpc/"

    # 创建存放npc序列帧的文件夹
    isExists = os.path.exists(npc_dir_path)
    if not isExists:
        os.makedirs(npc_dir_path)

    # 遍历源文件夹中的所有文件
    # print("full_paths:"+full_paths)
    for npc_file_obj in os.listdir(full_paths):
        custom_npc_file = full_paths + npc_file_obj

        # 获取npc外观id
        npc_file_name = str(npc_file_obj).split(".")[0]
        # print("npc_file_name:"+npc_file_name)
        with open(custom_npc_file, 'r') as f:
            content = f.readlines()
            # 获取补丁编号

            file_index_tab = parse_string_to_list(content[1], "=")
            file_index = file_index_tab[1]
            # print("file_index:"+str(file_index))

            # 获取npc序列帧开始编号
            start_tab = parse_string_to_list(content[18], "=")
            start_index = start_tab[1]
            start_img_name = str(start_index).zfill(6)

            # 获取npc序列帧数量
            frame_tab = parse_string_to_list(content[19], "=")
            frame_count = frame_tab[1]

            if len(npc_file_name) > 3:
                newname = "6"+npc_file_name[-3:]
                img_path = npc_dir_path+"/"+newname
                with open(output_path+"/npc_id修改记录.txt", mode="a") as ff:
                    ff.write("id:【"+npc_file_name+"】修改为→→→【"+newname+"】\n")

            if not isExists:
                os.makedirs(img_path)

            pickup_img(int(file_index), int(start_img_name),
                       int(frame_count), img_path)


# 定义ODBC驱动名称和连接字符串
DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'
DATABASE_FILE = os.path.join(m2_source_path, "Mud2", "DB","HeroDB.MDB")
def read_m2_db(tablename):
    _equip_list = []
    connection_string = f'DRIVER={DRIVER};DBQ={DATABASE_FILE}'
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            columns = ["Name","StdMode","Shape","Looks"] # 指定需要查询的列
            query = f"SELECT {','.join(columns)} from {tablename}"
            cursor.execute(query)

            # 读取结果集
            for row in cursor.fetchall():
                print(f"name:{row[0]},stdmode:{row[1]},shape:{row[2]},looks:{row[3]}")
                itemname = row[0]
                stdmode = row[1]
                shape = row[2]
                looks = row[3]
                # pickup_img(fileindex, imgindex, imgcount, savepath, _type=None):
                # with open(output_path+"/npc_id修改记录.txt", mode="a") as ff:
                    # ff.write("id:【"+npc_file_name+"】修改为→→→【"+newname+"】\n")

# read_m2_db("StdItems","31")
# pickup_npc_img(m2_source_path)
try:
    pickup_npc_img(m2_source_path)
    print(f"完成~")
    time.sleep(10)
except:
    print("请检查输入的路径是否正确")
    # with open(output_path+"/npc_id修改记录.txt", mode="a") as ff:
    #     ff.write("id:【"+npc_file_name+"】修改为→→→【"+newname+"】\n")
    time.sleep(10)