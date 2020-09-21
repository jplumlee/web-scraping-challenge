from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:/Users/jplum/chromedriver_win32/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}

def scrape():
# def mars_news():
    
    browser = init_browser()

    # URL for BeautifulSoup scraping
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Title soup
    response = requests.get(url)

    # Create a Beautiful Soup object
    title_soup = bs(response.text, 'html.parser')

    title = title_soup.find('div', class_='content_title').find('a')

    title = title.text

    # Read HTML from website and use BeautifulSoup to find the news title and paragraph text 
    html = browser.html

    # Create a Beautiful Soup object
    paragraph_soup = bs(html, 'html.parser')

    time.sleep(3)

    paragraph = paragraph_soup.find('div', class_='article_teaser_body')

    paragraph_text = paragraph.text

    mars_data['title'] = title
    mars_data['paragraph'] = paragraph_text

# def mars_image():

    # browser = init_browser()

    url3 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url3 = 'https://www.jpl.nasa.gov'

    browser.visit(url3)

    full_image = browser.find_by_id('full_image')
    full_image.click()

    time.sleep(3)
    # Read HTML from website and use BeautifulSoup to find the news title and paragraph text 
    html3 = browser.html

    # Create a Beautiful Soup object
    soup3 = bs(html3, 'html.parser')

    featured_image = soup3.find('img', class_="fancybox-image")['src']

    featured_image_url = base_url3 + featured_image

    mars_data['featured_image_url'] = featured_image_url

    # URL for pandas scraping
    url2 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url2)

    df = tables[2]

    df.columns=['Description', 'Mars']

    df.set_index('Description', inplace=True)

    df = df.to_html()

    mars_data['mars_facts'] = df
# def hemispheres():

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url4 = 'https://astrogeology.usgs.gov'
    browser.visit(url4)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')
    hemisphere_url = soup4.find_all('div', class_='item')

    image_urls = []

    for x in hemisphere_url:
        title = x.find('h3').text
        link = x.find('a')['href']
        browser.visit(base_url4 + link)
        html5 = browser.html
        image_soup = bs(html5, 'html.parser')
        image5 = base_url4 + image_soup.find('img', class_="wide-image")['src']
        image_urls.append({"title": title, "image_url": image5})

    mars_data['hemisphere_image_urls'] = image_urls

    browser.quit()

    return mars_data