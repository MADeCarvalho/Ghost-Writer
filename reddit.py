from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from time import sleep
from io import BytesIO
import gtts
import wave
import videomaker
import os

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
    XPATH = "//*[contains(concat(' ', @class, ' '), ' top-level ')]"
    return driver.find_elements_by_xpath(XPATH)

def resizeImage(img):
    basewidth = 1920
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    return img

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
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        box = (left, top, right, bottom)
        im = im.crop(box)  # defines crop points
        im = resizeImage(im)
        bg = Image.new(im.mode, (1920, 1080), color=(0, 0, 0))
        bg.paste(Image.open('utility\\sleeping_tiger_bg.jpg'))
        im_width, im_height = im.size
        box = (round(1920/2) - round(im_width/2), round(1080/2) - round(im_height/2))
        bg.paste(im, box)
        bg.save('images\\comment{}.png'.format(i))
        _textToSpeech(driver, comment, i)
        i = i+1
        try:
            driver.execute_script(
                "arguments[0].replaceWith(arguments[1]);", comment, comments[i])
        except IndexError:
            break


def _clickSeeAllButton(driver):
    XPATH = "//button[@class='p23tea-7 cMnkIS' or @class = 'j9NixHqtN2j8SKHcdJ0om s7bz5cq-7 bdkLQH']"
    button = driver.find_element_by_xpath(XPATH)
    action = ActionChains(driver)
    #driver.execute_script("arguments[0].scrollIntoView();", button)
    sleep(2)
    action.move_to_element(button).click().perform()


def _textToSpeech(driver, comment, index):
    try:
        XPATH = ".//p[@class='s1w8oh2o-10 bQeEFC']"
        paragraphs = comment.find_elements_by_xpath(XPATH)
        text = ''
        for p in paragraphs:
            text = text + ' ' + p.text
        tts = gtts.gTTS(text, lang='en-uk')
        tts.save('narrations\\comment{}.mp3'.format(index))
        #_speedUpAudio('narrations\\comment{}.mp3'.format(index))
    except:
        os.remove('images\\comment{}.png'.format(index))


def _titleToSpeech(driver, title):
    tts = gtts.gTTS(title.text)
    tts.save('narrations\\000.mp3')
    #_speedUpAudio('narrations\\000.mp3')


def _scrollFarm(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    commentCount = 0
    while commentCount < 80:
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


def _speedUpAudio(file):
    CHANNELS = 1
    swidth = 2
    Change_RATE = 1.6

    spf = wave.open(file, 'rb')
    RATE=spf.getframerate()
    signal = spf.readframes(-1)

    wf = wave.open('1.6x_'+file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*Change_RATE)
    wf.writeframes(signal)
    wf.close()

if __name__ == "__main__":
    driver = _initDriver()
    driver.get(_currentPage)
    _enterThread(driver)
    post_heading = driver.find_element_by_tag_name("h2")
    _titleToSpeech(driver, post_heading)
    post_div = driver.find_element_by_xpath(".//div[@data-test-id='post-content']")
    post_div.screenshot('images\\000.png')
    _clickSeeAllButton(driver)
    _scrollFarm(driver)
    comments = _getComments(driver)
    _getCommentScreenshots(driver, comments, post_heading)
    driver.close()
    videomaker.moviePyVideo()
