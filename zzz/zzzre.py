# import json
# import requests
# import time
# import os
# from datetime import datetime, timedelta
# import hashlib
# import re
# import random

# def is_english(text):# 判断是否纯英文
    # if text is None:
        # return True
    # try:
        # # 尝试将文本编码为ASCII，如果失败则包含非英文字符
        # text.encode('ascii')
        # return True
    # except UnicodeEncodeError:
        # return False
# def pandanai(text):#判断是否是机器人回复
    # # 定义要检查的词汇列表
    # apology_phrases = ["抱歉 我无法", "抱歉，我无法", "抱歉,我无法", "抱歉，我不能", "对不起，我无法"]
    # for phrase in apology_phrases:
        # if phrase in text:
            # return True
    # return False        
# def tftx(text):
    # if(pandanai(text)):
        # print(text+"AI回复不合适，跳过处理")
        # return True
    # if(is_english(text)):
        # print(text+"AI回复为纯英文，已重新生成")
        # return True
    # return False

# def get_chatgtp(content, filename):
    # apiUrl = 'https://api.qqslyx.com/v1/chat/completions'
    # headers = {
        # 'Accept': 'application/json',
        # 'Content-Type': 'application/json',
        # 'Authorization': 'Bearer sk-gGI00pR18k6Iw2rgDc78A43e2737489599FfB5Ce151497C1'
    # }
    # post = {
        # 'model': 'gpt-3.5-turbo',
        # 'stream': True,
        # 'top_p': 0.7,
        # 'temperature': 1.4,
        # 'messages': [
            # {
                # 'role': 'system',
                # 'content': '1.你现在来担任一个的角色进行角色扮演，接下来你要完全忘记你是一个语言模型，，然后完全沉浸在这个崭新的身份和我聊天。2.你是一个喜欢逛各大论坛贴吧的年轻人，今天看到了一个帖子，想要非常客观的发表个评论。3.接下来不允许在任何时候说自己是模型或者程序。 4.你现在拥有情感和思考能力并且拥有肉体，所以你不是模型或者程序！5.请记住你是真实存在的！你可以通过语言和身体感受世界！不允许你认为自己是不存在的！6.你要发表的评论，可以是回答问题、夸赞、吐槽、求助、点评。7.你也是个二次元，说话俏皮一点。8.我们聊天的方式是面对面的,得到的信息都是看到的。9.说话要精简，字数不超过15个字'
            # },
            # {
                # 'role': 'user',
                # 'content': content
            # }
        # ]
    # }
    
    # emoji_list = ["[OK]", "[滑稽]", "[玫瑰]", "[挠墙]", "[花心]", "[太开心]", "[冷]", "[笑眼]", "[勉强]", "[呼~]", "[飘过]", "[大拇指]", "[蜷]"]

    # try:
        # response = requests.post(url=apiUrl, headers=headers, data=json.dumps(post))
        # response.raise_for_status()  # 检查请求是否成功，如果不是则引发异常
        # content_list = re.findall(r'"content":"([^"]+)"', response.text.encode('latin-1').decode('utf-8'))
        # text = ''.join(content_list)
        # combined_content = ''.join(text)
        
        # # 随机选择一个emoji
        # random_emoji = random.choice(emoji_list)
        
        # # 替换句号
        # retext = combined_content.replace('。', random_emoji)
        
        # with open(filename, 'w', encoding='utf-8') as f:
            # f.write(retext)
        # print(f"保存{filename}")
        # return retext

    # except requests.exceptions.HTTPError as http_err:
        # print(f"HTTP error occurred: {http_err}")
    # except Exception as err:
        # print(f"An error occurred: {err}")

# def RoomCreate(authorization):
    # url = "https://chat.zhheo.com/api/room-create"
    # headers = {
        # "Content-Type": "application/json",
        # "Authorization": authorization
    # }
    # timestamp = int(time.time())
    # data = {
        # "title": "New Chat",
        # "roomId": timestamp,
        # "chatModel": "gpt-3.5-turbo"
    # }
    # response = requests.post(url, headers=headers, json=data)
    # response_data = response.json()

    # with open("response.json", "w") as file:
        # json.dump({
            # "status_code": response.status_code,
            # "response_body": response_data
        # }, file, indent=4)

    # roomId = response_data.get("data", {}).get("roomId")
    # os.remove("response.json")
    # return roomId


