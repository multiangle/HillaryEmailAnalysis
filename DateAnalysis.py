__author__ = 'multiangle'

import File_Interface as FI
import json
import os
import time

paths = os.listdir('.\static')
date_counter = {}
for path in paths:
    data = FI.load_pickle('.\static\{x}'.format(x=path))
    date_ori = data.get('Date')
    if date_ori:
        tag = time.strftime('%Y/%m/%d',date_ori)
        c = date_counter.get(tag)
        print(tag)
        if c:
            date_counter[tag]['count'] += 1
        else:
            date_counter[tag] = dict(
                date = tag,
                count = 1
            )
# date_counter = list(date_counter.values())
# date_counter = sorted(date_counter,key=lambda x:x['date'])
# for date in date_counter:
#     print('{a}\t{b}'.format(a=date['date'],b=date['count']))
