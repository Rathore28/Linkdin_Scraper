import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def login_linkedin(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

def scrape_jobs(email, password, keyword, location, num_jobs=20):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    login_linkedin(driver, email, password)

    jobs = []
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(2)

    search_keywords = driver.find_element(By.XPATH, "//input[contains(@aria-label,'Search jobs')]")
    search_keywords.send_keys(keyword)

    search_location = driver.find_element(By.XPATH, "//input[contains(@aria-label,'Search location')]")
    search_location.clear()
    search_location.send_keys(location)
    search_location.send_keys(Keys.RETURN)
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(jobs) < num_jobs:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")
        listings = soup.find_all("div", {"class": "job-card-container"})
        for job in listings:
            if len(jobs) >= num_jobs:
                break
            try:
                title = job.find("h3").get_text(strip=True)
                company = job.find("h4").get_text(strip=True)
                location = job.find("span", {"class": "job-card-container__metadata-item"}).get_text(strip=True)
                date_posted = job.find("time")["datetime"] if job.find("time") else "N/A"
                link = job.find("a", href=True)["href"]

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "date_posted": date_posted,
                    "job_url": "https://www.linkedin.com" + link
                })
            except Exception:
                continue

    driver.quit()

    df = pd.DataFrame(jobs)
    df = df.drop_duplicates(subset=["title", "company", "location"])
    return df
