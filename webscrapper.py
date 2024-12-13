import time
from selenium import webdriver
from datetime import datetime,timedelta
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
def convert_date(d):
    if "today" in d.lower():
        return datetime.now().date()
    elif "days ago" in d.lower():
        return((datetime.now() - timedelta(days=int(d.split()[1].replace(',', '')))).date())
    elif "on" in d.lower():
        return(datetime.strptime(d.split("on")[1].strip().replace(',', ''), "%B %d %Y").date())
def scrap(u,dates,rating,page,till):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    url=u
    driver.get(url)
    f=False
    itf=0
    while(True):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/1.8)")
        time.sleep(2)
        date=driver.find_elements(By.CLASS_NAME,"iLkEeQbexGs-")
        ratings=driver.find_elements(By.CLASS_NAME,"-k5xpTfSXac-")
        if len(date)==0 or len(ratings)==0:
            print("Refresh driver")
            driver.refresh()
            time.sleep(2)
        else:
            for bf,i in enumerate(date):
                if(convert_date(i.text)<till):
                    f=True
                    itf=bf
                    print(bf,"Naug")
                    break
                dates.append(convert_date(i.text))
            for k,i in enumerate(ratings):
                if(k==itf and f==True):
                    break
                rating.append(i.text)
            if(f==True):
                dates
                rating
                return
            try:
                button=driver.find_element(By.CSS_SELECTOR,"#reviews > section > footer > div > div:nth-child(3) > a > div > span > svg")
                button.click()
            except NoSuchElementException:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight/1.3)")
            except StaleElementReferenceException:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight/1.3)")
            except ElementClickInterceptedException:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight/1.3)")
            except ElementNotInteractableException:
                break
        
        