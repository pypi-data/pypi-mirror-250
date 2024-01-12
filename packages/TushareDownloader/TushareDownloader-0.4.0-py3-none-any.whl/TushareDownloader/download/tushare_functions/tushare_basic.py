"""
initilized tushare

Author: Yanzhong Huang
Email: yanzhong.huang@outlook.com

- get_token
- update_token
- set_tushare_token
- get_tushare_pro
"""

import tushare as ts  # type: ignore

from tushare.pro.client import DataApi  # get_tushare_pro return # type: ignore


TOKEN_PATH = 'download/tushare_functions/tushare_token.txt'


def get_token() -> str:
    """
    Get token from local path
    """
    with open(TOKEN_PATH, 'r') as f:
        token = f.read()
    return token


def update_token(token: str) -> None:
    """
    Update token, and save to local path
    """
    with open(TOKEN_PATH, 'w') as f:
        f.write(token)


def set_tushare_token() -> None:
    """
    set tushare token
    """
    ts.set_token(get_token())  # type: ignore


def get_tushare_pro() -> DataApi:
    """
    return tushare pro object    
    """
    return ts.pro_api(get_token())  
