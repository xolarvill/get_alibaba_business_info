# -*- coding: utf-8 -*-

from PIL import Image
import os
import xlwings as xw

def write_pic(sht, cell, img_name):
    """
    将图片写入Excel单元格
    
    :param sht: Excel工作表对象
    :param cell: 单元格位置
    :param img_name: 图片名称
    """
    path = f'./downloads_picture/{img_name}'
    print(path)
    fileName = os.path.join(os.getcwd(), path)
    img = Image.open(path).convert("RGB")
    print(img.size)
    w, h = img.size
    x_s = 70  # 设置宽 excel中，我设置了200x200的格式
    y_s = h * x_s / w  # 等比例设置高
    sht.pictures.add(fileName, left=sht.range(cell).left, top=sht.range(cell).top, width=x_s, height=y_s)

def insert_img_to_excel(excel_file='alibaba_com.xlsx', sheet_name='Sheet1'):
    """
    将下载好的产品图片插入到Excel表格中
    
    :param excel_file: Excel文件路径，默认为'alibaba_com.xlsx'
    :param sheet_name: 工作表名称，默认为'Sheet1'
    :return: 无返回值
    """
    # 确保downloads_picture目录存在
    if not os.path.exists("./downloads_picture"):
        print("错误：downloads_picture文件夹不存在，请先运行下载图片功能")
        return False
        
    # 打开Excel文件
    app = xw.App(visible=True, add_book=False)
    try:
        wb = app.books.open(excel_file)
        sht = wb.sheets[sheet_name]
        
        # 获取图片列表
        img_list = sht.range("L2").expand('down').value
        print(f"共找到 {len(img_list)} 个图片链接")
        
        # 插入图片
        inserted_count = 0
        for index, imgs in enumerate(img_list):
            cell = "C" + str(index + 2)
            imgsList = str(imgs).split(',')
            if len(imgsList) > 0 and imgsList[0] != 'nan':
                img = imgsList[0]
                img_name = img[24:]
                try:
                    write_pic(sht, cell, img_name)
                    print(f"已插入图片: {cell}, {img_name}")
                    inserted_count += 1
                except Exception as e:
                    print(f"没有找到这个img_name的图片 {img_name}: {e}")
        
        # 保存并关闭Excel
        wb.save()
        wb.close()
        print(f"共插入了 {inserted_count} 张图片到Excel表格中")
        return True
    except Exception as e:
        print(f"处理Excel时出错: {e}")
        return False
    finally:
        app.quit()