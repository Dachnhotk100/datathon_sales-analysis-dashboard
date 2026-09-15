from selenium import webdriver
driver = webdriver.Chrome() # Hoặc webdriver.Firefox() cho 
driver.get("http://gomotungkinh.com/")
button = driver.find_element_by_id("bonk")
button.click()