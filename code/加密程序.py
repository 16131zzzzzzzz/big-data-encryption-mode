# coding=utf-8
import random
import requests
import pandas as pd
import importlib,sys
import http.client
import json
from graphics import *
from urllib.parse import quote_plus
importlib.reload(sys)

base = '/v3/geocode/geo'
key  = 'cb649a25c1f81c1451adbeca73623251'

def geocd(address):
    path = '{}?address={}&key={}'.format(base, quote_plus(address), key)
    connection = http.client.HTTPConnection('restapi.amap.com',80)
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    return reply['geocodes'][0]['location']

def transform(location):
    parameters = {'coordsys':'gps','locations': location, 'key': '7ec25a9c6716bb26f0d25e9fdfa012b8'}
    base = 'http://restapi.amap.com/v3/assistant/coordinate/convert'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['locations']

def geocode(location):
    parameters = {'location': location, 'key': '7ec25a9c6716bb26f0d25e9fdfa012b8'}
    base = 'http://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['regeocode']['addressComponent']['district'],answer['regeocode']['formatted_address']

def change(BinNum):
    amount = random.randint(1,7)
    raw_string = str(BinNum)
    string = raw_string[2:]
    l = list(string)
    for i in range(amount):
        loc = random.randint(1,7)
        if l[loc] == '0':
            l[loc] = '1'
        else:
            l[loc] = '0'
    ac = ''.join(l)
    decout = int(ac,2)%10000
    return decout

def rdxor(ab):
    b = random.randint(0,255)
    c = ab^b
    return c

def DealWithPhoneNumber(StrInfo):
    StrPartInfo = StrInfo[7:11]
    IntPartInfo = int(StrPartInfo)
    BinPartInfo = bin(IntPartInfo)
    temp = change(BinPartInfo)
    buf = rdxor(temp)
    binbin = bin(buf)
    ans = change(binbin)
    ls = ""
    if ans<1000:
        x = random.randint(0,9)
        ls = str(x) +str(ans)
    else:
        ls = str(ans)
    return StrInfo[0:7]+ls

def DealWithAge(StrInfo):
    age = int(StrInfo)
    if age >= 0 and age <= 7:
        return random.randint(0,7)
    elif age >= 8 and age <= 14:
        return random.randint(8,14)
    elif age >= 15 and age <= 18:
        return random.randint(15,18)
    elif age >= 19 and age <= 24:
        return random.randint(19,24)
    elif age >= 25 and age <= 30:
        return random.randint(25,30)
    elif age >= 31 and age <=40 :
        return random.randint(31,40)
    elif age >= 41 and age <= 55:
        return random.randint(41,55)
    elif age >= 55 and age <= 70:
        return random.randint(55,70)
    else:
        return random.randint(70,90)

def DealWithAddress(address):
    df = pd.DataFrame(columns=['location','detail'])
    locations = geocd(address)
    dist, detail = geocode(transform(locations))
    df.loc[0] = [dist, detail]
    return df.to_dict('index')[0]['detail']

def convert(input):
    StrInfo = input.getText()
    if len(StrInfo) == 11:
        output = DealWithPhoneNumber(StrInfo)
    elif len(StrInfo) == 1 or len(StrInfo) == 2 or len(StrInfo) == 3:
        output = DealWithAge(StrInfo)
    elif len(StrInfo) == 8:
        output = "We can't deal with phone number now, please wait for programmer Bill."
    else:
        try:
            output = DealWithAddress(StrInfo)
        except:
            output = 'Failed\nNo Internet connection'
    return output

def main():
    win = GraphWin("Kandinsky", 500, 300)
    win.setCoords(0.0, 0.0, 30.0, 40.0)
    # 绘制输入接口
    Text(Point(10,30), " The info you want to convert:").draw(win)
    Text(Point(20,27), " (cell phone number or age or home address )").draw(win)
    Text(Point(10,10),  "converted info:").draw(win)
    input = Entry(Point(19.5,30), 25)
    input.setText("")
    input.draw(win)
    output = Text(Point(21,10),"")
    output.draw(win)
    button = Text(Point(15,20),"Convert It")
    button.draw(win)
    rect = Rectangle(Point(10,15), Point(20,25))
    rect.draw(win)
    # 等待鼠标点击
    win.getMouse()
    result = convert(input)
    # 转换输入
    output.setText(result)
    # 显示输出
    # 改变颜色
    #colorChange(win,input)
    # 改变按钮字体
    button.setText("Quit")
    # 等待点击事件，退出程序
    win.getMouse()
    win.close()

if __name__ == '__main__':
    main()
