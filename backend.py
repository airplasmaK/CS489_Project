# 장효진 , url 나누기 
'''
파싱
1. 길이
2. 단축 URL
3. @ 포함
______________________________________
4. // 포함 -->parsing 함수 사용해서
5. - 포함  -->parsing 함수 사용해서
6. 서브도메인 갯수 
7. http/https 사용여부  -->parsing 함수 사용해서 
'''
import csv
from enum import Enum

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
#parsing
# pip install parse
from parse import *

feature_datas = []

class Skill(Enum):
    legitimate = 0
    suspicious = 1
    phishing = 2



def parsing(input_url):
    # local_input = input_url
    # protocal = local_input.split("//")
    # print(protocal)
    
    result = parse("{protocol}//{domain}/{path}", input_url)
    if result == None:
        result = parse("{protocol}//{domain}/", input_url)
    # print(result["protocol"])
    return result

# parsing("https://naver.com/123")

# 길이 
def length_check(input_url):
    if len(input_url) < 54 :
        return Skill.legitimate
    elif 54 <= len(input_url) <= 75:
        return Skill.suspicious
    else:
        return Skill.phishing

# 단축 url
# https://metalkin.tistory.com/50
def short_url(input_url):
    return 0

# @포함 
def include_at(input_url):
    # print("include_at: ",input_url)
    domain = parsing(input_url)["domain"]
    if "@" in domain:
        # print("피싱")
        return Skill.phishing
    return Skill.legitimate

include_at("https://naver.com@bit.ly/")

# // included in URL
def include_double_slash(input_url):
    domain = parsing(input_url)["domain"]
    if "//" in domain:
        # print("피싱")
        return Skill.phishing
    return Skill.legitimate

# - included in URL
def include_hyp_slash(input_url):
    domain = parsing(input_url)["domain"]
    if "-" in domain:
        # print("피싱")
        return Skill.phishing
    return Skill.legitimate

# Too many subdomain
def too_many_subdomain(input_url):
    domain = parsing(input_url)["domain"]
    domain_list = str(domain).split(".")
    if len(domain_list) > 3:    # Maybe 2 --> we need to tune hyperparameter
        # print("피싱")
        return Skill.phishing   # Or should it be suspicious?
    return Skill.legitimate
    
def which_protocol(input_url):
    pt = parsing(input_url)["protocol"]
    if pt == "http":
        # print("Suspicious")
        return Skill.suspicious
    return Skill.legitimate


def make_feature(input_url):
    feature = [0 for i in range(7)]
    feature[0] = length_check(input_url)
    feature[1] = include_at(input_url)
    feature[2] = include_double_slash(input_url)
    feature[3] = too_many_subdomain(input_url)
    feature[4] = which_protocol(input_url)
    feature[5] = include_hyp_slash(input_url)
    feature[6] = 1

    feature_datas.append(feature)

# Shape of feature_data
# feature[0 ~ 5]=> The phishing detecting features (length, @, //, etc)
# feature[6] => "Label": 1 is for phishing, 0 is for legitimate)

f = open("phising_url.txt", 'r')
# print(datas)
for line in f:
    make_feature(line.strip())

f.close()

print(np.array(feature_datas).shape)

# Read the non-phishing sites
n = open("top-1m.csv")
idx = csv.reader(n)
not_ph = []
for line in idx:
    not_ph.append(line[1])
    if len(not_ph) > 2000:
        break

# Current Problem 1: Legitimate URLs do not have the protocols (eg. http, https)
for i in not_ph:
    make_feature(i)


'''

# Below is for logistic regression

W = torch.zeros((5, 1), requires_grad = True)
b = torch.zeros(1, requires_grad = True)

hypothesis = 1 / (1 + torch.exp(-(feature_datas.matmul(W) + b)))

optimizer = optim.SGD([W, b], lr=1)

nb_epochs = 1000
for epoch in range(nb_epochs + 1):

    # Cost 계산
    hypothesis = torch.sigmoid(x_train.matmul(W) + b)
    cost = -(y_train * torch.log(hypothesis) + 
             (1 - y_train) * torch.log(1 - hypothesis)).mean()

    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print('Epoch {:4d}/{} Cost: {:.6f}'.format(
            epoch, nb_epochs, cost.item()
        ))

'''
