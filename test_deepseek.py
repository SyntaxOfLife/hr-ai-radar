import requests
key = input("输入key: ")
r = requests.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": "Bearer " + key},
    json={"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10},
    timeout=15
)
print(r.status_code, r.text[:200])