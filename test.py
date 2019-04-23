from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from time import sleep
from io import BytesIO

_currentPage = 'https://www.reddit.com/r/AskReddit'
_commentNum = 0

def _initDriver():
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome( chrome_options=options)
    driver.maximize_window()
    driver.implicitly_wait(30)
    return driver


def _enterThread(driver) :
    link = driver.find_element_by_partial_link_text("hours ago")
    driver.get(link.get_attribute('href'))
    _currentPage = link 

def _getComments(driver) :  
    return driver.find_elements_by_xpath("//*[contains(concat(' ', @class, ' '), ' top-level ')]")

def _getCommentScreenshots(driver, comments):
  i = 0
  for comment in comments:
    driver.execute_script("arguments[0].scrollIntoView();", comment)
    location = comment.location
    size = comment.size
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png))
    left = location['x']
    top = driver.execute_script("arguments[0].getBoundingClientRect().top;", comment)
    print("top: {}".format(top))
  #  top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']  
    browser_navigation_panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
    print(browser_navigation_panel_height)
    box = (left, top, right, bottom)
    print(box)
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('images\\screenshot{}.png'.format(i))
    i = i+1

def _clickSeeAllButton(driver):  
  button = driver.find_element_by_xpath("//button[@class='p23tea-7 cMnkIS']")
  print(button)
  action = ActionChains(driver)
  #driver.execute_script("arguments[0].scrollIntoView();", button)
  sleep(2)
  action.move_to_element(button).click().perform()

if __name__ == "__main__":
  driver = _initDriver()
  driver.get(_currentPage)
  _enterThread(driver)
  post_heading = driver.find_element_by_tag_name("h2")
  post_heading.screenshot('images\\title.png')
  _clickSeeAllButton(driver)
  sleep(5)
  comments = _getComments(driver)
  print(len(comments))
  _getCommentScreenshots(driver, comments)




