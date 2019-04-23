from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from time import sleep
from io import BytesIO
import gtts
import wave

_currentPage = 'https://www.reddit.com/r/AskReddit'
_commentNum = 0


def _initDriver():
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.implicitly_wait(30)
    return driver


def _enterThread(driver):
    link = driver.find_element_by_partial_link_text("hours ago")
    driver.get(link.get_attribute('href'))
    _currentPage = link


def _getComments(driver):
    return driver.find_elements_by_xpath("//*[contains(concat(' ', @class, ' '), ' top-level ')]")


def _getCommentScreenshots(driver, comments, post_heading):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    i = 0
    driver.execute_script(
        "arguments[0].replaceWith(arguments[1]);", post_heading, comments[0])
    for comment in comments:
        location = comment.location
        size = comment.size
        png = driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        left = location['x']+47
        top = location['y']+72
        right = location['x'] + size['width']
        bottom = location['y'] + size['height'] + 125
        box = (left, top, right, bottom)
        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save('images\\screenshot{}.png'.format(i))
        _textToSpeech(driver, comment, i)
        i = i+1
        driver.execute_script(
            "arguments[0].replaceWith(arguments[1]);", comment, comments[i])


def _clickSeeAllButton(driver):
    button = driver.find_element_by_xpath("//button[@class='p23tea-7 cMnkIS']")
    action = ActionChains(driver)
    #driver.execute_script("arguments[0].scrollIntoView();", button)
    sleep(2)
    action.move_to_element(button).click().perform()

def _textToSpeech(driver, comment, index):
  text = comment.find_element_by_xpath("//p[@class='s1w8oh2o-10 bQeEFC']").text
  tts = gtts.gTTS(text, lang='en')
  tts.save('narrations\\comment{}.wav'.format(index))
  CHANNELS = 1
  swidth = 2
  Change_RATE = 2
  sleep(5)
  spf = wave.open('narrations\\comment{}.wav', 'rb')
  RATE=spf.getframerate()
  signal = spf.readframes(-1)

  wf = wave.open('changed_comment{}.wav', 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(swidth)
  wf.setframerate(RATE*Change_RATE)
  wf.writeframes(signal)
  wf.close()

def _scrollFarm(driver):
  SCROLL_PAUSE_TIME = 0.5

  # Get scroll height
  last_height = driver.execute_script("return document.body.scrollHeight")
  commentCount = 0
  while commentCount < 40:
      # Scroll down to bottom
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      commentCount = len(_getComments(driver))
      # Wait to load page
      sleep(SCROLL_PAUSE_TIME)
      # Calculate new scroll height and compare with last scroll height
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
          break
      last_height = new_height

if __name__ == "__main__":
    driver = _initDriver()
    driver.get(_currentPage)
    _enterThread(driver)
    post_heading = driver.find_element_by_tag_name("h2")
    post_heading.screenshot('images\\title.png')
    _clickSeeAllButton(driver)
    _scrollFarm(driver)
    comments = _getComments(driver)
    print(len(comments))
    _getCommentScreenshots(driver, comments, post_heading)
