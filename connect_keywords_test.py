import csv
import pandas as pd
from database import  Database
#from connect_keywords.database import Database

csv_file = csv.reader(open('finace_news_content.csv', 'r'))
csv_keyword = csv.reader(open('Keyword.csv', 'r'))
csv_select_one = csv.reader(open('select_one.csv', 'r'))
csv_select_double = csv.reader(open('select_double.csv', 'r'))

#获取contents:原数据库ID：content

contents = []
for row in csv_file:
    content = {}
    content['id'] = row[0]
    content['content'] = row[1].strip('\t\n')
    contents.append(content)
print(contents)

keyword_dict = {}
for row in csv_keyword:
    keyword_dict[row[1]] = row[2:]
print(keyword_dict)

select_one = []
for row in csv_select_one:
    value = str(row[0]).split('%')
    select_one.append(value[1])
print(select_one)

select_two = []
for row in csv_select_double:
    values = str(row[0]).split('%')[1]
    value = values.split(',')
    select_two.append(value)
print(select_two)


texts = []
connect_dict = {}
for i in range(len(contents)):
    flag = True
    text = contents[i]
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
            #取出个股及对应的关键字
            for key, value in keyword_dict.items():
                value = str(value[0]).split(',')
                #遍历指定个股的关键字
                for j in range(len(value)):
                    keyword = value[j]
                    #判断关键字是否在文本中
                    if keyword in content:
                    #判断文本是否已有匹配到的个股
                        for item in texts:
                            if item['id'] == text['id'] and text['id'] != None:
                                item['stoc_id'].extend([key])
                                #print(item['id'] + '1111111' )
                                flag = False
                        if flag:
                            jre = {}
                            jre['id'] = text['id']
                            jre['stoc_id'] = [key]
                            jre['content'] = content
                            texts.append(jre)
                            break
print(texts)




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
