__author__ = 'multiangle'

import urllib.request as request
import json
import time
import File_Interface as FI
import os

def getStructedData(url):
    user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent':user_agent}
    req = request.Request(url,headers=headers)
    text = request.urlopen(req,timeout=5)
    text = text.read().decode('utf8')
    return construct_data(text)

def construct_data(text):
    text = text.split('\r\n')
    for i in range(1,text.__len__())[::-1]:
        if text[i].__len__()>0 and (text[i][0]==' ' or text[i][0]=='\t') :
            text[i-1] += ' ' + text[i][1:]
            text.pop(i)
    # ############################################
    # for line in text:
    #     print(line)
    # ###########################################
    data = {}
    count = 0
    while True :
        if count>=text.__len__():
            break
        count += 1

        line = text[0]
        line_ori = line
        if line=='':
            continue
        if 'Accept-Language' in line or 'Content-Language' in line or 'MIME-Version' in line:
            break
        line = line.split(': ')
        if line.__len__()!=2:
            # raise Warning('冒号数不等于1，异常: '+line_ori)
            for i in range(2,line.__len__())[::-1]:
                line[i-1] += ': '+line[i]
                line.pop(i)
        [key,value] = line
        if key == 'From':
            data[key] = deal_name_mail_format(value)
        elif key == 'CC' or key == 'To' :
            name = []
            value_ori = value
            value = value.split(', ')
            for i in range(1,value.__len__())[::-1]:
                if '"' in value[i] and value[i][0]!='"':
                    value[i-1] += ', '+value[i]
                    value.pop(i)
            try:
                for item in value:
                    name.append(deal_name_mail_format(item))
            except:
                raise ValueError(value_ori)
            data[key] = name
        elif key == 'Message-ID' or key=='In-Reply-To':
            data[key] = value[1:-1]
        elif key == 'References':
            mail = []
            value = value.split(',')
            for item in value:
                mail.append(item[1:-1])
            data[key] = mail
        elif key == 'Date':
            data[key] = time.strptime(value,'%a, %d %b %Y %H:%M:%S %z')
        else:
            data[key] = value
        text.pop(0)
    return data

def deal_name_mail_format(input):
    if input[0]=='<' and input[-1]=='>':
        return {'mail':input[1:-1]}
    value = input.split(' <')
    if value.__len__()!=2:
        raise ValueError('deal_name_mail_format中出现未知格式: '+input)
    temp = {}
    if '"' in value[0]:
        if value[0][0]!='"' or value[0][-1]!='"':
            raise ValueError('剪切掉的不是": '+value[0])
        temp['name'] = value[0][1:-1]
    else:
        temp['name'] = value[0]
    temp['mail'] = value[1][:-1]
    return temp

# info = getStructedData('https://wikileaks.org/dnc-emails/get/58')
# print(json.dumps(info,indent=4))

# base_url = 'https://wikileaks.org/dnc-emails/get/{page}'
# base_path = '.\static\{page}.pkl'
# gotten_id = os.listdir('.\static')
# gotten_id = [int((x.split('.'))[0]) for x in gotten_id]
# task_pool = list(range(5000,10000))
# while True :
#     if task_pool.__len__()==0:
#         break
#     task_id = task_pool.pop(0)
#     if task_id in gotten_id:
#         continue
#     url = base_url.format(page = task_id)
#     path = base_path.format(page = task_id)
#     try:
#         info = getStructedData(url)
#         FI.save_pickle(info,path)
#         print('{t} succeed'.format(t=task_id))
#     except Exception as e:
#         task_pool.append(task_id)
#         print('{t} failed <--<--<--<--'.format(t=task_id))
#         print(e)

