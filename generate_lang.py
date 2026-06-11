import os
import requests
from collections import defaultdict
import matplotlib.pyplot as plt

TOKEN = os.getenv("TOKEN")

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
    r = requests.get(repo["languages_url"], headers=headers)
    langs = r.json()
    for k, v in langs.items():
        lang_bytes[k] += v

sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)

labels = [x[0] for x in sorted_langs]
values = [x[1] for x in sorted_langs]

total = sum(values)
percentages = [v / total * 100 for v in values]

# =========================
# 🔥 关键：不用y轴标签，改成“干净图 + 右侧文字”
# =========================
plt.figure(figsize=(10, max(4, len(labels) * 0.25)))

y_pos = range(len(labels))

plt.barh(y_pos, percentages)

plt.yticks([])  # ❌ 关闭y轴文字（关键防重叠）

# 手动写文字（不会重叠）
for i, (lang, pct) in enumerate(zip(labels, percentages)):
    plt.text(
        pct + 0.5,   # 放在条形右侧
        i,
        f"{lang} {pct:.1f}%",
        va='center',
        fontsize=9
    )

plt.xlabel("Percentage (%)")
plt.title("Language Usage (Including Private Repos)")

plt.tight_layout()
plt.savefig("language.svg", bbox_inches="tight", dpi=150)
