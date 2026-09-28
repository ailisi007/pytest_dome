# -*- coding: utf-8 -*-
import pytest
from src.testqingqiu import ReDate
from data.login_test import login_test_data


class TestLoginDataDriven:
    CORRECT_CAPTCHA = "2"


    @pytest.fixture(scope="function")
    def login_client(self):
        login_client = ReDate()
        yield login_client
        login_client.close_session()

    @pytest.fixture(scope="function")
    def captcha_client(self, login_client):
        response = login_client.get_yzm()
        assert response.status_code == 200
        data = response.json()
        return {"uuid": data["uuid"]}


    @pytest.mark.parametrize("test_case",login_test_data)
    def test_login_data_driven(self, login_client, captcha_client, test_case):

        test_id = test_case["id"]
        description = test_case["description"]
        username = test_case["username"]
        password = test_case["password"]
        code_type = test_case["code_type"]
        expected_code = test_case["expected_code"]
        expected_msg = test_case.get("expected_msg")
        check_token = test_case.get("check_token", False)


        code = self.CORRECT_CAPTCHA if code_type == "correct" else "9999"


        uuid = captcha_client["uuid"]


        print(f"\n执行用例：{test_id} - {description}")  
        response = login_client.get_token(
            username=username,
            password=password,
            uuid=uuid,
            code=code,
        )


        assert response.status_code == 200
        data = response.json()


        assert data["code"] == expected_code, \
            f"用例{test_id}失败：期望 code={expected_code}，实际 code={data['code']}"

        if expected_msg:
            assert data["msg"] == expected_msg, \
                f"用例{test_id}失败：期望 msg={expected_msg}，实际 msg={data['msg']}"

        if check_token:
            assert "token" in data
            assert data["token"] is not None and data["token"] != ""
            print(f"token:{data['token'][:30]}...")

        print(f"用例{test_id}通过！")
