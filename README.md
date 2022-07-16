# Douban图书爬虫&&数据分析项目

文件结构
```bash
|- README.md                # 本文件
|- 词频.png                 # 数据分析生成的简介词频图片
|- 科普图书数据.xlsx         # 科普图书数据共1000条
|- 通信.csv                 # 通信图书数据共27条 （不包含简介）
|- 通信detail.csv           # 通信图书数据共27条 （包含简介）
|- 通信detailxlsx.xlsx      # 通信图书数据xlsx格式共27条 （包含简介）
|- analyse.ipynb            # 数据分析ipynb文件
|- baidu_stopwords.txt      # 百度停用词文件
|- bookdetail.py            # 豆瓣图书详情页爬取（包含简介）
|- booklist.py              # 豆瓣图书tag页爬取（不包含简介）
|- bookcomment.py           # 浪潮之巅图书评论爬取
|- sentiment_classify.py    # 情感分析
|- sentiment_analysis.csv   # 情感分析数据导出
```

## 爬虫使用方法
安装
```bash
pip install pandas
pip install playwright
playwright install
```

## 数据分析使用方法
安装
```bash
pip install pandas
pip install matplotlib
pip install numpy
pip install jieba
pip install wordcloud
```