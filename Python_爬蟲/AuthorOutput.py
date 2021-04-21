import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json
import math
from collections import Counter
from matplotlib import pyplot as plt
import pandas as pd
import sys
import operator

    
         
###分析
push_user = []
with open('Beauty_message.json', 'r', encoding='utf-8') as f:
    data_list = json.load(f)
    
    for d in range(len(data_list)):
        push_user.append(data_list[d]['b_作者'])


with open("B_au/Beauty.txt",'a',encoding='utf-8') as f:
    json.dump(push_user, f, indent=2, sort_keys=True, ensure_ascii=False)
print('====================完成====================')
with open('B_au/Beauty.txt', 'r', encoding='utf-8') as f:
    data_list = json.load(f)
print("字詞統計中,請稍等......")
dic = {}
for ele in data_list :
    if ele not in dic:
        dic[ele] = 1
    else:
        dic[ele] = dic[ele] + 1

sorted_word = sorted(dic.items(), key = operator.itemgetter(1), reverse = True)
line = ''
for ele in sorted_word:
    #if( len(ele[0]) > 1 ): #只顯示一個字以上的詞，如需顯示一個字的詞請註解掉此行
        line += ele[0] + ' ' + str(ele[1]) + '\n'
with open("Movie_push.txt",'a',encoding='utf-8') as f:
    f.write(line)


