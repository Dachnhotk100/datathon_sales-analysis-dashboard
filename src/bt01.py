from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo WebDriver
driver = webdriver.Chrome()

# Mở trang
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name"
driver.get(url)

# Đợi 2 giây cho trang load
time.sleep(10)

# Lấy tất cả thẻ <a>
tags = driver.find_elements(By.TAG_NAME, "a")

# Lấy danh sách link
links = [tag.get_attribute("href") for tag in tags]

# In ra
for link in links:
    print(link)

driver.quit()
