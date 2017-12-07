#! /usr/bin/env python

"""Retrieve srt subtitles from Yle Areena"""

import sys
import urllib
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@contextmanager
def open_browser():
    """Temporary context manager as it is planned but not implemented yet in Selenium"""
    browser = webdriver.Chrome('/usr/bin/chromedriver')
    browser.implicitly_wait(10)
    yield browser
    browser.quit()


with open_browser() as browser:

    page_urls = sys.argv[1:]

    for page_url in page_urls:
        browser.get(page_url)
        title = browser.title.split('|')[0].strip()

        play_button = browser.find_element_by_class_name('kWidgetPlayBtn')
        play_button.click()
        player_frame = browser.find_element_by_class_name('mwEmbedKalturaIframe')
        browser.switch_to.frame(player_frame)

        player = browser.find_element_by_class_name('mwEmbedPlayer')
        pause_button = browser.find_element_by_class_name('playPauseBtn')
        while not pause_button.is_displayed():
            ActionChains(browser).move_to_element(player).perform()
        pause_button.click()
        tracks = browser.find_elements_by_tag_name('track')
        for track in tracks:
            subtitle_url = track.get_attribute('src')
            lang = track.get_attribute('srclang')
            label = track.get_attribute('label')
            fileext = track.get_attribute('fileext')
            filename = title + ' (' + label + ').' + lang + '.' + fileext
            subtitle = urllib.URLopener()
            subtitle.retrieve(subtitle_url, filename)


