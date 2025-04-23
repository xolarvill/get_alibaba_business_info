#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
阿里巴巴商家信息爬虫工具

此脚本整合了获取阿里巴巴国际站商家信息的三个主要功能：
1. 获取商家基本信息
2. 下载产品图片
3. 将图片插入Excel表格

使用方法：
python main.py [功能选项]

功能选项：
--all: 执行所有功能
--info: 仅获取商家信息
--img: 仅下载产品图片
--excel: 仅将图片插入Excel

示例：
python main.py --all
"""

import os
import sys
import argparse
from src import get_business_info, get_product_img, insert_img_to_excel

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='阿里巴巴商家信息爬虫工具')
    parser.add_argument('--all', action='store_true', help='执行所有功能')
    parser.add_argument('--info', action='store_true', help='仅获取商家信息')
    parser.add_argument('--img', action='store_true', help='仅下载产品图片')
    parser.add_argument('--excel', action='store_true', help='仅将图片插入Excel')
    parser.add_argument('--keyword', type=str, default='henan', help='搜索关键词，默认为"henan"')
    parser.add_argument('--pages', type=int, default=31, help='爬取页数，默认为31页')
    parser.add_argument('--excel-file', type=str, default='alibaba_com.xlsx', help='Excel文件名，默认为"alibaba_com.xlsx"')
    
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_args()
    
    # 确保downloads_picture目录存在
    if not os.path.exists("./downloads_picture"):
        os.makedirs("./downloads_picture")
        print("已创建downloads_picture文件夹")
    
    # 如果没有指定任何选项，显示帮助信息
    if not (args.all or args.info or args.img or args.excel):
        print("请指定要执行的功能，使用 --help 查看帮助信息")
        return
    
    # 执行所有功能或指定功能
    if args.all or args.info:
        print("\n===== 开始获取商家信息 =====")
        get_business_info(keyword=args.keyword, pages=args.pages)
    
    if args.all or args.img:
        print("\n===== 开始下载产品图片 =====")
        get_product_img()
    
    if args.all or args.excel:
        print("\n===== 开始将图片插入Excel =====")
        insert_img_to_excel(excel_file=args.excel_file)
    
    print("\n所有任务已完成！")

if __name__ == '__main__':
    main()