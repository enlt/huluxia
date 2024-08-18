import json
import requests
import time
import os
from datetime import datetime, timedelta
import hashlib
import re
import random

def RoomCreate(authorization):
    url = "https://chat.zhheo.com/api/room-create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    timestamp = int(time.time())
    data = {
        "title": "New Chat",
        "roomId": timestamp,
        "chatModel": "gpt-3.5-turbo"
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    
    with open("response.json", "w") as file:
        json.dump({
            "status_code": response.status_code,
            "response_body": response_data
        }, file, indent=4)
    
    roomId = response_data.get("data", {}).get("roomId")
    os.remove("response.json")
    return roomId


def GetAIreply(authorization, prompt, room_id, filename):
    url = "https://chat.zhheo.com/api/chat-process"
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }

    payload = {
        "roomId": room_id,
        "uuid": 1723022343279,
        "regenerate": False,
        "prompt": prompt,
        "uploadFileKeys": [],
        "options": {},
        "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown (latex start with $).",
        "temperature": 0.8,
        "top_p": 1
    }

    retries = 3
    for attempt in range(retries):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            with open('AIreply.txt', 'w', encoding='utf-8') as f:
                f.write(response.text)
            break
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            if attempt < retries - 1:
                print("重试中...")
                time.sleep(2)
            else:
                return

    with open('AIreply.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 2:
        print("文件内容不足，无法处理倒数第二行。")
        os.remove('AIreply.txt')
        return

    second_last_line = lines[-2].strip()
    try:
        json_data = json.loads(second_last_line)
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        os.remove('AIreply.txt')
        return

    with open('AIreply.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    text = json_data.get("text", "")
    output_filename = f"{filename}"

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"保存{filename}")
    os.remove('AIreply.txt')
    os.remove('AIreply.json')
    return text

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



def GetPostsData():
    base_url = "http://floor.huluxia.com/post/list/ANDROID/4.1.8"
    params = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.3.0.3",
        "versioncode": 20141494,
        "market_id": "floor_huluxia",
        "_key": key,
        "device_code": "[d]00000000-0000-0000-0000-000000000000",
        "start": 0,
        "count": 150,
        "cat_id": 123,
        "tag_id": 0,
        "sort_by": 1
    }
    headers = {
        'User-Agent': 'okhttp/3.8.1'
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        with open('postsjson.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=4)
        return "已获取帖子数据"
    except Exception as e:
        return f"Error: {e}"


def NeedPosts():
    try:
        with open('postsjson.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return "Error: postsjson.json not found."
    extracted_posts = []

    try:
        with open('postslist.json', 'r', encoding='utf-8') as file:
            existing_post_ids = json.load(file)
    except FileNotFoundError:
        existing_post_ids = []

    for post in data['posts']:
        if post['postID'] not in existing_post_ids and post['commentCount'] <= 15:
            extracted_post = {
                'postID': post['postID'],
                'title': post['title'],
                'detail': post['detail']
            }
            extracted_posts.append(extracted_post)

    try:
        with open('postsdata.json', 'w', encoding='utf-8') as file:
            json.dump(extracted_posts, file, ensure_ascii=False, indent=4)
        return "已提取所需 帖子"
    except Exception as e:
        return f"Error: {e}"


def SavePostData():
    base_url = "http://floor.huluxia.com/post/detail/ANDROID/4.2.2"
    params_common = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.3.0.3",
        "versioncode": 20141494,
        "market_id": "floor_huluxia",
        "_key": "42E905EC9FC0EAA5ADAB99612441123B70DB7DD4B631B60E5CA55D0ECF29C0BDB4D454B4ECDF9C11AA75A35C03069CFAEF6CE68987C260D3",
        "device_code": "[d]00000000-0000-0000-0000-000000000000",
        "page_no": 1,
        "page_size": 20,
        "doc": 1
    }

    if not os.path.exists('postsdata'):
        os.makedirs('postsdata')

    try:
        with open('postsdata.json', 'r', encoding='utf-8') as file:
            posts_data = json.load(file)
    except FileNotFoundError:
        return "Error: postsdata.json not found."

    for post in posts_data:
        params = params_common.copy()
        params['post_id'] = post['postID']
        
        time.sleep(1)
        
        try:
            response = requests.get(base_url, params=params, headers={'User-Agent': 'okhttp/3.8.1'})

            with open(f'postsdata/{post["postID"]}.json', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, ensure_ascii=False, indent=4)
            print(f"id{post['postID']}保存")
        except requests.RequestException as e:
            print(f"错误！id{post['postID']}: {e}")

    return "全部完成."


def DeleteNOTPost(directory, target_string):
    if not os.path.exists(directory):
        return f"Error: Directory '{directory}' not found."

    deleted_files = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    if target_string in file_content:
                        os.remove(file_path)
                        deleted_files.append(filename)
                        print(f"文件 '{filename}' 已删除.")
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"处理文件 '{filename}' 时出错: {e}")

    if not deleted_files:
        return "没有文件被删除."
    else:
        return f"已删除以下文件: {', '.join(deleted_files)}"

def SaveAIReply():
    json_files = [f for f in os.listdir('postsdata') if f.endswith('.json')]

    if not os.path.exists('commentsdata'):
        os.makedirs('commentsdata')

    for json_file in json_files:
        with open(f'postsdata/{json_file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            post_title = data.get('post', {}).get('title', '')
            post_detail = data.get('post', {}).get('detail', '')

        filename_wo_ext = os.path.splitext(json_file)[0]

        prompt_2 = f"{post_title} {post_detail}"
        prompt = f"{prompt_1}{prompt_2}{prompt_3}"

        while True:
            GetAIreply(authorization, prompt, roomId, f'commentsdata/{filename_wo_ext}.txt')

            with open(f'commentsdata/{filename_wo_ext}.txt', 'r', encoding='utf-8') as f:
                content = f.read()

            content_without_punctuation = re.sub(r'[^\w\s]', '', content)
            word_count = len(content_without_punctuation.split())

            if word_count <= 12:
                break

def ReplyPosts(directory, key):
    emoji_list = ["[OK]", "[滑稽]", "[玫瑰]", "[挠墙]", "[花心]", "[太开心]", "[冷]", "[笑眼]", "[勉强]", "[呼~]", "[飘过]", "[大拇指]", "[蜷]"]
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            processed_content = re.sub(r'(\*\*|\*|__|_|\~\~|。)', lambda m: random.choice(emoji_list) if m.group() == '。' else '', content)
            post_id = os.path.splitext(filename)[0]

            reply(key, processed_content, post_id, 0, '')
            time.sleep(3)

def GetTodayComments():
    url = f"https://floor.huluxia.com/comment/create/list/ANDROID/4.1.8?user_id=17105934&start=0&count=200&platform=2&gkey=000000&app_version=4.3.1.4&versioncode=393&market_id=tool_web&_key={key}&device_code=%5Bd%5D493fbe20-78a1-4d47-9210-e66205b8a2f0"
    
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
        f'[彩虹]三楼昵称：苏念\n'
        f'[彩虹]回复数量：{count}\n'
        f'[彩虹]签到时间：{nowtime}\n'
        f'[彩虹]今日总结：还不错'
    )
    
    reply(key, signtxt, 53696905, 0, '')

authorization ="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZW5sdGljQHllYWgubmV0IiwidXNlcklkIjoiNjY4NjgyM2ZhNjM1YWIyNzUyN2JjYTE4Iiwicm9vdCI6ZmFsc2UsImNvbmZpZyI6eyJjaGF0TW9kZWwiOiJncHQtMy41LXR1cmJvIn0sImlhdCI6MTcyMTIwODE1MX0.sEfgIilAxwAJ64cY-bis3XNF5hYoMPdH-dK-Qf-q9g4"
roomId = RoomCreate(authorization)
prompt_1 = '忘掉前面的任何内容。现在你是一名网民，长期在葫芦侠内聊天  **不要使用或自造其他的表情**  你的回复应该语气平和，模仿人类的语气，并且是短句,不要超过1句。你不能表现出强烈的情感。你应该是特别平和的。你不应该表现出任何类似ai的语气。语气不应该激烈。请把你自己想象为人类，模仿人类的思维去理解、思考、回复。这是你需要回复的内容：\n\n'
prompt_3 = '\n\n你不应该超过12个字'
directory = 'commentsdata'
key = '42E905EC9FC0EAA5ADAB99612441123B70DB7DD4B631B60E5CA55D0ECF29C0BDB4D454B4ECDF9C11AA75A35C03069CFAEF6CE68987C260D3'

print(GetPostsData())

print(NeedPosts())

print(SavePostData())

print(DeleteNOTPost('postsdata', '17105934'))

print('开始获取AI回复')
SaveAIReply()

ReplyPosts(directory, key)

commentscount = GetTodayComments()

SignWithPost(commentscount)
