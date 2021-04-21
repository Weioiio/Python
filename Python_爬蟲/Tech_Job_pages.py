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

###網站設定
PTT_URL = 'https://www.ptt.cc'


###抓網址前面處理
def get_web_page(url):
    ###爬文前暫停0.5秒
    time.sleep(0.5)
    res = requests.get(url = url, cookies = {'over18':'1'})

    ### server 回覆的狀態碼 200=正常，404=錯誤
    if res.status_code !=200:
        print('Error URL:',res.url)
        return None
    else:
        return res.text


def checkformat(soup, class_tag, data, index, link):
    # 避免有些文章會被使用者自行刪除 標題列 時間  之類......
    try:
        content = soup.select(class_tag)[index].text
    except Exception as e:
        print('checkformat error URL', link)
        # print 'checkformat:',str(e)
        content = "no " + data
    return content


###抓到網址後的後續處理
def get_articles(dom):
    soup = BeautifulSoup(dom,'html.parser')
    ###取得上一頁的連結
    paging_div = soup.select('div.btn-group-paging a')
    prev_url = PTT_URL+paging_div[1]['href']
    ###儲存取得的文章資料
    articles = []
    divs = soup.find_all('div','r-ent')
    ###抓整頁文章開頭
    for d in divs:
        ###取得推文-噓文數
        push_count=0
        if d.find('div','nrec').string:
            try:
                ###字串轉成數字
                push_count = int(d.find('div','nrec').string)
            except ValueError:  ###if轉換失敗，pushcount保持0
                pass

        ###取得文章連結作者標題
        if d.find('a'):     ###i有超連結，表示文章存在
            href = d.find('a')['href']
            title = d.find('a').string
            articles.append({
                'href':href,
                'title':title,
                'push_count':push_count
            })
    return articles,paging_div


    
###抓取文章內圖片網址
def parse(dom):
    soup = BeautifulSoup(dom,'html.parser')
    links = soup.find(id = 'main-content').find_all('a')
    ###儲存圖片url
    img_urls = []
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls


###抓取內文
def parse_comm(dom,g_id):
    soup = BeautifulSoup(dom,'html.parser')
    # author 文章作者
    author = checkformat(soup, '.article-meta-value', 'author', 0, dom)
    # title 文章標題  
    title = checkformat(soup, '.article-meta-value', 'title', 2, dom)
    # date 文章日期
    date = checkformat(soup, '.article-meta-value', 'date', 3, dom)
    # ip 文章文章ip       
    try:
        targetIP = u'※ 發信站: 批踢踢實業坊'
        ip = soup.find(string=re.compile(targetIP))
        ip = re.search(r"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*", ip).group()
    except:
        ip = "ip is not find"
    try:
        content = soup.find(id="main-content").text
        target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
        content = content.split(target_content)
        content = content[0].split(date)
        main_content = content[1].replace('\n', '  ')
    except Exception as e:
        main_content = 'main_content error'
        print('main_content error URL' + dom)
    num, g, b, n, message = 0, 0, 0, 0, []

    d=[]
    for tag in soup.select('div.push'):
        try:
            push_tag = tag.find("span", {'class': 'push-tag'}).text
            push_userid = tag.find("span", {'class': 'push-userid'}).text
            push_content = tag.find("span", {'class': 'push-content'}).text
            push_content = push_content[1:]
            push_ipdatetime = tag.find("span", {'class': 'push-ipdatetime'}).text
            push_ipdatetime = push_ipdatetime.rstrip()
            
            num += 1
            message.append(push_userid)
            

            # 計算推噓文數量 g = 推 , b = 噓 , n = 註解
            if push_tag == u'推 ':
                g += 1
            elif push_tag == u'噓 ':
                b += 1
            else:
                n += 1
        except Exception as e:
            print("push error URL:" + dom)

    messageNum = {"g": g, "b": b, "n": n, "all": num}
    """
    d = {"a_ID": g_id, "b_作者": author, "c_標題": title, "d_日期": date,
         "e_ip": ip, "f_內文": main_content, "g_推文": message, "h_推文總數": messageNum}
    """

    d.append({
        'a_ID':g_id,
        'b_作者': author,
        'c_標題': title,
        'd_日期': date,
        'e_ip': ip,
        'f_內文': main_content,
        'g_推文': message,
        'h_推文總數': messageNum

        })
    # json.dumps 序列化時預設為對中文使用ascii編碼
    json_data = json.dumps(d, ensure_ascii=False, indent=4, sort_keys=True) + ','
    """
    with open('message.json', 'a', encoding='utf-8') as f:
        json.dump(d, f, indent=4, sort_keys=True, ensure_ascii=False)
    """    
    return d



