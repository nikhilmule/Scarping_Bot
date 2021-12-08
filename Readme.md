# __Objective__ 

## The main goal of this project is to scrapy a dynamical website for extracting information about the car, dealer details and save it as CSV file

# __Explanation__

## __Establishing connection__

### In this project selenium, beautifulsoup are used for scraping the data
### For installing selenium here is the link
    - https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/
    - After downloading the driver and extract it in the C drive by creating seperate folder to it.
    - Specify executable path as C drive folder.
### Here in this code selenium is used for establishing the connection with the website and manipulating the initial popups
### Beautifulsoup is used to get the local copy of website in order to avoid the load on the server

## __Data analysis__

### Data frame is created with extracted data for this pandas library is utilized
### After performing the preprocessing the dataframe is saved as CSV file

## __Data Visualization__

### Geopandas is used for extracting the latitude and longitude of the dealer location
### For geopandas is better to create an virtual environment and install pandas, folium packages inside it
### Re-iterate the code
### Here in this project folium library is used for visualization
