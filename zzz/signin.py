import json
import requests
import time
import os
from datetime import datetime, timedelta
import hashlib
import re
import random

def reply(key, text, post_id, comment_id, image):

    device_code = "[d]00000000-0000-0000-0000-000000000000"

    sign_data = f"_key{key}comment_id{comment_id}device_code{device_code}images{image}post_id{post_id}text{text}fa1c28a5b62e79c3e63d9030b6142e4b".encode('utf-8')
    sign = hashlib.md5(sign_data).hexdigest()

    url = "https://floor.huluxia.com/comment/create/ANDROID/4.2"
    params = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.3.1.4",
        "versioncode": 393,
        "market_id": "tool_web",
        "_key": key,
        "device_code": device_code
    }
    data = {
        "post_id": post_id,
        "comment_id": comment_id,
        "text": text,
        "patcha": "",
        "images": image,
        "remindUsers": "",
        "sign": sign
    }
    headers = {
        "User-Agent": "okhttp/3.8.1"
    }

    response = requests.post(url, params=params, data=data, headers=headers)
    print(response.text)
    print(data)

def GetTodayComments():
    url = f"https://floor.huluxia.com/comment/create/list/ANDROID/4.1.8?user_id=36085245&start=0&count=200&platform=2&gkey=000000&app_version=4.3.1.4&versioncode=393&market_id=tool_web&_key={key}&device_code=%5Bd%5D493fbe20-78a1-4d47-9210-e66205b8a2f0"

    headers = {
        "User-Agent": "okhttp/3.8.1"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        comments = data.get('comments', [])
        filtered_comments = []
        current_time = datetime.utcnow() + timedelta(hours=8)

        for comment in comments:
            create_time = comment.get('createTime')
            category_id = comment.get('category', {}).get('categoryID')
            comment_time = datetime.utcfromtimestamp(create_time / 1000) + timedelta(hours=8)
            comment['createTime'] = comment_time.strftime('%Y-%m-%d %H:%M:%S')
            if comment_time.date() == current_time.date() and category_id == 123:
                filtered_comments.append({
                    "commentID": comment.get('commentID'),
                    "createTime": comment['createTime'],
                    "categoryID": category_id
                })
        with open("todaycomments.json", "w", encoding='utf-8') as f:
            json.dump(filtered_comments, f, ensure_ascii=False, indent=4)
        return len(filtered_comments)
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return 0

def SignWithPost(count):
    nowtime = datetime.now().strftime("%m%d")

    signtxt = (
        f'[彩虹]三楼昵称：内向的猫\n'
        f'[彩虹]回复数量：{count}\n'
        f'[彩虹]签到时间：{nowtime}\n'
        f'[彩虹]今日总结：还不错'
    )

    reply(key, signtxt, 53841849, 0, '')

key = '8730472954AD29E4BFF3D283AD7B117C7B685B9DBCDC948E6A5ECE27126D028FC416D5E1D4A0C87D23BF7E4D1A985F1AF12550A5C55BCEF3'

commentscount = GetTodayComments()

SignWithPost(commentscount)
