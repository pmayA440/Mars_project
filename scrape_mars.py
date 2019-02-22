import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from splinter import Browser


def scrape():
    mars = {}

# NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    # pull page data
    soup = BeautifulSoup(response.text, 'html.parser')
    # collect the latest News Title and Paragraph Text
    mars['Latest_News_Title'] = soup.find('div',class_='content_title').get_text()
    mars['Latest_News_Paragraph'] = soup.find('div',class_='rollover_description_inner').get_text()
    
# JPL Mars Space Images - Featured Image
    # JPL Mars Space Images - Featured Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response = requests.get(url2)
    soup = BeautifulSoup(response.text, 'html.parser')

    url = 'https://www.jpl.nasa.gov'
    image_path = soup.footer.a.get('data-fancybox-href')
    featured_image_url = url + image_path
    mars['featured_image_url'] = url + image_path
    
# Mars weather
    # Visit twitter
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)

    # Scrape the latest Mars weather tweet from the page
    soup = BeautifulSoup(response.text, 'html.parser')
    Tweet = soup.find_all('div', class_='js-tweet-text-container')[1]

    # Save the tweet text for the weather report
    mars["weather"] = Tweet.text.strip()

# Collect Mars Facts and use Pandas to scrape the table containing facts about the planet
    # Visit Mars Facts page
    url4 = 'https://space-facts.com/mars/'
    # Scrape the Mars facts in table
    tables = pd.read_html(url4)
    df = tables[0]
    df.set_index(0, inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    mars["Facts"] = df.to_html('table.html')
    

# Mars Hemispheres
# Obtain high resolution images for each of Mar's hemispheres
    url6 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(url6)
    soup = BeautifulSoup(response.text, 'html.parser')

    url = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/"
    end = ".tif/full.jpg"

    Mars_Hemispheres = []

    for link in soup.find_all('div', class_="item"):
        path = link.a.get('href')
        path2 = path.rsplit('/', 1)[-1]
        Mars_Hemispheres.append(url + path2 + end)

    mars['Cerberus_image_url'] = Mars_Hemispheres[0]
    mars['Schiaparelli_image_url'] = Mars_Hemispheres[1]
    mars['Syrtis_image_url'] = Mars_Hemispheres[2]
    mars['Valles_marineris_image_url'] = Mars_Hemispheres[3]
    

    # Return results
    return mars
