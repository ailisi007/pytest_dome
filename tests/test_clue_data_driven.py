# -*- coding: utf-8 -*-
"""
线索管理 —— 数据驱动测试
========================
和课程测试一样，用「数据驱动」的方式：
  - 测试数据放在 data/clue_data.py
  - 本文件只写一份测试逻辑，pytest 的 @parametrize 自动把每条数据跑一遍
"""
import time
import pytest
from data.clue_data import ADD_CLUE_TEST_DATA, QUERY_CLUE_TEST_DATA


class TestClueAdd:
    """插入线索 测试类（数据驱动）"""

    @pytest.mark.parametrize("test_case", ADD_CLUE_TEST_DATA)
    def test_add_clue_data_driven(self, logged_in_client, test_case):
        """插入线索用例。

        参数：
          logged_in_client：conftest.py 里定义好的「已登录客户端」夹具
          test_case        ：一条测试数据（一个字典）
        """
        # ---- 第 1 步：从测试数据里取字段 ----
        test_id = test_case["id"]
        description = test_case["description"]
        clue = test_case["clue"]
        experience = test_case["experience"]

        phone = "186" + str(int(time.time()))[-8:]

        print(f"\n{'=' * 60}")
        print(f"执行测试用例：{test_id} - {description}")
        print(f"请求参数：{clue}")

        # ---- 第 2 步：发送插入线索请求 ----
        response = logged_in_client.add_clue(
            name=clue["name"],
            phone=phone,
            channel=clue.get("channel", "0"),
            sex=clue.get("sex", 0),
            age=clue.get("age", 20),
            weixin=clue.get("weixin", ""),
            qq=clue.get("qq", ""),
        )

        # ---- 第 3 步：验证响应 ----
        assert response.status_code == 200
        data = response.json()
        print(f"响应数据：{data}")

        assert data["code"] == experience["code"], \
            f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
        if "msg" in experience:
            assert data["msg"] == experience["msg"], \
                f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        print(f" 用例 {test_id} 通过!")


class TestClueQuery:
    """查询线索 测试类（数据驱动）"""

    @pytest.mark.parametrize("test_case", QUERY_CLUE_TEST_DATA)
    def test_query_clue_data_driven(self, logged_in_client, test_case):
        """查询线索用例。"""
        # ---- 第 1 步：从测试数据里取字段 ----
        test_id = test_case["id"]
        description = test_case["description"]
        params = test_case["params"]
        experience = test_case["experience"]

        print(f"\n{'=' * 60}")
        print(f"执行测试用例：{test_id} - {description}")
        print(f"查询参数：{params}")

        # ---- 第 2 步：发送查询请求 ----
        response = logged_in_client.get_clue_list(
            phone=params.get("phone", ""),
        )

        # ---- 第 3 步：验证响应 ----
        assert response.status_code == 200
        data = response.json()
        print(f"响应数据：{data}")

        assert data["code"] == experience["code"], \
            f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
        if "msg" in experience:
            assert data["msg"] == experience["msg"], \
                f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        # ---- 第 4 步：如果需要，验证是否能查到数据 ----
        if experience.get("has_data", False):
            assert data["total"] > 0, \
                f"用例 {test_id} 失败: 期望能查到数据，实际 total=0"
            assert len(data.get("rows", [])) > 0, \
                f"用例 {test_id} 失败: rows 为空"
            print(f" 查到 {data['total']} 条线索")

        print(f" 用例 {test_id} 通过!")