import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions

class DriverInstance():
  """ Class containing driver and methods to scrape webpages
  Args:
    logger: The logger.
    is_headless: Run in headless mode.
  """
  def __init__(
    self,
    logger,
    is_headless=True,
    debug=False,
  ):
    self.logger = logger
    self.is_headless = is_headless
    self.debug = debug
    self.count = 1

    self.logger.info('Creating a DriverInstance...')
    self.create_driver()

  def create_driver(self):
    chrome_options = ChromeOptions()
    if self.is_headless:
      chrome_options.add_argument('--headless') # headless mode

    self.driver = webdriver.Chrome(chrome_options=chrome_options)

  def load_site(self, link):
    out = 'Loading page #{}'.format(self.count)
    self.logger.info(out)
    if self.debug:
      self.logger.info(link)
    self.driver.get(link)
    self.count+=1

  def close_window(self):
    self.driver.close()
  
  def get_topics(self):
    topics = []
    try:
      time.sleep(2) # wait for page to load
      elements = self.driver.find_elements_by_class_name("tag__2PqS")
      for e in elements:
        topics.append(e.get_attribute("innerHTML"))
    except:
      self.logger.error('An error occured while looking for topics')
    if self.debug:
      print(topics)
    return topics

  def get_stats(self):
    upvote = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[1]/div[2]/button[1]/span').get_attribute("innerHTML")
    downvote = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[1]/div[2]/button[2]/span').get_attribute("innerHTML")
    if self.debug:
      print(upvote,downvote)
    return upvote, downvote

  def run_automation(self): 
    self.logger.info("Running automation...")
    self.load_site()
    self.load
