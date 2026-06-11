import os
import requests
from collections import defaultdict

TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# 1. 获取所有 repo（包含 private）
repos = []
page = 1

while True:
    url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner"
    r = requests.get(url, headers=headers)
    data = r.json()

    if not data:
        break

    repos.extend(data)
    page += 1

lang_bytes = defaultdict(int)

# 2. 遍历每个 repo 的语言
for repo in repos:
    langs_url = repo["languages_url"]
    r = requests.get(langs_url, headers=headers)
    langs = r.json()

    for lang, size in langs.items():
        lang_bytes[lang] += size

# 3. 排序
sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)

labels = [x[0] for x in sorted_langs]
values = [x[1] for x in sorted_langs]

# 4. 生成 SVG
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title("Language Usage (Including Private Repos)")

plt.savefig("language.svg", bbox_inches="tight")
