import csv
import pandas as pd
from database import  Database
#from connect_keywords.database import Database

csv_file = csv.reader(open('finace_news_content.csv', 'r'))
csv_keyword = csv.reader(open('Keyword.csv', 'r'))
csv_errorkeyword = csv.reader(open('erroKeyword.csv', 'r'))
csv_select_one = csv.reader(open('select_one.csv', 'r'))
csv_select_double = csv.reader(open('select_double.csv', 'r'))
websites = ['新华网', '东方财富网']
#获取contents:原数据库ID：content

contents = []
for row in csv_file:
    content = {}
    content['id'] = row[0]
    content['content'] = row[2].strip('\t\n')
    contents.append(content)
print('新闻数量：', len(contents))

keyword_dict = {}
for row in csv_keyword:
    keyword_dict[row[1]] = row[2:]
print('关键字无意义的个股数量是：', len(keyword_dict))

#有歧义的关键字
errorkeyword_dict = {}
for row in csv_errorkeyword:
    errorkeyword_dict[row[1]] = row[2:]
print('关键字有异议的个股数量是：', len(errorkeyword_dict))

select_one = []
for row in csv_select_one:
    value = str(row[0]).split('%')
    select_one.append(value[1])
print('删除含有单个关键字的数量：', len(select_one))

select_two = []
for row in csv_select_double:
    values = str(row[0]).split('%')[1]
    value = values.split(',')
    select_two.append(value)
print('删除同时含有这两个关键字的数量：', len(select_two))

double_id = []
texts = []
connect_dict = {}
for i in range(len(contents)):
    flag = True
    text = contents[i]   #取出第i篇文档；是一个字典，存储的有id，content
    content = text['content']
    for m in range(len(select_one)):
        word = select_one[m]
        if word in content:
            flag = False
            break
    if flag:
        for n in range(len(select_two)):
            words = select_two[n]
            word1 = words[0]
            word2 = words[1]
            if word1 in content and word2 in content:
                flag = False
                break
        if flag:
            #取出有异议的个股及对应的关键字
            for key, value in errorkeyword_dict.items():
                #错误的词
                errorvalue = value[1]   #鄂尔多斯
                #正确的关键字
                key_value = str(value[0]).split(',')    #['600295', '鄂尔多斯']

                if key_value[0] in content or (key_value[1] in content and errorvalue not in content):
                    for item in texts:
                        if item['id'] == text['id'] and text['id'] != None:
                            if keyword not in websites:
                                item['stoc_id'].extend([key])
                                #print(item['id'] + keyword + key )
                                double_id.append(item['id'])
                                flag = False
                    if flag:
                        jre = {}
                        jre['id'] = text['id']
                        jre['stoc_id'] = [key]
                        jre['content'] = content
                        texts.append(jre)
                        #print(keyword + key)
                        break

            #取出没有异议的个股及对应的关键字
            for key, value in keyword_dict.items():
                value = str(value[0]).split(',')
                #print(value)    #['603773', '沃格光电']
                #遍历指定个股的关键字
                for j in range(len(value)):
                    keyword = value[j]   #关键字
                    #判断关键字是否在文本中
                    if keyword in content:
                    #判断文本是否已有匹配到的个股
                        for item in texts:
                            if item['id'] == text['id'] and text['id'] != None:
                                if keyword not in websites:
                                    item['stoc_id'].extend([key])
                                    #print(item['id'] + keyword + key )
                                    double_id.append(item['id'])
                                    flag = False
                        if flag:
                            jre = {}
                            jre['id'] = text['id']
                            jre['stoc_id'] = [key]
                            jre['content'] = content
                            texts.append(jre)
                            #print(keyword + key)
                            break
print(texts)
print(len(double_id))



def run():
    insert = 'INSERT IGNORE INTO news_connect_keywords(news_id, content, stock_id) VALUES (%s, %s, %s)'

    db = Database()
    db.connect('news_connect_keyword')

    for i in range(len(texts)):
        data = texts[i]
        db.execute(insert, [data['id'], data['content'], str(data['stoc_id'])])

    db.close()

# if __name__ == '__main__':
#      run()
