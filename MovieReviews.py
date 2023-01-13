import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

#Function to scrape review information
def Scrape(dataframe):
    #Find all reviews on the page
    reviews = driver.find_elements(By.CLASS_NAME, 'audience-reviews__item')

    #Extract data from each review
    data = {}
    for r in reviews:
        name = r.find_element(By.CLASS_NAME, 'audience-reviews__user-wrap')
        data['Name'] = [name.text]
        
        date = r.find_element(By.CLASS_NAME, 'audience-reviews__duration')
        data['Date'] = [date.text]
        
        score = r.find_element(By.CLASS_NAME, 'audience-reviews__score')
        stars = score.find_element(By.CLASS_NAME, 'star-display')
        starType = stars.find_elements(By.TAG_NAME, 'span')
        rating = 0.0
        for i in starType:
            if i.get_attribute('class') == 'star-display__filled ':
                rating = rating+1
            if i.get_attribute('class') == 'star-display__half ':
                rating = rating+.5
        data['Rating'] = [rating]

        review = r.find_element(By.CLASS_NAME, 'audience-reviews__review')
        data['Review'] = [review.text]

        #Add the data to the dataframe
        df = pd.DataFrame.from_dict(data)
        dataframe = pd.concat([dataframe, df])
        
    return dataframe

#Function to go to the next page of reviews
def NextPage():
    button = driver.find_element(By.CLASS_NAME, 'js-prev-next-paging-next')
    if button.text == 'NEXT':
        button.click()
    

###############################################################

#Create a dataframe to store our data
reviewData = pd.DataFrame(columns=['Name','Date','Rating','Review'])

#Open a web browser
driver = webdriver.Chrome()

#Go to the movie review url
driver.get('https://www.rottentomatoes.com/m/princess_bride/reviews?type=user')

#Web Scraping
for i in range(5):
    #Scrape all the reviews on the page
    reviewData = Scrape(reviewData)

    #Go to the next review page
    NextPage()

    #Wait for the next page to load - couldn't get selenium's explicit or implicit waiting to work 
    time.sleep(2)

#Close the web browser
driver.quit()

#Save data to csv
reviewData.to_csv('ReviewData.csv', index=False)
