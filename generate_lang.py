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

# ======================
# GitHub colors
# ======================
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

colors = [
    github_colors.get(lang, "#9e9e9e")
    for lang in labels
]

# ======================
# 🥧 Pie Chart
# ======================
plt.figure(figsize=(8, 8))

plt.pie(
    values,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.8,
    labeldistance=1.05,
    textprops={"fontsize": 9}
)

plt.title("Language Usage (GitHub Style)")
plt.tight_layout()
plt.savefig("language.svg", bbox_inches="tight", dpi=150)
