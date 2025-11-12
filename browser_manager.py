import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
import logging

logger = logging.getLogger(__name__)

class BrowserManager:
    def __init__(self):
        self.driver = None
        self.browser_type = None
    
    def start_browser(self, headless=True):
        methods = [
            self._try_chrome_automatic,
            self._try_chrome_manual, 
            self._try_firefox,
            self._try_edge
        ]
        
        for method in methods:
            logger.info(f"Trying method: {method.__name__}")
            driver = method(headless)
            if driver:
                self.driver = driver
                return True
        
        logger.error("All browser startup methods failed")
        return False
    
    def _try_chrome_automatic(self, headless):
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            if headless:
                options.add_argument("--headless")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            self.browser_type = "chrome_auto"
            logger.info("Chrome started automatically")
            return driver
            
        except Exception as e:
            logger.warning(f"Automatic Chrome failed: {e}")
            return None
    
    def _try_chrome_manual(self, headless):
        try:
            from selenium.webdriver.chrome.options import Options  
            options = Options()
            if headless:
                options.add_argument("--headless")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=options)
            
            self.browser_type = "chrome_manual" 
            logger.info("Chrome started manually")
            return driver
            
        except Exception as e:
            logger.warning(f"Manual Chrome failed: {e}")
            return None
    
    def _try_firefox(self, headless):
        try:
            from webdriver_manager.firefox import GeckoDriverManager
            from selenium.webdriver.firefox.options import Options
            
            options = Options()
            if headless:
                options.add_argument("--headless")
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
            self.browser_type = "firefox"
            logger.info("Firefox started successfully")
            return driver
            
        except Exception as e:
            logger.warning(f"Firefox failed: {e}")
            return None
    
    def _try_edge(self, headless):
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            from selenium.webdriver.edge.options import Options
            
            options = Options()
            if headless:
                options.add_argument("--headless")
            
            service = Service(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            
            self.browser_type = "edge"
            logger.info("Edge started successfully")
            return driver
            
        except Exception as e:
            logger.warning(f"Edge failed: {e}")
            return None
    
    def quit_browser(self):
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")