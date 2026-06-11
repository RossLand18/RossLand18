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

sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)

labels = [x[0] for x in sorted_langs]
values = [x[1] for x in sorted_langs]

total = sum(values)
percentages = [v / total * 100 for v in values]

# =========================
# 3. GitHub 官方颜色
# =========================
github_colors = {
    "Java": "#b07219",
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "Dockerfile": "#384d54",
    "Kotlin": "#A97BFF",
    "Go": "#00ADD8",
    "C": "#555555",
    "C++": "#f34b7d",
}

colors = [github_colors.get(lang, "#9e9e9e") for lang in labels]

# =========================
# 4. 画图（左饼图 + 右列表）
# =========================
fig, (ax1, ax2) = plt.subplots(
    1, 2,
    figsize=(12, 6),
    gridspec_kw={"width_ratios": [1.2, 1]}
)

# =========================
# 🥧 左：饼图
# =========================
wedges, texts, autotexts = ax1.pie(
    values,
    colors=colors,
    startangle=140,
    autopct="%1.1f%%",
    pctdistance=0.75
)

ax1.set_title("Language Usage")
ax1.axis("equal")

# =========================
# 📊 右：描述列表（关键）
# =========================
ax2.axis("off")

y = 0.95
line_height = 0.07

for lang, pct, color in zip(labels, percentages, colors):
    ax2.add_patch(
        plt.Rectangle(
            (0.05, y - 0.03),
            0.03,
            0.03,
            color=color,
            transform=ax2.transAxes,
            clip_on=False
        )
    )

    ax2.text(
        0.1,
        y,
        f"{lang}  {pct:.2f}%",
        transform=ax2.transAxes,
        fontsize=10,
        va="center"
    )

    y -= line_height

# =========================
# 5. 保存 SVG（GitHub README用）
# =========================
plt.tight_layout()
plt.savefig("language.svg", format="svg", bbox_inches="tight")
