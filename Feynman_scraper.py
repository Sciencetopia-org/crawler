import requests
import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.feynmanlectures.caltech.edu"
volume_links = ["/I_toc.html", "/II_toc.html", "/III_toc.html"]

with open("feynman_lectures.csv", "w", newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Volume", "Chapter Number", "Title", "URL"])

    for volume_link in volume_links:
        url = base_url + volume_link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        chapters = soup.find_all("div", class_="toc-chapter")

        for chapter in chapters:
            chapter_number = chapter.find("span", class_="tag").text
            title = chapter.find("a", class_="chapterlink").text
            title = title.split(".")[1].strip()

            # 提取 chapter_number 中的数字部分
            chapter_number_digits = "".join(filter(str.isdigit, chapter_number))

            # 构建chapter_url
            volume_prefix = volume_link.split("_")[0][1:]
            chapter_url = base_url + "/" + volume_prefix + "_" + chapter_number_digits + ".html"

            print(f"Volume: {volume_prefix}, Chapter Number: {chapter_number}, Title: {title}, URL: {chapter_url}")
            csv_writer.writerow([volume_prefix, chapter_number, title, chapter_url])

print("Done!")