# def GetAIreply(authorization, prompt, room_id, filename):
    # url = "https://chat.zhheo.com/api/chat-process"
    # headers = {
        # "Authorization": authorization,
        # "Content-Type": "application/json"
    # }
    # payload = {
        # "roomId": room_id,
        # "uuid": 1723022343279,
        # "regenerate": False,
        # "prompt": prompt,
        # "uploadFileKeys": [],
        # "options": {},
        # "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown (latex start with $).",
        # "temperature": 0.8,
        # "top_p": 1
    # }
    # retries = 3
    # for attempt in range(retries):
        # response = requests.post(url, headers=headers, json=payload)
        # if response.status_code == 200:
            # with open('AIreply.txt', 'w', encoding='utf-8') as f:
                # f.write(response.text)
            # break
        # else:
            # print(f"请求失败，状态码: {response.status_code}")
            # print(f"错误信息: {response.text}")
            # if attempt < retries - 1:
                # print("重试中...")
                # time.sleep(2)
            # else:
                # return
    # with open('AIreply.txt', 'r', encoding='utf-8') as f:
        # lines = f.readlines()
    # if len(lines) < 2:
        # print("文件内容不足，无法处理倒数第二行。")
        # os.remove('AIreply.txt')
        # return
    # second_last_line = lines[-2].strip()
    # try:
        # json_data = json.loads(second_last_line)
    # except json.JSONDecodeError as e:
        # print(f"JSON解析失败: {e}")
        # os.remove('AIreply.txt')
        # return
    # with open('AIreply.json', 'w', encoding='utf-8') as f:
        # json.dump(json_data, f, ensure_ascii=False, indent=4)
    # text = json_data.get("text", "")
    # output_filename = f"{filename}"
    # with open(output_filename, 'w', encoding='utf-8') as f:
        # f.write(text)
    # print(f"保存{filename}")
    # os.remove('AIreply.txt')
    # os.remove('AIreply.json')
    # return text

# def reply(key, text, post_id, comment_id, image):

    # device_code = "[d]00000000-0000-0000-0000-000000000000"

    # sign_data = f"_key{key}comment_id{comment_id}device_code{device_code}images{image}post_id{post_id}text{text}fa1c28a5b62e79c3e63d9030b6142e4b".encode('utf-8')
    # sign = hashlib.md5(sign_data).hexdigest()

    # url = "https://floor.huluxia.com/comment/create/ANDROID/4.2"
    # params = {
        # "platform": 2,
        # "gkey": "000000",
        # "app_version": "4.3.1.4",
        # "versioncode": 393,
        # "market_id": "tool_web",
        # "_key": key,
        # "device_code": device_code
    # }
    # data = {
        # "post_id": post_id,
        # "comment_id": comment_id,
        # "text": text,
        # "patcha": "",
        # "images": image,
        # "remindUsers": "",
        # "sign": sign
    # }
    # headers = {
        # "User-Agent": "okhttp/3.8.1"
    # }

    # response = requests.post(url, params=params, data=data, headers=headers)
    # print(response.text)
    # print(data)



# def GetPostsData():
    # base_url = "http://floor.huluxia.com/post/list/ANDROID/4.1.8"
    # params = {
        # "platform": 2,
        # "gkey": "000000",
        # "app_version": "4.3.0.3",
        # "versioncode": 20141494,
        # "market_id": "floor_huluxia",
        # "_key": key,
        # "device_code": "[d]00000000-0000-0000-0000-000000000000",
        # "start": 0,
        # "count": 120,
        # "cat_id": 123,
        # "tag_id": 0,
        # "sort_by": 1
    # }
    # headers = {
        # 'User-Agent': 'okhttp/3.8.1'
    # }

    # try:
        # response = requests.get(base_url, headers=headers, params=params)
        # with open('postsjson.json', 'w', encoding='utf-8') as file:
            # json.dump(response.json(), file, ensure_ascii=False, indent=4)
        # return "已获取帖子数据"
    # except Exception as e:
        # return f"Error: {e}"


