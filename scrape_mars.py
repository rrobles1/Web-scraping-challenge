from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

browser = init_browser()
def mars_news():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    latest_news = soup.find("div", class_='list_text')
    news_title = latest_news.find("div", class_="content_title").text
    news_p = latest_news.find("div", class_="article_teaser_body").text
    output = [news_title, news_p]
    return output

def mars_img():
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_img_url = "https://www.jpl.nasa.gov" + image
    return featured_img_url

def Mars_Weather():
    twitter_page_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_page_url)
    html = browser.html
    soup = bs(html, "html.parser")
    header = soup.find("div", class_="stream-item-header")
    tweet = soup.find("div", class_="js-tweet-text-container").text
    mars_weather = [header, tweet]
    return mars_weather

def mars_facts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[1])
    mars_data.columns = ["Measurement_Label", "Value"]
    mars_data = mars_data.set_index("Measurement_Label")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts

def mars_hemispheres():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []
    products = soup.find("div", class_="result-list")
    hemispheres = products.find_all("div", class_="item")
    
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_lnk = hemisphere.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov" + end_lnk
        browser.visit(img_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        img_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": img_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

def mars_scrape():
    final_product = {}
    output = mars_news()
    final_product["mars_news"] = output[0]
    final_product["paragraph_text"] = output[1]
    final_product["mars_img"] = mars_img()
    final_product["Mars_Weather"] = Mars_Weather()
    final_product["mars_facts"] = mars_facts()
    final_product["mars_hemispheres"] = mars_hemispheres()
    return final_product