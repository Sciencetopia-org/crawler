import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 定义爬取的页面数量
num_pages = 5

# Bilibili知识区的URL
base_url = "https://www.bilibili.com/v/knowledge/?spm_id_from=333.851.b_7072696d61727944696d656e73696f6e.3"

# 各分类的XPath
category_xpath_list = [
    '//div[@class="nav-list"]/div[1]/a',
    '//div[@class="nav-list"]/div[2]/a',
    '//div[@class="nav-list"]/div[3]/a',
    '//div[@class="nav-list"]/div[4]/a',
    '//div[@class="nav-list"]/div[5]/a',
    '//div[@class="nav-list"]/div[6]/a',
    '//div[@class="nav-list"]/div[7]/a',
    '//div[@class="nav-list"]/div[8]/a',
]

# 初始化WebDriver
edge_options = Options()
edge_options.use_chromium = True

driver = webdriver.Edge(service=Service(executable_path="msedgedriver"), options=edge_options)

# 打开Bilibili知识区页面
driver.get(base_url)
driver.maximize_window()

# # 点击登录按钮
# login_button = WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, '//a[@class="btn login"]'))
# )
# login_button.click()

# # 等待登录页面加载并输入用户名和密码
# username_input = WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, '//input[@name="tel"]'))
# )
# password_input = driver.find_element_by_xpath('//input[@name="pwd"]')

# username_input.send_keys("3146296455")
# password_input.send_keys("990603yufang")

# # 点击登录按钮
# submit_button = driver.find_element_by_xpath('//a[@class="btn btn-login"]')
# submit_button.click()

# # 等待登录成功
# WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, '//a[@class="h-avatar"]'))
# )

# 保存数据到CSV文件
with open("bilibili_videos.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Category", "Title", "Tags", "Video URL"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历各分类
    for category_xpath in category_xpath_list:
        # category_element = WebDriverWait(driver, 50).until(
        #     EC.presence_of_element_located((By.XPATH, category_xpath))
        # )
        category_element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "你的CSS选择器"))
        )

        category_name = category_element.text
        category_element.click()
        time.sleep(2)

        # 爬取指定页面数量
        for i in range(1, num_pages + 1):
            print(f"正在爬取【{category_name}】分类，第{i}页")
            video_list = driver.find_elements_by_css_selector(".video-list .video-item")

            for video in video_list:
                title = video.find_element_by_css_selector(".title").text
                tags = [tag.text for tag in video.find_elements_by_css_selector(".tag-area .tag")]
                video_url = video.find_element_by_css_selector(".title").get_attribute("href")

                writer.writerow({"Category": category_name, "Title": title, "Tags": ", ".join(tags), "Video URL": video_url})

            # 点击下一页
            if i < num_pages:
                next_page_button = driver.find_element_by_css_selector(".next")
                driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
                time.sleep(1)
                next_page_button.click()
                time.sleep(2)

driver.quit()
print("爬取完成！已将Bilibili知识区视频数据保存到bilibili_videos.csv文件中。")