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

import keras
from keras.callbacks import ReduceLROnPlateau
from keras.models import Sequential
import keras.optimizers
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization, Activation
from keras.callbacks import ModelCheckpoint
#parsing
# pip install parse

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

url_MLP = Sequential([
    Dense(32, activation = 'relu', input_shape = (16, )),
    Dense(16, activation = 'relu'),
    Dense(8, activation = 'relu'),
    Dense(4, activation = 'relu'),
    Dense(1, activation = 'sigmoid')
])

optimizer = keras.optimizers.Adam(lr = 0.0001)

checkpoint = ModelCheckpoint('url_MLP.h5', monitor = 'val', mode  ='max', verbose = 2, save_best_only=True)

url_MLP.fit()
