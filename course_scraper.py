import requests
from bs4 import BeautifulSoup
import csv

# 爬取目标页面
url = "https://github.com/prakhar1989/awesome-courses"

# 发送请求
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, "html.parser")

# 提取课程列表
course_list = soup.find("article").find_all("li")

# 保存数据到CSV文件
with open("courses.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Course Name", "Course Link", "University", "Description"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for course in course_list:
        course_info = course.find_all("a")
        if len(course_info) >= 2:
            course_name = course_info[0].text.strip()
            course_link = course_info[0]["href"]
            university = course_info[1].text.strip()
            description = course.get_text(strip=True)
            description = description.replace(course_name, "").replace(university, "").strip()

            writer.writerow({"Course Name": course_name, "Course Link": course_link, "University": university, "Description": description})

print("爬取完成！已将课程数据保存到courses.csv文件中。")