import requests  # 第三方库：用来发送 HTTP 请求（get / post 等）
class AIPClient:
    """AIPClient：对被测系统接口的统一封装。

    凡是「获取验证码、登录」等接口，都通过这个类来调用。
    好处：URL、请求头等公共信息只写一次，测试代码更简洁。
    """

    # 被测系统的根地址（所有接口地址都从这里拼接）
    Base_url = 'http://kdtx-test.itheima.net'

    def __init__(self):
        # 1) requests.Session()：创建一个「会话」。
        #    会话会自动保存 cookie、复用底层连接，比每次新建请求更高效。
        self.session = requests.Session()

        # 2) 公共请求头：告诉服务器「我是浏览器」「我发送的是 JSON 格式」。
        self.headers = {
        "User-Agent": "Mozilla/5.0(windows NT 10.0;Win64;x64) AppleWebKit/537.36",
        "Content-type" : "application/json"
        }
        # 3) 登录后拿到的 token 先存成空字符串，登录成功后再填进去
        self.token = ""

    def get_captcha(self):
        """获取验证码。

        返回：response（requests 的响应对象）
        响应体里主要有两个字段：
          - uuid：本次验证码的唯一标识（登录时要一起提交）
          - img ：验证码图片（base64 编码，需要人眼识别出数字）
        """
        url = self.Base_url + '/api/captchaImage'  # 拼接完整接口地址
        response = self.session.get(url, headers=self.headers)  # 发送 GET 请求
        return response
    def login(self,username,password,code,uuid):
        """登录接口。

        参数：
          username : 用户名
          password : 密码
          code     : 验证码（图片里看到的数字）
          uuid     : 验证码唯一标识（来自 get_captcha）

        返回：response（登录结果，成功时 body 里会带 token）
        """
        url = self.Base_url + '/api/login'  # 拼接完整接口地址

        # 要提交给服务器的数据（字典的键名必须和接口文档一致）
        data = {
            "username": username,
            "password": password,
            "uuid": uuid,
            "code": code,
        }

        # 关键点：用 json= 而不是 data= 发送。
        #   json= 会把字典自动转成 JSON 字符串；误用 data= 会被当成表单提交，服务器无法解析。
        response = self.session.post(url, json=data, headers=self.headers)
        return response

    def close(self):
        """关闭会话，释放连接资源。"""
        self.session.close()

    def set_token(self,token):
        self.token = token
        self.headers["Authorization"] = f"Bearer {self.token}"

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
            url = self.Base_url + '/api/clues/course'  # 新增课程的接口地址
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
            url = self.Base_url + '/api/clues/course/list'  # 查询列表的接口地址

            # 查询接口用 GET，参数用 params 拼在 URL 后面（而不是像新增那样放 body）
            params = {}
            if name:  # 传了名字，就按名字过滤
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
            # f-string 把课程 id 拼进地址里，例如 /api/clues/course/123
            url = self.Base_url + f'/api/clues/course/{course_id}'
            response = self.session.get(url, headers=self.headers)
            return response
