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
from enum import Enum

class Skill(Enum):
    legitimate = 0
    suspicious = 1
    phishing = 2

#parsing
# pip install parse
from parse import *

def parsing(input_url):
    # local_input = input_url
    # protocal = local_input.split("//")
    # print(protocal)
    
    result = parse("{protocol}//{domain}/{path}", input_url)
    # print(result["protocol"])
    return result

parsing("https://naver.com/123")

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
    domain = parsing(input_url)["domain"]
    if "@" in domain:
        print("피싱")
        return Skill.phishing
    return Skill.legitimate

include_at("https://naver.com@bit.ly/123")