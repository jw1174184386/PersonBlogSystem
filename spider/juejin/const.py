"""
        存放一些常量
"""

HEADERS = {
    'X-Agent':
        'Juejin/Web',
    'User-Agent':
        '{ua}',
    'Content-Type':
        'application/json',
}

DATA_RECOMMEND = '''{"extensions": {"query": {"id": "21207e9ddb1de777adeaca7a2fb38030"}},
    "operationName": "", "query": "",
    "variables": {
        "after": "{after}", "first": 20, "order": "POPULAR"
    }
}'''

DATA_BACKEND = '''{"extensions": {"query": {"id": "653b587c5c7c8a00ddf67fc66f989d42"}},
    "operationName": "",
    "query": "",
    "category": "5562b419e4b00c57d9b94ae2",
    "variables": {
        "after": "{after}", "first": 20, "order": "POPULAR", "tags": []
    }
}'''

DATA_CAREER = '''{"extensions": {"query": {"id": "653b587c5c7c8a00ddf67fc66f989d42"}},
    "operationName": "",
    "query": "",
    "category": "5c9c7cca1b117f3c60fee548",
    "variables": {
        "after": "{after}", "first": 20, "order": "POPULAR", "tags": []
    }
}'''


DATA_AI = '''{"extensions": {"query": {"id": "653b587c5c7c8a00ddf67fc66f989d42"}},
    "operationName": "",
    "query": "",
    "category": "57be7c18128fe1005fa902de",
    "variables": {
        "after": "{after}", "first": 20, "order": "POPULAR", "tags": []
    }
}'''

DATA_FRONTEND = '''{"extensions": {"query": {"id": "653b587c5c7c8a00ddf67fc66f989d42"}},
    "operationName": "",
    "query": "",
    "category": "5562b415e4b00c57d9b94ac8",
    "variables": {
        "after": "{after}", "first": 20, "order": "POPULAR", "tags": []
    }
}'''

DATA_LIST = [[DATA_RECOMMEND, 1], [DATA_BACKEND, 6], [DATA_CAREER, 7], [DATA_AI, 4], [DATA_FRONTEND, 9]]
DATA_DICT = [
    {'data': DATA_RECOMMEND, 'category': 1},
    {'data': DATA_AI, 'category': 4},
    {'data': DATA_BACKEND, 'category': 6},
    {'data': DATA_CAREER, 'category': 7},
    {'data': DATA_FRONTEND, 'category': 9},
]
