import requests
import csv
from bs4 import BeautifulSoup

def get_description(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"class": "proofContent"})
    if content:
        return content.text.strip()
    else:
        return ""

url = "https://statproofbook.github.io/I/ToC.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 提取所有章节
sections = soup.find_all("li")

# 准备CSV文件
with open("statproofbook.csv", "w", newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["类型", "链接", "标题", "内容"])

    # 解析每个章节
    for section in sections:
        # 提取所有概念定义
        definition_link_elements = section.find_all("a")

        if not definition_link_elements:
            continue

        for definition_link_element in definition_link_elements:
            definition = definition_link_element.text
            path = definition_link_element.get('href')

            if path is not None:
                definition_link = "https://statproofbook.github.io/" + path
                definition_type = "Definition" if "/D/" in definition_link else "Proof"
                description = get_description(definition_link)
                csv_writer.writerow([definition_type, definition_link, definition, description])

print("爬取完成！已将数据保存到statproofbook.csv文件中。")