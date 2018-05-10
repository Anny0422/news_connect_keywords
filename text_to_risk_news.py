#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 13:06:25 2018

@author: sensedealmba
"""

import os
import sys
import csv
import re
import pandas as pd
from collections import Counter
import glob
from riskdict import RiskDict


def load_txt(filepath):
    with open(filepath,'r',encoding = 'utf8') as f:
        lines = f.readlines()
    #print(lines)
    lines = [del_cid(line) for line in lines]
    #print(lines)
    lines = [re.sub(' ','',line.strip()) for line in lines if line.strip()]
    #print(lines[:1])
    #print(lines[1:])
    return lines[:1],lines[1:]    #为什么分成两部分？？？？？？
print(load_txt('news_connect_keywords.csv'))


class RiskDictError(KeyError):
    pass

def check_risk_dict(riskdict): #,
    for typ,rule in riskdict.items():
        keys = rule.keys()
        for key in keys:
            if not key in ['type','title','abstract']:
                if not key in ['del_title','del_abstract','del_type']:
                    raise RiskDictError('{}: {} is an illegal key'.format(typ,key))
            if [x for x in ['type','title','abstract'] if not x in keys]:
                raise RiskDictError('{}: missing key(s)'.format(typ))

#check_risk_dict(RiskDict)

def type_match(lines,riskdict):
    type_list = []
    for risk,subriskdict in riskdict.items():
        for regex in subriskdict['type']:
            if regex.search(lines):
                type_list.append(risk)
                break
    if type_list:
        return type_list
    return False

def read_type(lines,riskdict,pattern = re.compile('风险|警示|警示函|(?!(回复(的)？))问询(?!((的)？回复))|受.*(影响|冲击)|拖累|曝光')):  #按照type给新闻贴上风险、一定有风险和未知类别
    type_list = []
    filetype = type_match(lines,riskdict)
    if pattern.search(lines):
        if filetype:
            type_list.extend(filetype+['一定有风险'])
        else:
            type_list = ['风险新闻']
    elif filetype:
        type_list.extend(filetype)
    else:
        type_list = ['未知类别']
    return type_list

def match_regex(lines,regex_list):
    count = 0
    matched_lines = []
    for regex in regex_list:
        if regex.search(lines):
            count += 1
            matched_lines.append(lines)
    return count,matched_lines

def unmatch_regex(lines,risktype,location_key,subriskdict):
    count = 0
    delkey = 'del_'+location_key
    if not delkey in subriskdict.keys():
        return count
    if len(lines)!=0:
        regex_list = subriskdict[delkey]
        for regex in regex_list:
            if regex.search(lines):
                count += 1
                break
    elif len(lines)==0:
        count = 0
    return count

def detect_risk(lines,riskdict,type_list,location_key='title'):
    risk_list = []
    
    if not location_key in ['title','abstract']:
        raise RiskDictError('invalid key {}'.format(location_key))
    
    if type_list == ['风险新闻'] :#or type_list == ['未知类别']: #能提到啥就提啥
        for key,value in riskdict.items():
            regex_list = value[location_key]
            match_count,matched_lines = match_regex(lines,regex_list)
            match_count -= unmatch_regex(lines,key,location_key,value)
            if match_count>0:
                risk_list.extend([key])
        return risk_list
    
    for key in type_list:
        if key in riskdict.keys():
            regex_list = riskdict[key][location_key]
            match_count,matched_lines = match_regex(lines,regex_list)
            match_count -= unmatch_regex(lines,key,location_key,riskdict[key])
            if match_count>0:
               risk_list.extend([key])
        elif key == '一定有风险' and location_key == 'title':
            risk_list.extend(type_list[:-1])
    return risk_list

def rank_risks(risk_list):
    return [x[0] for x in sorted(Counter(risk_list).items(),key = lambda x:x[1],reverse=True)]

def write_into_files(risk_list,filepath,outdir):
    f = csv.reader(open(filepath,'r'))
    news=[]
    for line in f :
      news.append(line[0])
    print(news)
    data=pd.DataFrame(news)
    #print(data)
    data["type"]=risk_list
    data.to_csv(outdir,encoding='utf_8_sig')  

    
def text_to_risk2(filepath,riskdict=RiskDict):
    f = csv.reader(open(filepath,'r'))
    risklist=[]
    for lines in f:
        type_list = read_type(lines[1],riskdict)
        print(type_list)
#        title_risks = detect_risk(lines,riskdict,type_list,'title')
#    print(title_risks)
        fulltext_risks = detect_risk(lines[1],riskdict,type_list,'title')
#    print(abstract_risks)
        fulltext_risks = rank_risks(fulltext_risks)
        print(fulltext_risks)
        if type_list == ['风险新闻'] and not fulltext_risks:
            fulltext_risks = ['风险新闻(具体类别未匹配成功)']
        if not fulltext_risks:
            fulltext_risks = ['Unknown']
#        write_into_files(lines[0],fulltext_risks,filepath,outdir)
        risklist.append(fulltext_risks)
    return risklist

print(text_to_risk2('news_connect_keywords.csv', RiskDict))

def text_to_risk(title,abstract,riskdict=RiskDict):
    title = re.sub(' ','',title)
    titleline = [title]
    abstractlines = [re.sub(' ','',line.strip()) for line in abstract.split('\n') if line.strip()]
    type_list = read_type(title,riskdict)
#    print(type_list)
    title_risks = detect_risk(titleline,riskdict,type_list,'title')
#    print(title_risks)
    abstract_risks = detect_risk(abstractlines,riskdict,type_list,'abstract')
#    print(abstract_risks)
    fulltext_risks = rank_risks(title_risks + abstract_risks)
#    print(fulltext_risks)
    if type_list == ['风险新闻'] and not fulltext_risks:
        fulltext_risks = ['风险新闻(具体类别未匹配成功)']
    if not fulltext_risks:
        fulltext_risks = ['Unknown']
    return ';'.join(fulltext_risks)
    
# if __name__ == '__main__':
#
# #    title = sys.argv[1]
# #    abstract = sys.argv[2]
#     filepath='news_connect_keywords.csv'
#
#     outdir='risk_stocks.csv'
#     risk_list=text_to_risk2(filepath,RiskDict)
#     write_into_files(risk_list,filepath,outdir)














#    filefolder = '/Users/sensedealmba/Documents/sensedeal/data/title_n_ks'
#    outdir = '/Users/sensedealmba/Documents/sensedeal/test/risk/risk'
#    filelist = glob.glob(filefolder+'/*.txt')
#    risk_dict = {}
#    for filepath in filelist:
#        print(filepath)
#        risks = text_to_risk(filepath,RiskDict,outdir)
#        with open(filepath) as f:
#            text = f.read()
#        for risk in risks:
#            if risk in risk_dict.keys():
#                risk_dict[risk].append(filepath+'\n'+text+'\n')
#            else:
#                risk_dict[risk] = [filepath+'\n'+text+'\n']
#    for key,value in risk_dict.items():
#        with open(os.path.join(outdir,key+'.txt'),'w') as f:
#            f.write(''.join(value))
#    print('新文件生成完毕！')

