# -*- coding: utf-8 -*-

import time
import allure
import pytest
from data.clue_data import ADD_CLUE_TEST_DATA, QUERY_CLUE_TEST_DATA


@allure.epic("线索管理")
@allure.feature("插入线索")
class TestClueAdd:
    """插入线索 测试类（数据驱动）"""

    @pytest.mark.parametrize("test_case", ADD_CLUE_TEST_DATA)
    @allure.story("数据驱动插入线索")
    @allure.title("{test_case[id]} - {test_case[description]}")
    def test_add_clue_data_driven(self, logged_in_client, test_case):
        """插入线索用例。"""
        # 从测试数据里取字段
        test_id = test_case["id"]
        description = test_case["description"]
        clue = test_case["clue"]
        experience = test_case["experience"]

        phone = "186" + str(int(time.time()))[-8:]

        # 用 allure.step 包裹关键步骤
        with allure.step("步骤1：组装测试数据"):
            # 把测试数据附加到报告里，方便查看
            allure.attach(str(test_case), name="测试数据", attachment_type=allure.attachment_type.TEXT)
            print(f"\n执行测试用例：{test_id} - {description}")

        with allure.step("步骤2：发送插入线索请求"):
            response = logged_in_client.add_clue(
                name=clue["name"],
                phone=phone,
                channel=clue.get("channel", "0"),
                sex=clue.get("sex", 0),
                age=clue.get("age", 20),
                weixin=clue.get("weixin", ""),
                qq=clue.get("qq", ""),
            )
            # 把响应附加到报告
            allure.attach(response.text, name="响应数据", attachment_type=allure.attachment_type.JSON)

        with allure.step("步骤3：验证响应"):
            assert response.status_code == 200
            data = response.json()

            assert data["code"] == experience["code"], \
                f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
            if "msg" in experience:
                assert data["msg"] == experience["msg"], \
                    f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        print(f" 用例 {test_id} 通过!")


@allure.epic("线索管理")
@allure.feature("查询线索")
class TestClueQuery:
    """查询线索 测试类（数据驱动）"""

    @pytest.mark.parametrize("test_case", QUERY_CLUE_TEST_DATA)
    @allure.story("数据驱动查询线索")
    @allure.title("{test_case[id]} - {test_case[description]}")
    def test_query_clue_data_driven(self, logged_in_client, test_case):
        """查询线索用例。"""
        test_id = test_case["id"]
        params = test_case["params"]
        experience = test_case["experience"]

        with allure.step("步骤1：准备查询参数"):
            allure.attach(str(params), name="查询参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送查询请求"):
            response = logged_in_client.get_clue_list(
                phone=params.get("phone", ""),
            )
            allure.attach(response.text, name="响应数据", attachment_type=allure.attachment_type.JSON)

        with allure.step("步骤3：验证响应"):
            assert response.status_code == 200
            data = response.json()

            assert data["code"] == experience["code"], \
                f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
            if "msg" in experience:
                assert data["msg"] == experience["msg"], \
                    f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

            if experience.get("has_data", False):
                assert data["total"] > 0, \
                    f"用例 {test_id} 失败: 期望能查到数据，实际 total=0"
                assert len(data.get("rows", [])) > 0, \
                    f"用例 {test_id} 失败: rows 为空"

        print(f" 用例 {test_id} 通过!")