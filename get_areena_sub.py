# /bin/python3
#
# To retrieve srt subtitles from Yle Areena



from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
import sys

driver = webdriver.Chrome('/usr/bin/chromedriver')
# or driver = webdriver.PhantomJS('/usr/bin/phantomjs')
# or driver = webdriver.Firefox()
# or driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.implicitly_wait(10)

page_urls = sys.argv[1:]

for page_url in page_urls:
    driver.get(page_url)
    title = driver.title.split('|')[0].strip()     

    play_button = driver.find_element_by_class_name('kWidgetPlayBtn')
    play_button.click()
    player_frame = driver.find_element_by_class_name('mwEmbedKalturaIframe')
    driver.switch_to.frame(player_frame)

    player = driver.find_element_by_class_name('mwEmbedPlayer')
    pause_button = driver.find_element_by_class_name('playPauseBtn')
    while not pause_button.is_displayed():
        ActionChains(driver).move_to_element(player).perform()
    pause_button.click()
    tracks = driver.find_elements_by_tag_name('track')
    for track in tracks:
        subtitle_url = track.get_attribute('src')
        lang = track.get_attribute('srclang')
        label = track.get_attribute('label')
        fileext = track.get_attribute('fileext')
        filename = title + ' (' + label + ').' + lang + '.' + fileext
        subtitle = urllib.URLopener()
        subtitle.retrieve(subtitle_url, filename)

driver.quit()