###儲存相片在Host上
def save(img_urls,title):
    if img_urls:
        try:
            dname = title.strip()   # 用 strip() 去除字串前後的空白
            os.makedirs(dname)

            for img_url in img_urls:
                if img_url.split('//')[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'

                fname = img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
        except Exception as e:
            print(e)



###Math部分

###平均值            
def mean(x):
    return sum(x) / len(x)
###偏差值
def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]
###變異數 
def variance(x):
    deviations = de_mean(x)
    variance_x = 0
    for d in deviations:
        variance_x += d**2
    variance_x /= len(x)
    return variance_x
###內積
def dot(x, y):
    dot_product = sum(v_i * w_i for v_i, w_i in zip(x, y))
    dot_product /= (len(x))
    return dot_product
#相關係數
def correlation(x, y):
    variance_x = variance(x)
    variance_y = variance(y)
    sd_x = math.sqrt(variance_x)
    sd_y = math.sqrt(variance_y)
    dot_xy = dot(de_mean(x), de_mean(y))
    return dot_xy/(sd_x*sd_y)
# 將數字十分位化
def decile(num):  
    return (num // 10) * 10



###網址設定###
fp1=open('Tech_Job_title.json','w', encoding='UTF-8')
fp1.close()
fp2=open('Tech_Job_message.json','w', encoding='UTF-8')
fp2.close()
url = 'https://www.ptt.cc/bbs/Tech_Job/index3299.html'

###Main
i=1
result=[]
json_data=[]
message=[]
pagenum=1
for round in range(300):
    print('===================',pagenum,'===================')
    pagenum+=1
    current_page = get_web_page(url)
    articles = get_articles(current_page)[0]
    prev_url = get_articles(current_page)[1]
    next_url = PTT_URL+prev_url[1]['href']
    url =next_url
    for article in articles:
        result.append(article)
        print(i,'Processing', article)
        i+=1
        page = get_web_page(PTT_URL + article['href'])
        if page:
            #print(page)
            com_urls = parse_comm(page,i)
            for com_url in com_urls:
                json_data.append(com_url)
            #print(com_url)
            #img_urls = parse(page)
            #save(img_urls, article['title'])
            #article['num_image'] = len(img_urls)
    
         
# 儲存文章資訊
with open('Tech_Job_title.json', 'a', encoding='utf-8') as f:
    json.dump(result, f, indent=2, sort_keys=True, ensure_ascii=False)
with open('Tech_Job_message.json', 'a', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4, sort_keys=True, ensure_ascii=False)
    

###分析
push_users = []
with open('Tech_Job_message.json', 'r', encoding='utf-8') as f:
    data_list = json.load(f)
    
    for d in data_list:
        for x in d['g_推文']:
            #print(x)
            push_users.append(x)

with open('Tech_Job_message_process.json', 'w', encoding='utf-8') as f:
    json.dump(push_users, f, indent=2, sort_keys=True, ensure_ascii=False)



###Txt製作
with open('Tech_Job_process.json', 'r', encoding='utf-8') as f:
    data_list = json.load(f)

print("字詞統計中,請稍等......")
#字詞統計
dic = {}

for ele in data_list :
    if ele not in dic:
        dic[ele] = 1
    else:
        dic[ele] = dic[ele] + 1

sorted_word = sorted(dic.items(), key = operator.itemgetter(1), reverse = True)
line = ''
for ele in sorted_word:
    if( len(ele[0]) > 1 ): #只顯示一個字以上的詞，如需顯示一個字的詞請註解掉此行
        line += ele[0] + ' ' + str(ele[1]) + '\n'
with open("Tech_Job_push.txt",'a',encoding='utf-8') as f:
    f.write(line)
print('====================完成====================')


"""
print('圖片數:', images, 'Max:', max(images), 'Min:', min(images))
print('推文數:', pushes, 'Max:', max(pushes), 'Min:', min(pushes))
print('平均圖片數:', mean(images), '平均推文數:', mean(pushes))
print('相關係數:', correlation(images, pushes))


print('圖片數:', images, 'Max:', max(images), 'Min:', min(images))
print('推文數:', pushes, 'Max:', max(pushes), 'Min:', min(pushes))


# histogram
histogram = Counter(decile(push) for push in pushes)
print(histogram)

# histogram plot
plt.figure(1)
plt.bar([x-4 for x in histogram.keys()], histogram.values(), 8)
plt.axis([-5, 150, 0, 300])
plt.title('Pushes')
plt.xlabel('# of pushes')
plt.ylabel('# of posts')
plt.xticks([10 * i for i in range(4)])

# scattering plot
plt.figure(2)
plt.scatter(images, pushes)
plt.title('# of image v.s. push')
plt.xlabel('# of image')
plt.ylabel('# of push')
plt.axis('equal')

plt.show()
"""

