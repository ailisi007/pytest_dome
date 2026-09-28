from email import header

import requests



# 发送请求
url = 'http://kdtx-test.itheima.net/api/captchaImage'


# 定义请求头
headers = {
    "user-Agent":"Mozilla/5.0",
    'Content-Type':'application/json'
}

# 发送请求
response = requests.get(url,headers=headers)

# 查看
print("="*50)
print('响应码',response.status_code)
print("响应头",response.headers)
print('响应内容：',response.text[:200]) #只显示前200个字符
print('json数据',response.json())

# 如果返回值是json，解析成字典
if response.status_code == 200:
    try:
        data = response.json()
        print("json数据",data)

    #     从字典中提取想要的字段
        code=data['code']
        uuid=data["uuid"]
        print(f"验证文字：{code}")
        print(f"唯一标识：{uuid}")

    except Exception as e:
        print("json解析失败")
else:
    print(f"请求失败，{response.status_code}")





url2 = "http://kdtx-test.itheima.net/api/login"



body_data={
    "username": "admin",
    "password": "HM_2023_test",
    "code": "2",
    "uuid": uuid
}

response = requests.post(url=url2,json=body_data,headers=headers)



if response.status_code == 200:
    reData = response.json()
    if reData.get("code") ==200:
        token = reData.get('token')
        print("token为",token)
    else:
        print("登陆失败")
else:
    print("请求失败")



