# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestExistenceasserts():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_existenceasserts(self):
    self.driver.get("https://bruknow.library.brown.edu/discovery/fulldisplay?context=L&vid=01BU_INST:BROWN&search_scope=MyInst_and_CI&tab=Everything&docid=alma991003874639706966")
    WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Bookplate\')]")))
    self.driver.set_window_size(1257, 834)
    self.driver.execute_script("window.scrollTo(0,1795)")
    elements = self.driver.find_elements(By.XPATH, "//span[contains(.,\'Bookplate\')]")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, "div > prm-highlight .bul_pl_primo_bookplate_image")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Purchased with ")
    assert len(elements) > 0
  
