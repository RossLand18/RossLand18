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
# ❗过滤 HTML / CSS
# =========================
exclude_langs = {"HTML", "CSS"}

filtered = [
    (lang, size)
    for lang, size in lang_bytes.items()
    if lang not in exclude_langs
]

sorted_langs = sorted(filtered, key=lambda x: x[1], reverse=True)

labels = [x[0] for x in sorted_langs]
values = [x[1] for x in sorted_langs]

total = sum(values)
percentages = [v / total * 100 for v in values]

# =========================
# GitHub颜色
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
# 分层（上：主要，下：次要）
# =========================
mid = len(labels) // 2

top = list(zip(labels[:mid], percentages[:mid], colors[:mid]))
bottom = list(zip(labels[mid:], percentages[mid:], colors[mid:]))

# =========================
# 图形
# =========================
fig, (ax1, ax2) = plt.subplots(
    1, 2,
    figsize=(12, 6),
    gridspec_kw={"width_ratios": [1.2, 1]}
)

# =========================
# 🥧 饼图（纯颜色）
# =========================
ax1.pie(
    values,
    colors=colors,
    startangle=140
)

ax1.set_title("Language Usage (HTML/CSS excluded)")
ax1.axis("equal")

# =========================
# 📊 右侧（对齐版 legend）
# =========================
ax2.axis("off")

def draw_item(y, lang, pct, color):
    # 色块
    ax2.add_patch(
        plt.Rectangle(
            (0.05, y - 0.015),
            0.025,
            0.025,
            color=color,
            transform=ax2.transAxes,
            clip_on=False
        )
    )

    # 语言名称
    txt = ax2.text(
        0.1,
        y,
        lang,
        transform=ax2.transAxes,
        fontsize=10,
        va="center",
        ha="left"
    )

    # 先渲染一次，获取文字实际宽度
    fig.canvas.draw()

    bbox = txt.get_window_extent(
        renderer=fig.canvas.get_renderer()
    )

    # 转换为 Axes 坐标
    x_end = ax2.transAxes.inverted().transform(
        (bbox.x1, bbox.y0)
    )[0]

    # 百分比紧跟语言名称
    ax2.text(
        x_end + 0.02,
        y,
        f"{pct:.1f}%",
        transform=ax2.transAxes,
        fontsize=10,
        va="center",
        ha="left"
    )

# =========================
# 上半部分（主语言）
# =========================
y = 0.9
for lang, pct, color in top:
    draw_item(y, lang, pct, color)
    y -= 0.08

# =========================
# 下半部分（次语言）
# =========================
for lang, pct, color in bottom:
    draw_item(y, lang, pct, color)
    y -= 0.07

# =========================
# 保存
# =========================
plt.tight_layout()
plt.savefig("language.svg", format="svg", bbox_inches="tight")
