"""
This script allows the user to extract the data of Mercedes Benz G class and save the data in the format of CSV file

"""

'''
    Importing the libraries
    
'''
print('Please Install requirements.txt')
import time
import pandas as pd
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def cardata():
    
    
    """
    Intitial requriements
    - Download the selenium drivers from the documentation
    - create a new folder in c:drive with any name and extract the driver in this folder
    - !pip install requirements.txt
    
    Setting options allows us to show or hide the window and it also has more advance options like by adding additional arguments
    To avoid the timeexception messgae and page_load_strategy must equal to 'eager'
        - Generally page_load_strategy has three values like 'Normal', 'Eager', 'None'
        - By default it is set to the 'Normal' and which means it takes normal loading time and casuses the TimeExpection message
        - By setting the value to 'eager' it loads only the interactive page and processing speed is also very high
    
    Here in this code webdriver.Chrome is used and anyone can downlaod different browser drivers like firefox and others
    
        - driver.get is used to access the required website
        - here options allows user to open or not window of chrome and it allows gives additional arguments also
        - here implicitly_wait is used to give the time for website to load
        - driver.find_element_by_xpath is similar to accessing the elements by class name
        - for xpath right click on the website->inspect->select Id or class->rightclick->go to copy->select xpath
    
    """

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.page_load_strategy = 'eager'  

    """
        Establishing connection
    """

    driver = webdriver.Chrome(executable_path= "C:\\selenium browser drivers\\chromedriver.exe", options= options)

    driver.get("https://suchen.mobile.de/fahrzeuge/search.html?dam=0&fr=2020%3A&isSearchRequest=true&ms=17200%3B%3B12%3B%3B&s=Car&sfmr=false&vc=Car")

    driver.implicitly_wait(50) #waiting to load webpage

    #removing first popup (accept cookies)
    try:
        no_button = driver.find_element_by_class_name('mde-consent-accept-btn')
        no_button.click()
    except:
        print('No element with class name found. skipping...')

    driver.implicitly_wait(50)   
    #saving the search 
    try:
        no_button1 = driver.find_element_by_xpath('//*[@id="save-search-tutorial"]/span/i')
        no_button1.click()
    except:
        print('No element with class name found. skipping...')

    driver.implicitly_wait(50)

    '''
        Extracting 1st Page URL links
    '''

    time.sleep(10)
    page_sour = driver.page_source

    # using bs4 to save the website for extrcting the data

    from bs4 import BeautifulSoup 
    soup = BeautifulSoup(page_sour, 'lxml')
    d1 = soup.find_all('div', {'class': 'cBox cBox--content cBox--resultList'})
    d2 = d1[0]
    urls = []
    for i in d2.find_all('a', {'class': 'link--muted no--text--decoration'}):
        urls.append(i['href'])
    for i in d2.find_all('a', {'class': 'link--muted no--text--decoration result-item'}):
        urls.append(i['href'])

    def next_page(page):
        
        """ 
        Extracting Next Page URL links and it is continuously varying
    

        Returns:
            [URLs]: [of all next page]
        """
        next_pages_url = f'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&makeModelVariant1.makeId=17200&makeModelVariant1.modelGroupId=12&minFirstRegistrationDate=2020-01-01&pageNumber={page}&scopeId=C&sfmr=false'
        return next_pages_url

    next_pages = []
    for x in range(2,19):
        next_pages.append(next_page(x))
    
    '''
        using the sleep
    '''    

    time.sleep(30)

    '''
        Extracting the URL links of all ads in all pages
    '''
    xurls = []
    for i in next_pages:
        driver.get(i)
        ##driver.implicitly_wait(3000000)
        #time.sleep(10)
        page_sourx = driver.page_source
        soupx = BeautifulSoup(page_sourx, 'lxml')
        
        d1x = soupx.find_all('div', {'class': 'cBox cBox--content cBox--resultList'})
        d2x = d1x[0]
        for i in d2x.find_all('a', {'class': 'link--muted no--text--decoration'}):
            xurls.append(i['href'])
        for i in d2x.find_all('a', {'class': 'link--muted no--text--decoration result-item'}):
            xurls.append(i['href'])
        
    '''
        Concatenating all URLs together as a single list
    '''
    urls_ = urls + xurls

    """
        Extracting all requried information from the data
    
        As the website is dynamic in nature sometimes net price of car is not available
    """
        
    car_names = []    
    gross_prices = [] 
    net_prices = []
    milages = []
    vehicle_numbers = []
    dealer_names = []
    colors = []
    dealer_locations = []
    damages = []
    for i in range(len(urls_)):
    
        driver.get(urls_[i])
        #time.sleep(5)
        #driver.implicitly_wait(30000000000)
        page_sour2 = driver.page_source
        soup3 = BeautifulSoup(page_sour2, 'lxml')
        
        """
            for finding car name
        """
        try:
            car_name = soup3.find_all('h1', {'class': 'h2 u-margin-bottom-9 overlay-image-gallery-title'})[0].get_text()
            car_names.append(car_name)
        except IndexError:
            car_names.append('None')
        
        """
            for finding gross price
        """
        
        try:
            gross_price = soup3.find_all('span', {'data-testid': 'prime-price'})[0].get_text()
            gross_prices.append(gross_price)
        except IndexError:
            gross_prices.append('None')
    
        """
            for finding gross price
        """
        try:
            net_price = soup3.find_all('span', {'data-testid': 'sec-price'})[0].get_text()
            net_prices.append(net_price)
        except IndexError:
            net_prices.append('None')
    
        """
            for finding gross price
        """
        try:
            milage = soup3.find_all('div', {'class': 'g-col-6', 'id': 'mileage-v'})[0].get_text()
            milages.append(milage)
        except IndexError:
            milages.append('None')
    
        """
            for finding vehicle_number
        """
        try:
            vehicle_number = soup3.find_all('div', {'class': 'g-col-6', 'id': 'sku-v'})[0].get_text()
            vehicle_numbers.append(vehicle_number)
        except IndexError:
            vehicle_numbers.append('None')
        """
            for finding dealer_names
        """
        try:
            dealer_name = soup3.find_all('a', {'id': 'dealer-hp-link-bottom'})[0].get_text()
            dealer_names.append(dealer_name)
        except IndexError:
            dealer_names.append('None')
    
        """
            for finding gross price
        """
        try:
            color = soup3.find_all('div', {'class': 'g-col-6', 'id': "color-v"})[0].get_text()
            colors.append(color)
        except IndexError:
            colors.append('None')
    
        '''
            for finding dealer_location
        '''
        try:
            dealer_location = soup3.find_all('p', {'id': 'db-address'})[0].get_text()
            dealer_locations.append(dealer_location)
        except IndexError:
            dealer_locations.append('None')
    
        '''
            for finding damages
        '''
        try:
            damage = soup3.find_all('div', {'class': 'g-col-6', 'id': 'damageCondition-v'})[0].get_text()
            damages.append(damage)
        except IndexError:
            damages.append('None')
        
    '''

        Creating a data frame with above values
    '''

    df = pd.DataFrame({'vehicle_name': car_names , 'gross_price': gross_prices, 'net_price': net_prices, 
                   'vechile_number': vehicle_numbers, 'color': colors, 'dealer_name': dealer_names,
                   'dealer_location': dealer_locations,'milage' : milages, 'damage': damages})


    '''
        Analysis of the data to make it tidy
    '''

    #sorting the table via vehicle name
    df.sort_values(by= ['vehicle_name'], inplace= True)

    #reseting the index
    df.reset_index(drop = True, inplace= True)


    #removing the 'euro' symbol and '(Brutto)'
    df['gross_price'] = df['gross_price'].str.extract(r'(\d+.\d+)', expand = False)

    #removing the 'euro' symbol and '(netto)'
    df['net_price'] = df['net_price'].str.extract(r'(\d+.\d+)', expand = False)

    # creating the space between location
    df['dealer_location'] = df['dealer_location'].str.replace(pat= r'DE', repl= ', DE', regex= True)

    #creating two new columns
    df[['Address','City']] = df['dealer_location'].str.split(pat = '\, DE-\d+', expand= True)


    #dropping the duplicates
    df.drop_duplicates(inplace= True)

    #reseting the index
    df.reset_index(drop = True, inplace= True)

    #dropping the address column
    df.drop('Address', axis = 1, inplace= True)


    #extracting the model name from the model details
    df['Model'] = df['vehicle_name'].str.extract(pat = r"([^Mercedes\-Benz\s\s]\s\d+|[^Mercedes\-Benz\sG]\d+)", expand= False)

    """
    Final generating the CSV file
    """
    
    df.to_csv('Cars_data.csv')


if __name__ == "__main__":
    cardata()

