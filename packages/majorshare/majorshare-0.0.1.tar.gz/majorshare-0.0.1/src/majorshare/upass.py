# -*- coding:utf-8 -*- 
"""
majors数据API接口 
Created on 2023/08/08
@author: majors
"""

import os


TOKEN_FILE = 'majorshare_token.txt'


def set_token(token):
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, TOKEN_FILE)
    with open(fp, 'w') as file:
        file.write(token)
    print("token文件已存储至 ",fp)
    
def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, TOKEN_FILE)
    try:
        with open(fp, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"默认路径 {fp} 未发现token文件，如不小心清除，请使用set_token(token)重新设置")
        return None
