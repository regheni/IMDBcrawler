## selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# browser = webdriver.Firefox()#Chrome('./chromedriver.exe')
IMDB_WATCHLIST = "https://www.imdb.com/user/ur24609396/watchlist"
PATIENCE_TIME = 60
LOAD_MORE_BUTTON_XPATH = '//*[@id="center-1-react"]/div/div[3]/div[2]/button'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(IMDB_WATCHLIST)

while True:
    try:
        loadMoreButton = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
        time.sleep(2)
        loadMoreButton.click()
        time.sleep(5)
    except Exception as e:
        print(e)
        break
print("Complete")
time.sleep(10)
driver.quit()
