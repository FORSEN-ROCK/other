"""Bypass auth hh
"""
from selenium import webdriver


#class BypassBase(object):
#    pass


#class BypassBaseAuth(object):
#    auth_url = None
#    login_field_class = None
#    pass_field_class = None

#    def __init__(self):
#        self

class BrowserSeanceBase(object):

    def __init__(self):
        self.browser = webdriver.Chrome()

    def __del__(self):
        browser = getattr(self, 'browser', None)

        if browser:
            browser.close()

    def _set_url(self, url=None):
        if not url:
            raise URLError("URL it's bad: %s" %(url))

        browser = getattr(self, 'browser', None)

        if not browser:
            raise BrowserError("Not active connect")

        browser.get(url)

    def _get_html(self):
        browser = getattr(self, 'browser', None)

        if not browser:
            raise BrowserError("Not active connect")

        return browser.souce()

    def _screen_shot(self):
        browser = getattr(self, 'browser', None)

        if not browser:
            raise BrowserError("Not active connect")

        return browser.screen()

    def _get_element(self, target_name):
        element_name = getattr(self, "target_" + target_name, None)

        if element_name:
            browser = getattr(self, 'browser', None)
            element = browser.find_element_by_name(element_name)
        else:
            element = None

        return element