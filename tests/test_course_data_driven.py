# -*- coding: utf-8 -*-
"""
课程管理 —— 数据驱动测试
========================
和登录测试一样，用「数据驱动」的方式：
  - 测试数据放在 data/course_data.py
  - 本文件只写一份测试逻辑，pytest 的 @parametrize 自动把每条数据跑一遍
"""
import pytest
from data.course_data import ADD_COURSE_TEST_DATA, QUERY_COURSE_TEST_DATA

class TestCourseAdd:
    """新增课程 测试类（数据驱动）"""

    # @pytest.mark.parametrize：参数化，把 ADD_COURSE_TEST_DATA 里每条数据喂给 test_case
    @pytest.mark.parametrize("test_case", ADD_COURSE_TEST_DATA)
    def test_add_course_data_driven(self, logged_in_client, test_case):
        """新增课程用例。

        参数（都由 pytest 自动注入）：
          logged_in_client：conftest.py 里定义好的「已登录客户端」夹具
          test_case        ：一条测试数据（一个字典）
        """
        # ---- 第 1 步：从测试数据里取字段 ----
        test_id = test_case["id"]               # 用例编号
        description = test_case["description"]  # 用例描述
        course = test_case["course"]            # 要添加的课程信息（字典）
        experience = test_case["experience"]    # 期望结果（code / msg）
        check_exists = test_case.get("check_exists", False)  # 添加后是否验证存在

        print(f"\n{'=' * 60}")   # 打印分隔线（'=' 重复 60 次）
        print(f"执行测试用例：{test_id}-{description}")
        print(f"请求参数：{course}")

        # ---- 第 2 步：发送新增课程请求 ----
        # 注意：数据里字段叫 applicableperson（无下划线），
        #       但接口参数名是 applicable_person（有下划线），这里做了映射。
        response = logged_in_client.add_course(
            name=course["name"],
            subject=course["subject"],
            price=course["price"],
            applicable_person=course["applicableperson"],
            info=course.get("info", ""),  # info 是可选字段，用 get 取，缺省给空串
        )

        # ---- 第 3 步：验证响应 ----
        assert response.status_code == 200  # HTTP 状态码 200
        data = response.json()             # 把响应体解析成字典
        print(f"响应数据：{data}")

        # 断言业务状态码和提示信息，和期望一致
        assert data["code"] == experience["code"], \
            f"用例 {test_id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"
        if "msg" in experience:  # 期望里写了 msg 才校验
            assert data["msg"] == experience["msg"], \
                f"用例 {test_id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"

        print(f"✅ 断言通过: code={data['code']}, msg={data['msg']}")

        # ---- 第 4 步：如果需要，验证课程是否真的添加成功 ----
        if check_exists and experience["code"] == 200:
            # 用课程名称去查列表，确认能查到刚添加的课程
            list_response = logged_in_client.get_course_list(name=course["name"])
            list_data = list_response.json()

            assert list_data["code"] == 200  # 查询接口业务成功
            # 列表接口返回 {"total":N, "rows":[...]}，rows 是课程数组
            assert len(list_data.get("rows", [])) > 0, \
                f"课程 '{course['name']}' 未在列表中找到"

            # 验证查到的第一条课程信息是否正确
            found_course = list_data["rows"][0]
            assert found_course["name"] == course["name"], \
                f"课程名称不匹配: {found_course['name']} != {course['name']}"
            assert found_course["price"] == course["price"], \
                f"课程价格不匹配: {found_course['price']} != {course['price']}"

            course_id = found_course["id"]
            print(f"✅ 验证通过: 课程已存在，ID={course_id}")
        print(f"✅ 用例 {test_id} 通过!")