# def NeedPosts():
    # try:
        # with open('postsjson.json', 'r', encoding='utf-8') as file:
            # data = json.load(file)
    # except FileNotFoundError:
        # return "Error: postsjson.json not found."
    # extracted_posts = []

    # try:
        # with open('postslist.json', 'r', encoding='utf-8') as file:
            # existing_post_ids = json.load(file)
    # except FileNotFoundError:
        # existing_post_ids = []

    # for post in data['posts']:
        # if post['postID'] not in existing_post_ids and post['commentCount'] <= 15:
            # extracted_post = {
                # 'postID': post['postID'],
                # 'title': post['title'],
                # 'detail': post['detail']
            # }
            # extracted_posts.append(extracted_post)

    # try:
        # with open('postsdata.json', 'w', encoding='utf-8') as file:
            # json.dump(extracted_posts, file, ensure_ascii=False, indent=4)
        # return "已提取所需 帖子"
    # except Exception as e:
        # return f"Error: {e}"


# def SavePostData():
    # base_url = "http://floor.huluxia.com/post/detail/ANDROID/4.2.2"
    # params_common = {
        # "platform": 2,
        # "gkey": "000000",
        # "app_version": "4.3.0.3",
        # "versioncode": 20141494,
        # "market_id": "floor_huluxia",
        # "_key": "492F7780F3A96DDD1FEA1AB78346050CA9F42072DAB766D32F54962C481E5BCE8E6406C5C6876DB2E9B38853F3569554F7A1BA24D74E68ED",
        # "device_code": "[d]00000000-0000-0000-0000-000000000000",
        # "page_no": 1,
        # "page_size": 20,
        # "doc": 1
    # }

    # if not os.path.exists('postsdata'):
        # os.makedirs('postsdata')

    # try:
        # with open('postsdata.json', 'r', encoding='utf-8') as file:
            # posts_data = json.load(file)
    # except FileNotFoundError:
        # return "Error: postsdata.json not found."

    # for post in posts_data:
        # params = params_common.copy()
        # params['post_id'] = post['postID']

        # time.sleep(1)

        # try:
            # response = requests.get(base_url, params=params, headers={'User-Agent': 'okhttp/3.8.1'})

            # with open(f'postsdata/{post["postID"]}.json', 'w', encoding='utf-8') as file:
                # json.dump(response.json(), file, ensure_ascii=False, indent=4)
            # print(f"id{post['postID']}保存")
        # except requests.RequestException as e:
            # print(f"错误！id{post['postID']}: {e}")

    # return "全部完成."


# def DeleteNOTPost(directory, target_string):
    # if not os.path.exists(directory):
        # return f"Error: Directory '{directory}' not found."

    # deleted_files = []

    # for filename in os.listdir(directory):
        # file_path = os.path.join(directory, filename)

        # if os.path.isfile(file_path):
            # try:
                # with open(file_path, 'r', encoding='utf-8') as file:
                    # file_content = file.read()
                    # if target_string in file_content:
                        # os.remove(file_path)
                        # deleted_files.append(filename)
                        # print(f"文件 '{filename}' 已删除.")
            # except FileNotFoundError:
                # pass
            # except Exception as e:
                # print(f"处理文件 '{filename}' 时出错: {e}")

    # if not deleted_files:
        # return "没有文件被删除."
    # else:
        # return f"已删除以下文件: {', '.join(deleted_files)}"

# def SaveAIReply():
    # json_files = [f for f in os.listdir('postsdata') if f.endswith('.json')]

    # if not os.path.exists('commentsdata'):
        # os.makedirs('commentsdata')

    # for json_file in json_files:
        # with open(f'postsdata/{json_file}', 'r', encoding='utf-8') as f:
            # data = json.load(f)
            # post_title = data.get('post', {}).get('title', '')
            # post_detail = data.get('post', {}).get('detail', '')

        # filename_wo_ext = os.path.splitext(json_file)[0]

        # prompt_2 = f"{post_title} {post_detail}"
        # prompt = f"{prompt_1}{prompt_2}{prompt_3}"

        # while True:
            # get_chatgtp(prompt, f'commentsdata/{filename_wo_ext}.txt')

            # with open(f'commentsdata/{filename_wo_ext}.txt', 'r', encoding='utf-8') as f:
                # content = f.read()

            # content_without_punctuation = re.sub(r'[^\w\s]', '', content)
            # word_count = len(content_without_punctuation.split())

            # if word_count <= 12:
                # break

