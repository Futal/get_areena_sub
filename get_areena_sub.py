#! /usr/bin/env python

"""Retrieve srt subtitles from Yle Areena"""

from __future__ import print_function
import sys
import argparse
import urllib
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser(description='get SRT subtitles from Yle Areena programs')
parser.add_argument('urls', metavar='URL', nargs='+', help='a URL from Yle Areena')
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true', help='be verbose')
group.add_argument('-q', '--quiet', action='store_true', help='suppress all messages')
parser.add_argument('-w', '--wait', metavar='SEC', type=int, default=10, help='implicit wait in seconds (default: 10 s)')
args = parser.parse_args()

@contextmanager
def open_browser():
    """Temporary context manager as it is planned but not implemented yet in Selenium"""
    browser = webdriver.Chrome('/usr/bin/chromedriver')
    browser.implicitly_wait(args.wait)
    if args.verbose:
        print('Starting Chrome browser, implicit wait: {} seconds'.format(args.wait))
    yield browser
    browser.quit()
    if args.verbose:
        print('\nClosing the browser\n')


with open_browser() as browser:
    for url in args.urls:
        try:
            browser.get(url)
            title = browser.title.split('|')[0].strip()
            if args.verbose:
                print('\n{} [{}]'.format(title, url))
            
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
                if args.verbose:
                    print('    "{}"'.format(filename))
        except Exception:
            if not args.quiet:
                print('    Unable to retrieve subtitles from {}'.format(url))
