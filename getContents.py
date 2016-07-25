__author__ = 'multiangle'

import urllib.request as request
import json

def getStructedData(url):
    user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent':user_agent}
    req = request.Request(url,headers=headers)
    text = request.urlopen(req,timeout=4)
    text = text.read().decode('utf8')
    return construct_data(text)

def construct_data(text):
    text = text.split('\r\n')
    for i in range(1,text.__len__())[::-1]:
        if text[i].__len__()>0 and (text[i][0]==' ' or text[i][0]=='\t') :
            text[i-1] += ' ' + text[i][1:]
            text.pop(i)
    # for line in text:
    #     print(line)
    data = {}
    while True :
        line = text[0]
        line_ori = line
        if 'Accept-Language' in line:
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
            value = value.split(', ')
            for i in range(1,value.__len__())[::-1]:
                if '"' in value[i] and value[i][0]!='"':
                    value[i-1] += ', '+value[i]
                    value.pop(i)
            for item in value:
                name.append(deal_name_mail_format(item))
            data[key] = name
        elif key == 'Message-ID' or key=='In-Reply-To':
            data[key] = value[1:-1]
        elif key == 'References':
            mail = []
            value = value.split(',')
            for item in value:
                mail.append(item[1:-1])
            data[key] = mail
        else:
            data[key] = value
        text.pop(0)
    return data

def deal_name_mail_format(input):
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

info = getStructedData('https://wikileaks.org/dnc-emails/get/3')
print(json.dumps(info,indent=4))
