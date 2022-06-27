import requests
import json
import cv2
import numpy as np
import os
import sys
from PIL import  Image
from model import OcrHandle
import pandas as pd
import datetime
from wx_msg import sendEmail

def download_img(url_info):
    if url_info:
        print("-----------正在下载图片 %s -----------"%(url_info))
        # 这是一个图片的url
        try:
            url = url_info
            response = requests.get(url)
            # 获取的文本实际上是图片的二进制文本
            img = response.content
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            #保存路径
            path='%s.jpg' % ('curr_image')
            with open(path, 'wb') as f:
                f.write(img)
        except Exception as ex:
            print("--------出错继续----")
            pass

def load_images(uid='3262617', nums=5):
    currdate = datetime.date.today().strftime('%Y/%m%d')
    print("load today: {}".format(currdate))
    headers = {
        'Host': 'api.coolapk.com',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'X-App-Token': '6f3978292d6bf9fc196f6ad8ee3457212FD0D048-86C7-46C5-98D1-99F5FD4DF8970x626cd5df',
        'Accept-Language': 'zh-Hans-CN;q=1.0, en-CN;q=0.9',
        'X-Sdk-Locale': 'zh-CN',
        'X-Api-Version': '11',
        'X-App-Device': 'QMxASZu9GaQlGI7UGbwBXQgsTZsBHcBByOgsDI7AyO3kDOGRENEZUNGlTOtEDR4kTL1MkN00yNDZDOtgDNwQEMEZkM',
        'X-App-Code': '2110201',
        'User-Agent': 'Mozilla/5.0 (iPhone 11; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1 (#Build; Apple; iPhone 11; iOS14.8; 14.8) +iCoolMarket/4.4.4',
        'X-Sdk-Int': '14.8',
        'X-App-Version': '4.4.4',
        'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'SESSID=8108d6984a7d3e0ab251f2a3e25bc6197c7b800b',
        'X-App-Id': 'com.coolapk.app'
    }
    url = "https://api.coolapk.com/v6/user/feedList?page=1&uid={}".format(uid)
    response = requests.get(url, headers=headers).text
    response = json.loads(response)
    
    #读取最近5个post
    img_list = []
    for item in response['data'][0:nums]:
        if currdate in item['pic']:
            img_list.append(item['pic'])
    return img_list

if __name__ == '__main__':
    ocrHandle = OcrHandle("dbnet.onnx", "crnn_lite_lstm.onnx")
    image_url_list = load_images()
    for im_urr in image_url_list:
        
        download_img(im_urr)
        im_test = Image.open("curr_image.jpeg")
        ocr_result = ocrHandle.text_predict(im_test,256)
        if ocr_result[0][1] == 'L5':
            card_num = ocr_result[1][1] 
            print("5级黑卡:{}".format(card_num))
            sendEmail("5级黑卡:{}".format(card_num), card_num)