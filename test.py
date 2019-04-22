from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from time import sleep

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

def _getComment(driver, index = 0) :
    return driver.find_elements_by_xpath("//*[contains(concat(' ', @class, ' '), ' top-level ')]")[index]

def _getCommentLoop(driver, index, failCount = 0):
  comNo = index
  try:
    print("in try")
    comment = _getComment(driver, comNo)
    comment.screenshot("images\\comment{}.png".format(comNo))
    driver.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, comment)
    comNo = comNo + 1
    _getCommentLoop(driver, comNo)
  except Exception as e:
    _failCount = failCount +1
    print(e)
    print("fail at {}".format(comNo))
    if(_failCount > 3):
      return
    sleep(60)
    _getCommentLoop(driver, comNo, failCount=_failCount)

if __name__ == "__main__":
  driver = _initDriver()
  driver.get(_currentPage)
  _enterThread(driver)
  post_heading = driver.find_element_by_tag_name("h2")
  post_heading.screenshot('images\\title.png')
  _getCommentLoop(driver, 0)
  driver.close()




