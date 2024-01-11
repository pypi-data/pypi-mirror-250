import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumBrowser(webdriver.Chrome):
    def __init__(self, headless: bool = True, fullscreen: bool = False, extra_arguments: list[str] = []):
        options = Options()
        if headless:
            options.add_argument("--headless")
        if fullscreen and (not headless):
            options.add_argument("--kiosk")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36")
        options.add_argument("log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        for extra in extra_arguments:
            options.add_argument(extra)

        super().__init__(service=Service(ChromeDriverManager().install()), options=options)
    
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.page_source, "lxml")
    
    def open_new_tab(self, url: str = None) -> None:
        if (url is None):
            url = "http://bings.com"
        self.execute_script(f"window.open('{url}','_blank');")
        self.switch_to.window(self.current_window_handle)
    
    def goto_tab(self, index: int) -> None:
        self.switch_to.window(self.window_handles[index])

    def close_tab(self, index: int = None) -> None:
        current_tab = self.current_window_handle
        if index is not None:
            target_window_handle = self.window_handles[index]
        else:
            target_window_handle = current_tab
        self.switch_to.window(target_window_handle)
        self.close()
        if current_tab != target_window_handle:
            self.switch_to.window(current_tab)
        elif self.window_handles:
            self.switch_to.window(self.window_handles[0])
        
    def wait_for_visible_element(self, selector: tuple[By | str, str], timeout: int = 20) -> None:
        WebDriverWait(self, timeout).until(EC.visibility_of_element_located(selector))
