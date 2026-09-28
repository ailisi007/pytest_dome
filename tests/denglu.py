

import pytest
from src.testqingqiu import ReDate

test_username = "1231",
test_password = "86156"
test_code = 2
class Test_login:
    @pytest.fixture(scope="function")
    def client(self):
        client = ReDate()
        yield client
        client.close_session()
    #     获取uuid
    @pytest.fixture(scope="function")
    def captcha_info(self, client):
        # 获取验证码
        response = client.get_yzm()
        assert response.status_code == 200
        data = response.json()
        uuid = data["uuid"]
        return {"uuid": uuid}

    def test_login_success(self, client:ReDate, captcha_info: dict):
        """用例1（正向）：正确用户名 + 正确密码 + 正确验证码 → 登录成功。"""
        uuid = captcha_info["uuid"]
        response = client.get_token(username=test_username, password=test_password, code=test_code,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "操作成功"
        assert "token" in data
        assert data["token"] is not None and data["token"] != ""

        print(f"登陆成功，token：{data['token']}")