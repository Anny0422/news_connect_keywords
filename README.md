# news_connect_keywords
## finace_news_content.csv文件：下载的是去重后的数据；也是针对这一批数据给匹配上个股标签
## select_one.csv文件：若匹配上，则剔除content
## select_double.csv文件：两个关键字同时存在，若匹配上，则剔除content
## Keyword.csv文件：无异议的个股关键字
## erroKeyword.csv文件：有异议的个股关键字
## connect_keywords.py文件：定义了一个类：
get_contents(csv_file)：将待处理的文件转换成json形式：#contents是个列表，元素为字典，记录每个新闻的几个特征：原数据库ID,content,counts
connect_share(contents, del_one, del_two, error_keyword_dict, right_keyword_dict)：重要的函数：匹配个股；
             返回texts, len(double_id)；texts是一个json形式
run(texts)：更改database.cfg中的配置文件名，利用database.py中的数据库连接、插入、执行操作
## connect_keywords_share.py文件：初始模式，没有定义类和函数。
## test.py文件：用来查看结果


