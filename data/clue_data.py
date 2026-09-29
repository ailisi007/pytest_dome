# -*- coding: utf-8 -*-
"""线索管理测试数据"""

# ==================== 插入线索测试数据 ====================
ADD_CLUE_TEST_DATA = [
    {
        "id": "TEST_CLUE_ADD_001",
        "description": "正常插入线索--成功",
        "clue": {
            "name": "温国平",
            "phone": "18695235796",
            "channel": "0",
            "sex": 0,
            "age": 20,
            "weixin": "sdsadwwcs",
            "qq": "",
        },
        "experience": {
            "code": 200,
            "msg": "操作成功",
        },
    },
]


# ==================== 查询线索测试数据 ====================
QUERY_CLUE_TEST_DATA = [
    {
        "id": "TEST_CLUE_QUERY_001",
        "description": "查询所有线索--成功（不传手机号）",
        "params": {},
        "experience": {
            "code": 200,
            "msg": "查询成功",
            "has_data": True,
        },
    },
    {
        "id": "TEST_CLUE_QUERY_002",
        "description": "按手机号查询线索--成功",
        "params": {
            "phone": "18695235796",
        },
        "experience": {
            "code": 200,
            "msg": "查询成功",
            "has_data": True,
        },
    },
]