import requests
import random
import hashlib

def baidu_translate(text, appid="", appkey=""):
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = hashlib.md5((appid + text + str(salt) + appkey).encode()).hexdigest()

    params = {
        'q': text,
        'from': 'zh',
        'to': 'en',
        'appid': appid,
        'salt': salt,
        'sign': sign
    }

    response = requests.get(url, params=params)
    result = response.json()
    
    if 'trans_result' in result:
        return result['trans_result'][0]['dst']
    else:
        print("fail:", result)
        return None