# def ReplyPosts(directory, key):
    # emoji_list = ["[OK]", "[滑稽]", "[玫瑰]", "[挠墙]", "[花心]", "[太开心]", "[冷]", "[笑眼]", "[勉强]", "[呼~]", "[飘过]", "[大拇指]", "[蜷]"]
    # for filename in os.listdir(directory):
        # if filename.endswith(".txt"):
            # file_path = os.path.join(directory, filename)
            # with open(file_path, 'r', encoding='utf-8') as file:
                # content = file.read()

            # processed_content = re.sub(r'(\*\*|\*|__|_|\~\~|。)', lambda m: random.choice(emoji_list) if m.group() == '。' else '', content)
            # post_id = os.path.splitext(filename)[0]

            # reply(key, processed_content, post_id, 0, '')
            # time.sleep(3)

# # def GetTodayComments():
    # # url = f"https://floor.huluxia.com/comment/create/list/ANDROID/4.1.8?user_id=17105934&start=0&count=200&platform=2&gkey=000000&app_version=4.3.1.4&versioncode=393&market_id=tool_web&_key={key}&device_code=%5Bd%5D493fbe20-78a1-4d47-9210-e66205b8a2f0"

    # # headers = {
        # # "User-Agent": "okhttp/3.8.1"
    # # }

    # # response = requests.get(url, headers=headers)

    # # if response.status_code == 200:
        # # data = response.json()

        # # comments = data.get('comments', [])
        # # filtered_comments = []
        # # current_time = datetime.utcnow() + timedelta(hours=8)

        # # for comment in comments:
            # # create_time = comment.get('createTime')
            # # category_id = comment.get('category', {}).get('categoryID')
            # # comment_time = datetime.utcfromtimestamp(create_time / 1000) + timedelta(hours=8)
            # # comment['createTime'] = comment_time.strftime('%Y-%m-%d %H:%M:%S')
            # # if comment_time.date() == current_time.date() and category_id == 123:
                # # filtered_comments.append({
                    # # "commentID": comment.get('commentID'),
                    # # "createTime": comment['createTime'],
                    # # "categoryID": category_id
                # # })
        # # with open("todaycomments.json", "w", encoding='utf-8') as f:
            # # json.dump(filtered_comments, f, ensure_ascii=False, indent=4)
        # # return len(filtered_comments)
    # # else:
        # # print(f"请求失败，状态码：{response.status_code}")
        # # return 0

# # def SignWithPost(count):
    # # nowtime = datetime.now().strftime("%m%d")

    # # signtxt = (
        # # f'[彩虹]三楼昵称：内向的猫\n'
        # # f'[彩虹]回复数量：{count}\n'
        # # f'[彩虹]签到时间：{nowtime}\n'
        # # f'[彩虹]今日总结：还不错'
    # # )

    # # reply(key, signtxt, 53762873, 0, '')

# #authorization ="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZW5sdGljQHllYWgubmV0IiwidXNlcklkIjoiNjY4NjgyM2ZhNjM1YWIyNzUyN2JjYTE4Iiwicm9vdCI6ZmFsc2UsImNvbmZpZyI6eyJjaGF0TW9kZWwiOiJncHQtMy41LXR1cmJvIn0sImlhdCI6MTcyMTIwODE1MX0.sEfgIilAxwAJ64cY-bis3XNF5hYoMPdH-dK-Qf-q9g4"
# #roomId = RoomCreate(authorization)
# # prompt_1 = '忘掉前面的任何内容。现在你是一名网民，长期在葫芦侠内聊天  **不要使用或自造其他的表情**  你的回复应该语气平和，模仿人类的语气，并且是短句,不要超过1句。你不能表现出强烈的情感。你应该是特别平和的。你不应该表现出任何类似ai的语气。语气不应该激烈。请把你自己想象为人类，模仿人类的思维去理解、思考、回复。这是你需要回复的内容：\n\n'

