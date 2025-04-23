# -*- coding: utf-8 -*-

import requests
import pandas as pd
import os

def open_requests(img, img_name):
    """
    下载图片并保存到指定目录
    
    参数:
    img - 图片URL
    img_name - 保存的图片名称
    """
    img_url = 'https:' + img
    res = requests.get(img_url)
    with open(f"./downloads_picture/{img_name}", 'wb') as fn:
        fn.write(res.content)

def get_product_img(csv_file='./alibaba_com_img.csv'):
    """
    从CSV文件中读取产品图片链接并下载图片
    
    参数:
    csv_file - CSV文件路径，默认为'./alibaba_com_img.csv'
    """
    # 确保downloads_picture目录存在
    if not os.path.exists("./downloads_picture"):
        os.makedirs("./downloads_picture")
        
    # 读取CSV文件
    df1 = pd.read_csv(csv_file)
    
    # 下载图片
    downloaded_count = 0
    for imgs in df1["product_img"]:
        imgList = str(imgs).split(',')
        if len(imgList) > 0 and imgList[0] != 'nan':
            img = imgList[0]
            img_name = img[24:]
            print(f"正在下载: {img_name}")
            try:
                open_requests(img, img_name)
                downloaded_count += 1
            except Exception as e:
                print(f"下载失败: {e}")
    
    print(f"共下载了 {downloaded_count} 张产品图片到 downloads_picture 文件夹")
    return True