# alibababBsinessInfo

## 项目介绍

这是一个用于获取阿里巴巴国际站(alibaba.com)商家信息的爬虫工具。该工具可以自动抓取商家的基本信息、联系方式、产品图片等数据，并支持将产品图片插入到Excel表格中，方便用户进行数据分析和管理。

## 功能特点

本项目包含三个主要模块：

1. **D1_get_business_info.py**: 获取商家基本信息
   - 抓取公司名称、联系电话、主要产品、国家、地址等信息
   - 支持按关键词搜索（如示例中的"henan"）
   - 支持多页数据抓取
   - 将数据保存为CSV格式

2. **D2_get_product_img.py**: 下载产品图片
   - 从CSV文件中读取产品图片链接
   - 自动下载图片到本地文件夹

3. **D3_ins_img_to_excel.py**: 将图片插入Excel
   - 读取下载好的产品图片
   - 将图片插入到Excel表格中
   - 支持图片等比例缩放

## 使用方法

### 环境准备

1. 安装Python 3.x
2. 安装Chrome浏览器
3. 下载与Chrome版本匹配的ChromeDriver，放置在项目根目录下
4. 安装所需依赖库：
   ```
   pip install selenium requests pandas lxml pillow xlwings
   ```

### 使用步骤

1. **获取商家信息**
   ```
   python D1_get_business_info.py
   ```
   运行后需要手动登录阿里巴巴账号，登录成功后输入1继续执行程序。程序将自动抓取数据并保存为`alibaba_com_img.csv`。

2. **下载产品图片**
   ```
   python D2_get_product_img.py
   ```
   程序将从CSV文件中读取产品图片链接，并下载到`downloads_picture`文件夹中。

3. **将图片插入Excel**
   ```
   python D3_ins_img_to_excel.py
   ```
   程序将读取下载好的图片，并插入到`alibaba_com.xlsx`文件中。

## 注意事项

- 使用前请确保已创建`downloads_picture`文件夹
- 需要有效的阿里巴巴账号进行登录
- 爬取速度受网络环境影响，请耐心等待
- 请遵守阿里巴巴的使用条款，合理使用本工具

## 依赖库

- selenium: 用于浏览器自动化
- requests: 用于发送HTTP请求
- pandas: 用于数据处理
- lxml: 用于HTML解析
- PIL (Pillow): 用于图片处理
- xlwings: 用于Excel操作

## 项目结构

```
├── D1_get_business_info.py  # 获取商家基本信息
├── D2_get_product_img.py    # 下载产品图片
├── D3_ins_img_to_excel.py   # 将图片插入Excel
├── chromedriver            # Chrome浏览器驱动
├── README.md               # 项目说明文档
├── alibaba_com_img.csv     # 生成的数据文件
└── downloads_picture/      # 下载的图片存储文件夹
```
