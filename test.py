from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from resize_and_crop import resize_and_crop


options = Options()
options.add_argument("--disable-notifications")

driver = webdriver.Chrome( chrome_options=options)

driver.get("https://www.reddit.com/r/AskReddit")
link = driver.find_element_by_partial_link_text("hours ago")
link.click()

post_heading = driver.find_element_by_tag_name("h2")
top_left = post_heading.location
size = post_heading.size
screenshot =driver.get_screenshot_as_file("/images/test.png")
image = resize_and_crop("/images/test.png", (size["width"],size["height"]),"middle")

with file('test.png', 'wb') as f:
    f.write(region)