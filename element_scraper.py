from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ElementScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
    
    def scrape_element(self, selector, element_name):
        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            
            return {
                "text": element.text.strip() if element.text else "",
                "tag_name": element.tag_name,
                "is_displayed": element.is_displayed(),
                "location": element.location,
                "size": element.size
            }
            
        except Exception as e:
            print(f"Could not find {element_name}: {e}")
            return None
    
    def scrape_page_info(self, url):
        self.driver.get(url)
        time.sleep(3) 
        
        return {
            "title": self.driver.title,
            "current_url": self.driver.current_url,
            "page_source_length": len(self.driver.page_source)
        }