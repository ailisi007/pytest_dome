import requests


class ReDate():
    def __init__(self):
        # 获取url
        self.url ="http://kdtx-test.itheima.net"
        # 获取headers
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
            "Content-Type":"application/json"
        }
        # 获取session
        self.session = requests.session()

# 获取验证码函数
    def get_yzm(self):
        # 获取url
        url =self.url + "/api/captchaImage"      #字符串拼接
        # 获取请求头
        headers = self.headers
        # 定义请求数据
        reData = self.session.get(url = url,headers = headers)
        #返回响应数据
        return reData

# 获取（登录）函数
    def get_token(self,username,password,code,uuid):
        # 获取url
        url = self.url + "/api/login"
        # 获取header
        headers = self.headers
        # 获取body
        body ={
            "username":username,
            "password":password,
            "code":code,
            "uuid":uuid,
        }
        # 发送请求
        response = self.session.post(url = url,json = body,headers = headers)
        # 获取响应结果
        return response

    # 关闭会话
    def close_session(self):
        # 关闭session，释放里面的数据
        self.session.close()