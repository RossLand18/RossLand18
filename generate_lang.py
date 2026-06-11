import os
import requests
from collections import defaultdict
import matplotlib.pyplot as plt

TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

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

for repo in repos:
    langs_url = repo["languages_url"]
    r = requests.get(langs_url, headers=headers)
    langs = r.json()

    for lang, size in langs.items():
        lang_bytes[lang] += size

# 排序
sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)

labels = [x[0] for x in sorted_langs[:10]]  # 🔥 只取前10，避免拥挤
values = [x[1] for x in sorted_langs[:10]]

# 画水平条形图（不会重叠）
plt.figure(figsize=(8, 5))
plt.barh(labels[::-1], values[::-1])  # 反转让最大在上面

plt.title("Top Languages (Including Private Repos)")
plt.xlabel("Bytes of Code")

plt.tight_layout()
plt.savefig("language.svg", bbox_inches="tight")
