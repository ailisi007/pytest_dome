import requests


class AIPClient:
    """AIPClient：对被测系统接口的统一封装。

    凡是「获取验证码、登录、课程管理」等接口，都通过这个类来调用。
    好处：URL、请求头、Token 管理等公共信息只写一次，测试代码更简洁。
    """

    # 被测系统的根地址（所有接口地址都从这里拼接）
    BASE_URL = "http://kdtx-test.itheima.net"

    def __init__(self):
        # 1) requests.Session()：创建一个「会话」。
        #    会话会自动保存 cookie、复用底层连接，比每次新建请求更高效。
        self.session = requests.Session()

        # 2) 公共请求头：告诉服务器「我是浏览器」「我发送的是 JSON 格式」。
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
        }

        # 3) 登录后拿到的 token 先存成空字符串，登录成功后再填进去
        self.token = ""

    # ==================== 基础接口 ====================

    def get_captcha(self):
        """获取验证码。

        返回：response（requests 的响应对象）
        响应体里主要有两个字段：
          - uuid：本次验证码的唯一标识（登录时要一起提交）
          - img ：验证码图片（base64 编码，需要人眼识别出数字）
        """
        url = self.BASE_URL + "/api/captchaImage"
        response = self.session.get(url, headers=self.headers)
        return response

    def login(self, username, password, code, uuid):
        """登录接口。登录成功后，自动保存 token 并放进请求头。

        参数：
          username : 用户名
          password : 密码
          code     : 验证码（图片里看到的数字）
          uuid     : 验证码唯一标识（来自 get_captcha）

        返回：response（登录结果）
        """
        url = self.BASE_URL + "/api/login"
        data = {
            "username": username,
            "password": password,
            "uuid": uuid,
            "code": code,
        }
        response = self.session.post(url, json=data, headers=self.headers)

        # 登录成功后，自动保存 token 并放进请求头
        if response.json().get("code") == 200:
            self.token = response.json()["token"]
            self.headers["Authorization"] = f"Bearer {self.token}"

        return response

    def close(self):
        """关闭会话，释放连接资源。"""
        self.session.close()

    # ==================== 课程管理接口 ====================

    def add_course(self, name, subject, price, applicable_person, info=""):
        """新增课程（需先登录）。

        参数：
          name             : 课程名称
          subject          : 学科
          price            : 价格
          applicable_person: 适用人群
          info             : 课程介绍（可选，默认空字符串）
        """
        url = self.BASE_URL + "/api/clues/course"
        data = {
            "name": name,
            "subject": subject,
            "price": price,
            "applicable_person": applicable_person,
            "info": info,
        }
        response = self.session.post(url, json=data, headers=self.headers)
        return response

    def get_course_list(self, name="", subject="", price="", applicable_person="", info=""):
        """查询课程列表（需先登录）。

        所有参数都是可选的：传了就按条件过滤，不传就查全部。
        """
        url = self.BASE_URL + "/api/clues/course/list"

        # 查询接口用 GET，参数用 params 拼在 URL 后面
        params = {}
        if name:
            params["name"] = name
        if subject:
            params["subject"] = subject
        if price is not None:
            params["price"] = price
        if applicable_person:
            params["applicable_person"] = applicable_person
        if info:
            params["info"] = info

        response = self.session.get(url, params=params, headers=self.headers)
        return response

    def get_course_by_id(self, course_id):
        """根据课程 id 查询单条课程。"""
        url = self.BASE_URL + f"/api/clues/course/{course_id}"
        response = self.session.get(url, headers=self.headers)
        return response

    # ==================== 线索管理接口 ====================

    def add_clue(self, name, phone, channel="0", sex=0, age=20, weixin="", qq="", activity_id=""):
        """插入线索（需先登录）。

        参数：
          name        : 姓名
          phone       : 手机号
          channel     : 渠道（默认 "0"）
          sex         : 性别（0/1）
          age         : 年龄
          weixin      : 微信号
          qq          : QQ号
          activity_id : 活动ID（可选，默认空字符串）
        """
        url = self.BASE_URL + "/api/clues/clue"
        data = {
            "activityId": activity_id,
            "name": name,
            "phone": phone,
            "channel": channel,
            "sex": sex,
            "age": age,
            "weixin": weixin,
            "qq": qq,
        }
        return self.session.post(url, json=data, headers=self.headers)

    def get_clue_list(self, phone=""):
        """查询线索（需先登录）。

        参数：
          phone : 手机号（可选，传了就按手机号过滤，不传就查全部）
        """
        url = self.BASE_URL + "/api/clues/clue/list"
        params = {}
        if phone:
            params["phone"] = phone
        return self.session.get(url, params=params, headers=self.headers)