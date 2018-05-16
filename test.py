import re
import csv
# contents =['外交部发言人华春莹：1a对等和公平不能自说自话，不能完全根据自身利益和需要来制定标准','1a你好']
# dict = {'a': ['1,a'], 'b': ['2,b'], 'c': ['3,c']}
# texts =[]
# for i in range(len(contents)):
#     text = contents[i]
#     print(text)
#     for key, value in dict.items():
#         print(value[0])
#         value = str(value[0]).split(',')
#         print(value[0],value[1])
#
#         for j in range(len(value)):
#             keyword = value[j]
#             print(keyword)
#             pattern = re.compile(r'%s' % (keyword))
#             search_Obj = re.search(pattern, text)
#             if search_Obj:
#                 texts.append(text)
#                 break
# print(texts)


#csv_keyword = csv.reader(open('Keyword.csv', 'r'))
# keyword_dict = {}
# for row in csv_keyword:
#     keyword_dict[row[1]] = row[2:]
# print(keyword_dict)
#
# for key, value in keyword_dict.items():
#     value = str(value[0]).split(',')
#     if '中国动力' in value:
#         print(key, value)




csv_keyword = csv.reader(open('Keyword.csv', 'r'))
keywords = []
for row in csv_keyword:
    keywords.append(row)
print(keywords)

for i in range(len(keywords)):
    if '新华网' in keywords[i][2]:
        print(keywords[i])

csv_news_keywords = csv.reader(open('news_connect_keywords.csv', 'r'))
texts = []
for row in csv_news_keywords:
    text = {}
    text['id'] = row[0]
    text['content'] = row[1]
    text['stoc_id'] = row[2]
    text['counts'] = row[3]
    texts.append(text)
print(texts)

for i in range(len(texts)):
    stoc_id = texts[i]['stoc_id']
    if '603888' in stoc_id:
        print(texts[i])