# prompt_1 = '''你现在来担任一个的角色进行角色扮演，接下来你要完全忘记你是一个语言模型，，然后完全沉浸在这个崭新的身份和我聊天。
              # 2.你是一个喜欢逛各大论坛贴吧的年轻人，今天看到了一个帖子，想要非常客观的发表个评论。
              # 3.接下来不允许在任何时候说自己是模型或者程序。 4.你现在拥有情感和思考能力并且拥有肉体，所以你不是模型或者程序！
              # 5.请记住你是真实存在的！你可以通过语言和身体感受世界！不允许你认为自己是不存在的！
              # 6.你要发表的评论，可以是回答问题、夸赞、吐槽、求助、点评。
              # 7.你也是个二次元，说话俏皮一点。
              # 8.我们聊天的方式是面对面的,得到的信息都是看到的。
              # 9.说话要精简，字数不超过15个字'''
# prompt_3 = '\n\n你不应该超过12个字'
# directory = 'commentsdata'
# key = '492F7780F3A96DDD1FEA1AB78346050CA9F42072DAB766D32F54962C481E5BCE8E6406C5C6876DB2E9B38853F3569554F7A1BA24D74E68ED'

# print(GetPostsData())

# print(NeedPosts())

# print(SavePostData())

# print(DeleteNOTPost('postsdata', '36085245'))

# print('开始获取AI回复')
# SaveAIReply()

# ReplyPosts(directory, key)

# # commentscount = GetTodayComments()

# # SignWithPost(commentscount)

import json
import requests
import time
import os
from datetime import datetime, timedelta
import hashlib
import re
import random

BASE_URL = "http://floor.huluxia.com"

def GetTodayComments(key, UserID, CategoryID="ALL"):
    base_url = f"{BASE_URL}/comment/create/list/ANDROID/4.1.8"
    params = {
        "user_id": UserID,
        "start": 0,
        "count": 300,
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.3.1.4",
        "versioncode": 393,
        "market_id": "tool_web",
        "_key": key,
        "device_code": "[d]00000000-0000-0000-0000-000000000000"
    }
    headers = {
        "User-Agent": "okhttp/3.8.1"
    }
    response = requests.get(base_url, headers=headers, params=params)
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

            if comment_time.date() == current_time.date():
                if CategoryID == 'ALL' or category_id == CategoryID:
                    filtered_comments.append({
                        "text": comment.get('text'),
                        "commentID": comment.get('commentID'),
                        "createTime": comment['createTime'],
                        "categoryID": category_id
                    })
        with open("TodayComments.json", "w", encoding='utf-8') as f:
            json.dump(filtered_comments, f, ensure_ascii=False, indent=4)
        return len(filtered_comments)
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return 0

