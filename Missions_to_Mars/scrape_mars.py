# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return browser


def scrape_info():
    browser = init_browser()
    mars_data = {}
    # URL of page to be scraped nasa mars news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # get news title, news link, news text, news date
    results = soup.find_all('div', class_='list_text')
    news_title = results[0].find('div', class_='content_title').text
    news_link = results[0].find('a')['href']
    news_p = results[0].find('div', class_='article_teaser_body').text
    date = results[0].find('div', class_='list_date').text
    mars_data["news_title"] = news_title
    mars_data["news_links"] = 'https://mars.nasa.gov' + news_link
    mars_data["news_p"] = news_p
    mars_data["news_date"] = date

    # URL of page to be scraped JPL Mars Space
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # get image url from JPL Mars Space
    results = soup.find_all('div', class_='header')
    # scrape the url image full size
    imageurl = results[0].find('img', class_='headerimage fade-in').get('src')
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + imageurl
    mars_data["featured_image_url"] = featured_image_url

    # URL of page to be scraped Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.columns = ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)
    # create a html table of mars facts
    mars_df.to_html('mars_table.html')
    mars_df=mars_df.reset_index()
    mars_value=mars_df['Mars']
    mars_title=mars_title=['EquDia','PolDia','Mas','Moo','OrbDis','OrbPer','SurTem','FirRec','RecBy']
    mars_table= dict(zip(mars_title, mars_value))
    mars_data['mars_table']=mars_table
    
    # fuction to get the full size image url from Mars Hemispheres

    def mars_hemispheres(url):
        browser.visit(url)
        # Create BeautifulSoup object; parse with 'html.parser'
        html = browser.html
        soup = bs(html, 'html.parser')  # Retrieve the parent divs for all articles
        results = soup.find_all('div', class_='downloads')
        # scrape the url image full size
        url = results[0].find('a')['href']
        results = soup.find_all('div', class_='content')
        title = results[0].find('h2', class_='title').text
        return (url, title)

    # cerberus_enhanced
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    url, title = mars_hemispheres(url)
    cerburl = url
    cerbtitle = title
    # schiaparelli_enhanced
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    url, title = mars_hemispheres(url)
    schiurl = url
    schititle = title
    # syrtis_major_enhanced
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    url, title = mars_hemispheres(url)
    syrturl = url
    syrttitle = title

    # valles_marineris_enhanced
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    url, title = mars_hemispheres(url)
    vallurl = url
    valltitle = title
    # create a dictionary with Mars Hemispheres images: title and image url full size
    hemisphere_image_urls = [
        {"title": cerbtitle, "img_url": cerburl},
        {"title": schititle, "img_url": schiurl},
        {"title": syrttitle, "img_url": syrturl},
        {"title": valltitle, "img_url": vallurl},
    ]

    mars_data["hem_img_url"] = hemisphere_image_urls
    browser.quit()

    # Return results
    return mars_data

if __name__ == "__main__":
    scrape_info()