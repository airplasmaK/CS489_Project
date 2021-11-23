# 장효진 , url 나누기 
'''
1. 길이
2. 단축 URL
3. @ 포함
4. // 포함
5. - 포함
6. 서브도메인 갯수
7. http/https 사용여부
'''
#parsing
# pip install parse
from parse import *

def parsing(input_url):
    # local_input = input_url
    # protocal = local_input.split("//")
    # print(protocal)
    
    result = parse("{protocol}//{domain}/{path}", input_url)
    print(result["protocol"])

parsing("https://urp_success/123")

# 길이 

# 단축 url

# @포함 