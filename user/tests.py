from django.test import TestCase

# Create your tests here.
import uuid

print(uuid.uuid4())
a = {
                                    # 21207e9ddb1de777adeaca7a2fb38030
    "extensions": {"query": {"id": "21207e9ddb1de777adeaca7a2fb38030"}},
    "operationName": "", "query": "",
    "variables": {
        "after": "0.0909273991391759961", "first": 20, "order": "POPULAR"
    }
}

print(a)