#!/usr/bin/python3
# coding=utf-8
import http.client
import importlib
import json
import os
import random
import sys
from urllib.parse import quote_plus

import gi
import pandas as pd
import requests

from gi.repository import Gtk

importlib.reload(sys)
base = '/v3/geocode/geo'
key = 'cb649a25c1f81c1451adbeca73623251'


def geocd(address):
    path = '{}?address={}&key={}'.format(base, quote_plus(address), key)
    connection = http.client.HTTPConnection('restapi.amap.com', 80)
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    return reply['geocodes'][0]['location']


def transform(location):
    parameters = {'coordsys': 'gps', 'locations': location, 'key': '7ec25a9c6716bb26f0d25e9fdfa012b8'}
    base = 'http://restapi.amap.com/v3/assistant/coordinate/convert'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['locations']


def geocode(location):
    parameters = {'location': location, 'key': '7ec25a9c6716bb26f0d25e9fdfa012b8'}
    base = 'http://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['regeocode']['addressComponent']['district'], answer['regeocode']['formatted_address']


def change(BinNum):
    amount = random.randint(1, 7)
    raw_string = str(BinNum)
    string = raw_string[2:]
    l = list(string)
    for i in range(amount):
        loc = random.randint(1, 7)
        if l[loc] == '0':
            l[loc] = '1'
        else:
            l[loc] = '0'
    ac = ''.join(l)
    decout = int(ac, 2) % 10000
    return decout


def rdxor(ab):
    b = random.randint(0, 255)
    c = ab ^ b
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
    if ans < 1000:
        x = random.randint(0, 9)
        ls = str(x) + str(ans)
    else:
        ls = str(ans)
    return StrInfo[0:7] + ls


def DealWithAge(StrInfo):
    age = int(StrInfo)
    if 0 <= age <= 7:
        return random.randint(0, 7)
    elif 8 <= age <= 14:
        return random.randint(8, 14)
    elif 15 <= age <= 18:
        return random.randint(15, 18)
    elif 19 <= age <= 24:
        return random.randint(19, 24)
    elif 25 <= age <= 30:
        return random.randint(25, 30)
    elif 31 <= age <= 40:
        return random.randint(31, 40)
    elif 41 <= age <= 55:
        return random.randint(41, 55)
    elif 55 <= age <= 70:
        return random.randint(55, 70)
    else:
        return random.randint(70, 90)


def DealWithAddress(address):
    df = pd.DataFrame(columns=['location', 'detail'])
    locations = geocd(address)
    dist, detail = geocode(transform(locations))
    df.loc[0] = [dist, detail]
    return df.to_dict('index')[0]['detail']


def convert(inp):
    if len(inp) == 11:
        output = DealWithPhoneNumber(inp)
    elif len(inp) == 1 or len(inp) == 2 or len(inp) == 3:
        output = DealWithAge(inp)
    elif len(inp) == 8:
        output = "We can't deal with phone number now, please wait for programmer Bill."
    else:
        try:
            output = DealWithAddress(inp)
        except Exception:
            output = 'Failed\nNo Internet connection'
    return str(output)


# noinspection PyUnusedLocal
class Handler:
    @staticmethod
    def onDeleteWindow(*args):
        try:
            pass
        finally:
            Gtk.main_quit(*args)

    @staticmethod
    def clicked(entry):
        result = convert(str(entry.get_text()))
        buffer1.set_text(result)


builder = Gtk.Builder()
builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/a.glade")
builder.connect_signals(Handler())
window = builder.get_object("mainwindow")
window.show_all()
buffer1 = builder.get_object("textbuffer1")
Gtk.main()
