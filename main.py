__author__ = 'multiangle'

import os
import File_Interface as FI
from getContents import getStructedData
from SocialNetwork import generate_data_for_gelphi

# 建立存放文件的一些文件夹
files = os.listdir('.\\')
if 'static' not in files:
    os.mkdir('.\\static')
if 'temp_res' not in files:
    os.mkdir('.\\temp_res')

# 从wikileaks下载邮件内容并生成结构化数据
# ===============   ATTENTION   =============== :
# 由于邮件格式较繁杂，因此无法全部解析（5%左右）
base_url = 'https://wikileaks.org/dnc-emails/get/{page}'
base_path = '.\static\{page}.pkl'
gotten_id = os.listdir('.\static')
gotten_id = [int((x.split('.'))[0]) for x in gotten_id]
task_pool = list(range(1,2000))  # wikileak中的邮件编号
while True :
    if task_pool.__len__()==0:
        break
    task_id = task_pool.pop(0)
    if task_id in gotten_id:
        print('{id} skip'.format(id=task_id))
        continue
    url = base_url.format(page = task_id)
    path = base_path.format(page = task_id)
    try:
        info = getStructedData(url)
        FI.save_pickle(info,path)
        print('{t} succeed'.format(t=task_id))
    except Exception as e:
        # task_pool.append(task_id)
        print('{t} failed <--<--<--<--'.format(t=task_id))
        print(e)
print('文件已下载完毕')

# 生成社交网络数据(需要networkx包)
generate_data_for_gelphi()
print('gexf文件已经生成,存放路径: {path}\\temp_res'.format(path=os.getcwd()))