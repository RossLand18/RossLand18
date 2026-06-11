import os
import requests
from collections import defaultdict
import matplotlib.pyplot as plt

TOKEN = os.getenv("TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# =========================
# 1. 获取仓库
# =========================
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

# =========================
# 2. 统计语言
# =========================
lang_bytes = defaultdict(int)

for repo in repos:
    r = requests.get(repo["languages_url"], headers=headers)
    langs = r.json()
    for k, v in langs.items():
        lang_bytes[k] += v

# =========================
# ❗关键：过滤 HTML / CSS
# =========================
exclude_langs = {"HTML", "CSS"}

filtered_langs = [
    (lang, size)
    for lang, size in lang_bytes.items()
    if lang not in exclude_langs
]

# 排序
sorted_langs = sorted(filtered_langs, key=lambda x: x[1], reverse=True)

labels = [x[0] for x in sorted_langs]
values = [x[1] for x in sorted_langs]

# =========================
# 3. GitHub 颜色
# =========================
github_colors = {
    "Java": "#b07219",
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Shell": "#89e051",
    "Dockerfile": "#384d54",
    "Kotlin": "#A97BFF",
    "Go": "#00ADD8",
    "C": "#555555",
    "C++": "#f34b7d",
}

colors = [github_colors.get(lang, "#9e9e9e") for lang in labels]

# =========================
# 4. 上下分层（按占比）
# =========================
total = sum(values)

mid = len(labels) // 2

top_labels = labels[:mid]
bottom_labels = labels[mid:]

top_colors = colors[:mid]
bottom_colors = colors[mid:]

# =========================
# 5. 画布
# =========================
fig, (ax1, ax2) = plt.subplots(
    1, 2,
    figsize=(12, 6),
    gridspec_kw={"width_ratios": [1.2, 1]}
)

# =========================
# 🥧 饼图（纯颜色，无文字）
# =========================
ax1.pie(
    values,
    colors=colors,
    startangle=140
)

ax1.set_title("Language Usage (HTML/CSS excluded)")
ax1.axis("equal")

# =========================
# 📊 右侧 legend（分上下）
# =========================
ax2.axis("off")

y = 0.9

# 上半（主要语言）
for lang, color in zip(top_labels, top_colors):
    ax2.add_patch(
        plt.Rectangle((0.05, y - 0.03), 0.03, 0.03,
                      color=color, transform=ax2.transAxes)
    )
    ax2.text(0.1, y, lang, transform=ax2.transAxes,
             fontsize=10, va="center")
    y -= 0.08

# 分割线
ax2.text(0.05, y, "──────────", transform=ax2.transAxes)
y -= 0.08

# 下半（次要语言）
for lang, color in zip(bottom_labels, bottom_colors):
    ax2.add_patch(
        plt.Rectangle((0.05, y - 0.03), 0.03, 0.03,
                      color=color, transform=ax2.transAxes)
    )
    ax2.text(0.1, y, lang, transform=ax2.transAxes,
             fontsize=10, va="center")
    y -= 0.07

# =========================
# 6. 输出 SVG
# =========================
plt.tight_layout()
plt.savefig("language.svg", format="svg", bbox_inches="tight")
