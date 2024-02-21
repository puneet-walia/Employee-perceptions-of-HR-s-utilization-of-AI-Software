import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup as bs

# LinkedIn login credentials
username = "your_username"
password = "your_password"

linkedin_url = "https://www.linkedin.com/"

# Create a Chrome webdriver
driver = webdriver.Chrome()
driver.maximize_window()

# Open LinkedIn website
driver.get(linkedin_url)

# Log in
username_input = driver.find_element(By.ID, "session_key")
username_input.send_keys(username)

password_input = driver.find_element(By.ID, "session_password")
password_input.send_keys(password)

driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Search for posts about "Artificial Intelligence AND Human Resources"
search_term = "Artificial Intelligence AND Human Resources"
search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
search_bar.send_keys(search_term)
search_bar.send_keys(Keys.RETURN)

# Click on the 'Posts' filter
posts_filter_xpath = "/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[3]/button"
driver.find_element(By.XPATH, posts_filter_xpath).click()

# Set up variables for infinite scrolling
SCROLL_PAUSE_TIME = 1.5
max_scrolls = 5  # You can adjust this based on your needs
scrolls = 0
last_height = driver.execute_script("return document.body.scrollHeight")

# Create a list to store the data
data = []

# Start scrolling and extracting data
while scrolls < max_scrolls:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Increment the scroll counter
    scrolls += 1

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    # Extract information from the current page
    company_page = driver.page_source
    linkedin_soup = bs(company_page.encode("utf-8"), "html.parser")
    containers = linkedin_soup.findAll("div", {"class": "entity-result__content-container"})

    for container in containers:
        post_author = container.find("a", {"class": "author"}).text.strip()

        # Check if there is a "See more" button and click it
        see_more_button_xpath="-/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div/div[1]/div[1]/div/ul/li[3]/div/div/div/div/div/div[4]/div/button/span"
        see_more_button = driver.find_element(By.XPATH, see_more_button_xpath)
        if see_more_button:
            see_more_button.click()
            time.sleep(1)  # Wait for the content to expand

        post_content = container.find("p", {"class": "description"}).text.strip()
        data.append({"Authors": post_author, "Posts": post_content})

# Create a DataFrame from the list of data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('linkedin_posts.csv', index=False)

# Close the webdriver
driver.quit()