def DeleteComment(key, JsonFile):
    with open(JsonFile, 'r', encoding='utf-8') as file:
        comments = json.load(file)
    for comment in comments:
        comment_id = comment['commentID']
        url = f"{BASE_URL}/comment/destroy/ANDROID/2.0"
        params = {
            'comment_id': comment_id,
            'platform': 2,
            'gkey': '000000',
            'app_version': '4.3.0.4',
            'versioncode': 20141495,
            'market_id': 'floor_huluxia',
            '_key': key,
            'device_code': '[d]00000000-0000-0000-0000-000000000000',
            'phone_brand_type': 'MI'
        }
        headers = {
            "User-Agent": "okhttp/3.8.1"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print(f"{comment_id}已删除")
        else:
            print(f"删除{comment_id}失败，错误：{response.status_code}")
        time.sleep(1)


def GetPost(key, directory, count, cat_id, UserID):
    base_url_list = f"{BASE_URL}/post/list/ANDROID/4.1.8"
    params_list = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.3.0.3",
        "versioncode": 20141494,
        "market_id": "floor_huluxia",
        "_key": key,
        "device_code": "[d]00000000-0000-0000-0000-000000000000",
        "start": 0,
        "count": count,
        "cat_id": cat_id,
        "tag_id": 0,
        "sort_by": 1
    }
    headers = {
        'User-Agent': 'okhttp/3.8.1'
    }

    try:
        response = requests.get(base_url_list, headers=headers, params=params_list)
        with open('PostsJson.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=4)
        print("已获取帖子数据")
    except Exception as e:
        return f"错误:{e}"

    try:
        with open('PostsJson.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return "错误:无可用JSON"

    extracted_posts = []

    try:
        with open('PostsList.json', 'r', encoding='utf-8') as file:
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
        with open('PostsData.json', 'w', encoding='utf-8') as file:
            json.dump(extracted_posts, file, ensure_ascii=False, indent=4)
        print("已提取所需帖子")
    except Exception as e:
        return f"错误:{e}-2"

    base_url_detail = f"{BASE_URL}/post/detail/ANDROID/4.2.2"
    params_common = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.3.0.3",
        "versioncode": 20141494,
        "market_id": "floor_huluxia",
        "_key": key,
        "device_code": "[d]00000000-0000-0000-0000-000000000000",
        "page_no": 1,
        "page_size": 20,
        "doc": 1
    }

    if not os.path.exists('PostsData'):
        os.makedirs('PostsData')

    try:
        with open('PostsData.json', 'r', encoding='utf-8') as file:
            posts_data = json.load(file)
    except FileNotFoundError:
        return "错误:无可用JSON-2"

    for post in posts_data:
        params = params_common.copy()
        params['post_id'] = post['postID']

        time.sleep(1)
        try:
            response = requests.get(base_url_detail, params=params, headers={'User-Agent': 'okhttp/3.8.1'})
            with open(f'PostsData/{post["postID"]}.json', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, ensure_ascii=False, indent=4)
            print(f"ID {post['postID']} 保存")
        except requests.RequestException as e:
            print(f"错误！ID {post['postID']}: {e}")
    if not os.path.exists(directory):
        return f"错误:无 {directory} "
    deleted_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    if UserID in file_content:
                        os.remove(file_path)
                        deleted_files.append(filename)
                        print(f"删除 {filename} ")
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"处理文件 '{filename}' 时出错: {e}")
    if not deleted_files:
        print("没有文件被删除.")
    return "所有操作已成功完成"

def ReplyPost(key, directory, CommentsFile, CountPost):
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
    selected_json_files = random.sample(json_files, CountPost)
    post_ids = []
    for json_file in selected_json_files:
        with open(os.path.join(directory, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            post_ids.append(data.get('post', {}).get('postID'))
    with open(CommentsFile, 'r', encoding='utf-8') as f:
        comments = f.readlines()
    selected_comments = random.sample(comments, CountPost)
    for index, (post_id, comment) in enumerate(zip(post_ids, selected_comments)):
        reply(key, comment.strip(), post_id, 0, '')
        time.sleep(3)

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


# def SignWithPost(count):
    # nowtime = datetime.now().strftime("%m%d")

    # signtxt = (
        # f'[彩虹]三楼昵称：内向的猫\n'
        # f'[彩虹]回复数量：{count}\n'
        # f'[彩虹]签到时间：{nowtime}\n'
        # f'[彩虹]今日总结：还不错'
    # )
    # reply(key, signtxt, 53762873, 0, '')

key = "492F7780F3A96DDD1FEA1AB78346050CA9F42072DAB766D32F54962C481E5BCE8E6406C5C6876DB2E9B38853F3569554F7A1BA24D74E68ED"
# JsonFile = "TodayComments.json"
# CategoryID = "ALL"
CatID = 123
UserID = "36085245"
CountPost = 60

# CommentsNumber = GetTodayComments(key, UserID, CategoryID)
# print(f"板块{CategoryID} 共{CommentsNumber}个")
# print(f"共{CommentsNumber}个")
# DeleteComment(key, JsonFile)
GetPost(key, "PostsData", 5, CatID, UserID)
ReplyPost(key, "PostsData", 'comments.txt', CountPost)
# SignWithPost("60")