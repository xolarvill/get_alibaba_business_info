# alibababBsinessInfo

## 项目介绍

这是一个用于获取阿里巴巴国际站(alibaba.com)商家信息的爬虫工具。该工具可以自动抓取商家的基本信息、联系方式、产品图片等数据，并支持将产品图片插入到Excel表格中，方便用户进行数据分析和管理。

## 功能特点

本项目包含三个主要模块：

1. **获取商家基本信息**
   - 抓取公司名称、联系电话、主要产品、国家、地址等信息
   - 支持按关键词搜索（如示例中的"henan"）
   - 支持多页数据抓取
   - 将数据保存为CSV格式

2. **下载产品图片**
   - 从CSV文件中读取产品图片链接
   - 自动下载图片到本地文件夹

3. **将图片插入Excel**
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
   pip install selenium requests pandas lxml pillow xlwings argparse
   ```

### 使用步骤

#### 方法一：使用统一入口脚本（推荐）

项目提供了统一的入口脚本`main.py`，可以方便地执行所有功能或单独执行某个功能：

1. **执行所有功能**
   ```
   python main.py --all
   ```
   这将依次执行获取商家信息、下载产品图片、将图片插入Excel三个步骤。

2. **仅获取商家信息**
   ```
   python main.py --info
   ```
   运行后需要手动登录阿里巴巴账号，登录成功后输入1继续执行程序。程序将自动抓取数据并保存为`alibaba_com_img.csv`。

3. **仅下载产品图片**
   ```
   python main.py --img
   ```
   程序将从CSV文件中读取产品图片链接，并下载到`downloads_picture`文件夹中。

4. **仅将图片插入Excel**
   ```
   python main.py --excel
   ```
   程序将读取下载好的图片，并插入到`alibaba_com.xlsx`文件中。

5. **自定义参数**
   ```
   python main.py --all --keyword "zhejiang" --pages 10 --excel-file "my_data.xlsx"
   ```
   - `--keyword`: 设置搜索关键词，默认为"henan"
   - `--pages`: 设置爬取页数，默认为31页
   - `--excel-file`: 设置Excel文件名，默认为"alibaba_com.xlsx"

#### 方法二：单独运行各模块脚本

也可以单独运行各个功能模块的脚本：

1. **获取商家信息**
   ```
   python src/business_info.py
   ```

2. **下载产品图片**
   ```
   python src/product_img.py
   ```

3. **将图片插入Excel**
   ```
   python src/excel_img.py
   ```

### 作为模块导入

本项目也可以作为模块导入到其他Python项目中使用：

```python
# 导入模块
from alibababBsinessInfo import get_business_info, get_product_img, insert_img_to_excel

# 获取商家信息
get_business_info(keyword="henan", pages=5)

# 下载产品图片
get_product_img()

# 将图片插入Excel
insert_img_to_excel(excel_file="my_data.xlsx")
```

## 注意事项

- 使用前请确保已创建`downloads_picture`文件夹（使用`main.py`时会自动创建）
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
- argparse: 用于命令行参数解析

## 项目结构

```
├── main.py                 # 主入口脚本
├── __init__.py             # 包初始化文件
├── src/                    # 源代码目录
│   ├── __init__.py         # 模块初始化文件
│   ├── business_info.py    # 获取商家基本信息模块
│   ├── product_img.py      # 下载产品图片模块
│   └── excel_img.py        # 将图片插入Excel模块
├── chromedriver            # Chrome浏览器驱动
├── README.md               # 项目说明文档
├── alibaba_com_img.csv     # 生成的数据文件
└── downloads_picture/      # 下载的图片存储文件夹
```
